
# uvm sequencer is taken from uvm library
from uvm.seq.uvm_sequencer import UVMSequencer
from uvm.macros import uvm_component_utils
# our sequencer is inherited from UVMSequencer
class adder_sequencer(UVMSequencer):
    # initilize out seuqencer with default configuration
    def __init__(self, name, parent=None):
        super().__init__(name, parent)
# sequneer is component means that is aligned with uvm phases
# and work in parallel of driver
uvm_component_utils(adder_sequencer)
