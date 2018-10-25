# -*- coding: utf-8 -*-
"""
Created on Tue Oct 16 17:58:38 2018

@author: Dillon
"""
import numpy as np
import pandas as pd
import re

primary_dict = {2007:pd.to_datetime('8/28/08'),
                2008:pd.to_datetime('8/28/08'),
                2009:pd.to_datetime('9/02/10'),
                2010:pd.to_datetime('9/02/10'),
                2011:pd.to_datetime('8/30/12'),
                2012:pd.to_datetime('8/30/12'),
                2013:pd.to_datetime('8/28/14'),
                2014:pd.to_datetime('8/28/14'),
                2015:pd.to_datetime('9/01/16'),
                2016:pd.to_datetime('9/01/16')}


contrib_dict = {
        'Self (Candidate)': 'Self',
        'Business/Group/Organization': 'PAC',
       'Political Committee': 'PAC', 
       'Total of Contributions not exceeding $100': 'sub_100',
       'Candidate Committee':'Candidate_Committee', 
       'Individual':'Individual', 
       'PAC Committee':'PAC',
       'Out-of-State or Federal Committee':'PAC', 
       'Labor Union':'PAC',
       'Political Action Committee':'PAC', 
       'Dem or Rep National Sub-Committees':'National_Sub_Committees',
       'Non-Profit Organization':'PAC' ,
       'Ind_DE':'Ind_DE',
       'CF_ID':'CF_ID',
       'Contrib_Total':'Contrib_Total',
       'Total of Expenditures not exceeding $100':'sub_100',
       '3rd Party Advertiser' : 'PAC'
        }
expend_dict = {
        'Contributions':'Contributions',
        'Non-Candidate Loan Payment': 'Non_Cand_Loan',
        'Other Expenses': 'Other',
        'Fund Raiser':'Fund_Raiser',
        'Field Expenses ': 'Field_Expenses',
        'Media':'Media',
        'Postage':'Postage',
        'Salaries and Other compensation':'Staff',
        'Rent and Other Office expenses': 'Rent_Office_Expense',
        'Reimburse':'Reimburse',
        'Printing and Campaign Materials ': 'Printing',
        'Total of Expenditures not exceeding $100': 'Small_Expend',
        'Candidate Loan Payment':'Cand_Load',
        'Direct Mailing by Mail House (R)': 'Mail_House',
        'Debts Incurred Paid':'Debts',
        'In-Kind':'In-Kind',
        'Transfer': 'Transfer',
        'Data Conversion':'Conversion',
        'Return Contributions':'Return',
        'Purchase of Equipment':'Equipment',
        'Independent Expenditures':'Independent_Expenditures',
        'Interest':'Interest'
 }

