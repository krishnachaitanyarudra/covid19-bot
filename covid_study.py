# -*- coding: utf-8 -*-
"""
Created on Sun Sep  7 00:43:19 2020

@author: krishna chaitanya
"""

import requests


url = "https://covid-19india-api.herokuapp.com/all"



#response = requests.request("GET", url, headers=headers, data = payload)
response=requests.get(url)

covid_data=response.json()
#print(covid_data[1]['state_data'])#List of Dict

covid_data_states=covid_data[1]['state_data']
covid_data_total=covid_data[0]#dict


def getstatesdata(state):
    res=[x for x in covid_data_states if x['state'].lower().replace(" ","").strip()==state.lower().replace(" ","").strip()]
    res_f=''
    if len(res)>0:
        for key,value in res[0].items():
            res_f+=str(key)+" : "+str(value)+"\n"
    return res_f

def gettotaldata():
    res_t=''
    for key,value in covid_data_total.items():
        res_t+=str(key)+" : "+str(value)+"\n"
    return res_t






