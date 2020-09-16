#!/usr/bin/python3

import csv
import numpy as np
from datetime import datetime
import sys


IN_CONFIRMED= "/COVID-19/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv"
IN_RECOVERED = "/COVID-19/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv"
IN_DEATHS = "/COVID-19/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv"

OUT_CONFIRMED_TOTAL = "/total_confirmed.csv"
OUT_RECOVERED_TOTAL = "/total_recovered.csv"
OUT_DEATHS_TOTAL = "/total_deaths.csv"

OUT_CONFIRMED_TOTAL_GROW_PERCENT = "/total_grow_percent_confirmed.csv"
OUT_RECOVERED_TOTAL_GROW_PERCENT = "/total_grow_percent_recovered.csv"
OUT_DEATHS_TOTAL_GROW_PERCENT = "/total_grow_percent_deaths.csv"

OUT_CONFIRMED_BY_POPULATION = "/by_population_confirmed.csv"
OUT_RECOVERED_BY_POPULATION = "/by_population_recovered.csv"
OUT_DEATHS_BY_POPULATION = "/by_population_deaths.csv"

OUT_CONFIRMED_BY_POPULATION_GROW_PERCENT = "/by_population_grow_percent_confirmed.csv"
OUT_RECOVERED_BY_POPULATION_GROW_PERCENT = "/by_population_grow_percent_recovered.csv"
OUT_DEATHS_BY_POPULATION_GROW_PERCENT = "/by_population_grow_percent_deaths.csv"


# top five
OUT_TOP5_CONFIRMED_TOTAL = "/top5_total_confirmed.csv"
OUT_TOP5_DEATHS_TOTAL = "/top5_total_deaths.csv"

OUT_TOP5_CONFIRMED_TOTAL_GROW_PERCENT = "/top5_total_grow_percent_confirmed.csv"
OUT_TOP5_DEATHS_TOTAL_GROW_PERCENT = "/top5_total_grow_percent_deaths.csv"

OUT_TOP5_CONFIRMED_BY_POPULATION = "/top5_by_population_confirmed.csv"
OUT_TOP5_DEATHS_BY_POPULATION = "/top5_by_population_deaths.csv"

OUT_TOP5_CONFIRMED_BY_POPULATION_GROW_PERCENT = "/top5_by_population_grow_percent_confirmed.csv"
OUT_TOP5_DEATHS_BY_POPULATION_GROW_PERCENT = "/top5_by_population_grow_percent_deaths.csv"

OUT_AUSTRIA = "/austria.csv"

