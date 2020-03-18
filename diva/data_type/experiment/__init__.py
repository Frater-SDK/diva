from frater.data import data_types
from .experiment import Experiment

data_types.register_class(Experiment.data_type(), Experiment)
