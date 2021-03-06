import pandas as pd
import algorythm as alg
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import plotly.express as px
import os
import cufflinks as cf
import numpy as np
from scipy.signal import find_peaks

# df.drop(df.index[1:50], inplace=True) на случай если нужно будет удалить
# df.reset_index(inplace=True)

fig = go.Figure()
fig = make_subplots(rows=3, cols=1)
fig2 = go.Figure()
fig2 = make_subplots(rows=1, cols=1)
fig4 = go.Figure()
fig4 = make_subplots(rows=1, cols=1)
fig5 = go.Figure()
fig5 = make_subplots(rows=1, cols=1)
fig6 = go.Figure()
fig6 = make_subplots(rows=2, cols=1,
                     specs=[[{'is_3d': True}],
                            [{'is_3d': False}]],
                     )
#
fig3 = go.Figure()
fig3 = make_subplots(rows=3, cols=1)  # создание графиков

p = pd.read_csv(r"C:\Users\Skytech2028\Desktop\\nick\boreholeAnalisys\501.csv", encoding='utf8', sep=';',
                decimal=',', parse_dates=['Время (UTC)'],
                usecols=['Время (UTC)', 'Скв501_Скв501.%откр', 'Скв501_Скв501.Qгаз'])

for n in enumerate(p['Скв501_Скв501.%откр']):
    if n[1] <= 0 or n[1] > 100:
        p['Скв501_Скв501.%откр'][n[0]] = p['Скв501_Скв501.%откр'][n[0] - 1]

for n in enumerate(p['Скв501_Скв501.Qгаз']):
    if n[1] <= 0 or n[1] > 100:
        p['Скв501_Скв501.Qгаз'][n[0]] = p['Скв501_Скв501.Qгаз'][n[0] - 1]

fig2 = px.scatter(x=p["Время (UTC)"],
                  y=p["Скв501_Скв501.Qгаз"],
                  trendline="rolling", trendline_options=dict(function="median", window=100),
                  trendline_color_override="red")

p["Perc_Approxed"] = p["Скв501_Скв501.%откр"].rolling(100).mean()
p["Perc_Approxed_Diff"] = p["Perc_Approxed"].diff()
p["Char_Approxed"] = p["Скв501_Скв501.Qгаз"].rolling(100).mean()
p["Char_Approxed_Diff"] = p["Char_Approxed"].diff()

p['Q_diff'] = p['Скв501_Скв501.Qгаз'].diff()
p['Q_approx'] = fig2.data[1].y
p['Q_DiffApproxed'] = p['Q_approx'].diff()
p['Perc_Diff'] = p['Скв501_Скв501.%откр'].diff()

normalized_df = pd.DataFrame({'Q_approx': p['Q_approx'],
                              'Perc': p['Скв501_Скв501.%откр'],
                              'Q_DiffApproxed': p['Q_DiffApproxed'],
                              'Perc_Diff': p['Perc_Diff'],
                              "Q_OrigDiff": p['Q_diff'],
                              'Q_Orig': p['Скв501_Скв501.Qгаз'],
                              'Perc_Approxed': p['Perc_Approxed'],
                              'Perc_Approxed_Diff': p['Perc_Approxed_Diff'],
                              'Char_Approxed': p["Char_Approxed"],
                              'Char_Approxed_Diff': p["Char_Approxed_Diff"]})

normalized_df = (normalized_df - normalized_df.mean()) / normalized_df.std()

normalized_df["percForPeaks"] = 0

if normalized_df["Perc_Approxed"].min() < normalized_df["Char_Approxed"].min():
    normalized_df["Perc_Approxed"] -= normalized_df["Perc_Approxed"].min()-3
    normalized_df["Char_Approxed"] -= normalized_df["Perc_Approxed"].min()-3
else:
    normalized_df["Perc_Approxed"] -= normalized_df["Char_Approxed"].min()-3
    normalized_df["Char_Approxed"] -= normalized_df["Char_Approxed"].min()-3

normalized_df["Result"] = normalized_df["Char_Approxed"]/normalized_df["Perc_Approxed"]

for n in enumerate(normalized_df["Perc_Diff"]):
    if n[1] < 0:
        normalized_df["percForPeaks"][n[0]] = normalized_df["Perc_Diff"][n[0]] * -1
    else:
        normalized_df["percForPeaks"][n[0]] = normalized_df["Perc_Diff"][n[0]]

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
), row=3, col=1)  # fig

fig3.append_trace(go.Scatter(
    x=p['Время (UTC)'],
    y=normalized_df['Perc'],
    name='Percentage'
), row=1, col=1)

