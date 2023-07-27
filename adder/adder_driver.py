
import cocotb
from cocotb.triggers import *
# importing uvm driver and macros uvm_info and verbosity UVM_MEDIUM
# from uvm.base.uvm_callback import *
# from uvm.base.uvm_config_db import *
# from uvm.comps.uvm_driver import UVMDriver
# from uvm.macros import *
from uvm import *
# importing sequence item
from .adder_item import *

# driver inherted from UVMDriver
class adder_driver(UVMDriver):
    # class declaration
    def __init__(self, name, parent=None):
        super().__init__(name,parent)
        # uvm event for communication between differnect components
        self.trig = Event("trans_exec")  # event
        # virtual interface handel to write on transaction on them
        self.sigs = None  # vif
        # configuration need when we make our driver customizable
        self.cfg = None  # config
        # name of our class
        self.tag = "Adder_Master"

    # UVM build phase
    def build_phase(self, phase):
        super().build_phase(phase)
        # get agent handel
        agent = self.get_parent()
        if agent is not None:
            # take address of virtual interface from agent vif
            self.sigs = agent.vif
        else:
            arr = []
            # take interfcae handel from configuration database
            if (not UVMConfigDb.get(self, "", "adr_vif", arr)):
                # report fatal error when fail to find interface
                uvm_fatal("Adder", "No virtual interface specified for self driver instance")
            else:
                # save signal list from interface handel
                self.sigs = arr[0]

    # uvm run phase 
    async def run_phase(self, phase):
        # this will display on teminal when driver enter in run_phase
        uvm_info("Adder_Master", "adder_master run_phase started", UVM_MEDIUM)
        # simulation start with deasserting valid signal
        self.sigs.vld_i.value    = 0

        # termination of phase in one component will force to terminat 
        # all of the remaing components thats why we need to implement while 1 loop
        while True:
            # this line will stope simulation for 1 posedge
            await self.drive_delay()

            tr = []
            # get_next_item function wait until sequencer have atleast one transaction 
            # and save transaction handel on local veriable
            await self.seq_item_port.get_next_item(tr)
            tr = tr[0]
            # take disply on terminal insted of wavefrom that's why we use 
            # uvm_info with different verbosity
            uvm_info("Adder_MASTER", "Driving trans into DUT: " + tr.convert2string(), UVM_DEBUG)
           
            # interfcae driving protocol 
            await self.drive_delay()
            # pre interface wiritng 
            # await self.trans_received(tr)

            # interface writing 
            await self.write(tr)

            # post interface writing
            # await self.trans_executed(tr)
            
            # send message to sequencer we finished this transcation or return reposece if needed 
            # after that sequencer prepare sequence to generate new transaction
            self.seq_item_port.item_done()

            # generate interupr or event to inform we write transaction on interface
            self.trig.set()
    
    async def write(self, tr):
        uvm_info(self.tag, "Doing Adder write.", UVM_MEDIUM)
        # assign all the integer to relevetn signals
        self.sigs.a_i.value = tr.int_a
        self.sigs.b_i.value = tr.int_b
        # assert valid_i signal 
        self.sigs.vld_i.value = 1
        # wait for positive edge of the clock
        await self.drive_delay()
        #  deassert valid_i signal
        self.sigs.vld_i.value = 0
        await self.drive_delay()

        uvm_info(self.tag, "Finished Adder write.", UVM_MEDIUM)
    
    async def drive_delay(self):
        # wating to positive edge of clock
        await RisingEdge(self.sigs.clk)
        await Timer(1, "NS")

    
    async def trans_received(self, tr):
        await Timer(1, "NS")

    
    async def trans_executed(self, tr):
        await Timer(1, "NS")
# register or driver as a component in uvm_factory
uvm_component_utils(adder_driver)

