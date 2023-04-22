"""
    Contains some functions to preprocess the data used in the visualisation.
"""
import pandas as pd
import numpy as np
from typing import Callable
import math
from itertools import combinations


def clean_names(my_df: pd.DataFrame):
    """
    In the dataframe, formats the players'
    names so each word start with a capital letter.

    Returns:
        The df with formatted names
    """
    my_df_copy = my_df.copy()
    my_df_copy["Taille"] = my_df_copy["Taille"].dropna().apply(lambda x: x.capitalize())
    my_df_copy["Region"] = my_df_copy["Region"].dropna().apply(lambda x: x.capitalize())
    my_df_copy["Mode_transmission"] = (
        my_df_copy["Mode_transmission"].dropna().apply(lambda x: x.capitalize())
    )

    return my_df_copy


def convert_types(my_df, IC_or_IP):
    """
    Converts the decimal values into integer as we have binary variables and Year

    args:
        my_df: The dataframe to preprocess
    returns:
        The dataframe with rounded numbers
    """
    my_df["Year"] = my_df["Year"].astype("int")
    if IC_or_IP == "IP":
        my_df["Produire_IP"] = my_df.loc[:, "Produire_IP"].astype("Int64")
        my_df["Declarer_IP"] = my_df.loc[:, "Declarer_IP"].astype("Int64")
    elif IC_or_IP == "IC":
        my_df["Produire_IC"] = my_df.loc[:, "Produire_IC"].astype("Int64")
        my_df["Declarer_IC"] = my_df.loc[:, "Declarer_IC"].astype("Int64")

    my_df["Produire_RAS"] = my_df.loc[:, "Produire_RAS"].astype("Int64")
    my_df["Declarer_RAS"] = my_df.loc[:, "Declarer_RAS"].astype("Int64")

    my_df["Produire_TVQ"] = my_df.loc[:, "Produire_TVQ"].astype("Int64")
    my_df["Declarer_TVQ"] = my_df.loc[:, "Declarer_TVQ"].astype("Int64")
    return my_df


def remove_missing_values(my_df, IC_or_IP):
    """
    We remove all missing values, not taking into account the absence of IC or IQ column, as they are
    constrained to a logical rule

    args:
        my_df: The dataframe to preprocess
    returns:
        The dataframe with rounded numbers
    """
    print("Lignes avant la suppression des valeurs manquantes : ", len(my_df))

    if IC_or_IP == "IC":
        # Dans ce cas, si nous sommes dans la configuration contribuable, 
        # les valeurs NaN sont de vraies données manquantes
        my_df = my_df.dropna(
            subset=[
                "Year",
                "Taille",
                "Form_juridique",
                "Region",
                "Mode_transmission",
                "Produire_RAS",
                "Declarer_RAS",
                "Declarer_TVQ",
                "Produire_TVQ",
                "Declarer_IC",
                "Produire_IC",
            ]
        )
    elif IC_or_IP == "IP":
        my_df = my_df.dropna(
            subset=[
                "Year",
                "Taille",
                "Form_juridique",
                "Region",
                "Mode_transmission",
                "Produire_RAS",
                "Declarer_RAS",
                "Declarer_TVQ",
                "Produire_TVQ",
                "Declarer_IP",
                "Produire_IP",
            ]
        )
    elif IC_or_IP == None:
        my_df = my_df.dropna(
            subset=[
                "Year",
                "Taille",
                "Form_juridique",
                "Region",
                "Mode_transmission",
                "Produire_RAS",
                "Declarer_RAS",
                "Declarer_TVQ",
                "Produire_TVQ",
            ]
        )
    else:
        raise Exception("Choisir IC ou IP pour les modalités")

    print("Lignes après la suppression des valeurs manquantes : ", len(my_df))

    return my_df


def sort_by_yr(my_df):
    """
    Sorts the dataframe by year and then by continent.

    args:
        my_df: The dataframe to sort
    returns:
        The sorted dataframe.
    """
    my_df.sort_values(by=["Year"], inplace=True)
    return my_df


def combine_dfs(df, *dfs):
    """
    Combines the two dataframes

    args:
        df1: The first dataframe to combine
        dfs: The other dataframes, to be appended to the first
    returns:
        The dataframe containing both dataframes provided as arg.
        Each row of the resulting dataframe has a column 'Year'
        containing the value 2000 or 2015, depending on its
        original dataframe.
    """
    df_whole = df
    for d in dfs:
        df_whole = pd.concat([df_whole, d], ignore_index=True)

    return df_whole


