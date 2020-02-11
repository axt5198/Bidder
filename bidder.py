#!/usr/bin/python3.6

# import modules used here -- sys is a very standard one
import sys
import os
import requests
import csv
import json
import pandas as pd
import numpy as np

COLUMNS = ['Email','Card Type','Card Number','Card Expiry','CVV','Country','Phone Number','First Name','Last Name','Address 1','Address 2','Zip Code','City','State']
# Gather our code in a main() function
def main():
  proxiesFile = 'proxies.txt'
  accountsFile = 'profiles.csv'

  # #proxies = readProxies(proxiesFile)
  accounts = registerAccounts(accountsFile)

  # print(json.dumps(accounts, indent=4))

  # registered = registerAccounts(accounts)

  #login
  # login()

def registerAccounts(profilesFile):
  if not os.path.isfile(profilesFile):
    print(f"File does not exist. {profilesFile} Exiting.")
    sys.exit()

  # profiles = []

  profiles = pd.read_csv(profilesFile)

  for index, profile in profiles.iterrows():
    email = profile['Email']

    if isRegistered(profile):
      print(f'{email} is already registered')
      continue

    else:
      print(f'registering {email}')
      first = profile['First Name']
      last = profile['Last Name']
      if(signup(email, first, last)):
        markRegistered(profile) 
  return profiles

def isRegistered(profile):
  registered = pd.read_csv('registered.csv')

  if registered['Email'].str.contains(profile[0], regex=False).any():
    return True
  else:
    return False

def signup(email, first, last):
  headers = {'accept': '*/*', 'origin': 'https://accounts.stockx.com', 'content-type': 'application/json'}
  success = False

  body = {
    "connection": "production",
    "email": email,
    "password": "cookieSnores1",
    "user_metadata": {
        "first_name": first,
        "last_name": last,
        "language": "en-us",
        "gdpr": ""
    }
  }
  print(json.dumps(headers, indent=4))
  print(json.dumps(body,indent=4))
    
  r = requests.post('https://accounts.stockx.com/dbconnections/signup', headers=headers, json=body)
  print(r.text)
  if(r.status_code == 200):
    print(f'Account {email} was successfully registered.')
    success = True
    
  print(f'headers: {r.headers}')
  print(f'cookies: {r.cookies}')

  return success

def markRegistered(profile):
  df = pd.DataFrame(columns=COLUMNS)
  account = df.append(profile).set_index('Email')
  account.to_csv('registered.csv', mode='a', header=False)

# def login():

  #   url = "https://gateway.stockx.com/stage/v1/login"

  #   payload = {
  #     'email': 'noctuafinancial+2@gmail.com',
  #     'password': 'snoringCooki1'
  #   }"{\n\t\"email\": \"{{email}}\",\n\t\"password\": \"{{password}}\"\n}"
  #   headers = {
  #   'Accept': 'application/json',
  #   'Content-Type': 'application/json',
  #   }

  #   response = requests.post(url, headers=headers, json = payload)

  #   print(response.text.encode('utf8'))


def readProxies(proxiesFile):
  if not os.path.isfile(proxiesFile):
    print(f"File does not exist. {proxiesFile} Exiting.")
    sys.exit()

  proxies = {}

  with open(proxiesFile) as fp:
    registered = 0
    incoming = 0
    for line in fp:
      incoming+=1
      info = line.split(':')
      if(len(info) != 4):
        print(f'Poorly formmatted proxy at line {incoming}')
        continue
      
      ipAddr = info[0]
      port = info[1]
      username = info[2]
      pw = info[3]
      # print(f'IP Address: {ipAddr}')
      # print(f'Port: {port}')
      # print(f'Username: {username}')
      # print(f'Pw: {pw}')

      url = f"http://{username}:{pw}@{ipAddr}:{port}"

      key = ipAddr+":"+port

      if key in proxies:
        print(f'{url} already registered')
        continue

      proxies[url] = {'http': ipAddr, 'port': port, 'username': username, 'pw': pw,}
      registered+=1 

    print(f'{registered} / {incoming} proxies registered')

    return proxies
      



# Standard boilerplate to call the main() function to begin
# the program.
if __name__ == '__main__':
  main()
