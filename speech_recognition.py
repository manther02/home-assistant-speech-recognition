import sys, os, traceback, time, importlib, json, re
from pocketsphinx import LiveSpeech, get_model_path
from config_manager import ConfigManager

class SpeechRecognition:
    active_command = {
        'filled' : False,
        'module' : '',
        'class' : '',
        'base_function' : '',
        'function' : '',
        'base_command' : '',
        'command' : ''
    }

    config_manager = ConfigManager()

    config = config_manager.get()

    modules_base_path = os.path.abspath('modules')

    hmm = ''
    models = {}
    language = ''

    def __init__(self):
        self.config = self.config_manager.get()

        self.language = self.config['actual_language']
        language_config = self.config['languages'][self.language]

        self.hmm = os.path.abspath(language_config['hmm'])
        self.models = {
            'full' : {
                'lm' : os.path.abspath(language_config['models']['full']['lm']),
                'dic' : os.path.abspath(language_config['models']['full']['dic']),
            },
            'min' : {
                'lm' : os.path.abspath(language_config['models']['min']['lm']),
                'dic' : os.path.abspath(language_config['models']['min']['dic']),
            }
        }
        
        self.listenWakeWord()

    def listenWakeWord(self):
        print('Waiting Wake Word...')

        speech = LiveSpeech(
            hmm=self.hmm,
            lm=self.models['min']['lm'],
            dic=self.models['min']['dic']
        )

        for phrase in speech:
            if self.config['wake_word'] == self.treatCommand(phrase):
                os.system("espeak 'Yes?'")
                self.listenCommands()
                break

    def listenCommands(self):
        print('Listening Commands...')

        speech = LiveSpeech(
            hmm=self.hmm,
            lm=self.models['min']['lm'],
            dic=self.models['min']['dic']
        )

        now = int(time.time()) 
        text = ''

        #print(now)

        for phrase in speech:
            text = self.treatCommand(phrase)
            if text != '':
                break

        self.executeCommand(text)

    def listenSpeech(self):
        print('Listening Speech...')

        speech = LiveSpeech(
            verbose=False,
            sampling_rate=16000,
            buffer_size=2048,
            no_search=False,
            full_utt=False,
            hmm=self.hmm,
            lm=self.models['full']['lm'],
            dic=self.models['full']['dic']
        )

        text = ''

        for phrase in speech:
            text = self.treatCommand(phrase)
            if text != '':
                break

        self.listenWakeWord()

    def treatCommand(self, text):
        text = str(text).lower().strip()

        return text

    def executeCommand(self, command, speech = None):
        if action == 'askCommand':
            self.listenCommands()
        elif action == 'askSpeech':
            self.listenSpeech()
        else:
            self.listenWakeWord()

sr = SpeechRecognition()