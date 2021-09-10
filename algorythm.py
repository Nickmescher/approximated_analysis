import pandas as pd
import numpy as np


def algorythm(df, indices):
    answers = []
    for n in enumerate(indices[::-1]):
        if df["Perc_Diff"][n[1]] > 0:
            if df["Q_OrigDiff"][n[1]] > df["Q_OrigDiff"][n[1] + 1] and df["Q_OrigDiff"][n[1]] > \
                    df["Q_OrigDiff"][n[1] - 1]:
                # (df["Q_OrigDiff"][n[1] + 1] > df["Q_OrigDiff"][n[1] + 2] and df["Q_OrigDiff"][n[1] + 1] > df["Q_OrigDiff"][n[1]]):
                print("найден пик на")
                print(df["Time"][n[1]])
                answers[n[0]] = n[1]
        else:
            if (df["Q_OrigDiff"][n[1]] < df["Q_OrigDiff"][n[1] + 1] and df["Q_OrigDiff"][n[1]] < \
                    df["Q_OrigDiff"][n[1] - 1]):
                # (df["Q_OrigDiff"][n[1] + 1] < df["Q_OrigDiff"][n[1] + 2] and df["Q_OrigDiff"][n[1] + 1] < df["Q_OrigDifff"][n[1]]):
                print("найден пик на")
                print(df["Time"][n[1]])
                answers[n[0]] = n[1]

    return answers