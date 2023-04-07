from itertools import combinations
import numpy as np
import pandas as pd

import math


def bubble_processing(data_pd):
    ############################ Declarer RAS #########################################
    # Calculate the counts for Produire_IP == 1 and Produire_IP == 0 for each region, year, taille, and transmission
    grouped_data = (
        data_pd[data_pd["Declarer_RAS"] == 1]
        .groupby(["Year", "Region", "Mode_transmission", "Form_juridique"])
        .agg({"Produire_IP": ["sum", "count"]})
    )
    # # Reset index
    grouped_data = grouped_data.reset_index()
    # # Calculate the ratio

    grouped_data["Declarer_RAS/Produit_IP"] = (
        grouped_data[("Produire_IP", "sum")] / grouped_data[("Produire_IP", "count")]
    )
    grouped_data["Declarer_RAS/Produit_IP"] = grouped_data[
        "Declarer_RAS/Produit_IP"
    ].apply(lambda x: 0 if math.isnan(x) else x)
    # # Drop unnecessary columns
    grouped_data = grouped_data.drop(
        columns=[("Produire_IP", "sum"), ("Produire_IP", "count")]
    )

    # Calculate the counts for Produire_RAS == 1 and Produire_RAS == 0 for each region, year, taille, and transmission
    grouped_data1 = (
        data_pd[data_pd["Declarer_RAS"] == 1]
        .groupby(["Year", "Region", "Mode_transmission", "Form_juridique"])
        .agg({"Produire_RAS": ["sum", "count"]})
    )
    # # Reset index
    grouped_data1 = grouped_data1.reset_index()

    # # Calculate the ratio
    grouped_data1["Declarer_RAS/Produit_RAS"] = (
        grouped_data1[("Produire_RAS", "sum")]
        / grouped_data1[("Produire_RAS", "count")]
    )
    grouped_data1["Declarer_RAS/Produit_RAS"] = grouped_data1[
        "Declarer_RAS/Produit_RAS"
    ].apply(lambda x: 0 if math.isnan(x) else x)
    # # Drop unnecessary columns
    grouped_data1 = grouped_data1.drop(
        columns=[("Produire_RAS", "sum"), ("Produire_RAS", "count")]
    )

    # Calculate the counts for Produire_TVQ == 1 and Produire_TVQ == 0 for each region, year, taille, and transmission
    grouped_data2 = (
        data_pd[data_pd["Declarer_RAS"] == 1]
        .groupby(["Year", "Region", "Mode_transmission", "Form_juridique"])
        .agg({"Produire_TVQ": ["sum", "count"]})
    )
    # # Reset index
    grouped_data2 = grouped_data2.reset_index()
    # # Calculate the ratio
    grouped_data2["Declarer_RAS/Produit_TVQ"] = (
        grouped_data2[("Produire_TVQ", "sum")]
        / grouped_data2[("Produire_TVQ", "count")]
    )
    grouped_data2["Declarer_RAS/Produit_TVQ"] = grouped_data2[
        "Declarer_RAS/Produit_TVQ"
    ].apply(lambda x: 0 if math.isnan(x) else x)
    # # Drop unnecessary columns
    grouped_data2 = grouped_data2.drop(
        columns=[("Produire_TVQ", "sum"), ("Produire_TVQ", "count")]
    )

    # Calculate the counts for Produire_IC== 1 and Produire_IC == 0 for each region, year, taille, and transmission
    grouped_data3 = (
        data_pd[data_pd["Declarer_RAS"] == 1]
        .groupby(["Year", "Region", "Mode_transmission", "Form_juridique"])
        .agg({"Produire_IC": ["sum", "count"]})
    )
    # # Reset index
    grouped_data3 = grouped_data3.reset_index()
    # # Calculate the ratio
    grouped_data3["Declarer_RAS/Produit_IC"] = (
        grouped_data3[("Produire_IC", "sum")] / grouped_data3[("Produire_IC", "count")]
    )
    grouped_data3["Declarer_RAS/Produit_IC"] = grouped_data3[
        "Declarer_RAS/Produit_IC"
    ].apply(lambda x: 0 if math.isnan(x) else x)
    # # Drop unnecessary columns
    grouped_data3 = grouped_data3.drop(
        columns=[("Produire_IC", "sum"), ("Produire_IC", "count")]
    )

    ############################ Declarer IP #########################################

    # Calculate the counts for Produire_IP == 1 and Produire_IP == 0 for each region, year, taille, and transmission
    grouped_data4 = (
        data_pd[data_pd["Declarer_IP"] == 1]
        .groupby(["Year", "Region", "Mode_transmission", "Form_juridique"])
        .agg({"Produire_IP": ["sum", "count"]})
    )
    # # Reset index
    grouped_data4 = grouped_data4.reset_index()
    # # Calculate the ratio
    grouped_data4["Declarer_IP/Produit_IP"] = (
        grouped_data4[("Produire_IP", "sum")] / grouped_data4[("Produire_IP", "count")]
    )
    grouped_data4["Declarer_IP/Produit_IP"] = grouped_data4[
        "Declarer_IP/Produit_IP"
    ].apply(lambda x: 0 if math.isnan(x) else x)
    # # Drop unnecessary columns
    grouped_data4 = grouped_data4.drop(
        columns=[("Produire_IP", "sum"), ("Produire_IP", "count")]
    )

    # Calculate the counts for Produire_RAS == 1 and Produire_RAS == 0 for each region, year, taille, and transmission
    grouped_data5 = (
        data_pd[data_pd["Declarer_IP"] == 1]
        .groupby(["Year", "Region", "Mode_transmission", "Form_juridique"])
        .agg({"Produire_RAS": ["sum", "count"]})
    )
    # # Reset index
    grouped_data5 = grouped_data5.reset_index()
    # # Calculate the ratio
    grouped_data5["Declarer_IP/Produit_RAS"] = (
        grouped_data5[("Produire_RAS", "sum")]
        / grouped_data5[("Produire_RAS", "count")]
    )
    grouped_data5["Declarer_IP/Produit_RAS"] = grouped_data5[
        "Declarer_IP/Produit_RAS"
    ].apply(lambda x: 0 if math.isnan(x) else x)
    # # Drop unnecessary columns
    grouped_data5 = grouped_data5.drop(
        columns=[("Produire_RAS", "sum"), ("Produire_RAS", "count")]
    )

    # Calculate the counts for Produire_TVQ == 1 and Produire_TVQ == 0 for each region, year, taille, and transmission
    grouped_data6 = (
        data_pd[data_pd["Declarer_IP"] == 1]
        .groupby(["Year", "Region", "Mode_transmission", "Form_juridique"])
        .agg({"Produire_TVQ": ["sum", "count"]})
    )
    # # Reset index
    grouped_data6 = grouped_data6.reset_index()
    # # Calculate the ratio
    grouped_data6["Declarer_IP/Produit_TVQ"] = (
        grouped_data6[("Produire_TVQ", "sum")]
        / grouped_data6[("Produire_TVQ", "count")]
    )
    grouped_data6["Declarer_IP/Produit_TVQ"] = grouped_data6[
        "Declarer_IP/Produit_TVQ"
    ].apply(lambda x: 0 if math.isnan(x) else x)
    # # Drop unnecessary columns
    grouped_data6 = grouped_data6.drop(
        columns=[("Produire_TVQ", "sum"), ("Produire_TVQ", "count")]
    )

    # Calculate the counts for Produire_IC== 1 and Produire_IC == 0 for each region, year, taille, and transmission
    grouped_data7 = (
        data_pd[data_pd["Declarer_IP"] == 1]
        .groupby(["Year", "Region", "Mode_transmission", "Form_juridique"])
        .agg({"Produire_IC": ["sum", "count"]})
    )
    # # Reset index
    grouped_data7 = grouped_data7.reset_index()
    # # Calculate the ratio
    grouped_data7["Declarer_IP/Produit_IC"] = (
        grouped_data7[("Produire_IC", "sum")] / grouped_data7[("Produire_IC", "count")]
    )
    grouped_data7["Declarer_IP/Produit_IC"] = grouped_data7[
        "Declarer_IP/Produit_IC"
    ].apply(lambda x: 0 if math.isnan(x) else x)
    # # Drop unnecessary columns
    grouped_data7 = grouped_data7.drop(
        columns=[("Produire_IC", "sum"), ("Produire_IC", "count")]
    )

    ############################ Declarer IC  #########################################

    # Calculate the counts for Produire_IP == 1 and Produire_IP == 0 for each region, year, taille, and transmission
    grouped_data8 = (
        data_pd[data_pd["Declarer_IC"] == 1]
        .groupby(["Year", "Region", "Mode_transmission", "Form_juridique"])
        .agg({"Produire_IP": ["sum", "count"]})
    )
    # # Reset index
    grouped_data8 = grouped_data8.reset_index()
    # # Calculate the ratio
    grouped_data8["Declarer_IC/Produit_IP"] = (
        grouped_data8[("Produire_IP", "sum")] / grouped_data8[("Produire_IP", "count")]
    )
    grouped_data8["Declarer_IC/Produit_IP"] = grouped_data8[
        "Declarer_IC/Produit_IP"
    ].apply(lambda x: 0 if math.isnan(x) else x)
    # # Drop unnecessary columns
    grouped_data8 = grouped_data8.drop(
        columns=[("Produire_IP", "sum"), ("Produire_IP", "count")]
    )

    # Calculate the counts for Produire_RAS == 1 and Produire_RAS == 0 for each region, year, taille, and transmission
    grouped_data9 = (
        data_pd[data_pd["Declarer_IC"] == 1]
        .groupby(["Year", "Region", "Mode_transmission", "Form_juridique"])
        .agg({"Produire_RAS": ["sum", "count"]})
    )
    # # Reset index
    grouped_data9 = grouped_data9.reset_index()
    # # Calculate the ratio
    grouped_data9["Declarer_IC/Produit_RAS"] = (
        grouped_data9[("Produire_RAS", "sum")]
        / grouped_data9[("Produire_RAS", "count")]
    )
    grouped_data9["Declarer_IC/Produit_RAS"] = grouped_data9[
        "Declarer_IC/Produit_RAS"
    ].apply(lambda x: 0 if math.isnan(x) else x)
    # # Drop unnecessary columns
    grouped_data9 = grouped_data9.drop(
        columns=[("Produire_RAS", "sum"), ("Produire_RAS", "count")]
    )

    # Calculate the counts for Produire_TVQ == 1 and Produire_TVQ == 0 for each region, year, taille, and transmission
    grouped_data10 = (
        data_pd[data_pd["Declarer_IC"] == 1]
        .groupby(["Year", "Region", "Mode_transmission", "Form_juridique"])
        .agg({"Produire_TVQ": ["sum", "count"]})
    )
    # # Reset index
    grouped_data10 = grouped_data10.reset_index()
    # # Calculate the ratio
    grouped_data10["Declarer_IC/Produit_TVQ"] = (
        grouped_data10[("Produire_TVQ", "sum")]
        / grouped_data10[("Produire_TVQ", "count")]
    )
    grouped_data10["Declarer_IC/Produit_TVQ"] = grouped_data10[
        "Declarer_IC/Produit_TVQ"
    ].apply(lambda x: 0 if math.isnan(x) else x)
    # # Drop unnecessary columns
    grouped_data10 = grouped_data10.drop(
        columns=[("Produire_TVQ", "sum"), ("Produire_TVQ", "count")]
    )

    # Calculate the counts for Produire_IC== 1 and Produire_IC == 0 for each region, year, taille, and transmission
    grouped_data11 = (
        data_pd[data_pd["Declarer_IC"] == 1]
        .groupby(["Year", "Region", "Mode_transmission", "Form_juridique"])
        .agg({"Produire_IC": ["sum", "count"]})
    )
    # # Reset index
    grouped_data11 = grouped_data11.reset_index()
    # # Calculate the ratio
    grouped_data11["Declarer_IC/Produit_IC"] = (
        grouped_data11[("Produire_IC", "sum")]
        / grouped_data11[("Produire_IC", "count")]
    )
    grouped_data11["Declarer_IC/Produit_IC"] = grouped_data11[
        "Declarer_IC/Produit_IC"
    ].apply(lambda x: 0 if math.isnan(x) else x)
    # # Drop unnecessary columns
    grouped_data11 = grouped_data11.drop(
        columns=[("Produire_IC", "sum"), ("Produire_IC", "count")]
    )

    ############################ Declarer TVQ  #########################################

    # Calculate the counts for Produire_IP == 1 and Produire_IP == 0 for each region, year, taille, and transmission
    grouped_data12 = (
        data_pd[data_pd["Declarer_TVQ"] == 1]
        .groupby(["Year", "Region", "Mode_transmission", "Form_juridique"])
        .agg({"Produire_IP": ["sum", "count"]})
    )
    # # Reset index
    grouped_data12 = grouped_data12.reset_index()
    # # Calculate the ratio
    grouped_data12["Declarer_TVQ/Produit_IP"] = (
        grouped_data12[("Produire_IP", "sum")]
        / grouped_data12[("Produire_IP", "count")]
    )
    grouped_data12["Declarer_TVQ/Produit_IP"] = grouped_data12[
        "Declarer_TVQ/Produit_IP"
    ].apply(lambda x: 0 if math.isnan(x) else x)
    # # Drop unnecessary columns
    grouped_data12 = grouped_data12.drop(
        columns=[("Produire_IP", "sum"), ("Produire_IP", "count")]
    )

    # Calculate the counts for Produire_RAS == 1 and Produire_RAS == 0 for each region, year, taille, and transmission
    grouped_data13 = (
        data_pd[data_pd["Declarer_TVQ"] == 1]
        .groupby(["Year", "Region", "Mode_transmission", "Form_juridique"])
        .agg({"Produire_RAS": ["sum", "count"]})
    )
    # # Reset index
    grouped_data13 = grouped_data13.reset_index()
    # # Calculate the ratio
    grouped_data13["Declarer_TVQ/Produit_RAS"] = (
        grouped_data13[("Produire_RAS", "sum")]
        / grouped_data13[("Produire_RAS", "count")]
    )
    grouped_data13["Declarer_TVQ/Produit_RAS"] = grouped_data13[
        "Declarer_TVQ/Produit_RAS"
    ].apply(lambda x: 0 if math.isnan(x) else x)
    # # Drop unnecessary columns
    grouped_data13 = grouped_data13.drop(
        columns=[("Produire_RAS", "sum"), ("Produire_RAS", "count")]
    )

    # Calculate the counts for Produire_TVQ == 1 and Produire_TVQ == 0 for each region, year, taille, and transmission
    grouped_data14 = (
        data_pd[data_pd["Declarer_TVQ"] == 1]
        .groupby(["Year", "Region", "Mode_transmission", "Form_juridique"])
        .agg({"Produire_TVQ": ["sum", "count"]})
    )
    # # Reset index
    grouped_data14 = grouped_data14.reset_index()
    # # Calculate the ratio
    grouped_data14["Declarer_TVQ/Produit_TVQ"] = (
        grouped_data14[("Produire_TVQ", "sum")]
        / grouped_data14[("Produire_TVQ", "count")]
    )
    grouped_data14["Declarer_TVQ/Produit_TVQ"] = grouped_data14[
        "Declarer_TVQ/Produit_TVQ"
    ].apply(lambda x: 0 if math.isnan(x) else x)
    # # Drop unnecessary columns
    grouped_data14 = grouped_data14.drop(
        columns=[("Produire_TVQ", "sum"), ("Produire_TVQ", "count")]
    )

    # Calculate the counts for Produire_IC== 1 and Produire_IC == 0 for each region, year, taille, and transmission
    grouped_data15 = (
        data_pd[data_pd["Declarer_TVQ"] == 1]
        .groupby(["Year", "Region", "Mode_transmission", "Form_juridique"])
        .agg({"Produire_IC": ["sum", "count"]})
    )
    # # Reset index
    grouped_data15 = grouped_data15.reset_index()
    # # Calculate the ratio
    grouped_data15["Declarer_TVQ/Produit_IC"] = (
        grouped_data15[("Produire_IC", "sum")]
        / grouped_data15[("Produire_IC", "count")]
    )
    grouped_data15["Declarer_TVQ/Produit_IC"] = grouped_data15[
        "Declarer_TVQ/Produit_IC"
    ].apply(lambda x: 0 if math.isnan(x) else x)
    # # Drop unnecessary columns
    grouped_data15 = grouped_data15.drop(
        columns=[("Produire_IC", "sum"), ("Produire_IC", "count")]
    )

    # Merging data

    grouped_data["Declarer_RAS/Produit_RAS"] = grouped_data1["Declarer_RAS/Produit_RAS"]
    grouped_data["Declarer_RAS/Produit_TVQ"] = grouped_data2["Declarer_RAS/Produit_TVQ"]
    grouped_data["Declarer_RAS/Produit_IC"] = grouped_data3["Declarer_RAS/Produit_IC"]
    grouped_data["Declarer_IP/Produit_RAS"] = grouped_data5["Declarer_IP/Produit_RAS"]
    grouped_data["Declarer_IP/Produit_IP"] = grouped_data4["Declarer_IP/Produit_IP"]
    grouped_data["Declarer_IP/Produit_TVQ"] = grouped_data6["Declarer_IP/Produit_TVQ"]
    grouped_data["Declarer_IP/Produit_IC"] = grouped_data7["Declarer_IP/Produit_IC"]
    grouped_data["Declarer_IC/Produit_RAS"] = grouped_data9["Declarer_IC/Produit_RAS"]
    grouped_data["Declarer_IC/Produit_IP"] = grouped_data8["Declarer_IC/Produit_IP"]
    grouped_data["Declarer_IC/Produit_TVQ"] = grouped_data10["Declarer_IC/Produit_TVQ"]
    grouped_data["Declarer_IC/Produit_IC"] = grouped_data11["Declarer_IC/Produit_IC"]
    grouped_data["Declarer_TVQ/Produit_RAS"] = grouped_data13[
        "Declarer_TVQ/Produit_RAS"
    ]
    grouped_data["Declarer_TVQ/Produit_IP"] = grouped_data12["Declarer_TVQ/Produit_IP"]
    grouped_data["Declarer_TVQ/Produit_TVQ"] = grouped_data14[
        "Declarer_TVQ/Produit_TVQ"
    ]
    grouped_data["Declarer_TVQ/Produit_IC"] = grouped_data15["Declarer_TVQ/Produit_IC"]

    bublechart_data = grouped_data
    bublechart_data = bublechart_data.replace(np.nan, 0)
    bublechart_data
    return bublechart_data


def filter_bubble_data( df,year,trans,form,region):
    # apply filter 
    filtered_df = df[(df['Region'] == region) & (df['Mode_transmission'] == trans) & (df['Year'] == year) & (df['Form_juridique'] == form)]
    data = list(map(lambda x : (x[0].split("/")[0],x[0].split("/")[1],filtered_df [x].values[0]),list(df.columns)[4:]))
    dataframe = pd.DataFrame(data,columns=["Declarer","Produire","Ratio"])
    return dataframe