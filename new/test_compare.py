import matplotlib.pyplot as plt

cmd = []
cmd1, log1, time1 = [], [], []
cmd2, log2, time2 = [], [], []


with open("result1", "r") as result:
    line = result.readline()
    while line:
        log_likelihood, time = line.split()[-2], line.split()[-1]
        log1.append(log_likelihood)
        time1.append(time)
        # parse the cmd
        cmd.append(" ".join(line.split()[0: -2]))
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

