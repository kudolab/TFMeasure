import json
import sys

import requests
from requests.exceptions import Timeout

BASE_ORIGIN = "http://172.24.176.169"


def is_healthy():
    print("health check", file=sys.stderr)
    url = BASE_ORIGIN+"/health"
    try:
        response = requests.get(url, timeout=5.0)
    except Timeout:
        print("requet timeout", file=sys.stderr)
        return False
    return response.status_code == requests.codes.OK


def put_speaker_num(speaker_num: int):
    print("put_speaker_num", file=sys.stderr)
    URL = BASE_ORIGIN+"/speaker"
    speaker_data = {
        "speaker_num": speaker_num
    }

    headers = {"Content-Type": "application/json"}
    speaker_json = json.dumps(speaker_data).encode("utf-8")

    try:
        response = requests.put(URL, data=speaker_json, headers=headers, timeout=5.0)
    except Timeout:
        print("requet timeout", file=sys.stderr)
        return
    response.raise_for_status()
    responce_data = response.json()
    print(responce_data, file=sys.stderr)
