
# we need to detect rising edge in reset phase that'e why we need risingedge
from cocotb.triggers import RisingEdge
# import UVM 
from uvm import *
# import agent and scorebard
from adder.adder_agent import *
from adder_sb import *

# test bench environment is inherted from UVMEnv
class tb_env(UVMEnv):

    def __init__(self, name="tb_env", parent=None):
        super().__init__(name, parent)
        # decleare agent and scorebaord
        self.agnt = None
        self.sb = None
        self.vif = None
    
    # in build phase we need to reset the DUT that's why we need vif 
    def build_phase(self, phase):
        vif = []
        # get virtual interface handel from configuration database
        if not UVMConfigDb.get(self, "", "vif", vif):
           uvm_fatal("TB/ENV/NOVIF", "No virtual interface specified for environment instance")
        # take signsls form virtual interface
        self.vif = vif[0]
        # clear agent and scoreboard
        self.agnt = adder_agent.type_id.create("agnt", self)
        self.sb = adder_sb.type_id.create("predict", self)

    # connect phase connect connect moniter analysis port to scoreboard
    def connect_phase(self, phase):
        self.agnt.mon_bfr.ap.connect(self.sb.befor)
        self.agnt.mon_aft.ap.connect(self.sb.after)

    # if any error found in simulation return True else False
    def has_errors(self):
        return self.sb.error

    # in pre reset phase wait for clock and reset signal 
    async def pre_reset_phase(self, phase):
        phase.raise_objection(self, "Waiting for reset to be valid")
        # wait for valid value for reset signal
        while not (self.vif.rst_n.value.is_resolvable):
            await RisingEdge(self.vif.clk)
            uvm_info("WAIT_RST", "Waiting reset to become 0/1", UVM_MEDIUM)
        phase.drop_objection(self, "Reset is no longer X")

    # in reset phase reset DUT by asserting reset signal
    async def reset_phase(self, phase):
        # raise phase objection
        phase.raise_objection(self, "Env: Asserting reset for 10 clock cycles")

        uvm_info("TB/TRACE", "Resetting DUT...", UVM_NONE)
        # assert reset signal
        self.vif.rst_n.value <= 1
        uvm_info("TB/TRACE", "Reset Asserted", UVM_NONE)
        # wait for 10 cycles
        for _ in range(10):
            await RisingEdge(self.vif.clk)
        # deassert reset signal
        self.vif.rst_n.value <= 0
        uvm_info("TB/TRACE", "Reset Deasserted", UVM_NONE)
        # drop phase objection
        phase.drop_objection(self, "Env: HW reset done")
# register environment as component in uvm factory
uvm_component_utils(tb_env)
