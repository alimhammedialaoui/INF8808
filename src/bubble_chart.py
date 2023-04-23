import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import hover_template as hover


def get_plot(my_df):
    """
    Generates the bubble plot.

    Args:
        my_df: The dataframe to display
    Returns:
        The generated figure
    """
    
    df_temp1 = my_df.copy()
    df_temp2 = my_df.copy()
    df_temp1.insert(3, "Default", ["No"] * len(my_df["Ratio"]))
    df_temp2.insert(3, "Default", ["Yes"] * len(my_df["Ratio"]))
    df_temp1.loc[df_temp1["Default"] == "Yes", ["Ratio"]] = 1
    df_temp2.loc[df_temp2["Default"] == "Yes", ["Ratio"]] = 1
    df_temp1 = df_temp1.append({'Declarer': None, 'Produire': None, 'Ratio':1}, ignore_index=True)
    
    fig = px.scatter(
        df_temp1,
        x="Declarer",
        y="Produire",
        size="Ratio",
        size_max=30,
        text=list(
            map(
                lambda n: "{:.0f}%".format(int(round(n, 2) * 100)),
                list(df_temp1["Ratio"].values),
            )
        ),
        labels={"Declarer": "Déclarer sans erreurs", "Produire": "Produire à temps"},
        title="Analyse (en %) de la corrélation entre les indicateurs de déclaration et de production",
    )
    fig.update_traces(name="Scatter 1")
    fig.update_traces(textposition='middle center')
    
    trace_2 = go.Scatter(
            x=df_temp2["Declarer"],
            y=df_temp2["Produire"],
            mode="markers",
            marker=dict(
                size=df_temp2["Ratio"] * 100*0.6,
                sizemode="diameter",
                sizemin = 20,
            ),
            text=[f"{int(n)}%" for n in df_temp2["Ratio"] * 100],
            name ="Scatter 2",
            showlegend=False
        )
    fig.add_trace(trace_2)

    fig.update_traces(
        marker=dict(
            sizemin=7,
            size=df_temp1["Ratio"] * 1.7,
            color=px.colors.qualitative.Set1[0],
            opacity=[1] * len(my_df["Ratio"]) + [0.1] * len(my_df["Ratio"]),
        ),
        textposition="middle center",
        textfont =dict(color ="white", size = 10),
        selector = dict(name="Scatter 1")
    )
    fig.update_traces(
        marker=dict(
            color=px.colors.qualitative.Set1[0],
            opacity=[0.5] * len(my_df["Ratio"]) + [0.00] * len(my_df["Ratio"]),
        ),
        selector = dict(name="Scatter 2")
    )

    fig.update_traces(hovertemplate=hover.bubblechart_hover_template())
    fig.data = [fig.data[1], fig.data[0]]
    
    fig.update_layout(xaxis_title='')
    fig.add_annotation(x=-0.20, y=-0.17, 
                       xref="x", 
                       yref="paper", 
                       showarrow=False, 
                       text="Déclarer sans erreurs", 
                       font=dict(size=14), 
                       textangle=0)


    fig.update_layout(
        xaxis=dict(
            tickmode="linear",  # Set tick mode to linear
            dtick=0.5,  # Set the interval between ticks to 0.5
        ),
        yaxis=dict(
            tickmode="linear",  # Set tick mode to linear
            dtick=0.1,  # Set the interval between ticks to 0.5
        ),
        width=800,  # Set the width of the chart to 800 pixels
        height=600,  # Set the height of the chart to 600 pixels
    )

    fig.update_xaxes(labelalias=dict(Declarer_RAS="Déclarer RAS", 
                                     Declarer_IP="Déclarer IP",
                                     Declarer_TVQ="Déclarer TVQ",
                                     Declarer_IC="Déclarer IC",
                                     ))
    fig.update_yaxes(labelalias=dict(Produit_IC="Produire IC",
                                    Produit_IP="Produire IP",
                                    Produit_TVQ="Produire TVQ",
                                    Produit_RAS="Produire RAS"))

    return fig
