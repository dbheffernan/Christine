# -*- coding: utf-8 -*-
"""
Created on Tue Aug 14 18:37:27 2018

@author: Dillon
"""
import numpy as np
import pandas as pd
import re
import math
from glob import glob
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

master_fed_cols = ['Type',
 'CF_ID',
 'ORG_Name',
 'Last_Name',
 'First_Name',
 'Middle_Initial',
 'Drop_1',
 'Drop_2',
 'Address',
 'Drop_3',
 'City',
 'State',
 'zip',
 'DATE',
 'Expense_Purpose',
 'Employer',
 'Title',
 'Primay_General',
 'Year',
 'CTD_Amount',
 'Amount',
 'Drop_4',
 'Drop_5',
 'Drop_6',
 'Drop_7',
 'Drop_8',
 'Expense_Category',
 'Expend_Amount',
 'Drop_10',
 'Drop_11',
 ]
def fed_main():
    data = pd.DataFrame()
    for index, row in fcl.iterrows():
        details = federal_parser(CFID=row.CF_ID)
        details['Name'] = row.candidate_name
        details['Office']=row.Yoffice
        data = data.append(details, ignore_index=True)
    return data

def federal_parser(mid=federale,CFID=0,fed_contrib=final_fed_contr,fed_spend=final_fed_spend):
    mid = mid.loc[mid.committee_id == CFID]
    contrib = pd.DataFrame([[0]*9],columns=set(list(contrib_dict.values())))
    contrib.CF_ID = CFID
    contrib.Contrib_Total = sum(mid.total_receipts_period)
    contrib.Self = sum(mid.candidate_contribution_period + mid.loans_made_by_candidate_period)
    contrib.sub_100 = sum(mid.individual_unitemized_contributions_period)
    contrib.Ind_DE = fed_de(CFID, fed_contrib)
    contrib.Individual = sum(mid.individual_itemized_contributions_period) - contrib.Ind_DE
    contrib.National_Sub_Committees = sum(mid.political_party_committee_contributions_period)
    contrib.PAC = sum(mid.other_political_committee_contributions_period)
    contrib.Candidate_Committee = sum(mid.transfers_from_other_authorized_committee_period)
    expend = federal_expense_filler(fed_spend, CFID)
    #print(contrib)
    #print(fed_cand_dict[CFID])
    merged = pd.merge(contrib,expend, on='CF_ID')
    return merged

mod_purp_dict = [
 'Candidate Expenses',
 'Contributions',
 'Field Expenses',
 'Fund Raiser',
 'Mail',
 'Media',
 'Printing and Campaign Materials',
 'Rent and Other Office expenses',
 'Salaries and Other compensation',
 'smol']

fed_cand_dict = {
        'C00588285':'BHS',
        'C00590778':'LBR',
        'C00588491':'Townsend',
        'C00592857':'Barney',
        'C00566331':'Wade',
        'C00568329':'Smink',
        'C00473421':'Izzo 12',
        'C00503946':'Kovach',
        'C00521724':'KSpan',
        'C00349217':'Carper',
        'C00480558':'Rollins',
        'C00473421':'Izzo10',
        'C00476309':'Urquhart',
        'C00254938':'Castle',
        'C00449595':'COD',
        'C00437616':'Northington',
        'C00441600':'KHN',
        'C00511972':'Bad Wade',
        'C00446310':'Bullock'
        }
'''
primary_dict = {2007:pe08a,
                2008:pe08a,
                2009:pe10a,
                2010:pe10a,
                2011:pe12a,
                2012:pe12a,
                2013:pe14a,
                2014:pe14a,
                2015:pe16a,
                2016:pe16a}
'''

def federal_expense_filler(data, CFID):
    expend = pd.DataFrame([[0]*10],columns=mod_purp_dict)
    expend['CF_ID'] = CFID
    #cats = set(list(purp_dict.values()))
    total = 0
    df = data.loc[data.CF_ID == CFID]
    for cat in mod_purp_dict:
        cat = str(cat)
        df1 = df.loc[df.Expense_Category == cat]
        tot = sum(df1.Amount)
        total += tot
        print(cat,tot,fed_cand_dict[CFID])
        expend[cat] = expend[cat] + tot
    expend['Expend_Total'] = total
    return expend
        
def fed_globber():
    filenames = glob(r"c:\users\Dillon\downloads\Data\Carper\*.csv")
    print(1)
    master_fed = pd.DataFrame(columns=master_fed_cols)
    print(master_fed)
    for f in filenames:
        try:
            #print(f)
            fed = pd.read_csv(f,names=master_fed_cols,nrows=1)
            print(f, fed.CF_ID, fed.ORG_Name)
            master_fed = master_fed.append(fed, ignore_index=True)
            #print(3)
        except:
            print('whoopsie daisy')
    #contrib = master_fed.loc[master_fed.Type == 'SA11A1']
    #expend = master_fed.loc[master_fed.Type == 'SB17']
    #master_fed = contrib.append(expend, ignore_index=True)
    #master_fed = master_fed.drop(master_fed.columns[28:],axis=1)
    #master_fed = master_fed.drop(['Middle_Initial','Drop_1','Drop_2','Drop_3','Drop_4','Drop_5','Drop_6','Drop_7','Drop_8','Address','City','zip','Employer','Title','CTD_Amount'], axis=1)
    return master_fed

def fed_de(CFID,data):
    df= data.loc[data.CF_ID == CFID]
    df = df.loc[df.STATE == 'DE']
    tot = sum(df.Amount)
    return tot
        
def fed_expense_categorizer():
    df = pd.DataFrame()
    filt = re.compile('(SERVICE|EXPENSE|IN-KIND)')
    for index, row in fed_expend.iterrows():
        if row.Type == 'SB17':
            purpose = row.Expense_Purpose
            #filtered = filt.sub('',item)
            guess = process.extractOne(purpose, list(purp_dict.keys()))
            row.Expense_Category = purp_dict[guess[0]]
            print(purpose, row.Expense_Category)
        df = df.append(row)
    return df

def ratio_make(race_data,CF_ID):
    df = race_data.loc[race_data.CF_ID == CF_ID]
    for col in ['Individual', 'National_Sub_Committees', 'PAC', 'Ind_DE',
       'sub_100', 'Contrib_Total', 'Self', 'Candidate_Committee']:
        num = float(df[col])
        num2 = sum(race_data[col])
        df['PR: ' + col] = ratio(num, float(df.Contrib_Total))
        df['RR: ' + col] = ratio(num, num2)
        df['TR: ' + col] = ratio(num, sum(race_data.Contrib_Total))
    for col in ['Candidate Expenses', 'Contributions', 'Field Expenses', 'Fund Raiser',
                'Mail', 'Media', 'Printing and Campaign Materials','Rent and Other Office expenses', 
                'Salaries and Other compensation','smol', 'Expend_Total']:
        num = float(df[col])
        num2 = sum(race_data[col])
        df['PR: ' + col] = ratio(num, float(df.Expend_Total))
        df['RR: ' + col] = ratio(num, num2)
        df['TR: ' + col] = ratio(num, sum(race_data.Expend_Total))     
    return df

def final_fed_filler(data):
    data.Office = data.Office + " (" + data.Party + data.Cycle.astype(str) + ')'
    races = list(data.Office.unique())
    df1 = pd.DataFrame()
    for race in races:
        print(race)
        df2 = data.loc[data.Office == race]
        num = df2.shape[0]
        for index, row in df2.iterrows():
            cand = ratio_make(df2,row.CF_ID)
            cand['number'] = num
            df1 = df1.append(cand,ignore_index=True)
    return df1
            