import configparser
from ArgParser import ArgParser


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


def parse_part_aln(filename):
    if filename[-4:] != ".phy":
        print("partition alignments are wrong")
    else:
        return filename[:-4] + ".nex"


def gen_test_cmds(in_file='config.ini', out_file="test_cmds", flag=None, bin=None):
    configs = get_config(in_file)
    test_cmds = []
    # Generate test commands for single model
    for aln in configs["single_alignments"]:
        for opt in configs["generic_options"]:
            cmd = '-s ' + aln + ' -redo ' + opt
            if flag:
                cmd = cmd + ' ' + flag
            test_cmds.append(cmd)

    # Generate test commands for partition model
    for aln in configs["partition_alignments"]:
        # print(aln)
        for opt in configs["generic_options"]:
            for partOpt in configs["partition_options"]:
                cmd = '-s ' + aln + ' -redo ' + opt + ' ' + partOpt + ' ' + parse_part_aln(aln)
                if flag:
                    cmd = cmd + ' ' + flag
                test_cmds.append(cmd)

    with open(out_file, "w") as f:
        for cmd in test_cmds:
            f.write(cmd + "\n")
    f.close()
    print("test command generated")


def set_config(filename='config.ini'):
    pass


gen_test_cmds()
