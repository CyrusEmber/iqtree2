# read in through config and generate test commands
from config_parser import YmlParser
from executor import concurrent_commands
from logger import gen_log

if __name__ == '__main__':
    logger = gen_log("test")
    data = YmlParser('config.ini')
    test_cmds = data.gen_test_cmds(iqtree="iqtree1", bin="bin")
    concurrent_commands(test_cmds, result="result1")