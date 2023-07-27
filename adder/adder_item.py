
from uvm.seq.uvm_sequence_item import UVMSequenceItem
from uvm.macros import *
from uvm.base.uvm_object_globals import *

# seqnce item class will be inherted from UVMSequenceItem
class item(UVMSequenceItem):
    # initilizing and defining all the element will be use in our sequence item
    def __init__(self, name="item"):
        super().__init__(name)
        # adder need 2 integer numbers that's why we need 2 veriable there
        self.int_a = 0  
        self.int_b = 0 
        self.sum = 0
        # define the range of these integer
        self.rand('int_a', range(0, 256))
        self.rand('int_b', range(0, 256))

    # this function is used for print print our item
    def convert2string(self):
        # just convert our interger in string
        return sv.sformatf("first operent=%0h, secend operent=%0h", self.int_a, self.int_b)

# sequence item will be register as object becase need they will be distroyed after receving in driver
uvm_object_utils_begin(item)
# out veriable will take all the functinality from UVMSeqneceItem
uvm_field_int("int_a", UVM_ALL_ON)
uvm_field_int("int_b", UVM_ALL_ON)
uvm_field_int("sum", UVM_ALL_ON)
uvm_object_utils_end(item)
