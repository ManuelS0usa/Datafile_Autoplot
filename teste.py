

def upgrade_graph(contents, filename):
    fig = {
        'layout': go.Layout(
            plot_bgcolor=colors["graphBackground"],
            paper_bgcolor=colors["graphBackground"])
    }

    if contents:
        contents = contents[0]
        filename = filename[0]
        df = parse_data(contents, filename)
        df = df.set_index(df.columns[0])
        print(df)
        fig['data'] = df.iplot(asFigure=True, kind='scatter', mode='lines+markers', size=1)

    return fig
