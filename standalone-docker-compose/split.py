from os import listdir, mkdir
from os.path import isfile, join
import pandas as pd
import pdb
import matplotlib.pyplot as plt

def main():
    path = "./tmp/unsanitized_dataset"
    unsanitized_df = pd.read_csv(path)
    mkdir('res')
    dump_kmeans_execute(unsanitized_df)
    dump_sql_execute(unsanitized_df)
    dump_cpu_execute(unsanitized_df)

def dump_kmeans_execute(df):
    mkdir('res/kmeans-execute.csv')
    df[df.name == "kmeans"][['timestamp', 'total_runtime']].to_csv("res/kmeans-execute.csv/success.csv")

def dump_cpu_execute(df):
    mkdir('res/cpu-execute.csv')
    df[df.name == "sparkpi"][['timestamp', 'total_runtime']].to_csv("res/cpu-execute.csv/success.csv")


def dump_sql_execute(df):
    mkdir('res/sql-execute.csv')
    df[df.name == "sql"][['timestamp', 'total_Runtime']].to_csv("res/sql-execute.csv/success.csv")


if __name__ == "__main__":
    main()
