
import cocotb
from cocotb.triggers import *

from uvm.base.uvm_callback import *
from uvm.base.uvm_config_db import *

# import UVM monitor
from uvm.comps.uvm_monitor import UVMMonitor
# analysis port is taken form tlm ports
# analysis port is a piple between sender and reciver and it uni directional
from uvm.tlm1 import *
from uvm.macros import *

from .adder_item import *
# moniter which loooking for adder inputs
class monitor_befor(UVMMonitor):

    def __init__(self, name, parent=None):
        super().__init__(name, parent)
        # create analysis port by the name of ap
        self.ap = UVMAnalysisPort("ap", self)
        # interface signals
        self.sigs = None 
        self.cfg = None 
        # just to record number of transactions
        self.num_items = 0
        self.tag = "MONITOR_BEFOR"

    def build_phase(self, phase):
        super().build_phase(phase)
        agent = self.get_parent()
        if agent is not None:
            # take signals from agent virtual interface if agent have
            self.sigs = agent.vif
        else:
            arr = []
            # take handel from configuration database
            if UVMConfigDb.get(self, "", "vif", arr):
                uvm_info("adder monitor befor", "Got vif through ConfigDb for adder monitor instance")
                # take signals from virtual interface handel
                self.sigs = arr[0]
        if self.sigs is None:
            # crash simulation with fatal error if no interface available
            uvm_fatal("adder monitor befor", "No virtual interface specified for self monitor instance")

    async def run_phase(self, phase):
        # moniter don't need to drive any thing on interface
        while True:
            tr = None

            # always wait for one clock cycle
            await self.sample_delay()
            # Wait for asserting valid input signal
            # if input valid signal is asserted then brack while loop
            if self.sigs.vld_i == 1:
                # create item object
                tr = item.type_id.create("tr", self)
                # save the relevent signls from interface to item veriable
                tr.int_a = int(self.sigs.a_i.value)
                tr.int_b  = int(self.sigs.b_i.value)

                # self.trans_observed(tr)
                # just take a record after observing single transaction
                self.num_items += 1
                # send this item handel to scoreboard using analysis port
                self.ap.write(tr)
                # show results on terminal as a log
                uvm_info(self.tag, "Sampled adder input item: " + tr.convert2string(),
                    UVM_HIGH)

    # one clock edge waiting function
    async def sample_delay(self):
        await RisingEdge(self.sigs.clk)
        await Timer(1, "NS")
# register moniter as component in uvm factory
uvm_component_utils(monitor_befor)

# this moniter looking for output from DUT
class monitor_after(UVMMonitor):

    def __init__(self, name, parent=None):
        super().__init__(name, parent)
        # create analysis port
        self.ap = UVMAnalysisPort("ap", self)
        self.sigs = None 
        self.cfg = None 
        self.num_items = 0
        self.tag = "MONITOR_AFTER"

    def build_phase(self, phase):
        super().build_phase(phase)
        agent = self.get_parent()
        if agent is not None:
            # take singal from agent virtual interface
            self.sigs = agent.vif
        else:
            arr = []
            # get virtual interface handel from configureation  database
            if UVMConfigDb.get(self, "", "vif", arr):
                uvm_info(self.tag, "Got vif through ConfigDb for adder monitor instance")
                # save signls from virtula interface to local veriable
                self.sigs = arr[0]
        if self.sigs is None:
            # if no virtual interface is availe then creash simulation with fatal error
            uvm_fatal(self.tag, "No virtual interface specified for self monitor instance")

    async def run_phase(self, phase):
        while True:
            tr = None

            # wait for one posedge of clock
            await self.sample_delay()
            # if valid ouput signal asserted
            if self.sigs.vld_o == 1:
                tr = item.type_id.create("tr", self)
                # take result in local veriable from signal
                tr.sum = int(self.sigs.sum.value)

                # self.trans_observed(tr)
                self.num_items += 1
                # send complete object to scoreboard using analysis port
                self.ap.write(tr)
                # display adder result on terminal
                uvm_info(self.tag, "Sampled adder item: " + tr.convert2string(), UVM_HIGH)
    # this function generate wait for one clock cycle
    async def sample_delay(self):
        await RisingEdge(self.sigs.clk)
        await Timer(1, "NS")
# register our moniter as a component in uvm factory
uvm_component_utils(monitor_after)

