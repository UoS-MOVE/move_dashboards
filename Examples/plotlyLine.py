fig = go.Figure()
fig.add_trace(go.Scatter(x=df.Date, y=df['AAPL.High'], name="AAPL High",
                         line_color='deepskyblue'))

fig.add_trace(go.Scatter(x=df.Date, y=df['AAPL.Low'], name="AAPL Low",
                         line_color='dimgray'))

fig.update_layout(title_text='Time Series with Rangeslider',
                  xaxis_rangeslider_visible=True)



import dash_core_components as dcc
import plotly.graph_objs as go
fig = go.Figure(data=[go.Scatter(x=[1, 2, 3], y=[4, 1, 2])])
dcc.Graph(
        id='example-graph-2',
        figure=fig
    )