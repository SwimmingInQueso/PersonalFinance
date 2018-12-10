# Things left to do
# 1) Capitalization agnostic
# 2) Create rules based on more than just description (Values & Category for example)
# 3) Create select multiple option
# 4) Make sure Venmo payments are going in the right direction
# 5) What's going on with uber transactions

print("poop")

import numpy as np
import pandas as pd
from pandas import DataFrame,Series
from matplotlib import pyplot as plt
import csv
import os
from selenium import webdriver
import time
from selenium.webdriver.common import action_chains, keys
from datetime import datetime
import timedelta
import requests
import json
import unicodecsv as csv
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from shutil import copyfile

def import_data():
    global tr
    tr = pd.read_csv('Jan 1-2018 thru Dec 6-2018 transactions.csv')
    tr['timestamp'] = pd.to_datetime(tr['Date'])
    tr['year'], tr['month'] = tr['timestamp'].dt.year, tr['timestamp'].dt.month

def initial_categories():
    global groceries , rent, uber, transport, legal, shopping, restaurants, investments, travel, entertainment, ignore, categories
#     groceries, rent, uber, transport, legal, shopping, restaurants, investments, travel, entertainment, ignore, health = ([] for i in range(12))
    categories = {'groceries':groceries, 'rent': rent, 'Uber':uber, 'transport':transport, 'legal':legal, 'shopping':shopping, 'restaurants':restaurants, 'investments':investments, 'travel':travel, 'entertainment':entertainment, 'ignore':ignore}

def rerun():
    read_data_dict()
    map_descriptions()
    transform_to_df()
    
