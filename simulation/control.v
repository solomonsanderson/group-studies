module control(trig, rabi_trig, clk, rf, rabi);
  
input trig; // trigger input
input clk; // fpga clock as input
input rabi_trig;
output rf; // outputs to rf controller
output rabi;
reg rf;
reg rabi;

integer counter = 0; 
integer pi_2 = 333;  // this changes the frequency, it is the number of clock cycles for which the pin is low or high. 
//integer pi; // sets pi pulse to be twice the length of the pi over 2 
assign pi = pi_2 * 2;

// user inputs
integer dead_time = 5; //multiples of 5, micro seconds
integer dead_counts;
//assign dead_counts = (dead_time/5) * 333;
integer interval = 1000;
//integer interval_counts;
assign interval_counts = (interval / 5) * 333;



/*
always @(posedge clk) begin
	// deadtime at start. 
	if (counter <= dead_counts) begin
		$display("deadtime");
		assign rf = 0;
		counter <= counter + 1; 
	end 
	// pi/2 pulse 
	else if ( dead_counts < counter <= (pi_2 + dead_time)) begin 
		$display("pi/2");
		assign rf = 1;
		counter <= counter + 1;
	end 
	// first interval
	else if ((dead_counts + pi_2) < counter <= (dead_counts + pi_2 + interval_counts)) begin 
		$display("interval 1");
		assign rf = 0;
		counter <= counter + 1; 
	end 
	// pi pulse
	else if ((dead_counts + pi_2 + interval_counts) < counter <= (dead_counts + pi_2 + interval_counts + pi)) begin
		$display("pi pulse");
		assign rf = 1;
		counter <= counter + 1; 
	end
end
*/

reg[7:0] r_state = 0;
reg[31:0] r_counter = 0;
reg[31:0] pulse_length;


	
	// pi/2 pulse
	
	//else if


endmodule

module control_testbench;
 	//inputs 
	reg trig;
	reg clk; 
 	reg rf; //output
	reg rabi_trig = 0;
	
	//clock generation
	//start at time 0ns and loop after every 5ns // https://www.chipverify.com/verilog/verilog-simulation
	always #5 clk = ~clk;
	always #10 rabi_trig = ~rabi_trig;
	
	initial begin 
		$monitor("clk = %0d rf = %0d", clk, rf);
		/*rf = 0;
		#5 clk = 0;
		#15 rf = 1;
		#20 rf = 0;
		#15 rf = 1;
		#10 rf = 0;
		#10 $finish;
		#10 rabi_trig = 0;
		#50 rabi_trig = 1;
		#10 rabi_trig = 0*/
	end
	
	
	

endmodule
	



