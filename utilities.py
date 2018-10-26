# -*- coding: utf-8 -*-
"""
Created on Wed Oct 24 12:39:35 2018

@author: Dillon
"""
from fuzzywuzzy import fuzz, process
import pandas as pd
import Levenshtein as lv
import re
import dicts

def canlister (df,contribs):
    xcanlist = pd.DataFrame()
    for office in dicts.offices:
        x = df[df.off_trim == office]
        xcanlist = xcanlist.append(x)
        df = pd.DataFrame()
    for index, row in xcanlist.iterrows():
    #print(row.CF_ID)
        limited_contribs = contribs[contribs.Filing_Period.isin(dicts.period_dict['2008all'])]
        row['2008all'] =  limited_contribs[limited_contribs.CF_ID == row.CF_ID].Contribution_Amount.sum()
        limited_contribs = contribs[contribs.Filing_Period.isin(dicts.period_dict['2010all'])]
        row['2010all'] =  limited_contribs[limited_contribs.CF_ID == row.CF_ID].Contribution_Amount.sum()
        limited_contribs = contribs[contribs.Filing_Period.isin(dicts.period_dict['2012all'])]
        row['2012all'] =  limited_contribs[limited_contribs.CF_ID == row.CF_ID].Contribution_Amount.sum()
        limited_contribs = contribs[contribs.Filing_Period.isin(dicts.period_dict['2014all'])]
        row['2014all'] =  limited_contribs[limited_contribs.CF_ID == row.CF_ID].Contribution_Amount.sum()
        limited_contribs = contribs[contribs.Filing_Period.isin(dicts.period_dict['2016all'])]
        row['2016all'] =  limited_contribs[limited_contribs.CF_ID == row.CF_ID].Contribution_Amount.sum()
        df=df.append(row)
    return df

def text_match(results,canlist,contributions,periods):
    limited_contribs = contributions[contributions.Filing_Period.isin(dicts.period_dict[periods])]
    df1 = pd.DataFrame()
    for index, candidate in results.iterrows():
        try:
            potential_committees = canlist[canlist.off_trim == candidate.Office]
            potential_committees = potential_committees.drop_duplicates(subset=['CF_ID'])
            df = pd.DataFrame()
            for index, row in potential_committees.iterrows():
                limited_contrib= limited_contribs[limited_contribs.CF_ID == row.CF_ID]
                row['Total_Raised'] = limited_contrib.Contribution_Amount.sum()
                guess = candidate.Name
                row['Match_Score'] = fuzz.partial_token_set_ratio(guess,row.Committee_Name) #* (row.Total_Raised * .2)
                df = df.append(row)
            df = df.sort_values('Total_Raised', ascending=False).drop_duplicates('Match_Score')
            df =df.sort_values('Match_Score', ascending=False)
            df=df.reset_index(drop=True)
            head = df.loc[0,]    
            if(head.Match_Score < 50):
                print("Low match score, something might be up\n",  head.Committee_Name, candidate.Name, '\nHow about:\n')
                guesses = process.extract(candidate.Name, canlist.Committee_Name, scorer =fuzz.token_set_ratio, limit =10)
                guesses = pd.DataFrame(guesses,columns = ['Committee_Name','Match_Score','number'])
                guesses['Total_Raised'] = canlist.loc[guesses.number][periods].tolist()
                print(guesses)
                guesses['CF_ID'] =  canlist.loc[guesses.number]['CF_ID'].tolist()
                x = input('Look good? Enter number or \'n\' if not')
                if (x == 'n' or x == 'N'):
                    candidate['CF_ID'] = 0
                    candidate['Committee_Name'] =  'UNKNOWN COMMITTEE'
                    candidate['total'] = 0
                    candidate['match'] = 0
                else:
                    x = int(x)
                    head=guesses.loc[x]
                    candidate['CF_ID'] = head.CF_ID
                    candidate['Committee_Name'] =  head.Committee_Name
                    candidate['total'] = head.Total_Raised
                    candidate['match'] = head.Match_Score
            df1 = df1.append(candidate)
        except:
            print('match failed', candidate.Name)
            
    return df1

def fec_to_datetime(date):
    rex = re.compile(r'(\d\d)(\d\d)(\d\d)(\d\d)')
    date = str(re.sub(rex,r"\3-\4-\2",date))
    date = date.split('.')
    date= date[0]
    print(date)
    return pd.to_datetime(date)

def ml_updater(results,year,masterlist):
    ml = pd.DataFrame()
    for index, row in masterlist.iterrows():
        last = 'Incum_' + str(year-2)
        best = row[last],0
        for ind, candidate in results.iterrows():
            if row.name == candidate.Office:
                if candidate.Total > best[1]:
                    best = [candidate.Name,candidate.Total]
                    
        index = 'Incum_' + str(year)
        row[index]= best[0]
        ml = ml.append(row)
    return ml
            
def inc_checker(results,year,masterlist):
    data = []
    last = 'Incum_' + str(year - 2002)
    for index, row in results.iterrows():
        row.Incumbent = 0
        if (fuzz.ratio(row.Name , masterlist.loc[row.Office, last]) > 80):
            row.Incumbent = 1
        data.append(row)
    return pd.DataFrame(data)    
    
def won_checker(results, method):
    df = pd.DataFrame()
    if method == 0:
        for party in ['D','R']:
            pool = results[results.Party == party]
            for office in dicts.offices:
                candidates = pool[pool.Office == office]
                candidates = candidates.sort_values('Percent', ascending=False)
                candidates=candidates.reset_index(drop=True)
                candidates.loc[0,'Won'] = 1
                df = df.append(candidates)  
    if method == 1:
        for office in dicts.offices:
            candidates = results[results.Office == office]
            candidates = candidates.sort_values('Percent', ascending=False)
            candidates=candidates.reset_index(drop=True)
            candidates.loc[0,'Won'] = 1
            df = df.append(candidates)
    df = df.dropna(subset=['Name'])
    return df
        
def inc_updater(masterlist,year,cand):
    index = 'Incum_' + str(year)
    masterlist.loc[cand.Office,index] = cand.Name
    return
    
def inc_insurance(year,masterlist):
    incum = 'Incum_' + str(year)
    last = 'Incum_' + str(year-2)
    for index, row in masterlist.iterrows():
        masterlist[incum] = masterlist[last]
    return