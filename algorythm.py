import pandas as pd
import numpy as np


def algorythm(df, indices):
    for n in enumerate(indices[::-1]):
        if n[1] > 0:
            if (df["Q_Orig"][n[1]] > df["Q_Orig"][n[1] + 1] and df["Q_Orig"][n[1]] > df["Q_Orig"][n[1] - 1]) or \
                    (df["Q_Orig"][n[1] + 1] > df["Q_Orig"][n[1] + 2] and df["Q_Orig"][n[1]] > df["Q_Orig"][n[1]]):
                print("найден пик на")
                print(n[1])
        else:
            if (df["Q_Orig"][n[1]] < df["Q_Orig"][n[1] + 1] and df["Q_Orig"][n[1]] < df["Q_Orig"][n[1] - 1]) or \
                    (df["Q_Orig"][n[1] + 1] < df["Q_Orig"][n[1] + 2] and df["Q_Orig"][n[1]] < df["Q_Orig"][n[1]]):
                print("найден пик")
