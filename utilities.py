# -*- coding: utf-8 -*-
"""
Created on Mon Aug 20 15:52:01 2018

@author: Dillon
"""

def text_match(data,candlist):
    match=[]

    for index, row in data.iterrows():
        office = row.Office
        print(row.Name, office)
        match_list = candlist.loc[lambda candlist: candlist.off_trim == office]
        try:
            guess = process.extractOne(row.Name, match_list.Committee_Name)
            print(guess)
            if(guess[1]<66):
                guess2 = process.extract(row.Name, match_list.Committee_Name)
                print(guess2)
                x = int(input('num, 5=none: '))
                guess = guess2[x]
            match.append(guess[0])
        except:
            print('text match failed')
            match.append('X')
    data['Committee_Name']= match
    return pd.DataFrame(data)

def ID_match(data,canlist):
    match2=[]
    for index, row in canlist.iterrows():
        for index, row2 in data.iterrows():
            if(row.Committee_Name==row2.Committee_Name):
                    match2.append(row)
    match2 = pd.DataFrame(match2)
    match2 = match2.drop_duplicates(subset='CF_ID')
    match2 = match2.drop(['Committee_Type','off_trim','Office'],axis=1)
    data = pd.merge(data,match2,on='Committee_Name')
    return data

def ml_updater(results,year):
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
            
def inc_checker(results,year,ml):
    data = []
    
    last = 'Incum_' + str(year - 2)
    print(year, type(year))
    for index, row in results.iterrows():
        row.Incumbent = 0
        if (fuzz.ratio(row.Name , ml.loc[row.Office, last]) > 80):
            print(row.Name,row.Incumbent)
            #print(fuzz.ratio(row.Name , ml.loc[row.Office, last]),row.Name , ml.loc[row.Office, last])
            row.Incumbent = 1
        data.append(row)
    return pd.DataFrame(data)    
    
def won_checker(results, method,year=0):
    best = 0
    data = pd.DataFrame()
    if method == 0:
        dems = results.loc[(results.Party == 'D')]
        draces = dems['Office'].drop_duplicates()
        reps = results.loc[(results.Party == 'R')]
        rraces = reps['Office'].drop_duplicates()
        for race in draces.iteritems():
            runners = dems.loc[dems.Office == race[1]]
            for index, cand in runners.iterrows():
                if cand.Total > best:
                    best = cand.Total
            for index, cand in runners.iterrows():
                if cand.Total == best:
                    cand.Won = 1
                data = data.append(cand)
            best =0
        for race in rraces.iteritems():
            runners = reps.loc[reps.Office == race[1]]
            for index, cand in runners.iterrows():
                if cand.Total > best:
                    best = cand.Total
            for index, cand in runners.iterrows():
                if cand.Total == best:
                    cand.Won = 1
                data = data.append(cand)
            best =0   
    if method == 1:
        races = results['Office'].drop_duplicates()
        for race in races.iteritems():
            runners = results.loc[results.Office == race[1]]
            for index, cand in runners.iterrows():
                if cand.Total > best:
                    best = cand.Total
            for index, cand in runners.iterrows():
                if cand.Total == best:
                    cand.Won = 1
                    inc_updater(masterlist,year,cand)
                    #print(cand.Total, cand.Won)
                #print(cand)
                data = data.append(cand)
            best =0
    return pd.DataFrame(data)
        
def inc_updater(masterlist,year,cand):
    index = 'Incum_' + str(year)
    masterlist.loc[cand.Office,index] = cand.Name
    return
    
def inc_insurance(year):
    incum = 'Incum_' + str(year)
    last = 'Incum_' + str(year-2)
    for index, row in masterlist.iterrows():
        masterlist[incum] = masterlist[last]
    return

def fill_update(file,year,general):
    update = inc_checker(file,year,masterlist)
    inc_insurance(year)
    update = won_checker(update,general,year)
    return update

def county(canlist):
    can_list = []
    for index, row in canlist.iterrows():
        co = row.County
        if not pd.isnull(co):
            row.off_trim = row.off_trim + co
        print(row.off_trim)
        row.off_trim = str(row.off_trim).strip()
        can_list.append(row)
    return pd.DataFrame(can_list)

def contrib_list_cleanup(contrib_data):
    data = pd.DataFrame()
    rex = re.compile(r"(20)(\d\d) (20\d\d) ([A-Za-z]*) (\d\d/\d\d/20\d\d) (\d*) (Day)")
    rex2 = re.compile(r"(20)(\d\d) (\s)(Annual)")
    contrib_data = contrib_data[contrib_data.Office.notnull()]
    for index, row in contrib_data.iterrows():
        row['Contribution Date'] = pd.to_datetime(row['Contribution Date'])
        row['Filing Period'] = re.sub(rex,r"\2-\4_\6",row['Filing Period'])
        row['Filing Period'] = re.sub(rex2,r"\2-\4",row['Filing Period'])
        print(index, row['Filing Period'])
        data = data.append(row)
    return data

def fec_to_datetime(date):
    rex = re.compile(r'(\d\d)(\d\d)(\d\d)(\d\d)')
    date = str(re.sub(rex,r"\3-\4-\2",date))
    date = date.split('.')
    date= date[0]
    print(date)
    return pd.to_datetime(date)