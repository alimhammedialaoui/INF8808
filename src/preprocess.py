"""
    Contains some functions to preprocess the data used in the visualisation.
"""
import pandas as pd
import numpy as np
from typing import Callable
import math


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
        # Dans ce cas, si nous sommes dans la configuration contribuable, les valeurs NaN sont de vraies données manquantes
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
        # Dans ce cas, si nous sommes dans la configuration contribuable, les valeurs NaN sont de vraies données manquantes

        # Pour les particuliers, la partie RAS est majoritairement vide, donc on supprime beaucoup trop de données
        # Peut-être voir si le revenu à la source est démocratisé ou non au Québec, auquel cas il faudra mettre une règle ou combler par des 0 pour dire
        # qu'ils ne la déclarent pas (biais)
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
        # Dans ce cas, si nous sommes dans la configuration contribuable, les valeurs NaN sont de vraies données manquantes

        # Pour les particuliers, la partie RAS est majoritairement vide, donc on supprime beaucoup trop de données
        # Peut-être voir si le revenu à la source est démocratisé ou non au Québec, auquel cas il faudra mettre une règle ou combler par des 0 pour dire
        # qu'ils ne la déclarent pas (biais)
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
        df2: The second dataframe, to be appended to the first
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
    """
    Sums each player's total of number of lines and  its
    corresponding percentage per act.

    The sum of lines per player per act is in a new
    column named 'PlayerLine'.

    The percentage of lines per player per act is
    in a new column named 'PlayerPercent'

    Args:
        my_df: The pandas dataframe containing the data from the .csv file
    Returns:
        The modified pandas dataframe containing the
        information described above.
    """
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
    """
    Sums each player's total of number of lines and  its
    corresponding percentage per act.

    The sum of lines per player per act is in a new
    column named 'PlayerLine'.

    The percentage of lines per player per act is
    in a new column named 'PlayerPercent'

    Args:
        my_df: The pandas dataframe containing the data from the .csv file
    Returns:
        The modified pandas dataframe containing the
        information described above.
    """
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
   return my_df