fig3.append_trace(go.Scatter(
    x=p['Время (UTC)'],
    y=normalized_df['Q_approx'],
    name='Q'
), row=1, col=1)

fig3.append_trace(go.Scatter(
    x=p['Время (UTC)'],
    y=normalized_df['percForPeaks'],
    name='percForPeaks'
), row=2, col=1)

fig3.append_trace(go.Scatter(
    x=p['Время (UTC)'],
    y=normalized_df['Perc_Diff'],
    name='Perc_Diff'
), row=2, col=1)

fig3.append_trace(go.Scatter(
    x=p['Время (UTC)'],
    y=normalized_df['Q_OrigDiff'],
    name='Q_Diff'
), row=2, col=1)  # fig3

indices = find_peaks(normalized_df["percForPeaks"], threshold=1.15)[0]

fig3.append_trace(go.Scatter(
    x=p['Время (UTC)'],
    y=normalized_df['Perc_Approxed'],
    name='Perc_Approxed'
), row=1, col=1)

fig3.append_trace(go.Scatter(
    x=p['Время (UTC)'],
    y=normalized_df['Perc_Approxed_Diff'],
    name='Perc_Approxed_Diff'
), row=2, col=1)

fig3.append_trace(go.Scatter(
    x=p['Время (UTC)'],
    y=normalized_df['Perc_Approxed'],
    name='Perc_Approxed'
), row=3, col=1)

fig3.append_trace(go.Scatter(
    x=p['Время (UTC)'],
    y=normalized_df['Char_Approxed'],
    name='Char_Approxed'
), row=3, col=1)

fig3.append_trace(go.Scatter(
    x=p["Время (UTC)"][indices],
    y=[normalized_df["percForPeaks"][j] for j in indices],
    mode='markers',
    marker=dict(
        size=8,
        color='red',
        symbol='cross'
    ),
    name='Detected Peaks'
), row=2, col=1)  # fig3 + peaks

fig.update_layout(title_text="Скважина 501")
fig2.update_layout(title_text="Скважина 501")
fig3.update_layout(title_text="Скважина 501")

fig.show()
fig3.show()

normalized_df["Time"] = p['Время (UTC)']

quan = len(normalized_df["Perc_Diff"]) - 1

percs = []

for n in enumerate(indices[::-1]):
    percs.append(p['Скв501_Скв501.%откр'][n[1]])
    print(percs)

answers = alg.algorythm(normalized_df, indices)
print(answers)

endanswer = alg.comparing(indices[::-1], answers, percs)

fig4.append_trace(go.Scatter(
    x=p['Время (UTC)'][endanswer - 50:endanswer + 50],
    y=normalized_df['Perc'][endanswer - 50:endanswer + 50],
    name='Percentage'
), row=1, col=1)

fig4.append_trace(go.Scatter(
    x=p['Время (UTC)'][endanswer - 50:endanswer + 50],
    y=normalized_df['Q_approx'][endanswer - 50:endanswer + 50],
    name='Q'
), row=1, col=1)
# fig4

fig6.append_trace(go.Scatter3d(x=normalized_df['Perc_Approxed'], y=normalized_df['Char_Approxed'], z=normalized_df['Result']), row=1, col=1)

fig6.append_trace(go.Scatter(
    x=p['Время (UTC)'],
    y=normalized_df['Perc_Approxed'],
    name='Perc_Approxed'
), row=2, col=1)

fig6.append_trace(go.Scatter(
    x=p['Время (UTC)'],
    y=normalized_df['Char_Approxed'],
    name='Char_Approxed'
), row=2, col=1)

fig6.update_layout(scene = dict(
                    xaxis_title='Процент Открытия',
                    yaxis_title='Расход газа',
                    zaxis_title='Результат деления'),
                    margin=dict(r=20, b=10, l=10, t=10))

if not os.path.exists("images"):
    os.mkdir("images")
titleans = "Процент отсутствия отдачи "
dateans = p["Время (UTC)"][endanswer]
percans = p["Скв501_Скв501.%откр"][endanswer]
titleans += str(dateans)
titleans += " "
titleans += str(percans)
print(titleans)

fig4.update_layout(title_text=titleans)
fig4.show()
fig4.write_image("images/answer.pdf")
fig6.show()


_f = make_subplots(rows=2, cols=1, shared_xaxes=True)

_f1 = px.scatter(p, x='Q_DiffApproxed')
_f2 = px.scatter(p, x='Perc_Diff')

trace1 = _f1['data'][0]
trace2 = _f2['data'][0]

_f.append_trace(trace1, row=1, col=1)
_f.append_trace(trace2, row=2, col=1)

_f.show()

print()
