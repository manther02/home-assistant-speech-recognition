import sys, os, traceback, time, importlib, json, re

spec = importlib.util.spec_from_file_location('screen-manager', os.path.join(os.path.abspath('modules/screen-manager'), 'screen-manager.py'))
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

screenmanager = getattr(module, 'ScreenManager')('music-player')

class MusicPlayer:
    def __init__(self):
        print('--> MusicPlayer')

    def play(self, speech = None):
        if speech != None:
            print('--> playing : ' + speech)
            screenmanager.command("tizonia --youtube-audio-search '" + speech.replace("'", "") + "'\n")
        else:
            print('--> play')
            os.system("espeak 'Which music?'")
            return 'askSpeech'

    def next(self):
        print('--> next')
        screenmanager.command("n")

    def previous(self):
        print('--> previous')
        screenmanager.command("p")

    def pause(self):
        print('--> pause')
        screenmanager.command(" ")

    def resume(self):
        print('--> resume')
        screenmanager.command(" ")

    def stop(self):
        print('--> stop')
        screenmanager.command("q")
        return 'finished'