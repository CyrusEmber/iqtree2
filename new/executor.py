import datetime
import io
import logging
import multiprocessing
import sys
import time
import concurrent.futures
import subprocess
from concurrent.futures import ThreadPoolExecutor
import time

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
    # task_output = open("output", "a")
    process = subprocess.run(command, stderr=subprocess.STDOUT, stdout=subprocess.PIPE, shell=True)
    output = process.stdout.decode().strip()

    if process.returncode != 0:
        logger.error(f"Command {command} failed with Error code {process.returncode}")
        raise RuntimeError(f"failed with return code {process.returncode} ")

    return command, output


def concurrent_commands(cmds, processors=None, timeout=None, result="result"):
    ''' Default processors are maximum cores. Default timeout is no timeout. User can specify a timeout value.
        Run every task in parallel.
    '''
    # set logger
    logger = logging.getLogger("test")

    # set start time
    start_time = time.time()

    with ThreadPoolExecutor(max_workers=processors) as executor:
        futures = {executor.submit(run_command, cmd): cmd for cmd in cmds}

        # save the log-likelihood and running time results with a dict of cmd: (log_likelihood, total_time)
        result_dict = {}

        # Wait for the results
        for future in concurrent.futures.as_completed(futures, timeout=timeout):
            command = futures[future]
            try:
                # FIXME timeout
                cmd, output = future.result()
            except Exception as exc:
                print(f"Command {command} generated an error: {exc}")

            else:
                log_likelihood = None
                total_time = None
                # parse critical information from output file or (log file)
                outputs = output.split()
                for i in range(len(outputs)):
                    if outputs[i] == "log-likelihood:":
                        log_likelihood = outputs[i + 1]
                    if outputs[i] == "used:":
                        total_time = outputs[i + 1]
                result_dict[command] = (log_likelihood, total_time)
                print(f"Successfully run command {command}, log_likelihood: {log_likelihood}, total time: {total_time}")
                logger.info(f"Successfully run command {command}, log_likelihood: {log_likelihood}, total time: {total_time}")

    # set end time
    end_time = time.time()
    logger.info(f"All tests finished in --- {start_time - end_time} ---")

    # output the result to compare in later workflow
    # in format: cmd log-likelihood time
    if len(result_dict) > 0:
        with open(result, "w") as f:
            for item in result_dict:
                f.write(f"{item} {result_dict[item][0]} {result_dict[item][1]}\n")
        f.close()


