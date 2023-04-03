import configparser
import logging
import yaml
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


class YmlParser:
    def __init__(self, file):
        self.data = None
        self.parse(file)
        self.cmds = []
        self.special_test = {}
        print(self.data)

    def parse(self, file):
        try:
            with open(file, 'r') as f:
                self.data = yaml.safe_load(f)
        # code that handles the exception and upload the error to log file.
        except FileNotFoundError as e:
            logger.error(f"Error: {e}. File not found.")
        except Exception as e:
            logger.error(f"Error: {e}. Yaml file is not valid.")

    def gen_test_cmds(self, test_files="test_data/", iqtree="iqtree2", bin="build", out_file="test_cmds") -> list:
        """
        This function reads config file and output test commands in a list accordingly.
        """
        # Generate test commands for single model
        for aln in self.data["single_alignments"]:
            cmd = f"-s {test_files}{aln} -redo"
            self.cmds.append(cmd)

        # Generate test commands for partition model
        for part_aln in self.data["partition_alignments"]:
            for partOpt in self.data["partition_options"]:
                cmd = f"-s {test_files}{part_aln['aln']} -redo {partOpt} {test_files}{part_aln['prt']}"
                self.cmds.append(cmd)

        # test commands that with more options
        for opt in self.data["option"]:
            self.cmds = [f"{cmd} {opt}" for cmd in self.cmds]

        # adding iqtree directory to the start of cmd
        self.cmds = [f"{bin}/{iqtree} {cmd}" for cmd in self.cmds]

        # output the cmd for debug
        # with open(out_file, "w") as f:
        #     for cmd in test_cmds:
        #         f.write(cmd + "\n")
        #
        # f.close()

        return self.cmds

    def gen_specific_test(self):
        keys = ["EXPECT_LE", "EXPECT_GE", "EXPECT_GT", "EXPECT_LT", "EXPECT_EQ"]
        for test in self.data["specific_test"]:
            # tuple of (key, value) e.g. ("EXPECTEDLE", 0.01)
            cmd = CMD()
            for key in test:
                keyword = None
                expect = None
                if key == "cmd":
                    cmd.cmd = test["cmd"]
                elif key == "keyword":
                    keyword = test["keyword"]
                elif key in keys:
                    cmd.specific_test.append((key, test[key]))


            self.special_test[cmd] = cmd.specific_test


            cmd = test["cmd"]



    def set_config(filename='config.ini'):
        pass


class CMD:
    def __init__(self, single_aln=None, part_aln=None, part_option=None, option=None, test_dir=None, iqbin=None):
        """
        This class is used to generate test commands.
        Bin is the path to iqtree binary.
        """
        self.cmd = None

        # special test
        self.specific_test = []
        self.keyword = []

    # def gen_test_cmds(self):
    #     """
    #     This function reads config file and output test commands in a list accordingly.
    #     """
    #     # Generate test commands for single model
    #     cmd = ""
    #     if self.single_aln is not None:
    #         cmd = f"-s {self.test_dir}{self.single_aln} -redo"
    #
    #     # Generate test commands for partition model and
    #     elif self.part_option is not None:
    #         cmd = f"-s {self.test_dir}{self.part_aln['aln']} -redo {self.part_option} {self.test_dir}{self.part_aln['prt']}"
    #
    #     # test commands that with more options
    #     cmd = f"{cmd} {self.option}"
    #
    #     # adding iqtree directory to the start of cmd
    #     cmd = f"{self.bin} {cmd}"
    #
    #     self.cmd = cmd

    def equal(self, other): # FIXME
        if self.cmd == other.cmd:
            return True
        else:
            return False

# def get_config(filename='config.ini'):
#     config = configparser.ConfigParser()
#
#     config.read(filename)
#     config_dict = {}
#
#     # iterate through the config file
#     for section in config.sections():
#         config_list = []
#         # option is the index
#         for option in config.options(section):
#             value = config.get(section, option)
#             config_list.append(value)
#         config_dict[section] = config_list
#     return config_dict
#
#
# def gen_test_cmds(in_file='config.ini', out_file="test_cmds", test_files="test_data/", iqtree=None, bin="build", flag=None):
#     '''This function reads config file and output test commands accordingly.
#     It can output a txt file or return the test commands for further use.
#     '''
#
#     configs = get_config(in_file)
#     test_cmds = []
#     # Generate test commands for single model
#     for aln in configs["single_alignments"]:
#         for opt in configs["generic_options"]:
#             cmd = '-s ' + test_files + aln + ' -redo ' + opt
#             if flag:
#                 cmd = cmd + ' ' + flag
#             test_cmds.append(bin + "/" + iqtree + " " + cmd)
#
#     # Generate test commands for partition model
#     for aln in configs["partition_alignments"]:
#         aln, par = aln.split()
#         for opt in configs["generic_options"]:
#             for partOpt in configs["partition_options"]:
#                 cmd = '-s ' + test_files + aln + ' -redo ' + opt + ' ' + partOpt + ' ' + test_files + par
#                 if flag:
#                     cmd = cmd + ' ' + flag
#                 test_cmds.append(bin + "/" + iqtree + " " + cmd)
#
#     # execute it in the build directory
#     with open(out_file, "w") as f:
#         for cmd in test_cmds:
#             f.write(cmd + "\n")
#
#     f.close()
#     # print("test command generated")
#     # log file
#     if len(test_cmds) != 0:
#         logger.info("test command generated")
#     else:
#         logger.error("No test file generated, check config file (default config.ini).")
#
#     return test_cmds
