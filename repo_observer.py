import argparse
import os
import subprocess
import logging
from configparser import ConfigParser
from time import sleep

import sys


def poll():
    # 配置日志
    logging.basicConfig(
        filename='ci.log',
        level=logging.DEBUG,
        format='%(levelname)s:%(asctime)s:%(message)s'
    )
    log = open("ci.log", "a")
    sys.stdout = log
    sys.stderr = log

    parser = argparse.ArgumentParser()
    # metavar - A name for the argument in usage messages.
    parser.add_argument("--ini",
                        type=str,
                        help="config file")
    parser.add_argument("--repo",
                        metavar="REPO",
                        type=str,
                        help="path to the repository this will observe")
    parser.add_argument("--process",
                        metavar="PROCESS",
                        type=str,
                        help="process that should be restart")

    args = parser.parse_args()
    config_file = args.ini
    config = ConfigParser()
    config.read(config_file)
    repo = config.get('ci', 'repo') if not args.repo else args.repo
    process = config.get('ci', 'process') if not args.process else args.process
    while True:
        try:
            # call the bash script that will update the repo and check
            # for changes. If there's a change, it will drop a .commit_id file
            # with the latest commit in the current working directory
            subprocess.check_output(["./update_repo.sh", repo])
        except subprocess.CalledProcessError as e:
            raise Exception("Could not update and check repository. Reason: %s" % e.output)

        if os.path.isfile(".commit_id"):
            commit_file = open(".commit_id", "r")
            commit_id = commit_file.read()
            print('new commit polled: {commit}'.format(commit=commit_id))
            # great, we have a change
            try:
                subprocess.check_output(["./restart_process.sh", process])
                print('process {process} hae been restarted'.format(process=process))
            except subprocess.CalledProcessError as e:
                raise Exception("Fail to restart process {process}".format(process=process))

        sleep(10)

if __name__ == "__main__":
    poll()