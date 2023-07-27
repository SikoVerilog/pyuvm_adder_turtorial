
# import driver from uvm
from uvm.comps.uvm_agent import UVMAgent
from uvm.base import UVMConfigDb, UVM_LOW
from uvm.macros import *
from uvm.tlm1 import *
# import driver, moniter and sequencer
from .adder_driver import *
from .adder_sequencer import *
from .adder_monitor import *

# adder agent inherited from UVMAgent
class adder_agent(UVMAgent):

    def __init__(self, name, parent=None):
        super().__init__(name, parent)
        # create sequener
        self.sqr = None  
        # create driver
        self.drv = None
        # create befor and after moninter 
        self.mon_bfr = None
        self.mon_aft = None
        # viturl interface
        self.vif = None
        # display msg on temrinal
        uvm_info("adder_agent", "Agent Created", UVM_LOW)

    # build phase build all the relevevnt componets
    def build_phase(self, phase):
        uvm_info("adder_agent", "In Build Phase", UVM_LOW)
        # build sequencer
        self.sqr = adder_sequencer.type_id.create("sqr", self)
        # build driver 
        self.drv = adder_driver.type_id.create("drv", self)
        # build moniters
        self.mon_bfr = monitor_befor.type_id.create("mon_bfr", self)
        self.mon_aft = monitor_after.type_id.create("mon_aft", self)

        # looking for virtul interface
        arr = []
        # get virtual interface from configuration database
        if UVMConfigDb.get(self, "", "adr_vif", arr):
            self.vif = arr[0]
        if self.vif is None:
            # if failed to find interface then creah simulation with fatal error
            uvm_fatal("Adder Agent", "No virtual interface specified for adder_agent instance")

    # connect sequencer and driver to send and resive transaction from sequence
    def connect_phase(self, phase):
        uvm_info("adder_agent", "In Connect Phase", UVM_LOW)
        # connnect driver to sequencer
        self.drv.seq_item_port.connect(self.sqr.seq_item_export)

# register adder agent as component in uvm factory
uvm_component_utils(adder_agent)
