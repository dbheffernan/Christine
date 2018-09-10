# -*- coding: utf-8 -*-
"""
Created on Tue Aug 14 16:52:44 2018

@author: Dillon
"""
import numpy as np
import pandas as pd
import re
import math

from glob import glob

data = []
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

filepath = (r"c:\users\Dillon\downloads\finance data\16\results.txt")
x = input('input canlist, masterlist?')
if(x==1):
    canlist = pd.read_csv(r"canlistv3.csv")
    contribs = pd.read_csv(r"c:\users\Dillon\downloads\finance data\contrib.csv")
    contribs7 = pd.read_csv(r"c:\users\Dillon\downloads\finance data\08\contrib7.csv")
    contribs8 = pd.read_csv(r"c:\users\Dillon\downloads\finance data\contribs08.csv")
    contribs10 = pd.read_csv(r"c:\users\Dillon\downloads\finance data\contribs10.csv")
    contribs12 = pd.read_csv(r"c:\users\Dillon\downloads\finance data\contribs12.csv")
    masterlist = pd.read_csv(r"masterli.csv",index_col ='Office')

x = input('input expense?')
if(x==1):
    bigexpend = pd.read_csv(r"c:\users\Dillon\downloads\finance data\16\16expend.csv")
    expend15  = pd.read_csv(r"c:\users\Dillon\downloads\finance data\16\15expend.csv")
    expend14  = pd.read_csv(r"c:\users\Dillon\downloads\finance data\14\14expend.csv")
    expend13  = pd.read_csv(r"c:\users\Dillon\downloads\finance data\14\13expend.csv")
    expend12  = pd.read_csv(r"c:\users\Dillon\downloads\finance data\12\12expend.csv")
    expend11  = pd.read_csv(r"c:\users\Dillon\downloads\finance data\12\11expend.csv")
    expend10  = pd.read_csv(r"c:\users\Dillon\downloads\finance data\10\10expend.csv")
    expend09  = pd.read_csv(r"c:\users\Dillon\downloads\finance data\10\09expend.csv")
    expend08  = pd.read_csv(r"c:\users\Dillon\downloads\finance data\08\08expend.csv")
    bigexpend = bigexpend.append(expend15, ignore_index=True)
    bigexpend = bigexpend.append(expend14, ignore_index=True)
    bigexpend = bigexpend.append(expend13, ignore_index=True)
    bigexpend = bigexpend.append(expend12, ignore_index=True)
    bigexpend = bigexpend.append(expend11, ignore_index=True)
    bigexpend = bigexpend.append(expend10, ignore_index=True)
    bigexpend = bigexpend.append(expend09, ignore_index=True)
    bigexpend = bigexpend.append(expend08, ignore_index=True)

returns_dict = {
        'party': re.compile(r'(?P<party>.*); ; ; ; ;'),
        'office': re.compile(r'(?P<office>.*); ;'),
        'candidate': re.compile(r'(?P<candidate>.*);'),
        'state' : re.compile(r'State Office - (?P<state>.*)'),
        'nc': re.compile(r'County Office - New Castle County - (?P<nc>.*)'),
        'kc': re.compile(r'County Office - Kent County - (?P<kc>.*)'),
        'sc': re.compile(r'County Office - Sussex County - (?P<sc>.*)')
        }

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
       'Contrib_Total':'Contrib_Total'
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

dict_pics = {    
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

#results08p = parser(r"c:\users\Dillon\downloads\finance data\08resultsp.txt")
#results08p['Total'] = pd.to_numeric(results08p['Total'],errors='coerce')
#results08g = parser(r"c:\users\Dillon\downloads\finance data\08resultsg.txt")
#results08g['Total'] = pd.to_numeric(results08g['Total'],errors='coerce')
#results10p = parser(r"c:\users\Dillon\downloads\finance data\10resultsp.txt")
#results10p['Total'] = pd.to_numeric(results10p['Total'],errors='coerce')
#results12p = parser(r"c:\users\Dillon\downloads\finance data\12resultsp.txt")
#results12p['Total'] = pd.to_numeric(results12p['Total'],errors='coerce')
#results14p = parser(r"c:\users\Dillon\downloads\finance data\14resultsp.txt")
#results14p['Total'] = pd.to_numeric(results14p['Total'],errors='coerce')
#results16p = parser(r"c:\users\Dillon\downloads\finance data\16resultsp.txt")
#results16p['Total'] = pd.to_numeric(results16p['Total'],errors='coerce')

