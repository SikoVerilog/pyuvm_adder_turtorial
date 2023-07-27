
# uvm sequence is taken from uvm library
from uvm.seq import UVMSequence
from uvm.macros.uvm_object_defines import uvm_object_utils
from adder.adder_item import item

# our sequence is inhereted from UVMSequnece
class addr_seq(UVMSequence):
    # initilize the sequence
    def __init__(self, name="addr_seq"):
        UVMSequence.__init__(self, name)
        # our sequence will generate only 10 item if we need just update that veriable
        self.no_transaction = 10

    # body is the main function who send and recive the transaction from sequencer
    async def body(self):
        for i in range(self.no_transaction):
            # create sequcen item
            tran = item()
            # wait until driver ready for transaction
            await self.start_item(tran)
            # randomize our item to do ramdom test if we have fix sequence then just assign
            # value to our item veriables
            tran.randomize()
            # handover transaction to sequencer, to pass this to driver
            await self.finish_item(tran)
# sequce is an object means it will be distryed after compeleting the body function
uvm_object_utils(addr_seq)