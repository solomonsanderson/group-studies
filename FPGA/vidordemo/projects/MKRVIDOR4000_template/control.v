module control(trig, clk, rf);
  
input trig; // trigger input
input clk; // fpga clock as input
output rf; // outputs to rf controller


integer counter = 0; 
integer pi_2 = 333;  // this changes the frequency, it is the number of clock cycles for which the pin is low or high. 
integer pi; // sets pi pulse to be twice the length of the pi over 2 
assign pi = pi_2 * 2;

// user inputs
integer dead_time = 5; //multiples of 5, micro seconds
assign dead_counts = (dead_time/5) * 333;
integer interval = 1000;
assign interval_counts = (interval / 5) * 333;




// always @(posedge clk) begin
// 	// deadtime at start. 
// 	if (counter <= dead_counts) begin
// 		$display("deadtime");
// 		rf = 0;
// 		counter <= counter + 1; 
// 	end 
// 	// pi/2 pulse 
// 	else if ( dead_counts < counter <= (pi_2 + dead_time)) begin 
// 		$display("pi/2");
// 		rf = 1;
// 		counter <= counter + 1;
// 	end 
// 	// first interval
// 	else if ((dead_counts + pi_2) < counter <= (dead_counts + pi_2 + interval_counts)) begin 
// 		$display("interval 1");
// 		rf = 0;
// 		counter <= counter + 1; 
// 	end 
// 	// pi pulse
// 	else if ((dead_counts + pi_2 + interval_counts) < counter <= (dead_counts + pi_2 + interval_counts + pi)) begin
// 		$display("pi pulse");
// 		rf = 1;
// 		counter <= counter + 1; 
// 	end
// end
	
	
	// interval

	
	// pi/2 pulse
	
	//else if

// 
// endmodule

module control_testbench;

 	reg trig, clk; //inputs
 	wire rf; //output
	
 	parameter sim_delay = 1;
	
 	control ctrl(trig, clk, rf);
	
 	initial begin
 		trig = 1; clk = 0;
		// creating oscillating 
 		#(sim_delay) rf = 0;
 		#(sim_delay) rf = 1;
		#(sim_delay) rf = 0;
 		#(sim_delay) rf = 1;
		#(sim_delay) rf = 0;
 		#(sim_delay) rf = 1;
		#(sim_delay) rf = 0;
 		#(sim_delay) rf = 1;
		
 	#100; //let simulation finish
	end
endmodule
	



