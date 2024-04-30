from abc import ABCMeta, abstractmethod
import time
from sys import stdout
from typing import Union
import random

def printSlow(*args):
    for string in args:
        for i in string.upper():
            stdout.write(i)
            stdout.flush()
            time.sleep(0.01)
        print("")

class Singleton:
    _instance = None

    def __new__(cls,*args,**kwargs) -> 'Singleton':
        if not cls._instance:
            cls._instance = super().__new__(cls,*args,**kwargs)
        return cls._instance

class IBuilder(metaclass=ABCMeta):
    # BUILDER INTERFACE

    @staticmethod
    @abstractmethod
    def getResult():
        pass

class PlayerBuilder(IBuilder):
    # CONSTRUCTS PLAYER

    def __init__(self):
        self.product = Player()

    def buildName(self,inputName:str) -> 'PlayerBuilder':
        self.product.Name = inputName
        return self

    def getResult(self) -> 'Player':
        return self.product
    
class ICappedValue():
    # VALUE CAP INTERFACE

    def __init__(self,maxValue:float,minValue:float):
        self._value = maxValue
        self._maxValue = maxValue
        self._minValue = minValue
    
    @property
    def Value(self) -> float:
        return self._value
    @Value.setter
    def Value(self,inputValue:float):
        self._value = self._maxValue if inputValue > self._maxValue else self._minValue if inputValue < self._minValue else inputValue
    
    @property
    def MaxValue(self) -> float:
        return self._maxValue
    @MaxValue.setter
    def MaxValue(self,inputValue:float):
        self._maxValue = inputValue

    @property
    def MinValue(self) -> float:
        return self._minValue
    @MinValue.setter
    def MinValue(self,inputValue:float):
        self._minValue = inputValue

class Item:
    pass
    
class Balance(Singleton):
    
    def __init__(self,value:float=0):
        self._value = value
    
    @property
    def Value(self) -> float:
        return self._value
    @Value.setter
    def Value(self,inputValue:float) -> bool:
        if inputValue >= 0:
            self._value = inputValue
            return True
        else:
            self._value = 0
            return False

class Inventory(Singleton):
    
    def __init__(self,value:list=[]):
        self._value = value
    
    @property
    def Value(self) -> float:
        return self._value
    def addItem(self,item:Item):
        # ITEM LOGIC
        pass
    def removeItem(self,item:Item):
        # ITEM LOGIC
        pass

class Player(Singleton):
    # PLAYER SINGLETON

    def __init__(self):
        self._name = ""
        self._health = ICappedValue(None,None)
        self._balance = Balance()
        self._inventory = Inventory()
    
    @property
    def Name(self) -> str:
        return self._name
    @Name.setter
    def Name(self,inputName:str):
        self._name = inputName

    @property
    def CurrentHealth(self) -> float:
        return self._health.CurrentValue
    @CurrentHealth.setter
    def Health(self,inputHealth:float):
        self._health.CurrentValue = inputHealth
    
    @property
    def MaxHealth(self) -> float:
        return self._health.MaxValue
    @MaxHealth.setter
    def Health(self,inputHealth:float):
        self._health.MaxValue = inputHealth

    @property
    def Balance(self) -> float:
        return self._balance.Value
    @Balance.setter
    def Balance(self,inputBal:float):
        self._balance.Value = inputBal

    @property
    def Inventory(self) -> list:
        return self._inventory.Value
    def addInventory(self,item:Item):
        self._inventory.addItem(item)
    def removeInventory(self,item:Item):
        self._inventory.removeItem(item)

class Director:
    # BUILD DIRECTOR

    @staticmethod
    def constructPlayer(name:str):
        return PlayerBuilder()\
            .buildName(name)\
            .getResult()