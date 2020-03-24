import platform
import sys
import os
import re
import argparse
import csv
from utils import check_valid_ip, check_valid_host
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from subprocess import run, PIPE
from typing import Tuple, Dict

setting = {
    "verbose": False,
    "time": 0,
    "host": "",
    "directory": "",
    "buffer": 32
}


def check_valid_ping_name(name: str) -> Tuple[bool, str]:
    if check_valid_ip(name):
        return True, 'Valid IP Name'
    if check_valid_host(name):
        return True, ''
    return False, 'Invalid IP or Host Name'


def ping_message(sequence, success, response_time, ttl, start_time, log):
    return {
        "sequence": sequence,
        "success": success,
        "response_time": response_time,
        "ttl": ttl,
        "start_time": start_time,
        "end_time": datetime.now().strftime("%Y/%m/%d %H:%M:%S"),
        "log": log
    }


def ping(host: str, sequence: int, ping_count: int = 1) -> Dict:
    start_time = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    # check if the host is a valid domain name or ip
    valid, message = check_valid_ping_name(host)

    # return error message if the host is invalid
    if not valid:
        print(message)
        return ping_message(sequence, 0, 0, 0, start_time, message)

    # using os module to run the ping command
    count_option = "-n" if platform.system().lower() == "windows" else "-c"
    response = run(f'ping {count_option} {ping_count} -l {setting["buffer"]} {host}', stdout=PIPE,
                   stderr=PIPE, universal_newlines=True)

    # if the return code is 1, that means something is wrong
    if response.returncode == 1:
        print("Something is wrong")
        print(f"Error Message: {response.stdout}")
    # return the ping result if the return code is 0
    else:
        ping_result = response.stdout
        response_time_match = re.search(r'time=(\d+ms)', ping_result)
        ttl_match = re.search(r'TTL=(\d+)', ping_result)
        if response_time_match and ttl_match:
            response_time = int(float(response_time_match.group(1)[:-2]))
            ttl = int(float(ttl_match.group(1)))
            print(f"Sequence: {sequence}")
            if setting["verbose"]:
                print(ping_result)
            else:
                print(f"time={response_time} ms, ttl={ttl}")
            return ping_message(sequence, 1, response_time, ttl, start_time, ping_result)
        # cannot find the response time and ttl (print the error message)
        else:
            print("Cannot find the response time of the ping, Please check output below")
            print(ping_result)
            return ping_result(sequence, 0, 0, 0, start_time, ping_result)


def init_ping_plot():
    fig = plt.figure()
    ping_plot = fig.add_subplot(1, 1, 1)
    return ping_plot


def update_plot(ping_plot, sequence_list, ping_time_list):
    ping_plot.clear()
    # ping_plot.set_ylim([0, 100])
    ping_plot.set_xlabel("Sequence")
    ping_plot.set_ylabel("Response Speed")
    ping_plot.set_title("Ping Test")
    ping_plot.plot(sequence_list, ping_time_list, 'o-')


def update_log_file(csv_writer, ping_result):
    csv_writer.writerow({
        'sequence': ping_result['sequence'],
        'success': ping_result['success'],
        'response_time': ping_result['response_time'],
        'ttl': ping_result['ttl'],
        'start_time': ping_result['start_time'],
        'end_time': ping_result['end_time'],
        'log': ping_result['log']
    })


def check_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("host",
                        help="The host for the ping test",
                        type=str)
    parser.add_argument("-l",
                        "--buffer",
                        help="The send buffer size"
                             "\nDefault to be 32 bytes",
                        type=int,
                        default=0)
    parser.add_argument("-t",
                        "--time",
                        help="The duration of the ping test (in minute)"
                             "\nIf not specified, the test will run indefinitely",
                        type=int,
                        default=0)
    parser.add_argument("-v",
                        "--verbose",
                        help="Show the detail output",
                        default=False,
                        action="store_true")
    parser.add_argument("-d",
                        "--directory",
                        help="The relative path to store the log and graph file, Default to be the current directory",
                        default="")

    args = parser.parse_args()
    setting["host"] = args.host
    setting["verbose"] = args.verbose

    # Check if the buffer size specified is valid
    if args.buffer:
        if args.buffer < 0 or args.buffer > 65000:
            sys.exit("Bad value for option -l, valid range is from 0 to 65500.")
        else:
            setting["buffer"] = args.buffer

    # Check if the time specified is valid (positive number)
    if args.time:
        if args.time <= 0:
            sys.exit("Invalid Time")
        else:
            setting["time"] = args.time

    # Check if the directory specified exists
    if args.directory:
        if os.path.exists(os.path.join(os.getcwd(), args.directory)):
            setting["directory"] = args.directory
        else:
            sys.exit("The directory does not exist")


def save_graph(timestamp):
    graph_file = f'{timestamp}-ping-test.png'
    if setting["directory"] != "":
        graph_file = os.path.join(setting["directory"], graph_file)
    plt.savefig(graph_file)


def main():
    check_arguments()
    ping_plot = init_ping_plot()
    sequence_list = []
    ping_time_list = []
    test_timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    log_file = f'{test_timestamp}-ping-test.csv'
    if setting["directory"] != "":
        log_file = os.path.join(setting["directory"], log_file)

    target_end_time = None
    if setting["time"]:
        target_end_time = datetime.now() + timedelta(minutes=setting["time"])
    try:
        with open(log_file, 'w', newline='') as csv_file:
            fieldnames = ['sequence', 'success', 'response_time', 'ttl', 'start_time', 'end_time', 'log']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            sequence = 0
            while True:
                ping_result = ping(setting["host"], sequence)
                sequence += 1
                ping_time_list.append(ping_result["response_time"])
                sequence_list.append(sequence)
                update_plot(ping_plot, sequence_list, ping_time_list)
                update_log_file(writer, ping_result)
                plt.pause(0.05)

                if target_end_time and datetime.now() > target_end_time:
                    break
    except KeyboardInterrupt:
        print("Keyboard interrupt")
        save_graph(test_timestamp)
        sys.exit(0)
    save_graph(test_timestamp)
    plt.show()


if __name__ == "__main__":
    main()
