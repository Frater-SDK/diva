from typing import Dict
from uuid import UUID

from .object import Object
from .object_type import ObjectType
from ..trajectory.trajectory_factory import *

__all__ = ['diva_format_to_object', 'object_to_diva_format']


def object_to_diva_format(obj: Object) -> Dict:
    return {
        'objectID': UUID(obj.object_id).int,
        'objectType': obj.object_type.long_name,
        'localization': {
            obj.source_video: {
                str(bounding_box.frame_index): {
                    'boundingBox': {
                        'x': bounding_box.x,
                        'y': bounding_box.y,
                        'w': bounding_box.w,
                        'h': bounding_box.h
                    },
                    'presenceConf': bounding_box.confidence
                } for bounding_box in obj.trajectory.bounding_boxes}}
    }


def diva_format_to_object(obj: Dict) -> Object:
    object_type = ObjectType.from_long_name(obj['objectType'])
    source_video = list(obj['localization'].keys())[0]
    trajectory = diva_format_to_trajectory(obj['localization'][source_video])
    object_id = str(UUID(int=obj['objectID']))
    return Object(object_id=object_id, object_type=object_type, trajectory=trajectory, source_video=source_video)
