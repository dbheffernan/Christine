# -*- coding: utf-8 -*-
"""
Created on Mon Aug 20 15:54:20 2018

@author: Dillon
"""
import numpy as np
import pandas as pd
import re
import math

def filler(results_data, period, contrib_list,expend_list):
    df = pd.DataFrame()
    for index, row in results_data.iterrows():
        contrib = get_contrib(row.CF_ID, period, contrib_list)
        expend = get_expend(row.CF_ID,period, expend_list)
        expend = expend.drop('period',axis=1)
        details = pd.merge(contrib,expend, on='CF_ID')
        df = df.append(details)
    merged = pd.merge(results_data,df, on='CF_ID')
    merged = merged.drop(['Absentee','Machine','Committee_Status','Registered_Date','Amended_Date','Treasurer_Name','County','Treasurer_Address'],axis=1)
    return merged

def get_contrib(CFID,choices,contribu):
    data= contribu.loc[contribu['CF_ID']== CFID]
    period = pd.DataFrame()
    for choice in choices:
        df= data[data['Filing_Period'] == choice]
        period = period.append(df)
    data = period
    total = sum(data['Contribution_Amount'])
    add = pd.DataFrame([[0]*9],columns=set(list(contrib_dict.values())))
    for index, row in data.iterrows():
        ct1 = contrib_dict[row['Contributor_Type']]
        if(ct1 == 'Individual' and row['Contributor_State'] == 'DE'):
            ct1 = 'Ind_DE'
        if(row['Contribution_Amount'] < 101):
            ct1 = 'sub_100'
        add.loc[0,ct1]=add.loc[0,ct1]+row['Contribution_Amount']
        #print(CFID)
    add['Contrib_Total'] = total
    add['CF_ID'] = CFID
    add['period'] = choice
    #print(add.loc[0, 'Contrib_Total'], add.loc[0, 'CF_ID'])
    return add

def get_expend(CFID,choices,expend_list):
    data = expend_list.loc[expend_list['CF_ID']==CFID]
    period = pd.DataFrame()
    for choice in choices:
        df= data[data['Filing_Period'] == choice]
        period = period.append(df)
    data = period
    total = sum(data['Amount'])
    add = pd.DataFrame([[0]*10],columns=mod_purp_dict)
    print(total)
    for cat in mod_purp_dict:
        cat = str(cat)
        df1 = data.loc[data.Expense_Category == cat]
        tot = sum(df1.Amount)
        #print(cat,tot,data.columns)
        add[cat] = add[cat] + tot

    add['Expend_Total'] = total
    add['CF_ID'] = CFID
    add['period'] = choice
    return add
    



def ratio_maker(results_data,contrib=True):
        if contrib:
            out = pd.DataFrame()
            for party in parties:
                data = results_data.loc[results_data.Party == party]
                races = pd.Series(data.Office.unique())
                #print(races,type(races))

                for index , race in races.iteritems():
                    print(race)
                    race_data = data.loc[data.Office == race]
                    rto = sub_ratio(race,race_data)
                    print(rto, type(rto))
                    out = out.append(rto)
                    print(out, type(out))
            #out = pd.DataFrame(out)        
            print(out, type(out))
            return out
            
def ratio(x,y):
    if y == 0:
        return 0
    else:
        return (x/y)
    '''
def total_maker(race, race_data):
    Total = race_data.sum()
    Total.Name = 'TOTAL'
    #print(Total)
    Total.Incumbent = 0
    Total.Office = race
    Total.Percent = 100
    Total.Won = 0
    Total.Committee_Name = Total.Office + ' TOTAL'
    Total.CF_ID = 0
 '''   
    
    
def sub_ratio(race, race_data):
    out = []
    ratio_race_labels = pd.Series('ratio_race:' + ct1)
    ratio_cand_labels = pd.Series('ratio_cand:' + ct1)
    
    race_data = race_data.append(Total)
    for index, cand in race_data.iterrows():
        ratios = [ratio(cand.Self,cand.Contrib_Total),ratio(cand.Business,cand.Contrib_Total),ratio(cand.Political_Committee,cand.Contrib_Total),
                  ratio(cand.sub_100,cand.Contrib_Total),ratio(cand.Candidate_Committee,cand.Contrib_Total),ratio(cand.Individual,cand.Contrib_Total),
                  ratio(cand.PAC_Committee,cand.Contrib_Total),ratio(cand.Outside_Committee,cand.Contrib_Total),ratio(cand.Labor_Union,cand.Contrib_Total),
                  ratio(cand.PAC,cand.Contrib_Total),ratio(cand.National_Sub_Committees,cand.Contrib_Total),ratio(cand.NPO,cand.Contrib_Total),
                  ratio(cand.Ind_DE,cand.Contrib_Total)]
        ratio_cand = pd.Series(ratios, index=ratio_cand_labels)
                        #ratio_cand = ratio_cand.rename(columns = ratio_cand_labels)
                        #ratio_cand['CF_ID'] = cand.CF_ID
        ratio_race = pd.Series([ratio(cand.Self,Total.Self),ratio(cand.Business,Total.Business),ratio(cand.Political_Committee,Total.Political_Committee),
                                                   ratio(cand.sub_100,Total.sub_100),ratio(cand.Candidate_Committee,Total.Candidate_Committee),ratio(cand.Individual,Total.Individual),
                                                   ratio(cand.PAC_Committee,Total.PAC_Committee),ratio(cand.Outside_Committee,Total.Outside_Committee),ratio(cand.Labor_Union,Total.Labor_Union),
                                                   ratio(cand.PAC,Total.PAC),ratio(cand.National_Sub_Committees,Total.National_Sub_Committees),ratio(cand.NPO,Total.NPO),
                                                   ratio(cand.Ind_DE,Total.Ind_DE)], index = ratio_race_labels)
                        #ratio_race = ratio_race.rename(columns = ratio_race_labels)
                        #ratio_race['CF_ID'] = ratio_cand['CF_ID']
        ratio_race['ratio_race: Total_Contrib'] = ratio(cand.Contrib_Total,Total.Contrib_Total)
        cand = pd.concat([cand,ratio_cand, ratio_race])
        print(cand.Name)
        out.append(cand)
    return pd.DataFrame(out)
