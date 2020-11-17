import io
import os
import yaml
import subprocess
import hmac
import hashlib
import json
import requests

from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt

CONFIG = "configuration/config.yml"

# View to update the local ssh keys repository
@csrf_exempt
def gh_listener(request):
    if request.method == 'POST':
        
        with io.open(CONFIG, 'r') as stream:
            try:
                CONFIG_VARS = yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                print(exc)
                raise
        
        repo = CONFIG_VARS["GITHUB"]["REPOSITORY"]
        secret = CONFIG_VARS["GITHUB"]["SECRET"]
        token = CONFIG_VARS["GITHUB"]["OAUTHTOKEN"]

        encoded_secret = secret.encode()
        signature = 'sha1=' + hmac.new(encoded_secret, request.body, hashlib.sha1).hexdigest()
        
        if signature == request.headers['X-Hub-Signature']:

            pull = subprocess.Popen(["git", "pull", "origin", "master"], cwd=repo)
            output, error = pull.communicate()

            servers = os.listdir(repo+"servers/")

            with io.open(repo+"server-mappings.yml", "r") as stream:
                try:
                    server_mappings = yaml.safe_load(stream)
                except yaml.YAMLError as exc:
                    print(exc)
                    raise
            
            for server in servers:
                dest = server_mappings['servers'][server]
                keys = ""

                auth_users = open(repo+"servers/"+server, 'r')
                for user in auth_users:
                    try:
                        keys += open(repo+"public-keys/"+user.rstrip(), 'r').read()
                    except FileNotFoundError:
                        print(f"The public key for the user {user} does not exist. Couldn't add to {server}.")
                    except IsADirectoryError:
                        pass

                payload_keys = {'authorized_keys': keys}
                try:
                    r = requests.post(dest, json=payload_keys)
                    print("[SUCCESS]")
                except Exception as e:
                    print(f"[FAILURE] {e}")

            return HttpResponse("OK")

        else:
            return HttpResponseBadRequest("Signatures do not match.")

    else:
        return HttpResponseBadRequest("Only POST method allowed.")
