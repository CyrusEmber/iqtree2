import datetime
import logging
import multiprocessing
import sys
import time
import concurrent.futures
import subprocess
from concurrent.futures import ThreadPoolExecutor

from logger import gen_log

# set logger
logger = logging.getLogger("test")


def exec_commands(cmds, num_cpus=multiprocessing.cpu_count()):
    ''' Depreciated method
    Exec commands in parallel in multiple process
    (as much as we have CPU)

    '''
    if not cmds:
        return  # empty list

    def done(p):
        return p.poll() is not None

    def success(p):
        return p.returncode == 0

    def fail():
        sys.exit(1)

    # logger.info("Number of jobs = " + str(len(cmds)))
    processes = []
    while True:
        while cmds and len(processes) < num_cpus:
            task = cmds.pop(0)
            # print subprocess.list2cmdline(task)
            task_id, cmd = task.split(" ", 1)
            # logger.info("Executing job " + task_id + ": " + cmd.strip())
            # print cmd
            task_output = open(task_id + ".out", "w")
            time_cmd = "time " + cmd
            processes.append(
                [subprocess.Popen(time_cmd, stderr=subprocess.STDOUT, stdout=task_output, shell=True), task_id])

        for p in processes:
            if done(p[0]):
                if success(p[0]):
                    # print "Process with ID = ", p.pid, " has finished"
                    # print "number of processes before removal: ", len(processes)
                    # logger.info("Job " + p[1] + " has finished")
                    processes.remove(p)
                    # print "number of processes after removal: ", len(processes)
                else:
                    # logger.info("Job " + p[1] + " finished with ERROR CODE " + str(p[0].returncode))
                    processes.remove(p)

        if not processes and not cmds:
            break
        else:
            time.sleep(5)


def run_command(command):
    task_output = open("output", "a")
    process = subprocess.run(command, stderr=subprocess.STDOUT, stdout=task_output, shell=True)
    if process.returncode != 0:
        logger.error(f"Command {command} failed with Error code {process.returncode}")
        raise RuntimeError(f"failed with return code {process.returncode}, output is ")
    # FIXME fix output


    return command


def concurrent_commands(cmds, processors=None):
    # overwrite the output file for debug
    output = open("output", "w")
    output.close()
    with ThreadPoolExecutor(max_workers=processors) as executor:
        futures = {executor.submit(run_command, cmd): cmd for cmd in cmds}
        # Wait for the results
        for future in concurrent.futures.as_completed(futures):
            command = futures[future]
            try:
                # timeout=None FIXME timeout also capture timeout
                result = future.result()
            except Exception as exc:
                print(f"Command {command} generated an error: {exc}")
            else:
                cmd = result
                logger.info(f"Command {cmd} success")
    output.close()



