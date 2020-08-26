import os
import os
import string
import sys
import yaml
import pyping
import web
import psutil
import json
import pprint
from pathlib import Path
from __future__ import absolute_import
from flask import Flask
from healthcheck import HealthCheck

PORT = 8000
app = Flask(__name__)


@app.route("/")
def hello_world():
    return 'Hello!'

# wrap the flask app and give a heathcheck url
health = HealthCheck(app, "/healthz")

global configfile
configfile = './config.yaml'
configuration = None


class WebConfig():
    def GET(self):
        try:
            file = open(configfile, 'r')
            yamlconfig = yaml.safe_load(file)
            configuration = yaml.safe_dump(
                yamlconfig, default_flow_style=False, canonical=False)
            formatHelper = FormatHelper()
        except:
            e = sys.exc_info()[0]
            print e
            configuration = e

        return formatHelper.prettify(configuration)


class FormatHelper:
    def prettify(self, data):
        return pprint.pformat(data, indent=4, width=80)


class Config:
    def __init__(self):
        self.configuration = None

    def create(self, configfile):
        file = open(configfile, 'r')
        self.configuration = yaml.safe_load(file)
        return self.configuration



class healthz:
    def GET(self):
        try:
            configuration = Config().create(configfile)
            formatHelper = FormatHelper()
            x = 0
            error = 0
            data = {}
            for key, value in configuration.items():
                 if key == "status":
                    if type(value) is list:
                        tmpdict = {}
                        for v in value:
                            tmpdict1 = {}
                            x = x + 1
                            pypi = pyping.ping(v)
                            if pypi.ret_code != 0:
                                tmpdict1[v] = "Failed"
                                tmpdict[x] = tmpdict1
                                data[key] = tmpdict
                                error = error + 1
                            else:
                                tmpdict1[v] = "OK"
                                tmpdict[x] = tmpdict1
                                data[key] = tmpdict
                    else:
                        tmpdict = {}
                        pypi = pyping.ping(value)
                        if pypi.ret_code != 0:
                            tmpdict1[value] = "Failed"
                            data[key] = tmpdict1
                            error = error + 1
                        else:
                            tmpdict1[value] = "OK"
                            data[key] = tmpdict1
                       


health.add_check(healthz)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=PORT)