def group_and_get_sum_per_obligation(list_of_keys, my_df):
    my_df = my_df.groupby(list_of_keys).agg(
        {
            "Produire_IP": "sum",
            "Declarer_IP": "sum",
            "Produire_IC": "sum",
            "Declarer_IC": "sum",
            "Produire_RAS": "sum",
            "Declarer_RAS": "sum",
            "Produire_TVQ": "sum",
            "Declarer_TVQ": "sum",
        }
    )
    my_df.columns = [
        "Produire_IP_à_temps",
        "Declarer_IP_sans_erreurs",
        "Produire_IC_à_temps",
        "Declarer_IC_sans_erreurs",
        "Produire_RAS_à_temps",
        "Declarer_RAS_sans_erreurs",
        "Produire_TVQ_à_temps",
        "Declarer_TVQ_sans_erreurs",
    ]
    my_df = my_df.reset_index()
    return my_df


def group_and_get_means_per_obligation(list_of_keys, my_df):
    my_df = my_df.groupby(list_of_keys).agg(
        {
            "Produire_IP": "mean",
            "Declarer_IP": "mean",
            "Produire_IC": "mean",
            "Declarer_IC": "mean",
            "Produire_RAS": "mean",
            "Declarer_RAS": "mean",
            "Produire_TVQ": "mean",
            "Declarer_TVQ": "mean",
        }
    )
    my_df.columns = [
        "Produire_IP_à_temps",
        "Declarer_IP_sans_erreurs",
        "Produire_IC_à_temps",
        "Declarer_IC_sans_erreurs",
        "Produire_RAS_à_temps",
        "Declarer_RAS_sans_erreurs",
        "Produire_TVQ_à_temps",
        "Declarer_TVQ_sans_erreurs",
    ]
    my_df = my_df.reset_index()
    return my_df


def create_dataset_clustered_barchart(criteres, dataset, radio_fusion=False):
    for key, value in criteres.items():
        if value != 'ALL':
            dataset = dataset[dataset[key] == value]
    cols_to_select = ~dataset.columns.isin(list(criteres.keys()))
    
    # To compute the mean over the unaggregated dataset
    for key, value in criteres.items():
        if value == 'ALL':
            for col, boolean in zip(dataset.columns, cols_to_select):
                if boolean == True:
                    dataset[col] = dataset[col].mean()
    formated_dataset = pd.DataFrame(
        {
            "Obligation": ["Produire à temps", "Declarer sans erreurs"] * 8,
            "Lois": [
                "IP",
                "IP",
                "IC",
                "IC",
                "RAS",
                "RAS",
                "TVQ",
                "TVQ",
                "IP_P",
                "IP_D",
                "IC_P",
                "IC_D",
                "RAS_P",
                "RAS_D",
                "TVQ_P",
                "TVQ_D",
            ],
            "Valeurs": np.concatenate(
                [
                    dataset.loc[:,cols_to_select,]
                        .values[0] if len(dataset.loc[:,cols_to_select,].values) else [0]*8,
                    dataset.loc[:,cols_to_select,]
                        .values[0] if len(dataset.loc[:,cols_to_select,].values) else [0]*8,
                ]
            ),
            "Par obligation": [
                "Non",
                "Non",
                "Non",
                "Non",
                "Non",
                "Non",
                "Non",
                "Non",
                "Oui",
                "Oui",
                "Oui",
                "Oui",
                "Oui",
                "Oui",
                "Oui",
                "Oui",
            ],
        }
    )

    dico = {False: "Non", True: "Oui"}
    formated_dataset = formated_dataset[
        formated_dataset["Par obligation"] == dico[radio_fusion]
    ]

    return formated_dataset
'''
def create_dataset_stacked_barchart(dataset, criteres, obligation='Declarer', indicateur='TVQ'):
    dataset = dataset[dataset['Form_juridique'] == 'C'] # Only keep rows corresponding to corporations
    for key, value in criteres.items():
        if value != 'ALL':
            dataset = dataset[dataset[key] == value]


    column_to_select = obligation + "_" + indicateur

    nmb_of_ones = dataset.groupby(['Year', 'Taille']).agg({column_to_select: 'sum'}).reset_index()
    nmb_of_companies = dataset.groupby(['Year']).agg({column_to_select: 'size'}).add_suffix('_Tot')
    dataset = nmb_of_ones.join(nmb_of_companies, on="Year")
    dataset["Valeurs"] = dataset[column_to_select] / dataset[column_to_select + "_Tot"]
    dataset["Tot"] = dataset[column_to_select + "_Tot"]
    print(dataset)
    return dataset
'''

