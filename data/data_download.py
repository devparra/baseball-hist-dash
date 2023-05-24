# M.Parra 5-23-23
# This script is only used to retrieve the neccesarry database from WebucatorTraining
# This file will eventually be used to download and update with the latest data from Sean Lahman

# imported the requests library
import requests


# Download URL of database
download_url = "https://github.com/WebucatorTraining/lahman-baseball-mysql/raw/master/lahmansbaseballdb.sqlite"

# URL of the SQLite Database to be downloaded is defined as download_url
# create HTTP response object
response = requests.get(download_url)
  
# send a HTTP request to the server and save
# the HTTP response in a response object called r
with open("lahmansbaseballdb.sqlite",'wb') as file:
    # write the contents of the response
    # to a new file in binary mode
    file.write(response.content)