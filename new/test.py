# read in through config and generate test commands
import argparse

from ArgParser import ArgParser

from config_parser import YmlParser
from concurrent_running import concurrent_commands
from logger import gen_log

if __name__ == '__main__':
    parser = ArgParser()
    parser.standard_arg()
    args = parser.parse_args()

    # debug
    parser = YmlParser('config.yml', iqtree='iqtree-2.2.0', bin='bin')
    # concurrent_commands(parser.cmds, output_result="iqtree1_result.yml")


    # logger = gen_log(f"test {args.version}")


    # parser = YmlParser(args.config_file, iqtree=args.version, bin=args.bin)
    # args.output_file
    concurrent_commands(parser.cmds, output_result="iqtree-2.2.0.yml")
