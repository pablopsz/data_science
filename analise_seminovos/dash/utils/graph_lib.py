import plotly_express as px


class GraphLib:
    @staticmethod
    def line_chart(df, x, y, title, color):
        fig = px.line(df, x=x, y=y,title=title, color=color)
        return fig

    
    @staticmethod
    def bar_chart(df, x, y, title=None):
        fig = px.bar(df, x, y, title=title)
        return fig
