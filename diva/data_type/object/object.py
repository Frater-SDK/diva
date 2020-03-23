from dataclasses import dataclass, field
from typing import Union
from uuid import uuid4

from frater.data.category import Category
from frater.data.data_type import DataType
from frater.logging import get_summary
from .object_summary import get_object_summary
from ..bounding_box import BoundingBox
from ..temporal_range import TemporalRange
from ..trajectory import Trajectory


@dataclass
class Object(DataType):
    object_id: str = field(default_factory=lambda: str(uuid4()))
    object_type: Category = field(default_factory=lambda: Category(0, 'null', 'diva_objects'))
    trajectory: Trajectory = field(default_factory=Trajectory)
    source_video: str = ''
    experiment: str = ''

    def __len__(self):
        return len(self.temporal_range)

    def __getitem__(self, item: Union[int, slice]) -> Union[BoundingBox, 'Object']:
        if isinstance(item, int):
            return self.trajectory[item]
        elif isinstance(item, slice):
            trajectory = self.trajectory[item]
            return Object(object_id=self.object_id, object_type=self.object_type, trajectory=trajectory,
                          source_video=self.source_video, experiment=self.experiment)

    @property
    def temporal_range(self) -> TemporalRange:
        return self.trajectory.temporal_range

    @property
    def start_frame(self) -> int:
        return self.temporal_range.start_frame

    @property
    def end_frame(self) -> int:
        return self.temporal_range.end_frame

    def summary(self, multiline=True):
        return get_summary(self, get_object_summary, multiline)

    def add_bounding_box(self, bounding_box: BoundingBox):
        self.trajectory.add_bounding_box(bounding_box)
