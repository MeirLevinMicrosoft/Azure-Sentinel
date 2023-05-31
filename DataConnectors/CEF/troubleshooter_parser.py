import re
import csv
import argparse

# Create the command-line argument parser
parser = argparse.ArgumentParser(description="CEF troubleshooter parser")
parser.add_argument("log_file", type=str, nargs="?", default="cef_troubleshooter_collection_output.log", help="Path to the log file")
parser.add_argument("output_csv", type=str, nargs="?", default="troubleshooter_output.csv", help="Path to the output CSV file")
args = parser.parse_args()

log_file_path = args.log_file
output_csv_path = args.output_csv

processing = False  # Flag to indicate when processing should start
match_strings = ["agent_log_snip_warn", "agent_log_snip_info", "agent_log_snip_err"]


def print_error(input_str):
    print("\033[1;31;40m" + input_str + "\033[0m")


def print_known_errors(_line, level):
    if level == "err" and "parsemsg_rfc3164" in line:
        print_error(line)


def process_log_line(_line, _writer, level):
    # Extract date and content from the line
    match = re.match(r"^(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d+Z):(.*)$", line)
    if match:
        date = match.group(1)
        content = match.group(2)
        writer.writerow([date.strip(), level, content.strip()])
    else:
        print("Error: Failed to match pattern in line:", line)


with open(log_file_path, "r", encoding="utf8") as log_file, open(output_csv_path, "w", newline="", encoding="utf8") as output_csv:
    writer = csv.writer(output_csv)
    writer.writerow(["date", "level", "content"])  # Write header row
    log_level = ""

    for line in log_file:
        if any(match_string in line for match_string in match_strings):
            processing = True
            log_level = line.strip().split("_")[-1]
        elif line.strip() == "--------------------":
            processing = False
        elif processing and not line.isspace() and not len(line.strip()) == 0 and "output:" not in line:
            process_log_line(line, writer, log_level)
            print_known_errors(line, log_level)
