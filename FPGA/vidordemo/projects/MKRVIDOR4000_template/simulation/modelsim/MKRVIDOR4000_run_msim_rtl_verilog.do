transcript on
if ![file isdirectory verilog_libs] {
	file mkdir verilog_libs
}

vlib verilog_libs/altera_ver
vmap altera_ver ./verilog_libs/altera_ver
vlog -vlog01compat -work altera_ver {c:/intelfpga_lite/22.1std/quartus/eda/sim_lib/altera_primitives.v}

vlib verilog_libs/lpm_ver
vmap lpm_ver ./verilog_libs/lpm_ver
vlog -vlog01compat -work lpm_ver {c:/intelfpga_lite/22.1std/quartus/eda/sim_lib/220model.v}

vlib verilog_libs/sgate_ver
vmap sgate_ver ./verilog_libs/sgate_ver
vlog -vlog01compat -work sgate_ver {c:/intelfpga_lite/22.1std/quartus/eda/sim_lib/sgate.v}

vlib verilog_libs/altera_mf_ver
vmap altera_mf_ver ./verilog_libs/altera_mf_ver
vlog -vlog01compat -work altera_mf_ver {c:/intelfpga_lite/22.1std/quartus/eda/sim_lib/altera_mf.v}

vlib verilog_libs/altera_lnsim_ver
vmap altera_lnsim_ver ./verilog_libs/altera_lnsim_ver
vlog -sv -work altera_lnsim_ver {c:/intelfpga_lite/22.1std/quartus/eda/sim_lib/altera_lnsim.sv}

vlib verilog_libs/cyclone10lp_ver
vmap cyclone10lp_ver ./verilog_libs/cyclone10lp_ver
vlog -vlog01compat -work cyclone10lp_ver {c:/intelfpga_lite/22.1std/quartus/eda/sim_lib/cyclone10lp_atoms.v}

if {[file exists rtl_work]} {
	vdel -lib rtl_work -all
}
vlib rtl_work
vmap work rtl_work

vlog -sv -work work +incdir+C:/Users/Solom/OneDrive/Desktop/Control/FPGA/vidordemo/ip/SYSTEM_PLL {C:/Users/Solom/OneDrive/Desktop/Control/FPGA/vidordemo/ip/SYSTEM_PLL/SYSTEM_PLL.v}
vlog -sv -work work +incdir+C:/Users/Solom/OneDrive/Desktop/Control/FPGA/vidordemo/projects/MKRVIDOR4000_template {C:/Users/Solom/OneDrive/Desktop/Control/FPGA/vidordemo/projects/MKRVIDOR4000_template/MKRVIDOR4000_top.v}
vlog -sv -work work +incdir+C:/Users/Solom/OneDrive/Desktop/Control/FPGA/vidordemo/projects/MKRVIDOR4000_template {C:/Users/Solom/OneDrive/Desktop/Control/FPGA/vidordemo/projects/MKRVIDOR4000_template/control.v}
vlog -sv -work work +incdir+C:/Users/Solom/OneDrive/Desktop/Control/FPGA/vidordemo/projects/MKRVIDOR4000_template/db {C:/Users/Solom/OneDrive/Desktop/Control/FPGA/vidordemo/projects/MKRVIDOR4000_template/db/system_pll_altpll.v}

vlog -sv -work work +incdir+C:/Users/Solom/OneDrive/Desktop/Control/FPGA/vidordemo/projects/MKRVIDOR4000_template {C:/Users/Solom/OneDrive/Desktop/Control/FPGA/vidordemo/projects/MKRVIDOR4000_template/control.v}

vsim -t 1ps -L altera_ver -L lpm_ver -L sgate_ver -L altera_mf_ver -L altera_lnsim_ver -L cyclone10lp_ver -L rtl_work -L work -voptargs="+acc"  control_test

add wave *
view structure
view signals
run -all
