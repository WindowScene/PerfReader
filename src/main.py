import sys
import os
import zipfile
import csv
import re
import collections

import matplotlib
import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np



# placeholder for extracted logs path
path_to_extracted_folder = ""
receive_file_path = ""
saving_file_path = ""


def usage(err: None):
    print(f"""
Usage:
    main.py <support_log_root>
    docker run -v /Users/kirill/Documents/V/VBO/PerfReader-PY/misc/2021-11-11T141405Z_VeeamBackupOffice365Logs.zip:logs.zip feedthemachine/perf-reader:master-9e6fe7b logs.zip

Examples:
    To process an (unzipped) support log:
        {sys.argv[0].split("/")[-1]} ~/path/to/VeeamBackupOffice365Logs.zip
        """, file=sys.stdout)

    if err:
        print('Error: {}\n'.format(err), file=sys.stderr)


def unzip_logs(file_path):
    """Unzip all logs and return path to extracted folder"""
    print("unzipping logs ...")
    extracted_logs_path_list = file_path.split(os.path.sep)
    extracted_logs_folder_list = extracted_logs_path_list[0:len(extracted_logs_path_list)-1]
    path_to_logs_folder = os.path.sep.join(extracted_logs_folder_list)
    global path_to_extracted_folder
    path_to_extracted_folder = path_to_logs_folder + os.path.sep + "Extracted"
    with zipfile.ZipFile(file_path, "r") as zip_ref:
        zip_ref.extractall(path_to_extracted_folder)
        print("Extracted!")
    # extract_internal_folders(path_to_extracted_folder)
    print("path_to_extracted_folder: " + path_to_extracted_folder)
    return path_to_extracted_folder


def create_csv_files():
    global receive_file_path
    global saving_file_path
    receive_file_path = path_to_extracted_folder + os.sep + "receive.csv"
    saving_file_path = path_to_extracted_folder + os.sep + "saving.csv"

    with open(receive_file_path, "w") as r_file:
        writer = csv.writer(r_file)
        writer.writerow(["date", "rate"])

    with open(saving_file_path, "w") as s_file:
        writer = csv.writer(s_file)
        writer.writerow(["date", "rate"])


def process_proxy_files():
    r_rates = {}
    s_rates = {}
    for actual_file_name in os.listdir(os.path.abspath(path_to_extracted_folder)):
        if "Veeam.Archiver.Proxy" in actual_file_name:
            print(f"Processing {actual_file_name}")
            cur_dir_proxy_file = path_to_extracted_folder + os.sep + actual_file_name
            with open(rf"{cur_dir_proxy_file}", "r") as proxy_log_file:
                lines = proxy_log_file.readlines()
                for line in lines:
                    # find all receive rate lines
                    if "Receive rate:" in line:
                        r_rates[get_date_string(line)] = get_rate(line, "Receive rate:")
                    if "Saving rate :" in line:
                        s_rates[get_date_string(line)] = get_rate(line, "Saving rate :")
        sorted_dict = collections.OrderedDict(r_rates)
        with open(receive_file_path, "w") as r_file:
            writer = csv.writer(r_file)
            for k, v in sorted_dict.items():
                writer.writerow([k, v])

        sorted_dict = collections.OrderedDict(s_rates)
        with open(saving_file_path, "w") as s_file:
            writer = csv.writer(s_file)
            for k, v in sorted_dict.items():
                writer.writerow([k, v])


def get_rate(log_line, pattern_to_find):
    if pattern_to_find in log_line:
        return log_line.strip().split()[len(log_line.split())-2]


def get_date_string(log_line):
    date_string_pattern = re.compile("\\d*/\\d*/\\d* \\d*:\\d*:\\d* ?([AaPp][Mm])")
    if date_string_pattern.match(log_line) is not None:
        return date_string_pattern.match(log_line).group()


def extract_internal_folders(path_to_extracted_folder_internal):
    """Extracting archives in the extracted folder"""
    dir_list = os.listdir(path_to_extracted_folder_internal)
    zip_extension = ".zip"
    os.chdir(path_to_extracted_folder_internal)
    for file in dir_list:
        if file.endswith(zip_extension):
            file_name = os.path.abspath(file)
            with zipfile.ZipFile(file_name) as item:
                item.extractall()
                print(file_name + " extracted")
                os.remove(file_name)
                print("removed" + file_name)


def parse_unzipped_logs(unzipped_logs_folder):
    # print("Creating CVS files with write/read stats")
    pass


def plot():
    ts_axis = []
    rate_axis = []
    with open(receive_file_path, "r") as r_file:
        receive_csv_reader = csv.reader(r_file, delimiter=',')
        for row in receive_csv_reader:
            ts_axis.append(create_date_time(row[0]))
            rate_axis.append(int(row[1]))

    # plotting the points
    plt.plot(ts_axis, rate_axis)
    plt.yticks(np.arange(0, 0, 10.0))

    plt.xlabel('Timestamp')
    plt.ylabel('Rate')

    # giving a title to my graph
    plt.title('Processing rates')


    # function to show the plot
    plt.show()


def create_date_time(timestamp_string):
    return datetime.strptime(timestamp_string, '%d/%m/%Y %H:%M:%S %p')

def main(file_path):
    unzip_logs(file_path)
    parse_unzipped_logs(path_to_extracted_folder)
    create_csv_files()
    process_proxy_files()
    plot()


if __name__ == '__main__':
    # print("PerfReader - Scan logs and build performance statistics.")
    if len(sys.argv) == 2:
        main(sys.argv[1])
    else:
        usage("Missing file argument")
        sys.exit(-2)
