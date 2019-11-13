import os
import time
import speech_recognition as sr
from fuzzywuzzy import fuzz
import pyttsx3
import datetime
import webbrowser

# настройки
opts = {
    "alias": ('ержан', 'ерж', 'ержанина', 'ержаныч', 'ержан вставай', 'ержан бля', 'Геннадий',
              'алмаз', 'алмазан', 'алмазина', 'ержан подьем', 'ержан подъём', 'вставай ержан'),
    "tbr": ('скажи', 'расскажи', 'покажи', 'сколько', 'произнеси'),
    "cmds": {
        "ctime": ('текущее время', 'сейчас времени', 'который час', 'что по времени'),
        "radio": ('включи музыку', 'воспроизведи радио', 'включи радио'),
        "stupid1": ('расскажи анекдот', 'рассмеши меня', 'ты знаешь анекдоты')
    }
}

def makeSomething(zadanie):
    if 'открыть сайт' in zadanie:
        talk('Уже открываю')
        url = 'https://google.com'
        webbrowser.open(url)
    elif 'закрой' in zadanie:
        talk('Понял, закрываю')
        sys.exit()
    elif 'имя' in zadanie:
        talk('Я Ержан')


# функции
def speak(what):
    print(what)
    speak_engine.say(what)
    speak_engine.runAndWait()
    speak_engine.stop()


def callback(recognizer, audio):
    try:
        voice = recognizer.recognize_google(audio, language="ru-RU").lower()
        print("[log] Распознано: " + voice)

        if voice.startswith(opts["alias"]):
            # обращаются к Кеше
            cmd = voice

            for x in opts['alias']:
                cmd = cmd.replace(x, "").strip()

            for x in opts['tbr']:
                cmd = cmd.replace(x, "").strip()

            # распознаем и выполняем команду
            cmd = recognize_cmd(cmd)
            execute_cmd(cmd['cmd'])

    except sr.UnknownValueError:
        speak('Шо?')
        speak('А?А?А?')
        print("[log] Голос не распознан!")
    except sr.RequestError as e:
        print("[log] Неизвестная ошибка, проверьте интернет!")


def recognize_cmd(cmd):
    RC = {'cmd': '', 'percent': 0}
    for c, v in opts['cmds'].items():

        for x in v:
            vrt = fuzz.ratio(cmd, x)
            if vrt > RC['percent']:
                RC['cmd'] = c
                RC['percent'] = vrt

    return RC


def execute_cmd(cmd):
    if cmd == 'ctime':
        # сказать текущее время
        now = datetime.datetime.now()
        speak("Сейчас " + str(now.hour) + ":" + str(now.minute))

    elif cmd == 'radio':
        speak('Уже запускаю')
        # воспроизвести радио
        os.system('C:\listen.m3u')

    elif cmd == 'stupid1':
        speak('Хммм, дайте-ка подумать. Вспомнил!')
        # рассказать анекдот
        speak("Встречаются как то Саранча, Лера и Алмаз. Дальше не помню")

    else:
        print('Очень сложно для Ержана, ничего не понял')


# запуск
r = sr.Recognizer()
m = sr.Microphone(device_index=1)

with m as source:
    r.adjust_for_ambient_noise(source)

speak_engine = pyttsx3.init()

# Только если у вас установлены голоса для синтеза речи!
voices = speak_engine.getProperty('voices')
speak_engine.setProperty('voice', voices[4].id)

# forced cmd test
#speak("Встречаются как то Саранча, Лера и Алмаз. Дальше не помню")

#speak("Привет, я Ержан, смешной но глупый помошник. Начнём?")
speak("Ержан слушает")

stop_listening = r.listen_in_background(m, callback)
while True: time.sleep(0.1) # infinity loop
while True:
    makeSomething(commmand())