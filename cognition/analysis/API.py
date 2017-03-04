import http.client
from urllib import request, parse, error
import base64
import sys
import json
KEY = "50e5f02a03a84854ba1a036cfd370cb2"
URL = "westus.api.cognitive.microsoft.com"
GROUP_ID = "thisisatestid"


def createGroup(gid=GROUP_ID):
    headers = {
        # Request headers
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': KEY,
    }
    params = parse.urlencode({
    })
    body = {
        "name": "group1",
        "userData": ""
    }
    url = "/face/v1.0/persongroups/{}?{}".format(gid, params)
    algorithm("PUT", url, json.dumps(body), headers)


def detectFace(file):
    headers = {
        # Request headers
        'Content-Type': 'application/octet-stream',
        'Ocp-Apim-Subscription-Key': KEY,
    }

    params = parse.urlencode({
        # Request parameters
        'returnFaceId': 'true',
        'returnFaceLandmarks': 'false',
    })
    body = file.read()
    url = "/face/v1.0/detect?{}".format(params)
    return algorithm("POST", url, body, headers)["faceId"]


def createPerson(name, gid=GROUP_ID):
    headers = {
        # Request headers
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': KEY,
    }

    params = parse.urlencode({
    })
    body = {
        "name": name,
        "userData": "",
    }
    url = "/face/v1.0/persongroups/{}/persons?{}".format(gid, params)
    return algorithm("POST", url, json.dumps(body), headers)["personId"]


def addPersonFace(pid, file, gid=GROUP_ID):
    headers = {
        # Request headers
        'Content-Type': 'application/octet-stream',
        'Ocp-Apim-Subscription-Key': KEY,
    }

    params = parse.urlencode({
        # Request parameters
        'userData': "",
        'targetFace': "",
    })
    body = file.read()
    url = "/face/v1.0/persongroups/{}/persons/{}/persistedFaces?{}".format(
        gid, pid, params
    )
    algorithm("POST", url, body, headers)


def verify(fid, pid, gid=GROUP_ID):
    headers = {
        # Request headers
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': KEY,
    }

    params = parse.urlencode({
    })
    body = {
        "faceId": fid,
        "personId": pid,
        "personGroupId": gid
    }
    url = "/face/v1.0/verify/?{}".format(params)
    return algorithm("POST", url, json.dumps(body), headers)["isIdentical"]


def algorithm(method, url, body, headers):
    repeat = 0
    while repeat != 3:
        try:
            conn = http.client.HTTPSConnection(URL)
            conn.request(method, url, body, headers)
            response = conn.getresponse()
            data = response.read()
            print(data)
            if "error" in data:
                repeat += 1
            else:
                return data
            finally:
                conn.close()
        except Exception as e:
            print(e)


def main(argv):
    if argv[1] == "createGroup":
        createGroup()
    elif argv[1] == "createUser":
        createPerson(argv[2])
    elif argv[1] == "detect":
        f = open(argv[2], "rb")
        detectFace(f)
    elif argv[1] == "addFace":
        f = open(argv[3], "rb")
        addPersonFace(argv[2], f)
    elif argv[1] == "verify":
        verify(argv[2], argv[3])


if __name__ == "__main__":
    main(sys.argv)