purp_dict= {
        'Data Conversion': 'X', 
         'Field Expenses ':'Field Expenses',
       'Rent and Other Office expenses':'Rent and Other Office expenses', 
       'Fund Raiser': 'Fund Raiser',
       'Purchase of Equipment':'Rent and Other Office expenses', 
       'In-Kind':'Contributions', 
       'Media':'Media', 
       'Postage':'Mail',
       'Printing and Campaign Materials ':'Printing and Campaign Materials',
       'Salaries and Other compensation': 'Salaries and Other compensation', 
       'Expense Reimbursement':'Candidate Expenses',
       'Contribution to Committee':'Contributions', 
       'Fundraiser -General Expenses': 'Fund Raiser',
       'Fundraiser - Entertainment': 'Fund Raiser', 
       'Phone Bank':'Field Expenses',
       'Consulting Fees - Media':'Media', 
       'Postage ':'Mail',
       'Fundraiser - Food & Beverage': 'Fund Raiser', 
       'Meeting Expenses ':'Rent and Other Office expenses',
       'Bank Charges':'Fund Raiser', 
       'Billboards / Outdoor Advertising':'Media',
       'Media - Newspaper':'Media', 
       'Book/Brochure Advertising':'Media',
       'Candidate Expense-Ballot Fee':'Candidate Expenses', 
       'Wages - Campaign Staff': 'Salaries and Other compensation',
       'Office Supplies':'Rent and Other Office expenses', 
       'Media - Phones / Robo calls':'Media',
       'Contribution to federal committee':'Contributions', 
       'Printing - Brochures':'Printing and Campaign Materials',
       'Volunteer Meals':'Field Expenses', 
       'Media - Online Advertising':'Media',
       'Total of Expenditures not exceeding $100':'smol',
       'Printing Give away items (buttons bumper stickers t-shirts)':'Printing and Campaign Materials',
       'Event or Fair Booth Expenses':'Field Expenses',
       'Media - Billboards / Outdoor Advertising':'Media',
       'Utilities - Phone / Cell Phone ':'Rent and Other Office expenses',
       'Credit Card Service Processing Charges':'Fund Raiser',
       'Wages - Campaign Manager': 'Salaries and Other compensation', 
       'Media - TV':'Media', 
       'Office Rent':'Rent and Other Office expenses',
       'Utilities - Electrical ':'Rent and Other Office expenses', 
       'Mailing Service':'Mail', 
       'Printing - Copies':'Printing and Campaign Materials',
       'Consulting Fees - General': 'Salaries and Other compensation', 
       'Mailing List':'Mail',
       'Media - Graphic Design':'Media', 
       'Fundraiser - Hall Rental': 'Fund Raiser',
       'Media - Radio':'Media',
       'Printing - Yard Signs':'Printing and Campaign Materials',
       'Consultant Fees- Campaign workers': 'Salaries and Other compensation',
       'Payroll Company Management Expense':'Salaries and Other compensation',
       'Wages - Employment Taxes': 'Salaries and Other compensation',
       'Utilities - Internet Access ':'Rent and Other Office expenses', 
       'Fair Expenses':'Field Expenses',
       'For Close Out Only-Charitable Donation':'Contributions',
       'Printing Misc. (buttons  bumper stickers  t-shirts)':'Printing and Campaign Materials',
       'Survey/Polls':'Field Expenses', 
       'Media - Website Development':'Media',
       'Transfer to Other Registered political Committees':'Contributions',
       'Staff - Mileage': 'Salaries and Other compensation', 
       'Fundraiser - Auction Item': 'Fund Raiser',
       'Election -Day workers':'Field Expenses', 
       'Staff - Travel': 'Salaries and Other compensation',
       'IT - Campaign Software':'Field Expenses',
       'Staff - Parking': 'Salaries and Other compensation',
       'Staff - Lodging': 'Salaries and Other compensation',
       'IT - Campaign IT Maintenance':'Rent and Other Office expenses', 
       'Legal Fees - General':'Rent and Other Office expenses',
       'Staff - Gas ': 'Salaries and Other compensation', 
       'IT - Campaign Computer Equip':'Rent and Other Office expenses',
       'Gifts':'Candidate Expenses',
       'Legal Fees - Compliance/Administrative':'Rent and Other Office expenses', 
       'Utilities - Gas ':'Rent and Other Office expenses',
       'Office Furniture':'Rent and Other Office expenses', 
       'Office - Campaign Office Maintenance':'Rent and Other Office expenses',
       'Professional - Accounting':'Rent and Other Office expenses', 
       'Staff - Employee Benefits Costs': 'Salaries and Other compensation',
       'Legal Fees - Campaign Election Relates':'Rent and Other Office expenses', 
       'Media - Videos':'Media',
       'Media - Book/Brochure Advertising':'Media',
       'Media – Videos':'Media',
       'Media – Book/Brochure Advertising':'Media',
       'Research - Survey':'Field Expenses',
       'Candidate Expenses - Travel':'Candidate Expenses', 
       'Income Tax (Interest Income)': 'Salaries and Other compensation',
       'Staff - Insurance': 'Salaries and Other compensation',
       'Candidate Expenses - Meals':'Candidate Expenses',
       'Phones / Robo calls':'Media', 
       'Online Advertising':'Media', 
       'Graphic Design':'Media',
       'Tickets to Events':'Field Expenses',
       'CF_ID':'CF_ID',
       'Expend_Total':'Expend_Total',
       'Other':'X',
       'Other Expenses':'X'}
