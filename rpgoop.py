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

    def buildHealth(self) -> 'PlayerBuilder':
        self.product.MaxHealth = 100
        self.product.Health = 100
        return self

    def getResult(self) -> 'Player':
        return self.product

class Director:
    # BUILD DIRECTOR

    @staticmethod
    def constructPlayer(name:str):
        return PlayerBuilder()\
            .buildName(name)\
            .buildHealth()\
            .getResult()
    
class Flyweight:
    # FLYWEIGHT CONTAINS UNIQUE ID

    def __init__(self,code:int):
        self._code = code

    @property
    def Code(self) -> int:
        return self._code        

class Item(Flyweight):
    pass

class Wearable(Item):
    pass

class Weapon(Wearable):
    pass

class Clothing(Wearable):
    pass

class Collectable(Item):
    pass

class Consumable(Item):
    pass

class ItemFactory:
    # ITEM FACTORY

    availableIDs = [i for i in range(1000)]
    templateObject = {"Name":"","Price":0,"Type":Item,"id":availableIDs.pop(random.randint(0,len(availableIDs)))}

    allObjects = [

    ]

    @staticmethod
    def createObject(object:Union[Item,dict]):
        if type(object) == dict:
            object = object["Type"](object)
        return object
    
class FlyweightFactory(Singleton):
    # FLYWEIGHT FACTORY

    _flyweights : dict[int,Flyweight] = {i["id"]:ItemFactory.createObject(i) for i in ItemFactory.allObjects}

    def getFlyweight(cls,code:int) -> Flyweight:
        if code in cls._flyweights:
            return cls._flyweights[code]

class Balance(Singleton):
    
    _value = []
    
    @property
    def Value(cls) -> float:
        return cls._value
    @Value.setter
    def Value(cls,inputValue:float) -> bool:
        if inputValue >= 0:
            cls._value = inputValue
            return True
        else:
            cls._value = 0
            return False

class Inventory(Singleton):

    _value = []
    
    @property
    def Value(cls) -> float:
        return cls._value
    @classmethod
    def addItem(cls,item):
        # ITEM LOGIC
        pass
    @classmethod
    def removeItem(cls,item):
        # ITEM LOGIC
        pass

class Player(Singleton):
    # PLAYER SINGLETON

    _name = ""
    _health = ICappedValue(None,None)
    _balance = Balance()
    _inventory = Inventory()

    @property
    def Name(cls) -> str:
        return cls._name
    @Name.setter
    def Name(cls,inputName:str):
        cls._name = inputName

    @property
    def Health(cls) -> float:
        return cls._health.Value
    @Health.setter
    def Health(cls,inputHealth:float):
        cls._health.Value = inputHealth
    
    @property
    def MaxHealth(cls) -> float:
        return cls._health.MaxValue
    @MaxHealth.setter
    def Health(cls,inputHealth:float):
        cls._health.MaxValue = inputHealth

    @property
    def Balance(cls) -> float:
        return cls._balance.Value
    @Balance.setter
    def Balance(cls,inputBal:float):
        cls._balance.Value = inputBal

    @property
    def Inventory(cls) -> list:
        return cls._inventory.Value
    @classmethod
    def addInventory(cls,item):
        cls._inventory.addItem(item)
    @classmethod
    def removeInventory(cls,item):
        cls._inventory.removeItem(item)