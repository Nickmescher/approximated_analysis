import pandas as pd
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import plotly.express as px
import cufflinks as cf
import numpy as np
from sklearn.preprocessing import MinMaxScaler

# [4812:5370] для 501 скважины 'Time': p['Время (UTC)'],

fig = go.Figure()
fig = make_subplots(rows=3, cols=1)
fig2 = go.Figure()
fig2 = make_subplots(rows=1, cols=1)
fig3 = go.Figure()
fig3 = make_subplots(rows=2, cols=1)
fig4 = go.Figure()
fig4 = make_subplots(rows=1, cols=1)

p = pd.read_csv(r"C:\Users\Skytech2028\Desktop\\nick\boreholeAnalisys\501.csv", encoding='utf8', sep=';',
                decimal=',', parse_dates=['Время (UTC)'],
                usecols=['Время (UTC)', 'Скв501_Скв501.%откр', 'Скв501_Скв501.Qгаз'])

for n in enumerate(p['Скв501_Скв501.%откр']):
    if n[1] <= 0 or n[1] > 100:
        p['Скв501_Скв501.%откр'][n[0]] = p['Скв501_Скв501.%откр'][n[0] - 1]
    print(n)

for n in enumerate(p['Скв501_Скв501.Qгаз']):
    if n[1] <= 0 or n[1] > 100:
        p['Скв501_Скв501.Qгаз'][n[0]] = p['Скв501_Скв501.Qгаз'][n[0] - 1]
    print(n)

fig2 = px.scatter(x=p["Время (UTC)"],
                  y=p["Скв501_Скв501.Qгаз"],
                  trendline="rolling", trendline_options=dict(function="median", window=100))

p['diff'] = p['Скв501_Скв501.Qгаз'].diff()
p['Qnew'] = fig2.data[1].y
p['diff2'] = p['Qnew'].diff()
p['diff3'] = p['Скв501_Скв501.%откр'].diff()

df = pd.DataFrame({'Q': p['Qnew'],
                   'Perc': p['Скв501_Скв501.%откр']})

scaler = MinMaxScaler()

df_scaled = pd.DataFrame(scaler.fit_transform(df), columns=df.columns)

normalized_df = (df - df.mean()) / df.std()

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

fig3.append_trace(go.Scatter(
    x=p["Время (UTC)"],
    y=p["diff3"],
    name='PercentageDiff'
), row=1, col=1)

fig3.append_trace(go.Scatter(
    x=p["Время (UTC)"],
    y=p["diff2"],
    name='ApproxedDiff'
), row=2, col=1)

fig4.append_trace(go.Scatter(
    x=p['Время (UTC)'],
    y=df_scaled['Perc'],
    name='Percentage'
), row=1, col=1)

fig4.append_trace(go.Scatter(
    x=p['Время (UTC)'],
    y=df_scaled['Q'],
    name='Q'
), row=1, col=1)

fig.show()
fig2.show()
fig3.show()
fig4.show()

print(df)
print(df_scaled)
print()
