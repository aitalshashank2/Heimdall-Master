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


def locate(ip):

    r = requests.get(url=f"http://ip-api.com/json/{ip}", timeout=1)
    r = r.json()
    if r["status"] == "success":
        location = f"Latitude: {r.get('lat')}, Longitude: {r.get('lon')}\n{r.get('city')}, {r.get('regionName')}, {r.get('country')}"

        return {
            "title": "location",
            "value": location,
            "short": False
        }
    else:
        return {}


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
                try:
                    client = Log.objects.filter(ip=data["ip"], port=data["port"], activity="LOGIN_SSH_KEY").last().client
                except Log.DoesNotExist:
                    client = "Unidentified"

            log = Log(time=d, host=data["host"], user=data["user"], ip=data.get("ip"), port=data.get("port"), activity=data["activity"], client=client)
            log.save()

            headers = {
                'content-type': 'application/json',
            }
            payload = {
                'text': "Activity Detected"
            }
            
            if data["activity"] == "LOGIN_SSH_PWD":

                location = locate(data['ip'])

                payload = {
                    "color": "good",
                    "fields": [
                        {
                            "title": "Action",
                            "value": "SSH Login with password",
                            "short": False
                        },
                        {
                            "title": "Host User",
                            "value": data["user"],
                            "short": False
                        },
                        {
                            "title": "Server",
                            "value": data["host"],
                            "short": False
                        },
                        location
                    ]
                }

            elif data["activity"] == "LOGIN_SSH_KEY":

                location = locate(data['ip'])

                payload = {
                    "color": "good",
                    "fields": [
                        {
                            "title": "Action",
                            "value": "SSH Login with Key",
                            "short": False
                        },
                        {
                            "title": "User",
                            "value": data['client'],
                            "short": False
                        },
                        {
                            "title": "Host User",
                            "value": data["user"],
                            "short": False
                        },
                        {
                            "title": "Server",
                            "value": data["host"],
                            "short": False
                        },
                        location
                    ]
                }

            elif data["activity"] == "LOGOUT_SSH":

                location = locate(data['ip'])

                payload = {
                    "color": "warning",
                    "fields": [
                        {
                            "title": "Action",
                            "value": "SSH Logout",
                            "short": False
                        },
                        {
                            "title": "User",
                            "value": client,
                            "short": False
                        },
                        {
                            "title": "Host User",
                            "value": data["user"],
                            "short": False
                        },
                        {
                            "title": "Server",
                            "value": data["host"],
                            "short": False
                        },
                        location
                    ]
                }

            elif data["activity"] == "CHUSR_OPEN":

                payload = {
                    "color": "danger",
                    "fields": [
                        {
                            "title": "Action",
                            "value": "Opened Superuser Session",
                            "short": False
                        },
                        {
                            "title": "Host User",
                            "value": data["client"],
                            "short": False
                        },
                        {
                            "title": "Server",
                            "value": data["host"],
                            "short": False
                        }
                    ]
                }

            elif data["activity"] == "CHUSR_CLOSE":

                payload = {
                    "color": "danger",
                    "fields": [
                        {
                            "title": "Action",
                            "value": "Closed Superuser Session",
                            "short": False
                        },
                        {
                            "title": "Server",
                            "value": data["host"],
                            "short": False
                        }
                    ]
                }


            x = requests.post(SLACK, json=payload, headers=headers)

            return HttpResponse("Logged")
        else:
            return HttpResponseForbidden("Invalid Bipolar Signature")

    else:
        return HttpResponseBadRequest("Only POST request allowed")