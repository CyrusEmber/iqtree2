import matplotlib.pyplot as plt
import yaml

from config_parser import cmd_constructor
from ArgParser import ArgParser

parser = ArgParser()
parser.compare_arg()
args = parser.parse_args()

cmd = []
cmd1, log1, time1 = [], [], []
cmd2, log2, time2 = [], [], []

keys = ["equal", "greater", "less", "greater_equal", "less_equal", "between"]


def compare(value, expected_value, test):
    if value is None:
        pass
    elif test == "equal":
        return value == expected_value
    elif test == "greater":
        return value > expected_value
    elif test == "less":
        return value < expected_value
    elif test == "greater_equal":
        return value >= expected_value
    elif test == "less_equal":
        return value <= expected_value
    elif test == "between":
        if expected_value[0] < expected_value[1]:
            return expected_value[0] <= value <= expected_value[1]
        else:
            return expected_value[1] <= value <= expected_value[0]


# iqtree1
with open(args.iqtree1, "r") as result:
    data1 = yaml.safe_load(result)
    # iqtree2
    with open(args.iqtree2, "r") as result2:
        data2 = yaml.safe_load(result2)
        # check if the special tests results are true
        for i in range(len(data1)):
            for test_dict in data1[i]["tests"]:
                pass
            for test_dict2 in data2[i]["tests"]:
                # check if value satisfies the special test
                value = test_dict["value"]
                passed = True
                is_test = False
                for key in test_dict2.keys():
                    if key in keys:
                        is_test = True
                        if not compare(value, test_dict2[key], key):
                            test_dict2["result"] = "Failed"
                            passed = False
                        break
                if passed and is_test:
                    test_dict2["result"] = "Passed"
                if "value" in data1[i].keys():
                    data2[i]["iqtree1 result"] = data1[i]["value"]
                else:
                    data2[i]["iqtree1 result"] = "No Result"

        with open(args.output_file, "w") as f:
            yaml.dump(data2, f)
        f.close()

# plot
plt.subplot(2, 1, 1)
plt.plot(cmd, [float(log1[i]) - float(log2[i]) for i in range(len(log1))], label="difference")
plt.axhline(0, color='red')
plt.legend()
plt.title('log likelihood')
plt.subplot(2, 1, 2)

plt.plot(cmd, [float(time1[i]) / float(time2[i]) for i in range(len(log1))], label="ratio")
plt.axhline(1, color='red')
plt.legend()
plt.title('running time')
plt.savefig('compare result.png')
plt.show()
