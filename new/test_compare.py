import matplotlib.pyplot as plt

cmd1, log1, time1 = [], [], []
cmd2, log2, time2 = [], [], []


with open("result1", "r") as result:
    line = result.readline()
    while line:
        log_likelihood, time = line.split()[-2], line.split()[-1]
        log1.append(log_likelihood)
        time1.append(time)
        line = result.readline()
result.close()

with open("result2", "r") as result:
    line = result.readline()
    while line:
        log_likelihood, time = line.split()[-2], line.split()[-1]
        log2.append(log_likelihood)
        time2.append(time)
        line = result.readline()
result.close()

# plot
plt.subplot(2, 1, 1)
plt.plot(range(len(log1)), log1, label="iqtree1")
plt.plot(range(len(log2)), log2, label="iqtree2")
plt.legend()
plt.title('log likelihood')

plt.subplot(2, 1, 2)
plt.plot(range(len(time1)), time1, label="iqtree1")
plt.plot(range(len(time2)), time2, label="iqtree2")
plt.legend()
plt.title('running time')
plt.savefig('compare result.png')
plt.show()

