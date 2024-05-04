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

    def __init__(self,value:float,maxValue:float,minValue:float):
        self._value = value
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
    
    def __init__(self,code:int):
        self._code = code

    @property
    def Code(self) -> int:
        return self._code

class FlyweightFactory(Singleton):
    # FLYWEIGHT FACTORY

    _flyweights : dict[int,'IItem'] = {}

    @classmethod
    def getFlyweight(cls,flyweight:dict) -> Union[None,Flyweight]:
        if flyweight["id"] in cls._flyweights:
            return cls._flyweights[flyweight["id"]]
        return None
    
    @classmethod
    def addFlyweight(cls,flyweight:Flyweight):
        cls._flyweights[flyweight.Code] = flyweight

class IItem(Flyweight):
    # IItem INTERFACE

    _latestId = -1

    def __init__(self,item:dict):
        self._latestId += 1
        super().__init__(self._latestId)

        self._quantity = ICappedValue(0,float("inf"),0)

        self._name = item["Name"]
        self._price = item["Price"]

    @property
    def Quantity(self) -> int:
        return self._quantity
    @Quantity.setter
    def Quantity(self,value:int):
        self._quantity = value

    @property
    def Name(self) -> str:
        return self._name
    
    @property
    def Price(self) -> int:
        return self._price    

class Wearable(IItem):
    pass

class Weapon(Wearable):
    pass

class Clothing(Wearable):
    pass

class Collectable(IItem):
    pass

class Consumable(IItem):
    pass

class ItemCreator:
    # Item FACTORY

    _ItemTemplate = {"Name":"","Price":0,"id":0,"Type":IItem}

    @staticmethod
    def createItem(item:dict) -> IItem:
        requestedFlyweight = FlyweightFactory.getFlyweight(item)
        if requestedFlyweight:
            return requestedFlyweight
        else:
            result = IItem["Type"](item)
            FlyweightFactory.addFlyweight(result)
            return result

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
    _health = ICappedValue(None,None,None)
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
        cls._inventory.additem(item)
    @classmethod
    def removeInventory(cls,item):
        cls._inventory.removeitem(item)