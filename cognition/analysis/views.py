from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from threading import Thread
import urllib.request
import requests
from .models import Record, User, Attendance
from django.views.decorators.csrf import csrf_exempt
from threading import Thread
from queue import Queue
from concurrent.futures import ThreadPoolExecutor
from .API import addPersonFace, verify, createPerson, detectFace
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


def takeAttendance(files):
    attendance = Attendance()
    attendance.completed = False
    attendance.save()
    users = User.getAllUsers()
    for f in files:
        fid = detectFace(f)
        for u in users:
            if not attendance.hasTaken(users[u]):
                if verify(fid, u):
                    attendance.addStudent(users[u])
                    break
    attendance.complete()


@csrf_exempt
def submitPicture(request):
    if request.method == "POST":
        file = request.FILES["file"]
        data = file.read()
        executor.submit(worker, data)
        return HttpResponse(200)


def viewHistory(request):
    if request.method == "POST":
        records = Record.getAllRecords()
        return JsonResponse({"records": records})
    else:
        return render(request, "analysis/index.html")


@csrf_exempt
def submitAttendance(request):
    if request.method == "POST":
        number = int(request.POST.get("size"))
        files = []
        for i in range(number):
            files.append(request.FILES["file{}".format(i)])
        executor.submit(takeAttendance, files)
        return HttpResponse(200)


@csrf_exempt
def addUser(request):
    if request.method == "POST":
        userName = request.POST.get("name")
        face = request.FILES["face"]
        ID = createPerson(userName)
        print("user created")
        temp = User()
        temp.ID = ID
        temp.save()
        addPersonFace(ID, face)
        print("user face added")
        return HttpResponse(200)
    else:
        return render(request, "analysis/index.html")


def viewAttendance(request):
    if request.method == "GET":
        return render(request, "viewAttendance.html",
                      {"attendances": Attendance.getAllAttendances()})
    else:
        time = request.POST.get("time")
        a = Attendance.getByTimestamp(time)
        if a.hasCompleted():
            taken = a.getTakenStudents()
            untaken = a.getUntakenStudents()
            return JsonResponse({"completed": True, "taken": taken,
                                 "untaken": untaken})
        else:
            return JsonResponse({"completed": False})
