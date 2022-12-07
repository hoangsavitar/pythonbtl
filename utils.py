import pandas as pd
import numpy as np


def save_point(name_player, point):
    vt = -1
    df = pd.read_csv("rank.csv")
    for i in range(len(df)):
        if df['score'][i] < point:
            vt = i
            break
    if vt != -1:
        for i in range(len(df)-1, vt, -1):
            df['score'][i] = df['score'][i-1]
            df['name_player'][i] = df['name_player'][i-1]
        df['score'][vt] = point
        df['name_player'][vt] = name_player
        df.to_csv('rank.csv', index=False)
    print(df)
# save_point("nam", 6)