purp_dict2= {'Bank Charges':'Fund Raiser',
             'Mailing List': 'Mail',
             'Utilities ': 'Rent and Other Office expenses',
             'Contribution to Committee':'Contributions',
             'Wages ':'Salaries and Other compensation', 
             'Meeting Expenses ':'Candidate Expenses', 
             'Event or Fair Booth Expenses':'Field Expenses',
             'Total of Expenditures not exceeding $100':'smol', 
             'Other':'Other', 
             'Postage ':'Mail',
             'Fundraiser ':'Fund Raiser',
             'Fund Raiser':'Fund Raiser',
             'Book/Brochure Advertising':'Printing and Campaign Materials',
             'Media ':'Media', 
             'Mail':'Mail',
             'Salaries and Other compensation':'Salaries and Other compensation',
             'Contributions':'Contributions',
             'Rent and Other Office expenses':'Rent and Other Office expenses',
             'Election ':'Candidate Expenses',
             'Printing ':'Printing and Campaign Materials', 
             'Mailing Service':'Mail', 
             'Candidate Expenses':'Candidate Expenses',
             'Field Expenses':'Field Expenses',
             'smol':'smol',
             'Media':'Media',
             'Printing and Campaign Materials':'Printing and Campaign Materials',
             'Billboards / Outdoor Advertising':'Media',
             'Printing Give away items (buttons bumper stickers t':'Printing and Campaign Materials', 
             'IT ':'Rent and Other Office expenses',
             'Office Supplies':'Rent and Other Office expenses', 
             'Consultant Fees':'Salaries and Other compensation', 
             'Volunteer Meals':'Field Expenses', 
             'Consulting Fees ':'Salaries and Other compensation',
             'Credit Card Service Processing Charges':'Fund Raiser', 
             'Legal Fees ':'Rent and Other Office expenses',
             'Office Rent':'Rent and Other Office expenses',
             'Printing Misc. (buttons  bumper stickers  t':'Printing and Campaign Materials',
             'Contribution to federal committee':'Contributions', 
             'Candidate Expense':'Candidate Expenses', 
             'Office ':'Rent and Other Office expenses',
             'Staff ' :'Salaries and Other compensation',
             'Transfer to Other Registered political Committees':'Contributions',
             'Fair Expenses':'Field Expenses' ,
             'Payroll Company Management Expense':'Salaries and Other compensation', 
             'Data Conversion':'Data Conversion',
             'Phone Bank':'Field Expenses', 
             'For Close Out Only' :'Field Expenses',
             'Office Furniture' :'Rent and Other Office expenses',
             'Professional ':'Salaries and Other compensation',
             'Income Tax (Interest Income)':'Salaries and Other compensation', 
             'Survey/Polls' :'Field Expenses',
             'Research ':'Field Expenses'}
    
period_dict = {    
        '2016 30 Day Primary':13, 
        '2015 Annual':12, 
       '2014 8 Day Primary':11, 
       '2014 30 Day Primary':10,
       '2013 Annual':9, 
       '2011 Annual':6, 
       '2012 8 Day Primary':8,
       '2012 30 Day Primary':7,
       '2009 Annual':3, 
       '2010 30 Day Primary':4,
       '2010 8 Day Primary':2,
       '2008 8 Day Primary':2, 
       '2008 30 Day Primary':1,
       '2007 Annual':0,
       '2016 8 Day Primary':14}
periods = pd.Series([ '2006  Annual',
       '2007  Annual',
       '2008 2008 Primary 01/09/2008 8 Day',
       '2008 2008 General 02/04/2008 30 Day',
       '2008 2008 General 11/4/2008 30 Day',
       '2008 2008 General 11/4/2008 8 Day', 
       '2008  Annual',
       '2009  Annual',
       '2010 2010 Primary 09/14/2010 30 Day',
       '2010 2010 Primary 09/14/2010 8 Day'
       '2010 2010 General 11/02/2010 30 Day',
       '2010 2010 General 11/02/2010 8 Day',
       '2010  Annual',
       '2011  Annual',
       '2012 2012 Primary 09/11/2012 30 Day',
       '2012 2012 Primary 09/11/2012 8 Day'
       '2012 2012 General 11/06/2012 30 Day'
       '2012 2012 General 11/06/2012 8 Day',
       '2012  Annual', 
       '2013  Annual',
       '2014 2014 Primary 09/09/2014 30 Day',
       '2014 2014 Primary 09/09/2014 8 Day',
       '2014 2014 General 11/4/2014 30 Day',
       '2014 2014 General 11/4/2014 8 Day',
       '2014  Annual',
       '2015  Annual',
       '2016 2016 Primary 09/13/2016 30 Day',
       '2016 2016 Primary 09/13/2016 8 Day',
       '2016 2016 General 11/08/2016 30 Day',
       '2016 2016 General 11/08/2016 8 Day', 
       '2016  Annual',
       '2017  Annual',
       '2018 2018 Primary 09/06/2018 30 Day',
       '2018 2018 Primary 09/06/2018 8 Day'
       '2018 2018 General 11/06/2018 30 Day',
       '2018  Annual'] )

