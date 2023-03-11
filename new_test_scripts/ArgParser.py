import argparse


class ArgParser(argparse.ArgumentParser):
    def __init__(self):
        super().__init__()
        self.parser = argparse.ArgumentParser()

    def standard_arg(self):
        self.bin_arg()
        self.config_arg()

    def bin_arg(self):
        self.parser.add_argument('-b', '--binary', dest="iqtree_bin", help='Path to your IQ-TREE binary')

    def config_arg(self):
        self.parser.add_argument('-c', '--config', dest="config_file", help='Path to test configuration file')

    def output_arg(self):
        self.parser.add_argument('-o', '--output', dest="outFile", help='Output file for test cases')



