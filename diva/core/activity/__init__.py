from frater.io import register_json_serializer, register_json_deserializer

from .activity import Activity
from .activity_defaults import ACTIVITY_JSON_DEFAULT, ACTIVITY_PROPOSAL_JSON_DEFAULT
from .activity_factory import *
from .activity_functions import *
from .activity_proposal import ActivityProposal
from .activity_summary import *
from .activity_type import ActivityType, ActivityTypeGroup

register_json_serializer(Activity, activity_to_json)
register_json_deserializer(ACTIVITY_JSON_DEFAULT['data_type'], json_to_activity)

register_json_serializer(ActivityProposal, activity_proposal_to_json)
register_json_deserializer(ACTIVITY_PROPOSAL_JSON_DEFAULT['data_type'], json_to_activity_proposal)

__all__ = ['Activity', 'ActivityProposal', 'ActivityType',
           'ActivityTypeGroup', 'proposal_to_activity', 'activity_to_proposal',
           'get_activity_summary', 'get_activity_proposal_summary']
