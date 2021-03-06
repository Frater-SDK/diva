from dataclasses import dataclass, field
from typing import List, Union
from uuid import uuid4

from frater.data.data_type import DataType
from frater.logging import get_summary
from .activity_summary import get_activity_proposal_summary
from ..bounding_box import BoundingBox
from ..object import Object
from ..trajectory import Trajectory


@dataclass
class ActivityProposal(DataType):
    proposal_id: str = field(default_factory=lambda: str(uuid4()))
    trajectory: Trajectory = field(default_factory=Trajectory)
    objects: List[Object] = field(default_factory=list)
    source_video: str = ''
    experiment: str = ''

    @property
    def temporal_range(self):
        return self.trajectory.temporal_range

    @property
    def start_frame(self):
        return self.temporal_range.start_frame

    @property
    def end_frame(self):
        return self.temporal_range.end_frame

    def summary(self, multiline=True):
        return get_summary(self, get_activity_proposal_summary, multiline)

    def __len__(self):
        return len(self.temporal_range)

    def __getitem__(self, item: Union[int, slice]) -> Union[BoundingBox, 'ActivityProposal']:
        if isinstance(item, int):
            return self.trajectory[item]
        elif isinstance(item, slice):
            trajectory = self.trajectory[item]
            objects = [object[max(item.start, object.start_frame):min(item.stop, object.end_frame)]
                       for object in self.objects]
            return ActivityProposal(proposal_id=self.proposal_id, trajectory=trajectory, objects=objects,
                                    source_video=self.source_video, experiment=self.experiment)
