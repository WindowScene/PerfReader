import sys
import os
import zipfile
import csv
import re

# placeholder for extracted logs path
path_to_extracted_folder = ""


def usage(err: None):
    print(f"""
Usage:
    main.py <support_log_root>>

Examples:
    To process an (unzipped) support log:
        {sys.argv[0].split("/")[-1]} ~/path/to/VeeamBackupOffice365Logs.zip
        """, file=sys.stdout)

    if err:
        print('Error: {}\n'.format(err), file=sys.stderr)


def unzip_logs(file_path):
    """Unzip all logs and return path to extracted folder"""
    extracted_logs_path_list = file_path.split(os.path.sep)
    extracted_logs_folder_list = extracted_logs_path_list[0:len(extracted_logs_path_list)-1]
    path_to_logs_folder = os.path.sep.join(extracted_logs_folder_list)
    global path_to_extracted_folder
    path_to_extracted_folder = path_to_logs_folder + os.path.sep + "Extracted"
    with zipfile.ZipFile(file_path, "r") as zip_ref:
        zip_ref.extractall(path_to_extracted_folder)
    # extract_internal_folders(path_to_extracted_folder)
    # print(f"Log files in {file_path} were unzipped to {path_to_extracted_folder}")
    return path_to_extracted_folder


def create_csv_files():
    receive_file_path = path_to_extracted_folder + os.sep + "receive.csv"
    saving_file_path = path_to_extracted_folder + os.sep + "saving.csv"

    with open(receive_file_path, "w") as r_file:
        writer = csv.writer(r_file)
        writer.writerow(["date", "rate"])

    with open(saving_file_path, "w") as s_file:
        writer = csv.writer(s_file)
        writer.writerow(["date", "rate"])


def process_proxy_files():
    for actual_file_name in os.listdir(os.path.abspath(path_to_extracted_folder)):
        if "Veeam.Archiver.Proxy" in actual_file_name:
            get_date_string(path_to_extracted_folder + os.sep + actual_file_name)


def get_date_string(file_name):
    date_string_pattern = re.compile(r"\\d*/\\d*/\\d* \\d*:\\d*:\\d* ?([AaPp][Mm])")
    with open(rf"{file_name}", "r") as proxy_log_file:
        lines = proxy_log_file.readlines()
        for line in lines:
            print(line[0:10])
            # found = date_string_pattern.search(line)
            # print(found.group())
        # print(proxy_log_file[0:10])
    # print(date_string)


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


def main(file_path):
    print("unzipping logs ...")
    unzip_logs(file_path)
    print("path_to_extracted_folder: " + path_to_extracted_folder)
    # parse_unzipped_logs(path_to_extracted_folder)
    # print("path_to_extracted_folder after parse_unzipped_logs(path_to_extracted_folder) " + path_to_extracted_folder)
    # create_csv_files()
    # print("path_to_extracted_folder after create_csv_files() " + path_to_extracted_folder)
    # process_proxy_files()
    # print("path_to_extracted_folder after process_proxy_files() " + path_to_extracted_folder)


if __name__ == '__main__':
    # print("PerfReader - Scan logs and build performance statistics.")
    if len(sys.argv) == 2:
        main(sys.argv[1])
    else:
        usage("Missing file argument")
        sys.exit(-2)
