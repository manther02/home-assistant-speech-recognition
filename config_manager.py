import sys, os, traceback, time, importlib, json, re

class ConfigManager:
    obj = {}
    file = ''

    def __init__(self):
        self.file = os.path.abspath('config.json')
        self.load()

    def load(self):
        if os.path.exists(self.file):
            fp = open(self.file, "r")
            content = fp.read()
            fp.close()
            self.obj = json.loads(content)

    def backup(self, obj):
        if json.dumps(self.obj) != json.dumps(obj):
            fp = open(self.file + ".backup", "w")
            fp.write(json.dumps(self.obj))
            fp.close()
        
        self.obj = obj

    def save(self):
        fp = open(self.file, "w")
        fp.write(json.dumps(self.obj))
        fp.close()

    def get(self):
        return self.obj

    def change(self, obj):
        self.backup(obj)

        self.save()

        return self.obj
