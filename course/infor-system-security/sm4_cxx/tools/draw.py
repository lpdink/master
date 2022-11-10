import matplotlib.pylab as plt
import numpy as np
import os


def main():
    time_log_file = "./time.log"
    with open(time_log_file, "r") as file:
        lines = file.readlines()
    encrypt_time = {int(lines[index].split()[0]): float(lines[index].split()[1])
                    for index in range(0, len(lines), 2)}
    decrypt_time = {int(lines[index].split()[0]): float(lines[index].split()[1])
                    for index in range(1, len(lines), 2)}
    # breakpoint()

    plt.subplot(211)
    plt.bar(range(len(encrypt_time.keys())), list(
        encrypt_time.values()), tick_label=list(encrypt_time.keys()))
    plt.plot(range(len(encrypt_time.keys())),
             encrypt_time.values(), color="black")
    plt.xticks(fontsize=7)
    plt.ylabel("encrypt time(ms)", fontsize=7)
    plt.subplot(212)
    plt.bar(range(len(decrypt_time.keys())), list(
        decrypt_time.values()), tick_label=list(decrypt_time.keys()), color="red")
    plt.plot(range(len(decrypt_time.keys())),
             decrypt_time.values(), color="black")
    plt.xticks(fontsize=7)
    plt.xlabel("msg length", fontsize=7)
    plt.ylabel("decrypt time(ms)", fontsize=7)
    plt.savefig("speed.png")


if __name__ == "__main__":
    main()
