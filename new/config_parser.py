import configparser
import logging
import multiprocessing
import os
import subprocess
import sys
import time
from datetime import datetime

from ArgParser import ArgParser
from logger import gen_log

# config logger, useful when doing ui?
logger = logging.getLogger("test")


def get_config(filename='config.ini'):
    config = configparser.ConfigParser()

    config.read(filename)
    config_dict = {}

    # iterate through the config file
    for section in config.sections():
        config_list = []
        # option is the index
        for option in config.options(section):
            value = config.get(section, option)
            config_list.append(value)
        config_dict[section] = config_list
    return config_dict


def gen_test_cmds(in_file='config.ini', out_file="test_cmds", test_files="test_data/", iqtree=None, bin="build", flag=None):
    '''This function reads config file and output test commands accordingly.
    It can output a txt file or return the test commands for further use.
    '''

    configs = get_config(in_file)
    test_cmds = []
    # Generate test commands for single model
    for aln in configs["single_alignments"]:
        for opt in configs["generic_options"]:
            cmd = '-s ' + test_files + aln + ' -redo ' + opt
            if flag:
                cmd = cmd + ' ' + flag
            test_cmds.append(bin + "/" + iqtree + " " + cmd)

    # Generate test commands for partition model
    for aln in configs["partition_alignments"]:
        aln, par = aln.split()
        for opt in configs["generic_options"]:
            for partOpt in configs["partition_options"]:
                cmd = '-s ' + test_files + aln + ' -redo ' + opt + ' ' + partOpt + ' ' + test_files + par
                if flag:
                    cmd = cmd + ' ' + flag
                test_cmds.append(bin + "/" + iqtree + " " + cmd)

    # execute it in the build directory
    with open(out_file, "w") as f:
        for cmd in test_cmds:
            f.write(cmd + "\n")

    f.close()
    # print("test command generated")
    # log file
    if len(test_cmds) != 0:
        logger.info("test command generated")
    else:
        logger.error("No test file generated, check config file (default config.ini).")

    return test_cmds


def set_config(filename='config.ini'):
    pass


