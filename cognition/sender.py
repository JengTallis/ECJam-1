from sys import argv
import requests


url = "http://localhost:8000/post"
files = {"file": open(argv[1], "rb")}
response = requests.post(url, files=files)
print(response)