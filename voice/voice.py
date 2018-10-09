# encoding=utf-8

from aip import AipSpeech
from wxRobot import globalVars

if __name__ == '__main__':
    aipSpeech = AipSpeech(globalVars.get_API_ID(), globalVars.get_API_KEY(), globalVars.get_SECRET_KEY())