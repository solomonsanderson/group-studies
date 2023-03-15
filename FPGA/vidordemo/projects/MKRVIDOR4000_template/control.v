module control(mz_trig, rabi_trig, clk, rf, rabi);
 /*
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
assign interval_counts = (interval / 5) * 333;*/



// always @(posedge clk) begin
// 	// deadtime at start. 
// 	if (counter <= dead_counts) begin
// 		$display("deadtime");
// 		rf = 0;
// 		counter <= counter + 1; 
// 	end 
// 	// pi/2 pulse 
// 	else if ( dead_counts < counter <= (pi_2 + dead_counts)) begin 
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


	output rf;
	output rabi;
	//output clock;
	//output counter;
	input wire mz_trig;
	input wire rabi_trig;
	input wire clk;
	//reg clk;
	reg count;
	reg out;
	
	reg rf;
	//integer counter;
	integer long_counter;
	//parameter pi_2 = 5;
	parameter interval = 20;
	
	parameter mz_start_time = 0;
	integer pi_start;
	integer interval_2_start;
	integer second_pi_2_start;
	integer end_time;
	
	/*
	parameter PI = 666;
	parameter PI_2 = 333;
	parameter HALF_WAIT = 66666;
	parameter WAIT = 33333;
	parameter START = 66666;
	*/
	
	parameter PI = 666;
	parameter PI_2 = 333;
	parameter HALF_WAIT = 66666;
	parameter WAIT = 133332;
	parameter START = 66666;
		//reg[7:0] pi_start
	
	
	reg[31:0] r_counter;
	reg[31:0] pulse_length = 66; // initial pulse length is 1mus
	reg[7:0] r_state = 0; 
	
	always @(posedge clk) begin // probably dont need a pin to select the rabi script, just use trigger pin 
		case (r_state)
			0: begin // idle state
				rabi <= 0; 
				if (rabi_trig) begin // when pulse release pin is trigd, should only need a fixed trigger pulse length as should run till pulse is ended 
					r_state <= 1;
				end
			end
			1: begin // pulse state 
				r_counter <= r_counter + 1; // increment r_counter when trig pin is high
				rabi <= 1; // set high 
				if (r_counter >= pulse_length) begin
					pulse_length <= pulse_length + 66; // increase pulse length with each pulse
					r_counter <= 0; // reset counter
					r_state <= 0; // reset state, change this to 2 if we add delay after
				end
			end
			// could add 3rd state to add short interval after pulses to account for arduino delay in changing pin state.
		endcase
	end	
	
	
	reg[3:0] state = 0;
	reg[31:0] counter = 0; // need this to be at least 17 bit as wait for intervals is larger than 16 bit number 
	
	
	always @(posedge clk) begin
		counter <= counter + 1; // does this need to go in the if statement
		if (mz_trig == 1) begin
			case (state)
				0: begin // idle state
					rf <= 0;
					if (counter >= 400) begin
						counter <= 0;
						state <= 1;
					end
				end
				1: begin // first pulse state
					rf <= 1;
					if (counter >= 333) begin
						counter <= 0;
						state <= 2;
					end
				end
				2: begin // pause state
					rf <= 0;
					if (counter >= 66600) begin
						counter <= 0;
						state <= 3;
					end
				end
				3: begin // second pulse state
					rf <= 1;
					if (counter >= 666) begin
						counter <= 0;
						state <= 4;
					end
				end
				4: begin // third pulse state
					rf <= 0;
					if (counter >= 66600) begin
						counter <= 0;
						state <= 5;
					end
				end
				5: begin // final pulse state
					rf <= 1;
					if (counter >= 333) begin
					  rf <= 0;
					  state <= 6;
					  counter <= 0;
					end
					end
				6: begin // end delay to allow arduino pin to change
						if (counter >= 33300) begin
							rf <= 0; 
							state <= 0;
							counter <= 0;
						end
					end
	  endcase
	 end
end
		
	initial begin 
		rf <= 0;
		counter <= 0;
		long_counter <= HALF_WAIT;
		pi_start = mz_start_time + PI_2 + interval; // 30
		interval_2_start = mz_start_time + PI_2 + interval + PI; // 50
		second_pi_2_start = mz_start_time + PI_2 + PI + (2 * interval); // 70
		end_time = second_pi_2_start + PI_2;
	end



endmodule
	



