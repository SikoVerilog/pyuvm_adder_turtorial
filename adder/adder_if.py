
# interface is system Verilog component that is defined in UVM library
from cocotb.triggers import *

from uvm.base.sv import sv_if
# out interface will be inherited from sv_if
class addr_if(sv_if):
    # to initiate interface, we need bus_map means signals name and its direction
    def __init__(self, dut, bus_map=None, name="addr_if"):
        if bus_map is None:
            bus_map = {"clk": "clk", "a_i": "in_a", "b_i": "in_b",
                    "vld_i": "i_valid", "vld_o": "o_valid", "sum": "sum"}
	    # call its parent in it function
        super().__init__(dut, name, bus_map)
	    # take DUT reset signal as rst
        self.rstn = dut.resetn
    # start function just align out interface with DUT sampling time
    async def start(self):
        await Timer(0)
