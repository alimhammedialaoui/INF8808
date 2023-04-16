from itertools import combinations
import numpy as np
import pandas as pd

import math

def LEN(x):
    return len(x)

def bubble_processing(data_pd,year,region,trans,forme):
    # Filter data where Declarer_RAS is 1
    grouped_data = data_pd[data_pd["Declarer_RAS"] == 1]
    grouped_data = (
        grouped_data.groupby(["Year", "Region", "Mode_transmission", "Form_juridique"])
        .agg({"Produire_IP": ["sum", LEN]})
        .reset_index()
    )
    ############################ Declarer RAS #########################################
    # grouped_data = data_pd[data_pd["Declarer_RAS"] == 1].groupby(['Year', 'Region','Mode_transmission','Form_juridique']).agg({"Produire_IP": ["sum", "count"]})
    #  grouped_data =  data_filtered[ data_filtered["Declarer_RAS"] == 1].groupby(['Form_juridique']).agg({"Produire_IP": ["sum", "count"]})
    # # Reset index
    # data_filtered = data_filtered.reset_index()
    # # Calculate the ratio
    grouped_data["Declarer_RAS/Produit_IP"] = (
        grouped_data[("Produire_IP", "sum")] / grouped_data[("Produire_IP", "LEN")]
    )
    grouped_data["Declarer_RAS/Produit_IP"] = grouped_data[
        "Declarer_RAS/Produit_IP"
    ].apply(lambda x: 0 if math.isnan(x) else x)
    # # Drop unnecessary columns
    grouped_data = grouped_data.drop(
        columns=[("Produire_IP", "sum"), ("Produire_IP", "LEN")]
    )

    # Calculate the counts for Produire_RAS == 1 and Produire_RAS == 0 for each region, year, taille, and transmission
    grouped_data1 = (
        data_pd[data_pd["Declarer_RAS"] == 1]
        .groupby(["Year", "Region", "Mode_transmission", "Form_juridique"])
        .agg({"Produire_RAS": ["sum", LEN]})
    )
    # # Reset index
    grouped_data1 = grouped_data1.reset_index()
    # # Calculate the ratio
    grouped_data1["Declarer_RAS/Produit_RAS"] = (
        grouped_data1[("Produire_RAS", "sum")] / grouped_data1[("Produire_RAS", "LEN")]
    )
    # grouped_data1["Declarer_RAS/Produit_RAS"]= grouped_data1["Declarer_RAS/Produit_RAS"].apply(lambda x: 0 if math.isnan(x) else x)
    # # Drop unnecessary columns
    grouped_data1 = grouped_data1.drop(
        columns=[("Produire_RAS", "sum"), ("Produire_RAS", "LEN")]
    )

    # Calculate the counts for Produire_TVQ == 1 and Produire_TVQ == 0 for each region, year, taille, and transmission
    grouped_data2 = (
        data_pd[data_pd["Declarer_RAS"] == 1]
        .groupby(["Year", "Region", "Mode_transmission", "Form_juridique"])
        .agg({"Produire_TVQ": ["sum", LEN]})
    )
    # # Reset index
    grouped_data2 = grouped_data2.reset_index()
    # # Calculate the ratio
    grouped_data2["Declarer_RAS/Produit_TVQ"] = (
        grouped_data2[("Produire_TVQ", "sum")] / grouped_data2[("Produire_TVQ", "LEN")]
    )
    grouped_data2["Declarer_RAS/Produit_TVQ"] = grouped_data2[
        "Declarer_RAS/Produit_TVQ"
    ].apply(lambda x: 0 if math.isnan(x) else x)
    # # Drop unnecessary columns
    grouped_data2 = grouped_data2.drop(
        columns=[("Produire_TVQ", "sum"), ("Produire_TVQ", "LEN")]
    )

    # Calculate the counts for Produire_IC== 1 and Produire_IC == 0 for each region, year, taille, and transmission
    grouped_data3 = (
        data_pd[data_pd["Declarer_RAS"] == 1]
        .groupby(["Year", "Region", "Mode_transmission", "Form_juridique"])
        .agg({"Produire_IC": ["sum", LEN]})
    )
    # # Reset index
    grouped_data3 = grouped_data3.reset_index()
    # # Calculate the ratio
    grouped_data3["Declarer_RAS/Produit_IC"] = (
        grouped_data3[("Produire_IC", "sum")] / grouped_data3[("Produire_IC", "LEN")]
    )
    grouped_data3["Declarer_RAS/Produit_IC"] = grouped_data3[
        "Declarer_RAS/Produit_IC"
    ].apply(lambda x: 0 if math.isnan(x) else x)
    # # Drop unnecessary columns
    grouped_data3 = grouped_data3.drop(
        columns=[("Produire_IC", "sum"), ("Produire_IC", "LEN")]
    )

    ############################ Declarer IP #########################################

    # Calculate the counts for Produire_IP == 1 and Produire_IP == 0 for each region, year, taille, and transmission
    grouped_data4 = (
        data_pd[data_pd["Declarer_IP"] == 1]
        .groupby(["Year", "Region", "Mode_transmission", "Form_juridique"])
        .agg({"Produire_IP": ["sum", LEN]})
    )
    # # Reset index
    grouped_data4 = grouped_data4.reset_index()
    # # Calculate the ratio
    grouped_data4["Declarer_IP/Produit_IP"] = (
        grouped_data4[("Produire_IP", "sum")] / grouped_data4[("Produire_IP", "LEN")]
    )
    grouped_data4["Declarer_IP/Produit_IP"] = grouped_data4[
        "Declarer_IP/Produit_IP"
    ].apply(lambda x: 0 if math.isnan(x) else x)
    # # Drop unnecessary columns
    grouped_data4 = grouped_data4.drop(
        columns=[("Produire_IP", "sum"), ("Produire_IP", "LEN")]
    )

    # Calculate the counts for Produire_RAS == 1 and Produire_RAS == 0 for each region, year, taille, and transmission
    grouped_data5 = (
        data_pd[data_pd["Declarer_IP"] == 1]
        .groupby(["Year", "Region", "Mode_transmission", "Form_juridique"])
        .agg({"Produire_RAS": ["sum", LEN]})
    )
    # # Reset index
    grouped_data5 = grouped_data5.reset_index()
    # # Calculate the ratio
    grouped_data5["Declarer_IP/Produit_RAS"] = (
        grouped_data5[("Produire_RAS", "sum")] / grouped_data5[("Produire_RAS", "LEN")]
    )
    grouped_data5["Declarer_IP/Produit_RAS"] = grouped_data5[
        "Declarer_IP/Produit_RAS"
    ].apply(lambda x: 0 if math.isnan(x) else x)
    # # Drop unnecessary columns
    grouped_data5 = grouped_data5.drop(
        columns=[("Produire_RAS", "sum"), ("Produire_RAS", "LEN")]
    )

    # Calculate the counts for Produire_TVQ == 1 and Produire_TVQ == 0 for each region, year, taille, and transmission
    grouped_data6 = (
        data_pd[data_pd["Declarer_IP"] == 1]
        .groupby(["Year", "Region", "Mode_transmission", "Form_juridique"])
        .agg({"Produire_TVQ": ["sum", LEN]})
    )
    # # Reset index
    grouped_data6 = grouped_data6.reset_index()
    # # Calculate the ratio
    grouped_data6["Declarer_IP/Produit_TVQ"] = (
        grouped_data6[("Produire_TVQ", "sum")] / grouped_data6[("Produire_TVQ", "LEN")]
    )
    grouped_data6["Declarer_IP/Produit_TVQ"] = grouped_data6[
        "Declarer_IP/Produit_TVQ"
    ].apply(lambda x: 0 if math.isnan(x) else x)
    # # Drop unnecessary columns
    grouped_data6 = grouped_data6.drop(
        columns=[("Produire_TVQ", "sum"), ("Produire_TVQ", "LEN")]
    )

    # Calculate the counts for Produire_IC== 1 and Produire_IC == 0 for each region, year, taille, and transmission
    grouped_data7 = (
        data_pd[data_pd["Declarer_IP"] == 1]
        .groupby(["Year", "Region", "Mode_transmission", "Form_juridique"])
        .agg({"Produire_IC": ["sum", LEN]})
    )
    # # Reset index
    grouped_data7 = grouped_data7.reset_index()
    # # Calculate the ratio
    grouped_data7["Declarer_IP/Produit_IC"] = (
        grouped_data7[("Produire_IC", "sum")] / grouped_data7[("Produire_IC", "LEN")]
    )
    grouped_data7["Declarer_IP/Produit_IC"] = grouped_data7[
        "Declarer_IP/Produit_IC"
    ].apply(lambda x: 0 if math.isnan(x) else x)
    # # Drop unnecessary columns
    grouped_data7 = grouped_data7.drop(
        columns=[("Produire_IC", "sum"), ("Produire_IC", "LEN")]
    )

    ############################ Declarer IC  #########################################

    # Calculate the counts for Produire_IP == 1 and Produire_IP == 0 for each region, year, taille, and transmission
    grouped_data8 = (
        data_pd[data_pd["Declarer_IC"] == 1]
        .groupby(["Year", "Region", "Mode_transmission", "Form_juridique"])
        .agg({"Produire_IP": ["sum", LEN]})
    )
    # # Reset index
    grouped_data8 = grouped_data8.reset_index()
    # # Calculate the ratio
    grouped_data8["Declarer_IC/Produit_IP"] = (
        grouped_data8[("Produire_IP", "sum")] / grouped_data8[("Produire_IP", "LEN")]
    )
    grouped_data8["Declarer_IC/Produit_IP"] = grouped_data8[
        "Declarer_IC/Produit_IP"
    ].apply(lambda x: 0 if math.isnan(x) else x)
    # # Drop unnecessary columns
    grouped_data8 = grouped_data8.drop(
        columns=[("Produire_IP", "sum"), ("Produire_IP", "LEN")]
    )

    # Calculate the counts for Produire_RAS == 1 and Produire_RAS == 0 for each region, year, taille, and transmission
    grouped_data9 = (
        data_pd[data_pd["Declarer_IC"] == 1]
        .groupby(["Year", "Region", "Mode_transmission", "Form_juridique"])
        .agg({"Produire_RAS": ["sum", LEN]})
    )
    # # Reset index
    grouped_data9 = grouped_data9.reset_index()
    # # Calculate the ratio
    grouped_data9["Declarer_IC/Produit_RAS"] = (
        grouped_data9[("Produire_RAS", "sum")] / grouped_data9[("Produire_RAS", "LEN")]
    )
    grouped_data9["Declarer_IC/Produit_RAS"] = grouped_data9[
        "Declarer_IC/Produit_RAS"
    ].apply(lambda x: 0 if math.isnan(x) else x)
    # # Drop unnecessary columns
    grouped_data9 = grouped_data9.drop(
        columns=[("Produire_RAS", "sum"), ("Produire_RAS", "LEN")]
    )

    # Calculate the counts for Produire_TVQ == 1 and Produire_TVQ == 0 for each region, year, taille, and transmission
    grouped_data10 = (
        data_pd[data_pd["Declarer_IC"] == 1]
        .groupby(["Year", "Region", "Mode_transmission", "Form_juridique"])
        .agg({"Produire_TVQ": ["sum", LEN]})
    )
    # # Reset index
    grouped_data10 = grouped_data10.reset_index()
    # # Calculate the ratio
    grouped_data10["Declarer_IC/Produit_TVQ"] = (
        grouped_data10[("Produire_TVQ", "sum")]
        / grouped_data10[("Produire_TVQ", "LEN")]
    )
    grouped_data10["Declarer_IC/Produit_TVQ"] = grouped_data10[
        "Declarer_IC/Produit_TVQ"
    ].apply(lambda x: 0 if math.isnan(x) else x)
    # # Drop unnecessary columns
    grouped_data10 = grouped_data10.drop(
        columns=[("Produire_TVQ", "sum"), ("Produire_TVQ", "LEN")]
    )

    # Calculate the counts for Produire_IC== 1 and Produire_IC == 0 for each region, year, taille, and transmission
    grouped_data11 = (
        data_pd[data_pd["Declarer_IC"] == 1]
        .groupby(["Year", "Region", "Mode_transmission", "Form_juridique"])
        .agg({"Produire_IC": ["sum", LEN]})
    )
    # # Reset index
    grouped_data11 = grouped_data11.reset_index()
    # # Calculate the ratio
    grouped_data11["Declarer_IC/Produit_IC"] = (
        grouped_data11[("Produire_IC", "sum")] / grouped_data11[("Produire_IC", "LEN")]
    )
    grouped_data11["Declarer_IC/Produit_IC"] = grouped_data11[
        "Declarer_IC/Produit_IC"
    ].apply(lambda x: 0 if math.isnan(x) else x)
    # # Drop unnecessary columns
    grouped_data11 = grouped_data11.drop(
        columns=[("Produire_IC", "sum"), ("Produire_IC", "LEN")]
    )

    ############################ Declarer TVQ  #########################################

    # Calculate the counts for Produire_IP == 1 and Produire_IP == 0 for each region, year, taille, and transmission
    grouped_data12 = (
        data_pd[data_pd["Declarer_TVQ"] == 1]
        .groupby(["Year", "Region", "Mode_transmission", "Form_juridique"])
        .agg({"Produire_IP": ["sum", LEN]})
    )
    # # Reset index
    grouped_data12 = grouped_data12.reset_index()
    # # Calculate the ratio
    grouped_data12["Declarer_TVQ/Produit_IP"] = (
        grouped_data12[("Produire_IP", "sum")] / grouped_data12[("Produire_IP", "LEN")]
    )
    grouped_data12["Declarer_TVQ/Produit_IP"] = grouped_data12[
        "Declarer_TVQ/Produit_IP"
    ].apply(lambda x: 0 if math.isnan(x) else x)
    # # Drop unnecessary columns
    grouped_data12 = grouped_data12.drop(
        columns=[("Produire_IP", "sum"), ("Produire_IP", "LEN")]
    )

    # Calculate the counts for Produire_RAS == 1 and Produire_RAS == 0 for each region, year, taille, and transmission
    grouped_data13 = (
        data_pd[data_pd["Declarer_TVQ"] == 1]
        .groupby(["Year", "Region", "Mode_transmission", "Form_juridique"])
        .agg({"Produire_RAS": ["sum", LEN]})
    )
    # # Reset index
    grouped_data13 = grouped_data13.reset_index()
    # # Calculate the ratio
    grouped_data13["Declarer_TVQ/Produit_RAS"] = (
        grouped_data13[("Produire_RAS", "sum")]
        / grouped_data13[("Produire_RAS", "LEN")]
    )
    grouped_data13["Declarer_TVQ/Produit_RAS"] = grouped_data13[
        "Declarer_TVQ/Produit_RAS"
    ].apply(lambda x: 0 if math.isnan(x) else x)
    # # Drop unnecessary columns
    grouped_data13 = grouped_data13.drop(
        columns=[("Produire_RAS", "sum"), ("Produire_RAS", "LEN")]
    )

    # Calculate the counts for Produire_TVQ == 1 and Produire_TVQ == 0 for each region, year, taille, and transmission
    grouped_data14 = (
        data_pd[data_pd["Declarer_TVQ"] == 1]
        .groupby(["Year", "Region", "Mode_transmission", "Form_juridique"])
        .agg({"Produire_TVQ": ["sum", LEN]})
    )
    # # Reset index
    grouped_data14 = grouped_data14.reset_index()
    # # Calculate the ratio
    grouped_data14["Declarer_TVQ/Produit_TVQ"] = (
        grouped_data14[("Produire_TVQ", "sum")]
        / grouped_data14[("Produire_TVQ", "LEN")]
    )
    grouped_data14["Declarer_TVQ/Produit_TVQ"] = grouped_data14[
        "Declarer_TVQ/Produit_TVQ"
    ].apply(lambda x: 0 if math.isnan(x) else x)
    # # Drop unnecessary columns
    grouped_data14 = grouped_data14.drop(
        columns=[("Produire_TVQ", "sum"), ("Produire_TVQ", "LEN")]
    )

    # Calculate the counts for Produire_IC== 1 and Produire_IC == 0 for each region, year, taille, and transmission
    grouped_data15 = (
        data_pd[data_pd["Declarer_TVQ"] == 1]
        .groupby(["Year", "Region", "Mode_transmission", "Form_juridique"])
        .agg({"Produire_IC": ["sum", LEN]})
    )
    # # Reset index
    grouped_data15 = grouped_data15.reset_index()
    # # Calculate the ratio
    grouped_data15["Declarer_TVQ/Produit_IC"] = (
        grouped_data15[("Produire_IC", "sum")] / grouped_data15[("Produire_IC", "LEN")]
    )
    grouped_data15["Declarer_TVQ/Produit_IC"] = grouped_data15[
        "Declarer_TVQ/Produit_IC"
    ].apply(lambda x: 0 if math.isnan(x) else x)
    # # Drop unnecessary columns
    grouped_data15 = grouped_data15.drop(
        columns=[("Produire_IC", "sum"), ("Produire_IC", "LEN")]
    )

    # Merging data
    new_data = grouped_data

    new_data["Declarer_RAS/Produit_RAS"] = grouped_data1["Declarer_RAS/Produit_RAS"]
    new_data["Declarer_RAS/Produit_TVQ"] = grouped_data2["Declarer_RAS/Produit_TVQ"]
    new_data["Declarer_RAS/Produit_IC"] = grouped_data3["Declarer_RAS/Produit_IC"]
    new_data["Declarer_IP/Produit_RAS"] = grouped_data5["Declarer_IP/Produit_RAS"]
    new_data["Declarer_IP/Produit_IP"] = grouped_data4["Declarer_IP/Produit_IP"]
    new_data["Declarer_IP/Produit_TVQ"] = grouped_data6["Declarer_IP/Produit_TVQ"]
    new_data["Declarer_IP/Produit_IC"] = grouped_data7["Declarer_IP/Produit_IC"]
    new_data["Declarer_IC/Produit_RAS"] = grouped_data9["Declarer_IC/Produit_RAS"]
    new_data["Declarer_IC/Produit_IP"] = grouped_data8["Declarer_IC/Produit_IP"]
    new_data["Declarer_IC/Produit_TVQ"] = grouped_data10["Declarer_IC/Produit_TVQ"]
    new_data["Declarer_IC/Produit_IC"] = grouped_data11["Declarer_IC/Produit_IC"]
    new_data["Declarer_TVQ/Produit_RAS"] = grouped_data13["Declarer_TVQ/Produit_RAS"]
    new_data["Declarer_TVQ/Produit_IP"] = grouped_data12["Declarer_TVQ/Produit_IP"]
    new_data["Declarer_TVQ/Produit_TVQ"] = grouped_data14["Declarer_TVQ/Produit_TVQ"]
    new_data["Declarer_TVQ/Produit_IC"] = grouped_data15["Declarer_TVQ/Produit_IC"]

    # Filter the grouped data based on selected variable values
    if region != "ALL":
        new_data = new_data[new_data["Region"] == region]
    if trans != "ALL":
        new_data = new_data[new_data["Mode_transmission"] == trans]
    if year != "ALL":
        new_data = new_data[new_data["Year"] == year]

    new_data = new_data[new_data["Form_juridique"] == forme]

    mean_values = {
        "Declarer_RAS/Produit_IP":new_data["Declarer_RAS/Produit_IP"].mean(),
        "Declarer_RAS/Produit_RAS": new_data["Declarer_RAS/Produit_RAS"].mean(),
        "Declarer_RAS/Produit_TVQ":new_data["Declarer_RAS/Produit_TVQ"].mean(),
        "Declarer_RAS/Produit_IC":new_data["Declarer_RAS/Produit_IC"].mean(),
        "Declarer_IP/Produit_RAS":new_data["Declarer_IP/Produit_RAS"].mean(),
        "Declarer_IP/Produit_IP":new_data["Declarer_IP/Produit_IP"].mean(),
        "Declarer_IP/Produit_TVQ":new_data["Declarer_IP/Produit_TVQ"].mean(),
        "Declarer_IP/Produit_IC":new_data["Declarer_IP/Produit_IC"].mean(),
        "Declarer_IC/Produit_RAS":new_data["Declarer_IC/Produit_RAS"].mean(),
        "Declarer_IC/Produit_IP":new_data["Declarer_IC/Produit_IP"].mean(),
        "Declarer_IC/Produit_TVQ":new_data["Declarer_IC/Produit_TVQ"].mean(),
        "Declarer_IC/Produit_IC":new_data["Declarer_IC/Produit_IC"].mean(),
        "Declarer_TVQ/Produit_RAS":new_data["Declarer_TVQ/Produit_RAS"].mean(),
        "Declarer_TVQ/Produit_IP":new_data["Declarer_TVQ/Produit_IP"].mean(),
        "Declarer_TVQ/Produit_TVQ":new_data["Declarer_TVQ/Produit_TVQ"].mean(),
        "Declarer_TVQ/Produit_IC":new_data["Declarer_TVQ/Produit_IC"].mean()
    }
    final_dataframe = pd.DataFrame([mean_values])
    return final_dataframe


def filter_bubble_data(df,year,trans,form,region):
    ts = bubble_processing(df,year,region,trans,form)
    data = list(map(lambda x : (x.split("/")[0],x.split("/")[1],ts [x].values[0]),list(ts.columns)))
    dataframe = pd.DataFrame(data,columns=["Declarer","Produire","Ratio"])
    return dataframe