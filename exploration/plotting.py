import datetime as dt
import plotly.graph_objects as go

class CandlePlot:

    def __init__(self,df, candles = True):
        self.df_plot = df.copy()
        self.candles = candles
        # We do not change the original data !
        self.create_candle_fig()


    def add_timestr(self):
        self.df_plot['sTime'] = [dt.datetime.strftime(i, "s%Y-%m-%d %H:%M") for i in self.df_plot['time']]

    def create_candle_fig(self):
        self.add_timestr()
        self.fig = go.Figure()
        if self.candles==True:
            self.fig.add_trace(go.Candlestick(
                    x=self.df_plot['sTime'],
                    open=self.df_plot['mid_o'],
                    high=self.df_plot['mid_h'],
                    low=self.df_plot['mid_l'],
                    close=self.df_plot['mid_c'],
                    name='Candlesticks'),
                    )
    def update_layout(self,width, height, nticks):
        self.fig.update_yaxes(
            gridcolor='rgb(15,15,15)',
        )
        self.fig.update_xaxes(
            gridcolor='rgb(15,15,15)',
            rangeslider_visible=False,
            nticks = nticks,
        )
        self.fig.update_layout(
            width=width,
            height=height,
            margin = dict(l = 10, r = 10, t = 10, b = 10),
            paper_bgcolor='#1f2630',
            plot_bgcolor='#1f2630',
            font = dict(size = 8, color='white'),
        )
    def add_traces(self, line_traces):
        for t in line_traces:
            self.fig.add_trace(go.Scatter(
                x=self.df_plot['sTime'],
                y=self.df_plot[t],
                line = dict(width=2),
                name=t,
                line_shape='spline'
            ))

    def show_plot(self, width = 1500, height = 400, nticks = 10, line_traces = []):
        self.add_traces(line_traces)
        self.update_layout(width,height,nticks)
        self.fig.show()
