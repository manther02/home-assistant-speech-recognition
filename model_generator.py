import sys, os, traceback, time, importlib, json, re
from config_manager import ConfigManager

def readFile(file):
    content = ''
    
    if os.path.exists(file):
        fp = open(file, "r")
        content = fp.read()
        fp.close()

    return content

def writeFile(file, content):
    fp = open(file, "w")
    fp.write(content)
    fp.close()

config_manager = ConfigManager()
config = config_manager.get()

#Run all languages to group all the words

try:
    for language in config['languages']:
        words = []

        try:
            if not(config['wake_word'] in words):
                words.append(config['wake_word'])
        except KeyError:
            print('Wake word required')
            sys.exit(1)
            pass

        for module in config['modules']:
            try:
                for word in module['extra_words'][language]:
                    if not(word in words):
                        words.append(word)
            except KeyError:
                pass

            try:
                for action in module['actions']:
                    for command in action['commands'][language]:
                        if not(command in words):
                            words.append(command)
                    for actions_action in action['actions']:
                        for command in actions_action['commands'][language]:
                            if not(command in words):
                                words.append(command)
            except KeyError:
                print('Modules are required to have actions')
                sys.exit(1)
                pass

        aux_words = []

        for phrase in words:
            splitted_phrase = phrase.split(' ')

            for word in splitted_phrase:
                word = word.lower().strip()

                if not(word in aux_words) and word != '':
                    aux_words.append(word)

        words = aux_words

        #Get the language full dic, with all the words and use it to generate the min dic with the only needed ones

        models_config = config['languages'][language]['models']

        full_dic_path = models_config['full']['dic']
        min_dic_path = models_config['min']['dic']

        full_dic = readFile(full_dic_path)

        full_dic_words = full_dic.split('\n')

        full_dic_words_phm = {}

        for word in full_dic_words:
            splitted_word = re.split(r'\t+', word)

            if len(splitted_word) == 1:
                splitted_word = word.split(' ')

                key = 0

                while len(splitted_word) > 2:
                    phoneme = splitted_word[2]

                    if key > 1:
                        splitted_word[1] += ' ' + phoneme
                        del splitted_word[2]
                
                    key+=1

            if len(splitted_word) == 2:
                splitted_word[0] = splitted_word[0].lower().strip()
                splitted_word[1] = splitted_word[1].lower().strip()

                if splitted_word[0] != '' and splitted_word[1] != '':
                    full_dic_words_phm[splitted_word[0]] = splitted_word[1]

        min_dic_content = ''

        for word in words:
            try:
                min_dic_content += word + '\t' + full_dic_words_phm[word] + '\n'
            except KeyError:
                print('The word "' + word + '" does not exist on the provided: ' + full_dic_path)
                sys.exit(1)
                pass

        writeFile(min_dic_path, min_dic_content)
except KeyError:
    print('Wrong config format')
    sys.exit(1)
    pass