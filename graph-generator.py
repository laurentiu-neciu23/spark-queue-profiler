from os import listdir
from os.path import isfile, join
import pandas as pd
import pdb
import matplotlib.pyplot as plt

paths = ["./results.local", "./results.yarn", "./results.standalone"]
graph_keys = ["sql-execute.csv", "cpu-execute.csv", "kmeans-execute.csv"]

def main():
    runtime_means = {}
    runtimes = {}
    timestamps = {}

    for path in paths:
        environment = path.split('.')[-1]
        runtime_means[environment] = {}
        runtimes[environment] = {}
        timestamps[environment] = {}

        for csv_dir in listdir(path):
            wf_csv_dir = join(path, csv_dir) + '/'
            csvs = [f for f in listdir(wf_csv_dir) if isfile(join(wf_csv_dir, f))]
            csv_name = filter(lambda csv: csv.split('.')[-1] == 'csv', csvs)[0]
            full_path = join(wf_csv_dir, csv_name)
            runtime_means[environment][csv_dir] = total_runtime_mean(full_path)
            timestamps[environment][csv_dir] = df_timestamps(full_path)
            runtimes[environment][csv_dir] = df_runtimes(full_path)

    draw_comparative_graphs(runtime_means)
    draw_dotted_graphs(timestamps)
    draw_runtime_graphs(runtimes)




def total_runtime_mean(path):
    df = pd.read_csv(path)
    if df.columns.contains('total_Runtime'):
        return pd.read_csv(path).total_Runtime[1:].mean()
    else:
        return pd.read_csv(path).total_runtime[1:].mean()

def df_timestamps(path):
    df = pd.read_csv(path)
    return df.timestamp


def df_runtimes(path):
    df = pd.read_csv(path)
    if df.columns.contains('total_Runtime'):
        return pd.read_csv(path).total_Runtime
    else:
        return pd.read_csv(path).total_runtime



def draw_dotted_graphs(data):
    for environment in data.keys():
        graphs = data[environment]
        start_index = 0
        plt.clf()
        plt.title("Timeline of execution")
        for graph in graph_keys:
            xs = data[environment][graph].values
            ys = range(start_index, start_index + len(xs))
            start_index = start_index + len(xs)
            normalised_xs = [x - xs.min() for x in xs]
            plt.plot(normalised_xs, ys, 'o')
        plt.legend(graph_keys)
        plt.savefig("timeline_" + environment + ".png")

def draw_runtime_graphs(data):
    for environment in data.keys():
        graphs = data[environment]
        start_index = 0
        
        plt.clf()
        plt.title("Runtime of execution")
        for graph in graph_keys:
            xs = data[environment][graph].values
            ys = range(start_index, start_index + len(xs))
            start_index = start_index + len(xs)
            plt.plot(ys, xs, 'o')
        plt.legend(graph_keys)
        plt.savefig("runtime_" + environment + ".png")


def draw_comparative_graphs(runtime_means):
    for graph_key in graph_keys:
        environments = []
        means = []
        for enviro in runtime_means.keys():
            environments += [enviro]
            means += [runtime_means[enviro][graph_key]]
        indices = range(1, 4)
        plt.clf()
        plt.bar(indices, means)
        plt.title(graph_key)
        plt.xticks(indices, environments)
        plt.savefig(graph_key + ".png")

if __name__ == "__main__":
    main()

