import sys
import requests
import pdb
import time
import pandas as pd
import subprocess
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import re
import functools

LOCAL_BENCHMARK = "./local_benchmark.sh"
FUNCTIONS = ["sql", "pi", "kmeans"]

def main():
    import os
    os.chdir("./docker-compose")
    # Generate data
    exec_sync("generate")
    pooled_stats = {}
    pooled_stats['baseline'] = pool()

    # Run each function on yarn 
    for f in FUNCTIONS:
        process = exec_async(f)
        pooled_stats[f] = pool()
        await_async(process)

    plot(pooled_stats)



def exec_sync(function_name):
    subprocess.run([LOCAL_BENCHMARK, "--function", function_name], check=True)


def exec_async(function_name):
    return subprocess.Popen([LOCAL_BENCHMARK, "--function", function_name])


def plot(pooled_stats):
    colors = {
        "sql": "r", 
        "pi": "g",
        "kmeans": "b",
        "baseline": "black" 
    }

    patches_colors = {
        "sql": "red",
        "pi": "green",
        "kmeans": "blue",
        "baseline": "black" 
    }

    titles = {
        'allocated_bytes': "Execution timeline vs Allocation Bytes.", 
        'cpu': "Execution timeline vs Cpu Percent Usage.",
        'disk_reads': "Execution timeline vs Disk Reads Completed.",
        'disk_writes': "Execution timeline vs Disk Writes Completed."
    }

    ylabels = {
        'allocated_bytes': "Allocated memory (GB).", 
        'cpu': "Mean CPU utilization since process started (%).",
        'disk_reads': "Total disk reads since process started (4KB page).",
        'disk_writes': "Total disk wr itessince process started (4KB page)."
    }

    patches = [mpatches.Patch(color=color, label=label) for label, color in patches_colors.items()]

    for key in titles.keys():
        plt.clf()
        plt.title(titles[key])
        plt.xlabel("Elapsed time (s).")
        plt.ylabel(ylabels[key])
        for stat in pooled_stats.keys():
            df = pooled_stats[stat]
            ys = df[key].values
            xs = df.running_time.values
            plt.legend(handles=patches)
            plt.plot(xs, ys, colors[stat])
        plt.savefig(key + '.pdf')


# Spinlock awaits the process.
# I know this is a spinlock I don't care it shouldn't influence the benchmark
def await_async(process):
    while True:
        retcode = process.poll()
        if retcode is not None: 
            return retcode
        else:
            time.sleep(2)


def pool():
    target_time = 200
    running_time = 0
    data = {'running_time': [], 'allocated_bytes': [], 'cpu': [], 'disk_reads': [], 'disk_writes': []}
    starting_user_times, starting_total_times = fetch_cpu()
    start_disk_writes = fetch_disk_writes_completed()
    start_disk_reads = fetch_disk_reads_completed()

    while running_time < target_time:
        time_start = time.time()

        allocated_bytes = fetch_allocated_bytes()
        user_times, total_times = fetch_cpu()
        cpu = ((user_times - starting_user_times) / (total_times - starting_total_times)) * 100
        disk_writes = fetch_disk_writes_completed() - start_disk_writes
        disk_reads = fetch_disk_reads_completed() - start_disk_reads

        time.sleep(1.5)
        time_finish = time.time()
        running_time += time_finish - time_start
        print("[INFO][StatisticsDatasetExtractor][MEM] Detected allocated_bytes of: " + str(allocated_bytes) + " at time: " + str(running_time) + ".")
        print("[INFO][StatisticsDatasetExtractor][CPU] Detected cpu of: " + str(cpu) + "at time: " + str(running_time) + ".")
        print("[INFO][StatisticsDatasetExtractor][DISK_WRITES] Detected disk_writes of: " + str(disk_writes) + "at time: " + str(running_time) + ".")
        print("[INFO][StatisticsDatasetExtractor][DISK_READS] Detected disk_reads of: " + str(disk_reads) + "at time: " + str(running_time) + ".")


        data['running_time'].append(running_time)
        data['allocated_bytes'].append(allocated_bytes)
        data['disk_reads'].append(disk_reads)
        data['disk_writes'].append(disk_writes)
        data['cpu'].append(cpu)

    return pd.DataFrame(data=data)


def fetch_all(port):
    response = requests.get('http://localhost:' + str(port) + '/metrics')
    return response.text.split('\n')           
        

def fetch_allocated_bytes():
    parsed_lines = fetch_all(9100)           
    free_bytes = list(filter(lambda x: x.startswith('node_memory_MemAvailable_bytes '), parsed_lines))
    free_bytes_float = float(free_bytes[0].split(' ')[1])
    
    total_bytes = list(filter(lambda x: x.startswith('node_memory_MemTotal_bytes '), parsed_lines))
    total_bytes_float = float(total_bytes[0].split(' ')[1])
    
    return (total_bytes_float - free_bytes_float)/1000000000


def fetch_cpu():
    parsed_lines = fetch_all(9100)

    # node_cpu_seconds_total{cpu="0",mode="idle"} 1837.25
    # node_cpu_seconds_total{cpu="0",mode="iowait"} 6.5
    # node_cpu_seconds_total{cpu="0",mode="irq"} 0
    # node_cpu_seconds_total{cpu="0",mode="nice"} 0
    # node_cpu_seconds_total{cpu="0",mode="softirq"} 0.64
    # node_cpu_seconds_total{cpu="0",mode="steal"} 0
    # node_cpu_seconds_total{cpu="0",mode="system"} 12.16
    # node_cpu_seconds_total{cpu="0",mode="user"} 88.49

    cpu_regex = r'^(node_cpu_seconds_total\{cpu=)"(0|1|2|3)",mode="(idle|iowait|irq|nice|softirq|steal|system|user)"\} (.*)'
    mapped_lines = list(map(lambda x: re.split(cpu_regex, x), parsed_lines))

    # x = ['', 'node_cpu_seconds_total{cpu=', '0', 'idle', '2759.44', '']
    time_cpu_lines = list(filter(lambda x: len(x) != 1, mapped_lines))
    user_time_cpu_lines = list(filter(lambda x: x[3] == "user" or x[3] == "system", time_cpu_lines))

    total_times = functools.reduce(lambda x, y: x + float(y[4]), time_cpu_lines, 0)
    user_times = functools.reduce(lambda x, y: x + float(y[4]), user_time_cpu_lines, 0)
    return (user_times, total_times)

def fetch_disk_writes_completed():
    parsed_lines = fetch_all(9103)
    disk_writes_completed_line = list(filter(lambda x: x.startswith('node_disk_writes_completed_total{device="sda"} '), parsed_lines))
    disk_writes = float(disk_writes_completed_line[0].split(' ')[1])
    return disk_writes


def fetch_disk_reads_completed():
    parsed_lines = fetch_all(9103)   
    disk_reads_completed_line = list(filter(lambda x: x.startswith('node_disk_reads_completed_total{device="sda"} '), parsed_lines))
    disk_reads = float(disk_reads_completed_line[0].split(' ')[1])
    return disk_reads 





if __name__ == "__main__":
    main()
