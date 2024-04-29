from abc import ABCMeta, abstractmethod
import time
from sys import stdout
from typing import Union
import random

def printSlow(*args): # POLISH UP
    for string in args:
        for i in string.upper():
            stdout.write(i)
            stdout.flush()
            time.sleep(0.01)
        print("")

class IBuilder(metaclass=ABCMeta):
    # BUILDER INTERFACE

    @staticmethod
    @abstractmethod
    def getResult():
        pass