def create_dataset_stacked_barchart(dataset, criteres, obligation='Declarer', indicateur='TVQ'):
    dataset = dataset[dataset['Form_juridique'] == 'C'] # Only keep rows corresponding to corporations
    for key, value in criteres.items():
        if value != 'ALL':
            dataset = dataset[dataset[key] == value]

    #dataset2 = dataset.copy()
    column_to_select = obligation + "_" + indicateur

    nmb_of_ones = dataset.groupby(['Year', 'Taille']).agg({column_to_select: 'sum'}).reset_index()
    nmb_of_companies = dataset.groupby(['Year']).agg({column_to_select: 'size'}).add_suffix('_Tot')
    num_companies_by_size = dataset.groupby(['Year', 'Taille']).agg({column_to_select: 'size'})
    
    num_companies_by_size["tot_by_size"] = num_companies_by_size[column_to_select]

    num_companies_by_size = num_companies_by_size.drop(columns=[column_to_select]).reset_index()
    #print(num_companies_by_size)
    dataset = nmb_of_ones.join(nmb_of_companies, on=["Year"])
    
    dataset["Tot_par_taille"] = num_companies_by_size["tot_by_size"] / dataset[column_to_select + "_Tot"] * 100
    dataset["Valeurs"] = dataset[column_to_select] / dataset[column_to_select + "_Tot"] * 100
    dataset["Tot"] = dataset[column_to_select + "_Tot"]
    dataset = dataset.drop(columns=[column_to_select, column_to_select + '_Tot'])
    #print(dataset)

    return dataset

def filter_line_chart_df(my_df,region,obligation,indicateur,transmission):
   if region == 'ALL' and transmission != 'ALL':
       my_df = my_df[my_df['Mode_transmission'] == transmission]
   elif transmission == 'ALL' and region != 'ALL':
       my_df = my_df[(my_df['Region'] == region)]
   elif region != 'ALL' and transmission != 'ALL':
       my_df = my_df[(my_df['Region'] == region) 
                        & (my_df['Mode_transmission'] == transmission)]
   else:
       my_df = my_df 
       
   my_df = my_df.groupby(["Year","Form_juridique"]).agg({'Produire_IP': 'mean', 'Declarer_IP': 'mean',
                                                    'Produire_IC': 'mean', 'Declarer_IC': 'mean',
                                                    'Produire_RAS': 'mean', 'Declarer_RAS': 'mean',
                                                    'Produire_TVQ': 'mean', 'Declarer_TVQ': 'mean'}).reset_index()
   if obligation == 'Declarer':
      column_to_select = "Declarer_" + indicateur
   elif obligation == 'Produire':
      column_to_select = "Produire_" + indicateur
   else:
      raise(Exception)
   my_df = my_df[["Year", "Form_juridique", column_to_select]]
   my_df = my_df.rename(columns={column_to_select: "Valeurs"})
   my_df = my_df[my_df['Valeurs'] > 0]
   return my_df

from Levenshtein import distance

def uniform_regions(regions_df,quebec_map_regions):
    dico_regions = {}
    for region in regions_df:
        #print(region)
        key = region
        min = 50
        key_region = None
        for region_map in quebec_map_regions:
            #print(region , region_map)
            d = distance(region,region_map)
            if(d<min):
                min = d
                key_region = region_map
        dico_regions[key] = key_region 
    return dico_regions



def map_df(df,dico_regions,transmission,indicateur,forme_jur,obligation,year):
    if year != 'ALL' and transmission !='ALL':
        df = df[(df['Year']== year) & (df['Mode_transmission']==transmission) & (df['Form_juridique'] == forme_jur)]
    elif year == 'ALL' and transmission !='ALL':
        df = df[(df['Mode_transmission']==transmission) & (df['Form_juridique'] == forme_jur)]
    elif year != 'ALL' and transmission =='ALL':
        df = df[(df['Year']== year) & (df['Form_juridique'] == forme_jur)]
    else :
        df = df[(df['Form_juridique'] == forme_jur)]
    if obligation == 'Declarer':
        column_to_select = "Declarer_" + indicateur
    elif obligation == 'Produire':
        column_to_select = "Produire_" + indicateur
    df = df[['Region',column_to_select]]
    df = df.replace({"Region": dico_regions})
    df = df.groupby('Region').mean()
    df = df.reset_index()
    df[column_to_select] = round(df[column_to_select],4)*100
    return df, column_to_select

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
    final_dataframe = final_dataframe.replace(np.nan, 0)
    return final_dataframe


def filter_bubble_data(df,year,trans,form,region):
    ts = bubble_processing(df,year,region,trans,form)
    data = list(map(lambda x : (x.split("/")[0],x.split("/")[1],ts [x].values[0]),list(ts.columns)))
    dataframe = pd.DataFrame(data,columns=["Declarer","Produire","Ratio"])
    return dataframe