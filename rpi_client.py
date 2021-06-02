import json
import sys

import requests

BASE_ORIGIN = "http://172.24.176.169"


def is_healthy():
    url = "/health"
    response = requests.get(url)
    return response.status_code == requests.codes.OK


def put_speaker_num(speaker_num: int):
    URL = "http://172.24.176.51/speaker"
    speaker_data = {
        "speaker_num": speaker_num
    }

    headers = {"Content-Type": "application/json"}
    speaker_json = json.dumps(speaker_data).encode("utf-8")

    response = requests.put(URL, data=speaker_json, headers=headers)
    response.raise_for_status()
    responce_data = response.json()
    print(responce_data, file=sys.stderr)