# https://en.wikipedia.org/wiki/List_of_European_countries_by_population
countries_template = {
    "Russia": { "population": 146877088, "eu": True, "top5": True},
    "Brazil": { "population": 208360000, "eu": False, "top5": True},
    "Germany": { "population": 82887000, "eu": True},
    "Turkey": { "population": 82003882, "eu": True},
    "France": { "population": 67372000, "eu": True},
    "United Kingdom": { "population": 66435550, "eu": True},
    "Italy": { "population": 60390560, "eu": True},
    "Spain": { "population": 46733038, "eu": True},
    "Poland": { "population": 38433600, "eu": True},
    "Ukraine": { "population": 37289000, "eu": True},
    "Romania": { "population": 19523621, "eu": True},
    "Kazakhstan": { "population": 18356900, "eu": True},
    "Netherlands": { "population": 17417600, "eu": True},
    "Belgium": { "population": 11449656, "eu": True},
    "Greece": { "population": 10768193, "eu": True},
    "Czechia": { "population": 10627794, "eu": True},
    "Sweden": { "population": 10319601, "eu": True},
    "Portugal": { "population": 10276617, "eu": True},
    "Azerbaijan": { "population": 10000000, "eu": True},
    "Hungary": { "population": 9771000, "eu": True},
    "Belarus": { "population": 9477100, "eu": True},
    "Austria": { "population": 8857960, "eu": True},
    "Switzerland": { "population": 8526932, "eu": True},
    "Bulgaria": { "population": 7000039, "eu": True},
    "Serbia": { "population": 6963764, "eu": True},
    "Denmark": { "population": 5806015, "eu": True},
    "Finland": { "population": 5522015, "eu": True},
    "Slovakia": { "population": 5445087, "eu": True},
    "Norway": { "population": 5323933, "eu": True},
    "Ireland": { "population": 4921500, "eu": True},
    "Croatia": { "population": 4105493, "eu": True},
    "Georgia": { "population": 3729600, "eu": True},
    "Bosnia and Herzegovina": { "population": 3511372, "eu": True},
    "Armenia": { "population": 2969200, "eu": True},
    "Albania": { "population": 2870324, "eu": True},
    "Lithuania": { "population": 2791903, "eu": True},
    "Moldova": { "population": 2681735, "eu": True},
    "North Macedonia": { "population": 2075301, "eu": True},
    "Slovenia": { "population": 2070050, "eu": True},
    "Latvia": { "population": 1921300, "eu": True},
    "Kosovo": { "population": 1798506, "eu": True},
    "Estonia": { "population": 1319133, "eu": True},
    "Cyprus": { "population": 8642, "eu": True},
    "Montenegro": { "population": 622359, "eu": True},
    "Luxembourg": { "population": 602005, "eu": True},
    "Malta": { "population": 475701, "eu": True},
    "Iceland": { "population": 35562, "eu": True},
    "Jersey": { "population": 1055, "eu": True},
    "Isle of Man": { "population": 83314, "eu": True},
    "Andorra": { "population": 74794, "eu": True},
    "Guernsey": { "population": 62063, "eu": True},
    "Faroe Islands": { "population": 51237, "eu": True},
    "Monaco": { "population": 383, "eu": True},
    "Liechtenstein": { "population": 38201, "eu": True},
    "Gibraltar": { "population": 33573, "eu": True},
    "San Marino": { "population": 33407, "eu": True},
    "Åland Islands": { "population": 29489, "eu": True},
    "Vatican City": { "population": 799, "eu": True},
    "US": { "population":  329968629, "top5": True},
    "India": { "population": 1380004000, "top5": True},
    "China": { "population": 1427647786},
    "Peru": { "population": 31237385, "top5": True},
    "South Africa": { "population": 18216000}
}

confirmed_fixes_dict = {'Italy|2020-03-12': 15113,
                        'Spain|2020-03-12': 3146,
                        'France|2020-03-12': 2876,
                        'United Kingdom|2020-03-12': 590,
                        'Germany|2020-03-12': 2745,
                        'Argentina|2020-03-12': 19,
                        'Australia|2020-03-12': 122,
                        'Belgium|2020-03-12': 314,
                        'Chile|2020-03-12': 23,
                        'Colombia|2020-03-12': 9,
                        'Greece|2020-03-12': 98,
                        'Indonesia|2020-03-12': 34,
                        'Ireland|2020-03-12': 43,
                        'Japan|2020-03-12': 620,
                        'Netherlands|2020-03-12': 503,
                        'Qatar|2020-03-12': 262,
                        'Singapore|2020-03-12': 178,
                        'Switzerland|2020-03-12': 854
                        }
                        
deaths_fixes_dict = {'Italy|2020-03-12': 1016,
                     'Spain|2020-03-12': 86,
                     'France|2020-03-12': 61,
                     'United Kingdom|2020-03-12': 10,
                     'Germany|2020-03-12': 6,
                     'Argentina|2020-03-12': 1,
                     'Australia|2020-03-12': 3,
                     'Greece|2020-03-12': 1,
                     'Indonesia|2020-03-12': 1,
                     'Ireland|2020-03-12': 1,
                     'Japan|2020-03-12': 15,
                     'Netherlands|2020-03-12': 5,
                     'Switzerland|2020-03-12': 4
                     }
                     
recovered_fixes_dict = {'Italy|2020-03-12': 1258,
                        'Spain|2020-03-12': 189,
                        'France|2020-03-12': 12,
                        'United Kingdom|2020-03-12': 19,
                        'Germany|2020-03-12': 25
                        }

def extract_fixes( fixes, fixes_dict, type):

    for key in fixes_dict.keys():
        country_to_be_fixed = key.split('|')[0]
        date_to_be_fixed = datetime.strptime( key.split('|')[1], "%Y-%m-%d").strftime("%d.%m.%Y")
        value_to_be_fixed = fixes_dict[key]
        
        if( country_to_be_fixed not in fixes):
            fixes[country_to_be_fixed] = {}
        if( type not in fixes[country_to_be_fixed]):
            fixes[country_to_be_fixed][type] = {}
        fixes[country_to_be_fixed][type][date_to_be_fixed] = value_to_be_fixed

    return fixes


