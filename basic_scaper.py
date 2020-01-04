import requests

import pandas as pd
from bs4 import BeautifulSoup


# scrape listing page
doctors = [] 
page_number = 1
base_url = 'https://www.doctolib.fr/radiologue/paris'
page = requests.get(base_url)
while page.status_code == 200:
    soup = BeautifulSoup(page.text, 'html.parser')
    elements = soup.find_all('div', {'class': 'dl-search-result'})
    for elt in elements:
        doctor = {} 
        doctor['title'] = elt.find('a', {'class': 'dl-search-result-name js-search-result-path'}).text
        doctor['subtitle'] = elt.find('div', {'class': 'dl-search-result-subtitle'}).text.replace('\n', '')
        doctor['address'] = elt.find('div', {'class': 'dl-text dl-text-body'}).text
        doctor['latitude'] = elt['data-lat']
        doctor['longitude'] = elt['data-lng']
        if elt.find('div', {'class': 'dl-search-result-specialities'}) is not None:
            doctor['n_doctors'] = elt.find('div', {'class': 'dl-search-result-specialities'}).text
        else:
            doctor['n_doctors'] = ''
        if elt.find('div', {'class': 'dl-search-result-regulation-sector dl-text-body'}) is not None:
            doctor['sector'] = elt.find('div', {'class': 'dl-search-result-regulation-sector dl-text-body'}).text
        else:
            doctor['sector'] = '' 
        doctors.append(doctor)
    print(f'{len(doctors)} doctors already scraped !')
    if len(elements) < 10: 
        break
    page_number += 1 
    url = f'{base_url}/?page={page_number}'
    page = requests.get(url)
doctors_df = pd.DataFrame(doctors)
doctors_df.to_csv('radiologues.csv', index=False, sep=';')
