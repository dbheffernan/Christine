# -*- coding: utf-8 -*-
"""
Created on Thu Oct 25 19:14:12 2018

@author: Dillon
"""
import ingestion 
import utilities
import dicts
import pandas as pd

def results_processing(results,election_type,year):
    results = results.drop(['Absentee','Machine','Total'],axis=1)
    results = utilities.won_checker(results,election_type)
    results = utilities.inc_checker(results,year,masterlist)
    periods = dicts.period_dict[str(year)+dicts.type_dict[election_type]]
    results = utilities.text_match(results,canlist,state_contribs,periods)
    results = filler(results, periods, ingestion.state_contribs,ingestion.state_expend)

    
def filler(results_data, periods, contrib_list,expend_list):
    df = pd.DataFrame()
    for index, row in results_data.iterrows():
        contrib = get_contrib(row.CF_ID, periods, contrib_list)
        expend = get_expend(row.CF_ID,periods, expend_list)
        details = pd.merge(contrib,expend, on='CF_ID')
        df = df.append(details)
    merged = pd.merge(results_data,df, on='CF_ID')
    return merged

def get_contrib(CF_ID,periods,contrib_list):
    df= contrib_list[(contrib_list.CF_ID == CF_ID) and (contrib_list.Filing_Period.isin(periods))]
    total = sum(df['Contribution_Amount'])
    add = pd.DataFrame([[0]*9],columns=set(list(dicts.contrib_dict.values())))
    for index, row in df.iterrows():
        print(row.Contributor_Type)
        ct1 = row.Contributor_Type
        if(ct1 == 'Individual' and row['Contributor_State'] == 'DE'):
            ct1 = 'Ind_DE'
        if(row['Contribution_Amount'] < 101):
            ct1 = 'sub_100'
        add.loc[0,ct1]=add.loc[0,ct1]+row['Contribution_Amount']    
    add['Contrib_Total'] = total
    add['CF_ID'] = CF_ID
    return add

def get_expend(CF_ID,periods,expend_list):
    df =expend_list[(expend_list.CF_ID == CF_ID) and (expend_list.Filing_Period.isin(periods))]
    total = sum(df['Amount'])
    add = pd.DataFrame([[0]*10],columns=dicts.mod_purp_dict)
    for cat in dicts.mod_purp_dict:
        cat = str(cat)
        df1 = df.loc[df.Expense_Category == cat]
        tot = sum(df1.Amount)
        #print(cat,tot,data.columns)
        add[cat] = add[cat] + tot

    add['Expend_Total'] = total
    add['CF_ID'] = CF_ID
    return add