periods2 = pd.Series([ '2006 Annual',
       '2007 Annual', #1
       '2008 8 Day Primary', #2
       '2008 30 Day Primary', #3
       '2008 30 Day General', #4
       '2008 8 Day General', #5
       '2008 Annual',#6
       '2009 Annual',#7
       '2010 30 Day Primary',#8
       '2010 8 Day Primary',#9
       '2010 30 Day General',#10
       '2010 8 Day General'#11
       '2010 Annual',#12
       '2011 Annual',#13
       '2012 30 Day Primary',#14
       '2012 8 Day Primary',#15
       '2012 30 Day General',#16
       '2012 8 Day General'#17
       '2012 Annual', #18
       '2013 Annual',#19
       '2014 30 Day Primary',#20
       '2014 8 Day Primary',#21
       '2014 30 Day General',#22
       '2014 8 Day General'#23
       '2014 Annual',#24
       '2015 Annual',#25
       '2016 30 Day Primary',#26
       '2016 8 Day Primary',#27
       '2016 30 Day General',#28
       '2016 8 Day General', #29
       '2016 Annual',#30
       '2017 Annual',#31
       '2018 2018 Primary 09/06/2018 30 Day',#32
       '2018 2018 Primary 09/06/2018 8 Day'#33
       '2018 2018 General 11/06/2018 30 Day',#34
       '2018  Annual'] )#35
period_dict = {
        '2008all':[1,2,3,4,5,6],
        '2008p':[1,2,3],
        '2010all':[7,8,9,10,11,12],
        '2010p':[7,8,9],
        '2012all':[13,14,15,16,17,18],
        '2012p':[13,14,15],
        '2014all':[19,20,21,22,23,24],
        '2014p':[19,20,21],
        '2016all':[25,26,27,28,29,30],
        '2016p':[25,26,27],
        '2018all':[31,32,33,34,35],
        '2018p':[31,32,33],
        }
