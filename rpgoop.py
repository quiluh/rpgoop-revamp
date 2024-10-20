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

class IIterator(metaclass=ABCMeta):
    # ITERATOR INTERFACE

    @staticmethod
    @abstractmethod
    def hasNext() -> bool:
        pass

    @staticmethod
    @abstractmethod
    def next():
        pass

class Iterable(IIterator):
    # CONCRETE INERATOR

    def __init__(self,aggregrates) -> None:
        self._index = 0
        self._aggregrates = aggregrates
    
    def next(self):
        if self._index < len(self._aggregrates):
            aggregate = self._aggregrates[self._index]
            self._index += 1
            return aggregate
        raise Exception("AtEndOfIteratorException","At End of Iterator")
    
    def hasNext(self) -> bool:
        return self._index < len(self._aggregrates)

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
    
    def buildStrength(self) -> 'PlayerBuilder':
        self.product.Strength = random.randint(1,3)
        self.product.Strength.MaxValue = float("inf")
        self.product.Strength.MinValue = 0

    def getResult(self) -> 'Player':
        return self.product

class Director:
    # BUILD DIRECTOR

    @staticmethod
    def constructPlayer(name:str):
        return PlayerBuilder()\
            .buildName(name)\
            .buildHealth()\
            .buildStrength()\
            .getResult()    

class Flyweight:
    
    def __init__(self,code:int):
        self._code = code

    @property
    def Code(self) -> int:
        return self._code

class FlyweightFactory(Singleton):
    # FLYWEIGHT FACTORY

    _flyweights : dict[int,'Item'] = {}

    @classmethod
    def getFlyweight(cls,flyweight:dict) -> Union[None,Flyweight]:
        if flyweight["id"] in cls._flyweights:
            return cls._flyweights[flyweight["id"]]
        return None
    
    @classmethod
    def addFlyweight(cls,flyweight:Flyweight):
        cls._flyweights[flyweight.Code] = flyweight

class Item(Flyweight):
    # Item INTERFACE

    def __eq__(self,other):
        if isinstance(other, self):
            return self.Code == other.Code
        return False

    def __init__(self,item:dict):
        super().__init__(item["id"])

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

class ItemCreator:
    # Item FACTORY
    
    _ids = Iterable([i for i in range(1000)])

    itemTemplate = {"Name":"","Price":0,"id":_ids.next(),"Type":Item}

    @staticmethod
    def createItem(item:dict) -> Item:
        requestedFlyweight = FlyweightFactory.getFlyweight(item)
        if requestedFlyweight:
            return requestedFlyweight
        else:
            result = item["Type"](item)
            FlyweightFactory.addFlyweight(result)
            return result

class Balance(Singleton):
    
    _value = 0.0
    
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
    def addItem(cls, item: Item) -> bool:
        # Check if the item is already in the list
        existing_item = next((i for i in cls._value if i == item), None)
        if existing_item:
            existing_item.Quantity += 1
            return True
        else:
            item.Quantity = 1
            cls._value.append(item)
            return False

    @classmethod
    def removeItem(cls, item: Item) -> bool:
        existing_item = next((i for i in cls._value if i == item), None)
        if existing_item:
            if existing_item.Quantity > 0:
                existing_item.Quantity -= 1
            else:
                cls._value.remove(item)
            return True
        return False


class Player(Singleton):
    # PLAYER SINGLETON

    _name = ""
    _health = ICappedValue(None,None,None)
    _balance = Balance()
    _inventory = Inventory()
    _strength = ICappedValue(None,None,None)

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
    def Strength(cls) -> float:
        return cls._strength.Value
    @Strength.setter
    def Strength(cls,inputStrength:float):
        cls._strength.Value = inputStrength

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