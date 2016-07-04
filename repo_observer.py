import argparse
import os
import subprocess
from time import sleep


def poll():
    parser = argparse.ArgumentParser()
    # metavar - A name for the argument in usage messages.
    parser.add_argument("repo",
                        metavar="REPO",
                        type=str,
                        help="path to the repository this will observe")
    parser.add_argument("process",
                        metavar="PROCESS",
                        type=str,
                        help="process that should be restart")

    args = parser.parse_args()
    while True:
        try:
            # call the bash script that will update the repo and check
            # for changes. If there's a change, it will drop a .commit_id file
            # with the latest commit in the current working directory
            subprocess.check_output(["./update_repo.sh", args.repo])
        except subprocess.CalledProcessError as e:
            raise Exception("Could not update and check repository. Reason: %s" % e.output)

        if os.path.isfile(".commit_id"):
            # great, we have a change
            try:
                subprocess.check_output(["./restart_process.sh", args.process])
            except subprocess.CalledProcessError as e:
                raise Exception("Fail to restart process {process}".format(process=args.process))

        sleep(10)

if __name__ == "__main__":
    poll()