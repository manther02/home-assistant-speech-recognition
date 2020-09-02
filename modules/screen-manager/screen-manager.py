import sys, os, traceback, time, importlib, json, re
from subprocess import PIPE, Popen

def exec(command):
    process = Popen(
        args=command,
        stdout=PIPE,
        shell=True
    )

    result = str(process.communicate()[0]).lower().strip()

    return result

class ScreenManager:
    name = ''

    def __init__(self, name):
        self.name = self.treatName(name)
        self.new()

    def checkIfExist(self):
        result = exec("screen -S " + self.name + " -X stuff \"\n\"")

        if re.search('no screen session', result):
            return False

        return True

    def new(self):
        if not(self.checkIfExist()):
            exec("screen -dmS " + self.name)

    def command(self, command):
        exec("screen -S " + self.name + " -X stuff \"" + command + "\"")

    def delete(self):
        exec("screen -XS " + self.name + " quit")

    def treatName(self, name):
        return 's-' + name + '-e'