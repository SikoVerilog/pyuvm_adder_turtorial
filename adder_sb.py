
# import all the uvm form its library
from uvm import *
# declear analysis port using implementation port
uvm_analysis_imp_befor = uvm_analysis_imp_decl("_befor")
uvm_analysis_imp_after = uvm_analysis_imp_decl("_after")

#  scorebard inherired from UVMScoreboard
class adder_sb(UVMScoreboard):

    def __init__(self, name, parent=None):
        super().__init__(name, parent)
        self.befor = uvm_analysis_imp_befor("befor", self)
        self.after = uvm_analysis_imp_after("after", self)
        # handeling veriable
        self.n_obs_thresh = 10 # how many transaction will be observed
        self.m_sb = [] # fifo to store adder input result
        self.error = 0 # failing indicator
        self.errs = 0 # count number of failer
        self.m_n_obs = 0 # number of observed transaction

    # built phase
    def build_phase(self, phase):
        thr = []
        # get the threshold value from configuration database 
        if UVMConfigDb.get(self, "", "n_obs_thresh", thr):  # cast to 'void' removed
            self.n_obs_thresh = thr[0]

    # when any transaction appier on befor analysis port then 
    # this funcation called with transaction handel
    def write_befor(self, tr):
        # display input on terminal using uvm_info
        uvm_info("inputs to adder ", tr.convert2string(), UVM_MEDIUM)
        # create result and store in fifo using append call from list
        self.m_sb.append(tr.int_a + tr.int_b)

    # when any transaction appier on after analysis port then 
    # this funcation called with transaction handel
    def write_after(self, tr):
        exp = 0
        # display transaction on terminal using uvm_info
        uvm_info("SB/OBS", sv.sformatf("Observed: 0x%h (item: %d)",
            tr.sum,self.m_n_obs), UVM_MEDIUM)
        # pop result from fifo using pop funcation
        exp = self.m_sb.pop(0)
        # compare the dut recive results with our model results
        if tr.sum != exp:
            # if there is any conflict then mark as error 
            self.errs += 1
            self.error = 1
            # show both the value on terminal as uvm error
            uvm_error("SB/MISMTCH", sv.sformatf("Symbol 0x%h observed instead of expected 0x%h",
                tr.sum, exp))
        #  incrment our observed trancation veriable because we resive at least one transaction regardles faulty or not
        self.m_n_obs += 1
    
    # on reset phase reset our counters and fifo
    async def reset_phase(self, phase):
        self.m_n_obs = 0
        self.m_sb = []

    # in main phase we wait for thresh hold number achive then brack main phase from scoreboard
    async def main_phase(self, phase):
        # we can hold phase by raising objection it will raised until we drop.
        phase.raise_objection(self, "Have not checked enough data")
        # wait until observed trnsaction achive thresh hold value
        while True:
            await Timer(250, "NS")
            if self.m_n_obs >= self.n_obs_thresh:
                break
        # drop the objection by calling drop_objection that will force all the uvm component to drop there phase
        phase.drop_objection(self, "Enough data has been observed")
    
    # generate error if we failed to recive thresh hold value
    def check_phase(self, phase):
        if self.m_n_obs < self.n_obs_thresh:
            uvm_error("ERR/SCB", "Not enough items were observed")
            self.error = 1
# register scorebaord as component in uvm factory
uvm_component_utils(adder_sb)