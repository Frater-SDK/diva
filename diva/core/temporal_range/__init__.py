from frater.io import register_json_serializer, register_json_deserializer

from .temporal_range import TemporalRange
from .temporal_range_defaults import TEMPORAL_RANGE_JSON_DEFAULT
from .temporal_range_factory import *
from .temporal_range_functions import *
from .temporal_range_summary import *

register_json_serializer(TemporalRange, temporal_range_to_json)
register_json_deserializer(TEMPORAL_RANGE_JSON_DEFAULT['data_type'], json_to_temporal_range)

__all__ = ['TemporalRange', 'compute_temporal_iou', 'get_temporal_range_summary']
