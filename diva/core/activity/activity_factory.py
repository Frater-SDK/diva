import operator
import uuid
from functools import reduce
from typing import Dict

from .activity import Activity, ActivityType
from ..object.object_factory import *
from ..trajectory import Trajectory

__all__ = ['diva_format_to_activity', 'activity_to_diva_format']


def diva_format_to_activity(activity: Dict) -> Activity:
    activity_type = ActivityType.from_long_name(activity['activity'])
    confidence = activity['presenceConf'] if 'presenceConf' in activity else 1.0
    probabilities = [0.0 if i != activity_type.value else confidence for i in range(len(ActivityType))]
    activity_id = uuid.UUID(int=activity['activityID']) if 'activityID' in activity else uuid.uuid4()

    source_video = list(activity['localization'].keys())[0]
    objects = [diva_format_to_object(obj) for obj in activity['objects']]
    trajectory = reduce(operator.add, [object.trajectory for object in objects], Trajectory())
    experiment = ''

    return Activity(activity_id=str(activity_id), activity_type=activity_type,
                    trajectory=trajectory, objects=objects,
                    source_video=source_video, experiment=experiment,
                    confidence=confidence, probabilities=probabilities)


def activity_to_diva_format(activity: Activity) -> Dict:
    return {
        'activityID': uuid.UUID(activity.activity_id).int,
        'activity': activity.activity_type.long_name,
        'presenceConf': activity.confidence,
        'localization': {
            activity.source_video: {
                str(activity.temporal_range.start_frame): 1,
                str(activity.temporal_range.end_frame): 0
            }
        },
        'objects': [
            object_to_diva_format(obj) for obj in activity.objects
        ]
    }
