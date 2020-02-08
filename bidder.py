#!/usr/bin/python3.6

# import modules used here -- sys is a very standard one
import sys
import os
import requests

# Gather our code in a main() function
def main():
  proxiesFile = 'proxies.txt'

  proxies = readProxies(proxiesFile)


  
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
