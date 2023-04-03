# read in through config and generate test commands
from config_parser import YmlParser
from executor import concurrent_commands
from logger import gen_log

if __name__ == '__main__':
    logger = gen_log("test")
    data = YmlParser('config.yml')
    # print(data.data)
    data.gen_specific_test()
    test_cmds = data.gen_test_cmds(iqtree="iqtree", bin="bin")
    concurrent_commands(test_cmds, result="result1")