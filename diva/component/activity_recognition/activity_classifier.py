from dataclasses import dataclass, field
from typing import List

from frater.component import ComponentConfig
from frater.component.component import IOComponent
from frater.stream import InputStream, OutputStream

from diva.core import Activity, ActivityProposal, Modality


@dataclass
class ActivityClassifierConfig(ComponentConfig):
    classifier_name: str = ''
    weights: str = ''
    num_categories: int = 0
    batch_size: int = 1
    modality: str = field(default='RGB')
    gpus: List[int] = field(default_factory=list)
    input_components: int = 1

    @property
    def modality_type(self) -> Modality:
        return Modality[self.modality]


class ActivityClassifier(IOComponent):
    def __init__(self, config: ActivityClassifierConfig, input_stream: InputStream, output_stream: OutputStream):
        super(ActivityClassifier, self).__init__(config, input_stream, output_stream)

    @staticmethod
    def init_state():
        return {'eos_count': 0, 'current_batch': list()}

    @property
    def input_components(self):
        return self.config.input_components

    @property
    def current_batch(self):
        return self.state['current_batch']

    @property
    def batch_size(self):
        return self.config.batch_size

    def preprocess(self, proposal: ActivityProposal):
        self.add_to_batch(proposal)
        if self.batch_is_ready():
            return self.current_batch

    def process(self, proposals: List[ActivityProposal]) -> List[Activity]:
        raise NotImplementedError

    def after_process(self):
        if self.batch_is_ready():
            self.reset_batch()

    def on_end_of_stream(self):
        self.state['eos_count'] += 1
        if self.state['eos_count'] >= self.input_components:
            if len(self.current_batch) > 0:
                self.batch_lifecycle(self.current_batch)
                self.reset_batch()

    def add_to_batch(self, proposal: ActivityProposal):
        self.current_batch.append(proposal)

    def batch_is_ready(self):
        return len(self.current_batch) == self.batch_size

    def reset_batch(self):
        self.state['current_batch'] = list()

    def batch_lifecycle(self, batch):
        output = self.process(batch)
        self.after_process()
        postprocessed_output = self.postprocess(output)
        self.after_postprocess()
        self.send_output(postprocessed_output)
