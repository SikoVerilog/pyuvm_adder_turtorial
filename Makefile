# This file is public domain, it can be freely copied without restrictions.
# SPDX-License-Identifier: CC0-1.0

TOPLEVEL_LANG ?= verilog
SIM ?= icarus

PWD=$(shell pwd)


ifeq ($(TOPLEVEL_LANG),verilog)
    # Dut file
    VERILOG_SOURCES = $(PWD)/adder.sv

    ifneq ($(filter $(SIM),riviera activehdl),)
        COMPILE_ARGS += -sv2k12
    endif
else
    $(error "A valid value (verilog) was not provided for TOPLEVEL_LANG=$(TOPLEVEL_LANG)")
endif

# Fix the seed to ensure deterministic tests
export RANDOM_SEED := 123456789

TOPLEVEL    := adder
MODULE      := tb_top
PLUSARGS    += +UVM_TESTNAME=test
COCOTB_RESULTS_FILE = results.xml

include $(shell cocotb-config --makefiles)/Makefile.sim


# Profiling

DOT_BINARY ?= dot

test_profile.pstat: sim

callgraph.svg: test_profile.pstat
	$(shell cocotb-config --python-bin) -m gprof2dot -f pstats ./$< | $(DOT_BINARY) -Tsvg -o $@

.PHONY: profile
profile:
	COCOTB_ENABLE_PROFILING=1 $(MAKE) callgraph.svg
