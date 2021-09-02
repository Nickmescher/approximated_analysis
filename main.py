import pandas as pd
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import plotly.express as px
import cufflinks as cf
import numpy as np
from sklearn import preprocessing

# [4812:5370] для 501 скважины

fig = go.Figure()
fig = make_subplots(rows=3, cols=1)
cf.go_offline()
fig2 = go.Figure()
fig2 = make_subplots(rows=1, cols=1)

p = pd.read_csv(r"C:\Users\Skytech2028\Desktop\\nick\boreholeAnalisys\501.csv", encoding='utf8', sep=';',
                decimal=',', parse_dates=['Время (UTC)'])

for n in enumerate(p['Скв501_Скв501.%откр']):
    n = list(n)
    if n[1] <= 0:
        p['Скв501_Скв501.%откр'][n[0]] = p['Скв501_Скв501.%откр'][n[0]-1]
    print(n)

for n in enumerate(p['Скв501_Скв501.Qгаз']):
    n = list(n)
    if n[1] <= 0:
        p['Скв501_Скв501.Qгаз'][n[0]] = p['Скв501_Скв501.Qгаз'][n[0]-1]
    print(n)

p['diff'] = p['Скв501_Скв501.Qгаз'].diff()

fig2 = px.scatter(x=p["Время (UTC)"],
                  y=p["Скв501_Скв501.Qгаз"],
                  trendline="rolling", trendline_options=dict(function="median", window=100))

p['diff2'] = fig2.data[1].y
p['diff2'] = p['diff2'].diff()

fig.append_trace(go.Scatter(
    x=p["Время (UTC)"],
    y=p['Скв501_Скв501.%откр'],
    name="Процент открытия",
), row=1, col=1)

fig.append_trace(go.Scatter(
    x=p["Время (UTC)"],
    y=p["Скв501_Скв501.Qгаз"],
    name="Расход газа",
), row=2, col=1)

fig.append_trace(go.Scatter(
    x=fig2.data[1].x,
    y=fig2.data[1].y,
    name="approximated",
), row=3, col=1)

fig.update_layout(title_text="Скважина 501")

p["time"] = p["Время (UTC)"]

fig3 = px.line(x=p["Время (UTC)"],
               y=p["diff2"], )

fig.show()
fig2.show()
fig3.show()
print(p["diff2"])
print()