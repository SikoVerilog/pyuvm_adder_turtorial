
# cocotb is the platform which run our python uvm environment with DUT in its simulator in our case that is iverilog
import cocotb
# to drive DUT clock need to be driven all simulation time we take clock
from cocotb.clock import Clock
# when we need to wait for some time then we need timer
from cocotb.triggers import Timer
# uvm is python-uvm library which contain all the uvm utilities 
from uvm import *
# tb_env is out environment class that is use in our test
from tb_env import tb_env
# importing interface
from adder.adder_if import addr_if
from adder_seq import *


# Test class contain all the UVM components and its sequences inherited 
# from UVMTest which is defied in uvm library
class test(UVMTest):

    def __init__(self, name, parent=None):
	    # calling its parent init function
        super().__init__(name, parent)
	    # create test environment 
        self.env = tb_env("env")
    
    # After preparing complete environment that function state 
    # simulation in its run phase
    def start_of_simulation_phase(self, phase):
	    # top is reference to access each and every component 
        # in UVM simulation
        cs_ = UVMCoreService.get()
        top = cs_.get_root()
    
    # check phase just check did we found any conflict between 
    # DUT and our refernce
    def check_phase(self, phase):
        self.error = self.env.has_errors()
        if self.error:
	        # if we found any error in our simulation we report 
            # them as fatal error
            uvm_fatal("TEST FAILED", "check_phase of test threw fatal")
    # sequne run in run_phase of the test
    async def run_phase(self, phase):
        # rase objection
        phase.raise_objection(self, "start sequence")
        # create sequence object
        seq = addr_seq("seq")
        # start sequence with handel of sequencr our agent which is 
        # decleared in environment
        await seq.start(self.env.agnt.sqr)
        phase.drop_objection(self, "Env: adder sequence done")

# all those class who destroy in during simulation we need to 
# mark them as uvm components
uvm_component_utils(test)

# this class take a simple just take clock and reset signal to reset DUT in its reset phase
class tb_ctl_if():
    def __init__(self, clk, rst_n):
        self.clk = clk
        self.rst_n = rst_n

# this funcation use time that's why it is async
# purpose of this funcation to initiate the reset and clock signal 
# and start clock in independedt thread that will return at the end of simulation 
async def do_reset_and_start_clocks(dut):
    await Timer(100, "NS")
    dut.resetn <= 0
    await Timer(200, "NS")
    dut.clk <= 0
    await Timer(500, "NS")
    # use fork untility from cocotb to run clock all the time of simulation
    cocotb.fork(Clock(dut.clk, 50, "NS").start())

# test need to set in cocotb test that is the starting point where
# out test call created and that start our uvm environment
@cocotb.test()
async def test(dut):
    # Create the interfaces and bus map
    adder_bus_map = {"clk": "clk", "a_i": "in_a", "b_i": "in_b",
                    "vld_i": "i_valid", "vld_o": "o_valid", "sum": "sum"}
    # initilizing our interface with adder bus map
    adr_vif = addr_if(dut, bus_map=adder_bus_map, name="")

    rst_if = tb_ctl_if(
        clk=dut.clk,
        rst_n=dut.resetn
    )
    # we need to set our interfacer in uvm configuration database by its set function
    # that will be accessable in there agent by configDb get function
    UVMConfigDb.set(None, "env", "vif", rst_if)
    UVMConfigDb.set(None, "env.agnt", "adr_vif", adr_vif)
    # fork our clock and reset initization function
    cocotb.fork(do_reset_and_start_clocks(dut))
    # run_test will creat out UVMTest class befor stating any phase
    await run_test()
