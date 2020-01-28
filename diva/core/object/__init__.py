from frater.io import register_json_serializer, register_json_deserializer

from .object import Object
from .object_defaults import OBJECT_JSON_DEFAULT, OBJECT_DETECTION_JSON_DEFAULT
from .object_detection import ObjectDetection
from .object_factory import *
from .object_functions import *
from .object_summary import *
from .object_type import ObjectType

register_json_serializer(Object, object_to_json)
register_json_deserializer(OBJECT_JSON_DEFAULT['data_type'], json_to_object)

register_json_serializer(ObjectDetection, object_detection_to_json)
register_json_deserializer(OBJECT_DETECTION_JSON_DEFAULT['data_type'], json_to_object_detection)

__all__ = ['Object', 'ObjectDetection', 'ObjectType', 'objects_have_temporal_overlap',
           'objects_have_spatiotemporal_overlap', 'temporally_segment_object']