def extract( countries, fixes, data_in, type):

    with open( data_in, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        headers = next(reader)
        data = np.array(list(reader))
        
    # fix dates
    days = []
    for x in range( 4, len(headers)):
        headers[x] = datetime.strptime( headers[x], "%m/%d/%y").strftime("%d.%m.%Y")
        days.append( headers[x])

    # sum up countries
    sum_countries = {}
    for country in data:
        for x in range( 4, len(country)):
            if(( country[1] == country[0] or country[0] == "") and country[1] in fixes and type in fixes[country[1]] and headers[x] in fixes[country[1]][type]):
                value = fixes[country[1]][type][headers[x]]
            else:
                if( country[x] == ''):
                    value = 0
                else:
                    value = int( country[x])
        
            if( country[1] not in sum_countries):
                sum_countries[country[1]] = {}
            
            if( headers[x] not in sum_countries[country[1]]):
                sum_countries[country[1]][headers[x]] = value
            else:
                sum_countries[country[1]][headers[x]] += value

    
    for country in sum_countries:
        if( country not in countries):
            continue
        
        dates_total = {}
        dates_total_grow_percent = {}
        dates_by_population = {}
        dates_by_population_grow_percent = {}
                
        last_data = 0
        last_data_by_population = 0
        last_grow_percent = 0
        last_grow_percent_by_population = 0
        
        for day in days:
            value = sum_countries[country][day]
            
            try:
                dates_total[day] = value
                if( dates_total[day] == 0):
                    dates_total[day] = ""
                dates_by_population[day] = float(value) / float(countries[country]["population"]) * 100000
                if( dates_by_population[day] == 0):
                    dates_by_population[day] = ""
            except Exception as e:
                dates_total[day] = ""
                dates_by_population[day] = ""
                    
            if( dates_total[day] != ""):
                if( last_data != 0):
                    dates_total_grow_percent[day] = (dates_total[day] - last_data) / last_data * 100
                    last_grow_percent = dates_total_grow_percent[day]
                            
                    dates_by_population_grow_percent[day] = (dates_by_population[day] - last_data_by_population) / last_data_by_population * 100
                    last_grow_percent_by_population = dates_by_population_grow_percent[day]
                else:
                    dates_total_grow_percent[day] = 0
                    last_grow_percent = 0
                            
                    dates_by_population_grow_percent[day] = 0
                    last_grow_percent_by_population = 0
                last_data = dates_total[day]
                last_data_by_population = dates_by_population[day]
            else:
                dates_total_grow_percent[day] = last_grow_percent
                dates_by_population_grow_percent[day] = last_grow_percent_by_population
            
            if( dates_total_grow_percent[day] == 0):
                dates_total_grow_percent[day] = ""
            if( dates_by_population_grow_percent[day] == 0):
                dates_by_population_grow_percent[day] = ""
        
        if( countries[country]["population"] >= 100000): # filter out countries < 100.000 people
            countries[country][type+"_by_population"] = dates_by_population
            countries[country][type+"_by_population_grow_percent"] = dates_by_population_grow_percent
            
    return countries, days

def output( countries, days, data_out, type, filter):
    
    f = open( data_out, 'w')
    with f:
        writer = csv.writer(f)
        header = ["country"]
        for country in countries:
            if( filter in countries[country] and countries[country][filter] == True and type in countries[country]):
                header.append( country)
        
        writer.writerow(header)
        
        for day in days:
            row = [day]
            
            for x in range( 1, len(header)):
                #if( filter in countries[country] and countries[country][filter] == True):
                #    row.append( countries[header[x]][type][day])
                row.append( countries[header[x]][type][day])
            
            writer.writerow(row)
        

def output_single( countries, days, data_out, country):
    
    f = open( data_out, 'w')
    with f:
        writer = csv.writer(f)
        #header = [ "source", "confirmed_total", "deaths_total",
        #        "confirmed_by_population", "deaths_by_population",
        #        "confirmed_total_grow_percent", "deaths_total_grow_percent",
        #        "confirmed_by_population_grow_percent", "deaths_by_population_grow_percent"
        #    ] 
        header = [ "source", "confirmed_total", "recovered_total", "deaths_total",
                "confirmed_by_population", "recovered_by_population", "deaths_by_population",
                "confirmed_total_grow_percent", "recovered_total_grow_percent", "deaths_total_grow_percent",
                "confirmed_by_population_grow_percent", "recovered_by_population_grow_percent", "deaths_by_population_grow_percent"
            ] 
        
        writer.writerow(header)
        
        for day in days:
            row = [day]
            
            for x in range( 1, len(header)):
                row.append( countries[country][header[x]][day])
            
            writer.writerow(row)

def sort( unsorted):
    countries = {}

    for key in sorted( unsorted.keys()):
        countries[key] = unsorted[key]

    return countries

def main():
    dir = sys.argv[1]

    fixes = extract_fixes( {}, confirmed_fixes_dict, "confirmed")
    #fixes = extract_fixes( fixes, recovered_fixes_dict, "recovered")
    fixes = extract_fixes( fixes, deaths_fixes_dict, "deaths")

    countries = sort( countries_template)

    countries, days = extract( countries, fixes, dir+IN_CONFIRMED, "confirmed")
    countries, days = extract( countries, fixes, dir+IN_RECOVERED, "recovered")
    countries, days = extract( countries, fixes, dir+IN_DEATHS, "deaths")

    output( countries, days, dir+OUT_CONFIRMED_TOTAL, "confirmed_total", "eu")
    output( countries, days, dir+OUT_RECOVERED_TOTAL, "recovered_total", "eu")
    output( countries, days, dir+OUT_DEATHS_TOTAL, "deaths_total", "eu")

    output( countries, days, dir+OUT_CONFIRMED_TOTAL_GROW_PERCENT, "confirmed_total_grow_percent", "eu")
    output( countries, days, dir+OUT_RECOVERED_TOTAL_GROW_PERCENT, "recovered_total_grow_percent", "eu")
    output( countries, days, dir+OUT_DEATHS_TOTAL_GROW_PERCENT, "deaths_total_grow_percent", "eu")

    output( countries, days, dir+OUT_CONFIRMED_BY_POPULATION, "confirmed_by_population", "eu")
    output( countries, days, dir+OUT_RECOVERED_BY_POPULATION, "recovered_by_population", "eu")
    output( countries, days, dir+OUT_DEATHS_BY_POPULATION, "deaths_by_population", "eu")
    
    output( countries, days, dir+OUT_CONFIRMED_BY_POPULATION_GROW_PERCENT, "confirmed_by_population_grow_percent", "eu")
    output( countries, days, dir+OUT_RECOVERED_BY_POPULATION_GROW_PERCENT, "recovered_by_population_grow_percent", "eu")
    output( countries, days, dir+OUT_DEATHS_BY_POPULATION_GROW_PERCENT, "deaths_by_population_grow_percent", "eu")


    output( countries, days, dir+OUT_TOP5_CONFIRMED_TOTAL, "confirmed_total", "top5")
    output( countries, days, dir+OUT_TOP5_DEATHS_TOTAL, "deaths_total", "top5")
    output( countries, days, dir+OUT_TOP5_CONFIRMED_TOTAL_GROW_PERCENT, "confirmed_total_grow_percent", "top5")
    output( countries, days, dir+OUT_TOP5_DEATHS_TOTAL_GROW_PERCENT, "deaths_total_grow_percent", "top5")
    output( countries, days, dir+OUT_TOP5_CONFIRMED_BY_POPULATION, "confirmed_by_population", "top5")
    output( countries, days, dir+OUT_TOP5_DEATHS_BY_POPULATION, "deaths_by_population", "top5")
    output( countries, days, dir+OUT_TOP5_CONFIRMED_BY_POPULATION_GROW_PERCENT, "confirmed_by_population_grow_percent", "top5")
    output( countries, days, dir+OUT_TOP5_DEATHS_BY_POPULATION_GROW_PERCENT, "deaths_by_population_grow_percent", "top5")
    
    output_single( countries, days, dir+OUT_AUSTRIA, "Austria") 
    
main();
