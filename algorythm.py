import pandas as pd
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import plotly.express as px
import cufflinks as cf
import numpy as np
from sklearn.preprocessing import MinMaxScaler


def algorythm(df):
    normal_df = df
    k = 0
    quan = len(normal_df["Perc_Diff"]) - 1
    meanPerc = normal_df["Perc_Diff"].median()
    while (quan > 3):
        if abs(normal_df["Perc_Diff"][quan] - normal_df["Perc_Diff"][quan - 1]) > abs(normal_df["Perc_Diff"][quan - 2] - normal_df["Perc_Diff"][quan - 3]):
            if abs(normal_df["Q_Diff"][quan] - normal_df["Q_Diff"][quan - 1]) > abs(normal_df["Q_Diff"][quan - 2] - normal_df["Q_Diff"][quan - 3]):
                print("case happened")
                k += 1
        quan -= 1
    print(k)
    return quan
