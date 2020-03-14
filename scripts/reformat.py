#!/usr/bin/python3

import csv
import numpy as np
from datetime import datetime
import sys


IN_CONFIRMED= "/COVID-19/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv"
IN_RECOVERED = "/COVID-19/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Recovered.csv"
IN_DEATHS = "/COVID-19/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Deaths.csv"

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




OUT_AUSTRIA = "/austria.csv"

# https://en.wikipedia.org/wiki/List_of_European_countries_by_population
countries_template = {
    "Russia": { "population": 146877088},
    "Germany": { "population": 82887000},
    "Turkey": { "population": 82003882},
    "France": { "population": 67372000},
    "United Kingdom": { "population": 66435550},
    "Italy": { "population": 60390560},
    "Spain": { "population": 46733038},
    "Poland": { "population": 38433600},
    "Ukraine": { "population": 37289000},
    "Romania": { "population": 19523621},
    "Kazakhstan": { "population": 18356900},
    "Netherlands": { "population": 17417600},
    "Belgium": { "population": 11449656},
    "Greece": { "population": 10768193},
    "Czechia": { "population": 10627794},
    "Sweden": { "population": 10319601},
    "Portugal": { "population": 10276617},
    "Azerbaijan": { "population": 10000000},
    "Hungary": { "population": 9771000},
    "Belarus": { "population": 9477100},
    "Austria": { "population": 8857960},
    "Switzerland": { "population": 8526932},
    "Bulgaria": { "population": 7000039},
    "Serbia": { "population": 6963764},
    "Denmark": { "population": 5806015},
    "Finland": { "population": 5522015},
    "Slovakia": { "population": 5445087},
    "Norway": { "population": 5323933},
    "Ireland": { "population": 4921500},
    "Croatia": { "population": 4105493},
    "Georgia": { "population": 3729600},
    "Bosnia and Herzegovina": { "population": 3511372},
    "Armenia": { "population": 2969200},
    "Albania": { "population": 2870324},
    "Lithuania": { "population": 2791903},
    "Moldova": { "population": 2681735},
    "North Macedonia": { "population": 2075301},
    "Slovenia": { "population": 2070050},
    "Latvia": { "population": 1921300},
    "Kosovo": { "population": 1798506},
    "Estonia": { "population": 1319133},
    "Cyprus": { "population": 8642},
    "Montenegro": { "population": 622359},
    "Luxembourg": { "population": 602005},
    "Malta": { "population": 475701},
    "Iceland": { "population": 35562},
    "Jersey": { "population": 1055},
    "Isle of Man": { "population": 83314},
    "Andorra": { "population": 74794},
    "Guernsey": { "population": 62063},
    "Faroe Islands": { "population": 51237},
    "Monaco": { "population": 383},
    "Liechtenstein": { "population": 38201},
    "Gibraltar": { "population": 33573},
    "San Marino": { "population": 33407},
    "Åland Islands": { "population": 29489},
    "Vatican City": { "population": 799}
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


    for country in data:
        if( country[1] in countries):
            if( country[1] == country[0] or country[0] == ""):
                dates_total = {}
                dates_total_grow_percent = {}
                dates_by_population = {}
                dates_by_population_grow_percent = {}
                
                last_data = 0
                last_data_by_population = 0
                last_grow_percent = 0
                last_grow_percent_by_population = 0
                for x in range( 4, len(country)):
                    if( country[1] in fixes and type in fixes[country[1]] and headers[x] in fixes[country[1]][type]):
                        value = fixes[country[1]][type][headers[x]]
                        print( "fixed: %s %s %s %s -> %s" % ( country[1], type, headers[x], country[x], value ))
                    else:
                        value = country[x]
            
                    try:
                        dates_total[headers[x]] = int(value)
                        dates_by_population[headers[x]] = float(value) / float(countries[country[1]]["population"]) * 100000
                    except Exception as e:
                        dates_total[headers[x]] = ""
                        dates_by_population[headers[x]] = ""
                    
                    if( dates_total[headers[x]] != ""):
                        if( last_data != 0):
                            dates_total_grow_percent[headers[x]] = (dates_total[headers[x]] - last_data) / last_data * 100
                            last_grow_percent = dates_total_grow_percent[headers[x]]
                            
                            dates_by_population_grow_percent[headers[x]] = (dates_by_population[headers[x]] - last_data_by_population) / last_data_by_population * 100
                            last_grow_percent_by_population = dates_by_population_grow_percent[headers[x]]
                        else:
                            dates_total_grow_percent[headers[x]] = 0
                            last_grow_percent = 0
                            
                            dates_by_population_grow_percent[headers[x]] = 0
                            last_grow_percent_by_population = 0
                        last_data = dates_total[headers[x]]
                        last_data_by_population = dates_by_population[headers[x]]
                    else:
                        dates_total_grow_percent[headers[x]] = last_grow_percent
                        dates_by_population_grow_percent[headers[x]] = last_grow_percent_by_population
                
                
                countries[country[1]][type+"_total"] = dates_total
                countries[country[1]][type+"_total_grow_percent"] = dates_total_grow_percent
                if( countries[country[1]]["population"] >= 100000): # filter out countries < 100.000 people
                    countries[country[1]][type+"_by_population"] = dates_by_population
                    countries[country[1]][type+"_by_population_grow_percent"] = dates_by_population_grow_percent
            

    return countries, days

def output( countries, days, data_out, type):
    
    f = open( data_out, 'w')
    with f:
        writer = csv.writer(f)
        header = ["country"]
        for country in countries:
            if( type in countries[country]):
                header.append( country)
        
        writer.writerow(header)
        
        for day in days:
            row = [day]
            
            for x in range( 1, len(header)):
                row.append( countries[header[x]][type][day])
            
            writer.writerow(row)
        

def output_single( countries, days, data_out, country):
    
    f = open( data_out, 'w')
    with f:
        writer = csv.writer(f)
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


def main():
    dir = sys.argv[1]

    fixes = extract_fixes( {}, confirmed_fixes_dict, "confirmed")
    fixes = extract_fixes( fixes, recovered_fixes_dict, "recovered")
    fixes = extract_fixes( fixes, deaths_fixes_dict, "deaths")

    countries, days = extract( countries_template, fixes, dir+IN_CONFIRMED, "confirmed")
    countries, days = extract( countries, fixes, dir+IN_RECOVERED, "recovered")
    countries, days = extract( countries, fixes, dir+IN_DEATHS, "deaths")

    output( countries, days, dir+OUT_CONFIRMED_TOTAL, "confirmed_total")
    output( countries, days, dir+OUT_RECOVERED_TOTAL, "recovered_total")
    output( countries, days, dir+OUT_DEATHS_TOTAL, "deaths_total")

    output( countries, days, dir+OUT_CONFIRMED_TOTAL_GROW_PERCENT, "confirmed_total_grow_percent")
    output( countries, days, dir+OUT_RECOVERED_TOTAL_GROW_PERCENT, "recovered_total_grow_percent")
    output( countries, days, dir+OUT_DEATHS_TOTAL_GROW_PERCENT, "deaths_total_grow_percent")

    output( countries, days, dir+OUT_CONFIRMED_BY_POPULATION, "confirmed_by_population")
    output( countries, days, dir+OUT_RECOVERED_BY_POPULATION, "recovered_by_population")
    output( countries, days, dir+OUT_DEATHS_BY_POPULATION, "deaths_by_population")
    
    output( countries, days, dir+OUT_CONFIRMED_BY_POPULATION_GROW_PERCENT, "confirmed_by_population_grow_percent")
    output( countries, days, dir+OUT_RECOVERED_BY_POPULATION_GROW_PERCENT, "recovered_by_population_grow_percent")
    output( countries, days, dir+OUT_DEATHS_BY_POPULATION_GROW_PERCENT, "deaths_by_population_grow_percent")
    
    output_single( countries, days, dir+OUT_AUSTRIA, "Austria") 
    
main();
