import json
from enum import IntEnum

__long_names__ = ['Null', 'Door', 'Tree', 'Receptacle', 'Dumpster', 'Parking_Meter', 'ATM', 'Umbrella',
                  'Construction_Barrier', 'Other', 'Person', 'Vehicle', 'Bike', 'Construction_Vehicle',
                  'Push_Pulled_Object', 'Prop', 'Animal', 'Articulated_Infrastructure']


class ObjectType(IntEnum):
    """
    Object Types for DIVA
    """
    NULL = 0  # Null
    DOOR = 1  # Door
    TREE = 2  # Tree
    RECEPTACLE = 3  # Receptacle
    DUMPSTER = 4  # Dumpster
    PARKING_METER = 5
    ATM = 6
    UMBRELLA = 7
    CONSTRUCTION_BARRIER = 8
    OTHER = 9
    PERSON = 10
    VEHICLE = 11
    BIKE = 12  # Bike
    CONSTRUCTION_VEHICLE = 13  # Construction_Vehicle
    PUSH_PULLED_OBJECT = 14  # Push_Pulled_Object
    PROP = 15  # Prop
    ANIMAL = 16  # Animal
    ARTICULATED_INFRASTRUCTURE = 17  # Articulated_Infrastructure

    @property
    def long_name(self):
        return __long_names__[int(self.value)]

    @classmethod
    def from_long_name(cls, long_name: str) -> 'ObjectType':
        return ObjectType(__long_names__.index(long_name))

    def to_dict(self):
        return {'data_type': 'object_type', 'object_type': self.value}

    def to_json(self):
        return json.dumps(self.to_dict())

    @classmethod
    def from_dict(cls, d: dict):
        return ObjectType(d['object_type'])

    @classmethod
    def from_json(cls, s: str):
        return ObjectType.from_dict(json.loads(s))
