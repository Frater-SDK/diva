from frater.io import register_json_serializer, register_json_deserializer

from .video import Video
from .video_defaults import VIDEO_JSON_DEFAULT
from .video_factory import *
from .video_summary import *

register_json_serializer(Video, video_to_json)
register_json_deserializer(VIDEO_JSON_DEFAULT['data_type'], json_to_video)

__all__ = ['Video', 'get_video_summary']
