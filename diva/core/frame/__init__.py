from frater.io import register_json_serializer, register_json_deserializer

from .frame import Frame, CroppedFrame
from .frame_defaults import FRAME_JSON_DEFAULT, CROPPED_FRAME_JSON_DEFAULT
from .frame_factory import *
from .frame_summary import *
from .modality import Modality

register_json_serializer(Frame, frame_to_json)
register_json_deserializer(FRAME_JSON_DEFAULT['data_type'], json_to_frame)

register_json_serializer(CroppedFrame, cropped_frame_to_json)
register_json_deserializer(CROPPED_FRAME_JSON_DEFAULT['data_type'], json_to_cropped_frame)

__all__ = ['Frame', 'CroppedFrame', 'Modality', 'get_frame_summary']
