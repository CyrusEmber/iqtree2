# read in through config and generate test commands
from config_parser import gen_test_cmds
from executor import concurrent_commands
from logger import gen_log

if __name__ == '__main__':
    logger = gen_log("test")
    test_cmds = gen_test_cmds(in_file='config.ini')
    concurrent_commands(test_cmds)
