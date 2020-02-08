#!/usr/bin/python3.6

# import modules used here -- sys is a very standard one
import sys
import os
import requests
import csv
import json

# Gather our code in a main() function
def main():
  proxiesFile = 'proxies.txt'
  accountsFile = 'profiles.csv'

  proxies = readProxies(proxiesFile)
  accounts = readAccounts(accountsFile)

  print(json.dumps(accounts, indent=4))

  # registered = registerAccounts(accounts)



def readAccounts(accountsFile):
  if not os.path.isfile(accountsFile):
    print(f"File does not exist. {accountsFile} Exiting.")
    sys.exit()

  accounts = []

  with open(accountsFile) as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
      accounts.append(row)

  return accounts



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
