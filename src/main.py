import sys
import os
import zipfile


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
    extracted_logs_path_list = file_path.split(os.path.sep)
    extracted_logs_folder_list = extracted_logs_path_list[0:len(extracted_logs_path_list)-1]
    path_to_logs_folder = "/".join(extracted_logs_folder_list)

    path_to_extracted_folder = path_to_logs_folder + os.path.sep + "Extracted"
    with zipfile.ZipFile(file_path, "r") as zip_ref:
        zip_ref.extractall(path_to_extracted_folder)
    extract_internal_folders(path_to_extracted_folder)
    print(f"Log files in {file_path} were unzipped to {path_to_extracted_folder}")
    return path_to_extracted_folder


def extract_internal_folders(path_to_extracted_folder):
    """Extracting archives in the extracted folder"""
    dir_list = os.listdir(path_to_extracted_folder)
    zip_extension = ".zip"
    os.chdir(path_to_extracted_folder)
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
    # print(f"Unzipping logs archive")
    unzipped_logs_folder = unzip_logs(file_path)
    # print(f"Parsing log files to build statistics")
    parse_unzipped_logs(unzipped_logs_folder)


if __name__ == '__main__':
    # print("PerfReader - Scan logs and build performance statistics.")
    if len(sys.argv) == 2:
        main(sys.argv[1])
    else:
        usage("Missing file argument")
        sys.exit(-2)
