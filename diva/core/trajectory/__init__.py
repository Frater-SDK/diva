from frater.io import register_json_serializer, register_json_deserializer

from .trajectory import Trajectory
from .trajectory_defaults import TRAJECTORY_JSON_DEFAULT
from .trajectory_factory import *
from .trajectory_functions import *
from .trajectory_summary import *

register_json_serializer(Trajectory, trajectory_to_json)
register_json_deserializer(TRAJECTORY_JSON_DEFAULT['data_type'], json_to_trajectory)

__all__ = ['Trajectory', 'compute_spatiotemporal_iou', 'scale_trajectory', 'get_trajectory_summary']
