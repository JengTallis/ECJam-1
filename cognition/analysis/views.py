from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from threading import Thread
import urllib.request
import requests
from .models import Record
from django.views.decorators.csrf import csrf_exempt
from threading import Thread
from queue import Queue
from concurrent.futures import ThreadPoolExecutor
# Create your views here.


URL = "https://westus.api.cognitive.microsoft.com/emotion/v1.0/recognize"
KEY = "04578e189b6f45c0842acf276495e256"
executor = ThreadPoolExecutor()


def process(file):
    header = dict()
    header["Ocp-Apim-Subscription-Key"] = KEY
    header["Content-Type"] = "application/octet-stream"
    result = None
    response = requests.request("post", URL, json=None, params=None,
                                data=file, headers=header)
    code = response.status_code
    if code == 429:
        print("Message: {}".format(response.json()['error']['message']))
    elif code == 200 or code == 201:
        if 'content-length' in response.headers and\
           int(response.headers['content-length']) == 0:
            result = None
        elif 'content-type' in response.headers and\
             isinstance(response.headers['content-type'], str):
            if 'application/json' in response.headers['content-type'].lower():
                result = response.json() if response.content else None
            elif 'image' in response.headers['content-type'].lower():
                result = response.content
            else:
                print("Error code: {}".format(code))
                print("Message: {}".format(
                      response.json()['error']['message']))
    return result


def worker(data):
    result = process(data)
    if result:
        value = compute(result)
        print(value)
        r = Record()
        r.value = value
        r.save()


def compute(value):
    for face in value:
        scores = face["scores"]
        break
    result = sum(sum(face["scores"].values()) for face in value)
    return result


@csrf_exempt
def submitPicture(request):
    if request.method == "POST":
        file = request.FILES["file"]
        data = file.read()
        executor.submit(worker, data)
        return HttpResponse(200)


def viewHistory(request):
    records = Record.getAllRecords()
    return JsonResponse({"records": records})
