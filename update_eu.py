#! /usr/bin/env python3

import requests

query = """
SELECT ?country ?countryLabel WHERE {
  ?country wdt:P463 wd:Q458.
  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
}
"""

url = 'https://query.wikidata.org/sparql'
data = requests.get(url, headers={'Accept': 'application/json'}, params={'query': query, 'format': 'json'}).json()

countries = [result['countryLabel']['value'] for result in data['results']['bindings']]
# align the country names with those used in the GSoC list
countries = [c.replace("Kingdom of the ", "").replace("Republic of ", "") for c in countries]

for country in countries:
    print(country)
