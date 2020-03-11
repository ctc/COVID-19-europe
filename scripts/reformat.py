#!/usr/bin/python3

import csv
import numpy as np
from datetime import datetime
import sys


IN_CONFIRMED= "/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv"
IN_RECOVERED = "/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Recovered.csv"
IN_DEATHS = "/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Deaths.csv"

OUT_CONFIRMED_TOTAL = "/total_confirmed.csv"
OUT_RECOVERED_TOTAL = "/total_recovered.csv"
OUT_DEATHS_TOTAL = "/total_deaths.csv"

OUT_CONFIRMED_POPULATION = "/by_population_confirmed.csv"
OUT_RECOVERED_POPULATION = "/by_population_recovered.csv"
OUT_DEATHS_POPULATION = "/by_population_deaths.csv"

OUT_AUSTRIA = "/austria.csv"

# https://en.wikipedia.org/wiki/List_of_European_countries_by_population
countries_template = {
    "Russia": { "population": 146877088},
    "Germany": { "population": 82887000},
    "Turkey": { "population": 82003882},
    "France": { "population": 67372000},
    "UK": { "population": 66435550},
    "Italy": { "population": 60390560},
    "Spain": { "population": 46733038},
    "Poland": { "population": 38433600},
    "Ukraine": { "population": 37289000},
    "Romania": { "population": 19523621},
    "Kazakhstan": { "population": 18356900},
    "Netherlands": { "population": 17417600},
    "Belgium": { "population": 11449656},
    "Greece": { "population": 10768193},
    "Czech Republic": { "population": 10627794},
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


def extract( countries, data_in, type):

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
            dates_total = {}
            dates_by_population = {}
            for x in range( 4, len(country)):
                try:
                    dates_total[headers[x]] = int(country[x])
                    dates_by_population[headers[x]] = float(country[x]) / float(countries[country[1]]["population"]) * 100000
                except Exception as e:
                    dates_total[headers[x]] = ""
                    dates_by_population[headers[x]] = ""
            countries[country[1]][type+"_total"] = dates_total
            if( countries[country[1]]["population"] >= 100000): # filter out countries < 100.000 people
                countries[country[1]][type+"_by_population"] = dates_by_population
            

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
                "confirmed_by_population", "recovered_by_population", "deaths_by_population"]
        
        writer.writerow(header)
        
        for day in days:
            row = [day]
            
            for x in range( 1, len(header)):
                row.append( countries[country][header[x]][day])
            
            writer.writerow(row)


def main():
    dir = sys.argv[1]

    countries, days = extract( countries_template, dir+IN_CONFIRMED, "confirmed")
    countries, days = extract( countries, dir+IN_RECOVERED, "recovered")
    countries, days = extract( countries, dir+IN_DEATHS, "deaths")
    
    output( countries, days, dir+OUT_CONFIRMED_TOTAL, "confirmed_total")
    output( countries, days, dir+OUT_RECOVERED_TOTAL, "recovered_total")
    output( countries, days, dir+OUT_DEATHS_TOTAL, "deaths_total")

    output( countries, days, dir+OUT_CONFIRMED_POPULATION, "confirmed_by_population")
    output( countries, days, dir+OUT_RECOVERED_POPULATION, "recovered_by_population")
    output( countries, days, dir+OUT_DEATHS_POPULATION, "deaths_by_population")
    
    output_single( countries, days, dir+OUT_AUSTRIA, "Austria") 
    
main();
