import io
import yaml
import json
import datetime
import pytz
import hmac
import hashlib
import requests

from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone

from bipolar.models import Log

CONFIG = "../configuration/config.yml"

with io.open(CONFIG, 'r') as stream:
    CONFIG_VARS = yaml.safe_load(stream)

SERVERSIDE_SECRET = CONFIG_VARS['SERVERSIDE']['SECRET']
SLACK = CONFIG_VARS['SLACK']


@csrf_exempt
def log(request):

    signature = 'sha1=' + hmac.new(SERVERSIDE_SECRET.encode(), request.body, hashlib.sha1).hexdigest()

    if(request.method == "POST"):

        XBIPOLARSIGNATURE = request.headers.get("X-Bipolar-Signature")

        if(signature == XBIPOLARSIGNATURE and all([signature, XBIPOLARSIGNATURE])):
            data = json.loads(request.body)
            m = datetime.datetime.strptime(data["month"], "%b").month
            t = data["time"].split(':')
            d = datetime.datetime(timezone.now().year, m, int(data["date"]), int(t[0]), int(t[1]), int(t[2]))

            client = data.get("client")

            if data["activity"] == "LOGOUT_SSH":
                client = Log.objects.get(ip=data["ip"], port=data["port"], activity="LOGIN_SSH_KEY").client

            log = Log(time=d, host=data["host"], user=data["user"], ip=data["ip"], port=data["port"], activity=data["activity"], client=client)
            log.save()

            headers = {
                'content-type': 'application/json',
            }
            payload = {
                'text': "Activity Detected"
            }

            if data["activity"] == "LOGIN_SSH_PWD":
                payload = {
                    "text": f"Someone logged into {data['user']}@{data['host']} by using password."
                }
            elif data["activity"] == "LOGIN_SSH_KEY":
                payload = {
                    "text": f"{data['client']} logged into {data['user']}@{data['host']} using SSH Key."
                }
            elif data["activity"] == "LOGOUT_SSH":
                payload = {
                    "text": f"{client} logged off from {data['user']}@{data['host']}"
                }

            requests.post(SLACK, json=payload, headers=headers)

            return HttpResponse("Logged")
        else:
            return HttpResponseForbidden("Invalid Bipolar Signature")

    else:
        return HttpResponseBadRequest("Only POST request allowed")