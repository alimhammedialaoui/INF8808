import plotly.express as px
import pandas as pd
import hover_template as hover


def get_plot(my_df):
    """
    Generates the bubble plot.

    The x and y axes are log scaled, and there is
    an animation between the data for years 2000 and 2015.

    The discrete color scale (sequence) to use is Set1 (see : https://plotly.com/python/discrete-color/)

    The markers' maximum size is 30 and their minimum
    size is 6.

    Args:
        my_df: The dataframe to display
        gdp_range: The range for the x axis
        co2_range: The range for the y axis
    Returns:
        The generated figure
    """
    # TODO : Define figure with animation
    df_temp1 = my_df.copy()
    df_temp2 = my_df.copy()
    df_temp1.insert(3, "Default", ["No"] * len(my_df["Ratio"]))
    df_temp2.insert(3, "Default", ["Yes"] * len(my_df["Ratio"]))
    df_whole = pd.concat([df_temp1, df_temp2], ignore_index=True)
    df_whole.loc[df_whole["Default"] == "Yes", ["Ratio"]] = 1
    
    fig = px.scatter(
        df_whole,
        x="Declarer",
        y="Produire",
        size="Ratio",
        text=list(
            map(
                lambda n: "{:.2f}%".format(round(n, 2) * 100),
                list(df_whole["Ratio"].values),
            )
        ),
        labels={"Declarer": "Déclarer sans erreurs", "Produire": "Produire à temps"},
        title="Analyse (en %) de la corrélation entre les indicateurs de déclaration et de production",
    )
    # a = [1] * len(my_df["Ratio"]) + [0.1] * len(my_df["Ratio"])
    # print(len(a))
    # print(a)
    fig.update_traces(
        marker=dict(
            sizemin=7,
            color=px.colors.qualitative.Set1[0],
            opacity=[1]*len(my_df["Ratio"]) + [0.1]*len(my_df["Ratio"]),

        ),
        textposition="top center",
    )
    fig.update_traces(hovertemplate=hover.bubblechart_hover_template())
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
    return fig