def read_data_dict():
    global mydict

    import csv
    mydict = []
    with open('Jan 1-2018 thru Dec 6-2018 transactions.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            mydict.append(row)

def map_descriptions():
    global newlist
    newlist = []
    l = categories
    l_list = list(l.keys())
    ignore_accts = ['Brokerage Account','Individual - Tod ','Linkedin Plan - Ending in 6082','Microsoft Corporati','Roth','Ira']

    for count in range(0,len(mydict)): # going through the entire list of ordered dictionaries
        x = list(mydict[count].items()) # turning the ordered dictionary into a list of items
        x.append(('Supercat','Uncategorized'))
        newlist.append(x)

    for count in range(0,len(newlist)):    
        for count1 in range(0,len(l_list)):
            if any(y.lower() in newlist[count][2][1].lower() for y in l[l_list[count1]]): 
                newlist[count][6] = ('Supercat',l_list[count1])

    for count in range(0,len(newlist)):    
            if any(y in newlist[count][1][1] for y in ignore_accts): 
                newlist[count][6] = ('Supercat','ignore')
                
    return newlist

def transform_to_df():
    import csv
    map_descriptions()
    myData = []

    cols = []
    for count in range(0,len(newlist[0])):
        cols.append(newlist[0][count][0])

    myData.append(cols)
    for count in range(0,len(newlist)):
        row = []
        for x in range(0,7):
            y = newlist[count][x][1]
            row.append(y)
        myData.append(row)

    myFile = open('csvexample3.csv', 'w')  
    with myFile:  
       writer = csv.writer(myFile)
       writer.writerows(myData)
        
    global tr
    tr = pd.read_csv('csvexample3.csv')
    tr['timestamp'] = pd.to_datetime(tr['Date'])
    tr['year'], tr['month'] = tr['timestamp'].dt.year, tr['timestamp'].dt.month
    
def enter_cat():
    global uncat_only
    replay = True
    while replay == True:
        array = input("Which array do you want to update? \n groceries, rent, uber, transport, legal, shopping, restaurants, investments, travel, entertainment, ignore")
        value = input("Which value do you want to add?")
        if (array == 'done' or value == 'done'):
            break
        else:
            try: 
                categories[array].append(value)
            except:
                create_new = input("That is not a category. Would you like to add it as one?")
                if create_new == 'yes':
                    array_values = []
                    categories.update({array:array_values})
                    categories[array].append(value)
                    
def clean_up(row):
    if (row['Description'] == 'Linkedin') and (row['Amount'] == -1199.4):
        val = 'business'
    elif (row['Description'] == 'Linkedin-xxx*xxx9816') and (row['Amount'] == -180.0):
        val = 'business'
    elif ("Sreekar Jasthi" in row['Description']) and (row['Amount'] >1000.0):
        val = 'rent'
    elif ("Akshay Verma" in row['Description']) and (row['Amount'] >1000.0):
        val = 'rent'
    elif (row['Category'] == 'Restaurants') and (row['Supercat'] == 'uncategorized'):
        val = row['Category'].lower()
    else:
        val =  row['Supercat'].lower()
    return val
                    
def sum_groupby(groupby,values):
    x = tr.groupby(groupby)[values].sum()
    return x.reset_index()
# uncat_only = tr[tr.Supercat == "Uncategorized"].sort_values(by=['Amount'])

def plot_cats(df,cat1,cat2,cat3,cat4,cat5):
    pivot = tr.groupby(['Category2', 'month'])["Amount"].sum()
    pivot = pivot.to_frame().reset_index()
    
    plt.figure(figsize=(20,10))

    cat1 = pivot[pivot.Category2 == cat1]
    plt.plot(cat1.month,abs(cat1.Amount))
    cat2 = pivot[pivot.Category2 == cat2]
    plt.plot(cat2.month,abs(cat2.Amount))
    cat3 = pivot[pivot.Category2 == cat3]
    plt.plot(cat3.month,abs(cat3.Amount))
    cat4 = pivot[pivot.Category2 == cat4]
    plt.plot(cat4.month,abs(cat4.Amount))
    cat5 = pivot[pivot.Category2 == cat5]
    plt.plot(cat5.month,abs(cat5.Amount))

    
    plt.xlabel("Month")
    plt.ylabel("$ Spent")

    plt.show()

def get_data():
    chromedriver = "/Users/ronakshah/Downloads/chromedriver"
    os.environ["webdriver.chrome.driver"] = chromedriver
    driver = webdriver.Chrome(chromedriver)
    driver.get ("https://home.personalcapital.com/page/login/goHome")
    

############################## Navigate through login flow
    for x in range(0,4):
        if x == 0: # enter email address
            driver.find_element_by_name("username").send_keys("rshah0749@gmail.com") 
            # Hit tab before enter
            tab = action_chains.ActionChains(driver) 
            tab.send_keys(Keys.TAB)
            tab.perform()
            del tab
        elif x == 1: # Enter SMS option
            time.sleep(1)
        elif x == 2: # give time for the SMS code to be entered
            time.sleep(10)
        elif x == 3: # put in the password
            driver.find_element_by_name("passwd").send_keys("password")     
        
        # Pushing enter
        enter = action_chains.ActionChains(driver) 
        enter.send_keys(Keys.ENTER)
        enter.perform() 
        time.sleep(2)
        
        del enter
        x=x+1
############################### Navigate through the webpage
    driver.get ("https://home.personalcapital.com/page/login/app#/all-transactions")
    time.sleep(5)
    driver.find_element_by_class_name("qa-start-date").clear()
    time.sleep(2)
                         
    driver.find_element_by_class_name("qa-start-date").send_keys("12/01/17")
    time.sleep(3)

    driver.find_element_by_class_name("pc-input-group__field").click()

    
#     driver.find_Element(By.cssSelector("pc-input-group__field.ng-pristine.ng-valid")).click();

    
    tab1 = action_chains.ActionChains(driver) 
    tab1.send_keys(Keys.TAB)
    tab1.perform()
    time.sleep(3)
    
    tab2 = action_chains.ActionChains(driver) 
    tab2.send_keys(Keys.TAB)
    tab2.perform()
    time.sleep(3)
    
    tab3 = action_chains.ActionChains(driver) 
    tab3.send_keys(Keys.TAB)
    tab3.perform()
    time.sleep(3)
    
#     tab4 = action_chains.ActionChains(driver) 
#     tab4.send_keys(Keys.TAB)
#     tab4.perform()
#     time.sleep(3)
    
#     tab5 = action_chains.ActionChains(driver) 
#     tab5.send_keys(Keys.TAB)
#     tab5.perform()
#     time.sleep(3)
    
    enter4 = action_chains.ActionChains(driver) 
    enter4.send_keys(Keys.ENTER)
    enter4.perform() 

###############################
    
    

    time.sleep(20)
    driver.quit()    
    
