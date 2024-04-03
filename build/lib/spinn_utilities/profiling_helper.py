from spynnaker.pyNN.utilities import neo_convertor
from spynnaker.pyNN.models.populations import Population
import numpy
import os

class ProfilingHelper(object):
    @classmethod
    def enable_recording(self, pop):
        pop.record(["spikes", "v", "packets-per-timestep"])

    @classmethod
    def record_full_data_to_csv(self, pop: Population , path = None): 
        if path == None:
            path = os.path.dirname(os.path.abspath(__file__))
        cells = pop.get_data(
            variables=["spikes", "v", "packets-per-timestep"])
        spikes = neo_convertor.convert_spikes(cells)
        v = cells.segments[0].filter(name='v')[0]
        packets = cells.segments[0].filter(name='packets-per-timestep')[0]

        numpy.savetxt(os.path.join(path, "spikes_%s.csv" % pop.label()), spikes, delimiter=",")
        numpy.savetxt(os.path.join(path, "v_%s.csv" % pop.label()), v, delimiter=",")
        numpy.savetxt(os.path.join(path, "packets_%s.csv" % pop.label()), packets, delimiter=",")
