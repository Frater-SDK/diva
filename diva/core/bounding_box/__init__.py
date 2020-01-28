from frater.io import register_json_serializer, register_json_deserializer

from .bouding_box_summary import *
from .bounding_box import BoundingBox
from .bounding_box_defaults import BOUNDING_BOX_JSON_DEFAULT
from .bounding_box_factory import *
from .bounding_box_functions import *

register_json_serializer(BoundingBox, bounding_box_to_json)
register_json_deserializer(BOUNDING_BOX_JSON_DEFAULT['data_type'], json_to_bounding_box)

__all__ = ['BoundingBox', 'combine_bounding_boxes', 'compute_spatial_iou', 'convert_descriptors_to_bounding_box',
           'linear_interpolate_bounding_boxes', 'scale_bounding_box', 'get_bounding_box_summary']