office_dict = {'Governor':'GOVERNOR',
 '(Governor)':'GOVERNOR',
 'Lieutenant Governor':'LIEUTENANT GOVERNOR',
 '(Lieutenant Governor)':'LIEUTENANT GOVERNOR',
 'Insurance Commissioner':'INSURANCE COMMISSIONER',
 '(Insurance Commissioner)':'INSURANCE COMMISSIONER',
 'Attorney General':'ATTORNEY GENERAL',
 '(Attorney General)':'ATTORNEY GENERAL',
 'State Treasurer':'STATE TREASURER',
 '(State Treasurer)':'STATE TREASURER',
 'Auditor of Accounts':'AUDITOR OF ACCOUNTS',
 '(Auditor of Accounts)':'AUDITOR OF ACCOUNTS',
 'District 01 (State Senator)':'STATE SENATOR DISTRICT 1',
 'District 02 (State Senator)':'STATE SENATOR DISTRICT 2',
 'District 03 (State Senator)':'STATE SENATOR DISTRICT 3',
 'District 04 (State Senator)':'STATE SENATOR DISTRICT 4',
 'District 05 (State Senator)':'STATE SENATOR DISTRICT 5',
 'District 06 (State Senator)':'STATE SENATOR DISTRICT 6',
 'District 07 (State Senator)':'STATE SENATOR DISTRICT 7',
 'District 08 (State Senator)':'STATE SENATOR DISTRICT 8',
 'District 09 (State Senator)':'STATE SENATOR DISTRICT 9',
 'District 10 (State Senator)':'STATE SENATOR DISTRICT 10',
 'District 11 (State Senator)':'STATE SENATOR DISTRICT 11',
 'District 12 (State Senator)':'STATE SENATOR DISTRICT 12',
 'District 13 (State Senator)':'STATE SENATOR DISTRICT 13',
 'District 14 (State Senator)':'STATE SENATOR DISTRICT 14',
 'District 15 (State Senator)':'STATE SENATOR DISTRICT 15',
 'District 16 (State Senator)':'STATE SENATOR DISTRICT 16',
 'District 17 (State Senator)':'STATE SENATOR DISTRICT 17',
 'District 18 (State Senator)': 'STATE SENATOR DISTRICT 18',
 'District 19 (State Senator)':'STATE SENATOR DISTRICT 19',
 'District 20 (State Senator)':'STATE SENATOR DISTRICT 20',
 'District 21 (State Senator)':'STATE SENATOR DISTRICT 21',
 'District 01 (State Representative)':'STATE REPRESENTATIVE DISTRICT 1',
 'District 02 (State Representative)':'STATE REPRESENTATIVE DISTRICT 2',
 'District 03 (State Representative)':'STATE REPRESENTATIVE DISTRICT 3',
 'District 04 (State Representative)':'STATE REPRESENTATIVE DISTRICT 4',
 'District 05 (State Representative)':'STATE REPRESENTATIVE DISTRICT 5',
 'District 06 (State Representative)':'STATE REPRESENTATIVE DISTRICT 6',
 'District 07 (State Representative)':'STATE REPRESENTATIVE DISTRICT 7',
 'District 08 (State Representative)':'STATE REPRESENTATIVE DISTRICT 8',
 'District 09 (State Representative)':'STATE REPRESENTATIVE DISTRICT 9',
 'District 10 (State Representative)':'STATE REPRESENTATIVE DISTRICT 10',
 'District 11 (State Representative)':'STATE REPRESENTATIVE DISTRICT 11',
 'District 12 (State Representative)':'STATE REPRESENTATIVE DISTRICT 12',
 'District 13 (State Representative)':'STATE REPRESENTATIVE DISTRICT 13',
 'District 14 (State Representative)':'STATE REPRESENTATIVE DISTRICT 14',
 'District 15 (State Representative)':'STATE REPRESENTATIVE DISTRICT 15',
 'District 16 (State Representative)':'STATE REPRESENTATIVE DISTRICT 16',
 'District 17 (State Representative)':'STATE REPRESENTATIVE DISTRICT 17',
 'District 18 (State Representative)':'STATE REPRESENTATIVE DISTRICT 18',
 'District 19 (State Representative)':'STATE REPRESENTATIVE DISTRICT 19',
 'District 20 (State Representative)':'STATE REPRESENTATIVE DISTRICT 20',
 'District 21 (State Representative)':'STATE REPRESENTATIVE DISTRICT 21',
 'District 22 (State Representative)':'STATE REPRESENTATIVE DISTRICT 22',
 'District 23 (State Representative)':'STATE REPRESENTATIVE DISTRICT 23',
 'District 24 (State Representative)':'STATE REPRESENTATIVE DISTRICT 24',
 'District 25 (State Representative)':'STATE REPRESENTATIVE DISTRICT 25',
 'District 26 (State Representative)':'STATE REPRESENTATIVE DISTRICT 26',
 'District 27 (State Representative)':'STATE REPRESENTATIVE DISTRICT 27',
 'District 28 (State Representative)':'STATE REPRESENTATIVE DISTRICT 28',
 'District 29 (State Representative)':'STATE REPRESENTATIVE DISTRICT 29',
 'District 30 (State Representative)':'STATE REPRESENTATIVE DISTRICT 30',
 'District 31 (State Representative)':'STATE REPRESENTATIVE DISTRICT 31',
 'District 32 (State Representative)':'STATE REPRESENTATIVE DISTRICT 32',
 'District 33 (State Representative)':'STATE REPRESENTATIVE DISTRICT 33',
 'District 34 (State Representative)':'STATE REPRESENTATIVE DISTRICT 34',
 'District 35 (State Representative)':'STATE REPRESENTATIVE DISTRICT 35',
 'District 36 (State Representative)':'STATE REPRESENTATIVE DISTRICT 36',
 'District 37 (State Representative)':'STATE REPRESENTATIVE DISTRICT 37',
 'District 38 (State Representative)':'STATE REPRESENTATIVE DISTRICT 38',
 'District 39 (State Representative)':'STATE REPRESENTATIVE DISTRICT 39',
 'District 40 (State Representative)':'STATE REPRESENTATIVE DISTRICT 40',
 'District 41 (State Representative)':'STATE REPRESENTATIVE DISTRICT 41',
 'County Executive':'COUNTY EXECUTIVE (N)',
 '(County Executive)':'COUNTY EXECUTIVE (N)',
 'President of County Council':'PRESIDENT OF COUNTY COUNCIL (N)',
 '(President of County Council)':'PRESIDENT OF COUNTY COUNCIL (N)',
 'District 06 (County Council)':'COUNTY COUNCIL DISTRICT 6 (N)',
 'District 07 (County Council)':'COUNTY COUNCIL DISTRICT 7 (N)',
 'District 08 (County Council)':'COUNTY COUNCIL DISTRICT 8 (N)',
 'District 09 (County Council)':'COUNTY COUNCIL DISTRICT 9 (N)',
 'District 10 (County Council)':'COUNTY COUNCIL DISTRICT 10 (N)',
 'District 11 (County Council)':'COUNTY COUNCIL DISTRICT 11 (N)',
 'District 12 (County Council)': 'COUNTY COUNCIL DISTRICT 12 (N)',
 'Mayor':'MAYOR',
 '(Mayor)':'MAYOR',
 'President of City Council':'PRESIDENT OF CITY COUNCIL',
 '(President of City Council)':'PRESIDENT OF CITY COUNCIL',
 'District 01 (City Treasurer)':'CITY TREASURER',
 'District 01 City Treasurer':'CITY TREASURER',
 'At Large (City Council)':'CITY COUNCIL AT LARGE',
 'At large (City Council)':'CITY COUNCIL AT LARGE',
 'District 01 City Council':'CITY COUNCIL DISTRICT 1',
 'District 01 (City Council)':'CITY COUNCIL DISTRICT 1',
 'District 02 City Council':'CITY COUNCIL DISTRICT 2',
 'District 02 (City Council)':'CITY COUNCIL DISTRICT 2',
 'District 03 City Council':'CITY COUNCIL DISTRICT 3',
 'District 03 (City Council)':'CITY COUNCIL DISTRICT 3',
 'District 04 City Council':'CITY COUNCIL DISTRICT 4',
 'District 04 (City Council)':'CITY COUNCIL DISTRICT 4',
 
 'District 05 City Council':'CITY COUNCIL DISTRICT 5',
 'District 05 (City Council)':'CITY COUNCIL DISTRICT 5',
 
 'District 06 City Council':'CITY COUNCIL DISTRICT 6',
 'District 06 (City Council)':'CITY COUNCIL DISTRICT 6',
 
 'District 07 City Council':'CITY COUNCIL DISTRICT 7',
 'District 07 (City Council)':'CITY COUNCIL DISTRICT 7',
 'District 08 City Council':'CITY COUNCIL DISTRICT 8',
 'District 08 (City Council)':'CITY COUNCIL DISTRICT 8',
 'Levy Court Commissioner at Large': 'LEVY COURT AT LARGE (K)',
 '(Levy Court Commissioner at Large)': 'LEVY COURT AT LARGE (K)',
 'District 01 (District Levy Court Commissioner)':'1ST LEVY COURT DISTRICT (K)',
 'District 02 (District Levy Court Commissioner)':'2ND LEVY COURT DISTRICT (K)',
 'District 03 (District Levy Court Commissioner)':'3RD LEVY COURT DISTRICT (K)',
 'District 04 (District Levy Court Commissioner)':'4TH LEVY COURT DISTRICT (K)',
 'District 05 (District Levy Court Commissioner)':'5TH LEVY COURT DISTRICT (K)',
 'District 06 (District Levy Court Commissioner)':'6TH LEVY COURT DISTRICT (K)',
 'Commissioner':'X',
 'District 01 (Council Member)':'X',
 'Clerk of Peace': 'CLERK OF PEACE',
 'Recorder of Deeds':'RECORDER OF DEEDS',
 '(Recorder of Deeds)':'RECORDER OF DEEDS',
 'School Board Member':'X',
 'Register of Wills': 'REGISTER OF WILLS',
 '(Register of Wills)': 'REGISTER OF WILLS', 
 'Comptroller':'X',
 'District 01 (County Council)':'District 01 (County Council)',
 'District 02 (County Council)':'District 02 (County Council)',
 'District 03 (County Council)':'District 03 (County Council)',
 'District 04 (County Council)':'District 04 (County Council)',
 'District 05 (County Council)':'District 05 (County Council)', 
 'Sheriff':'SHERIFF',
 'District 06 Council Person':'X',
 'District 01 Council Person':'X', 
 'District 03 (Council Member)':'X',
 'District 02 (Council Member)':'X', 
 'District 05 Council Person':'X',
 'District 04 (Council Member)':'X',
 '(School Board Member)':'X',
 '(Sheriff)':'SHERIFF', 
 '(Clerk of Peace)': 'CLERK OF PEACE',
 'District 05 (Council Person)':'X',
 '(Commissioner)':'X',
 '(City Council)':'X', 
 'District E (School Board Member)':'X',
 'District B (School Board Member)':'X',
 '(Mayor_)':'X',
 'At Large (School Board Member)':'X',
 'District C (School Board Member)':'X',
 'District G (School Board Member)':'X'}