 	module simulation(rf, rabi, counter);
/*	initial begin
		control_testbench(trig, clk, rf);
	end
	
	output rf;
	input clk;
	input trig;
*/
		output rf;
		output counter;
		output rabi;
		reg rabi_trig = 0; 
		reg trig;
		reg clk;
		reg rf;
		reg rabi;
		//integer counter; 
		integer pi_2;
		integer interval;
		integer pi;
		
		integer mz_start_time;
		integer pi_start;
		integer interval_2_start;
		integer second_pi_2_start;
		integer end_time;
		//parameter PULSE_LENGTH = 10;
		
		//reg[7:0] pi_start
		
		reg[4:0] state = 0;
		reg[16:0] counter = 0;
		
		
		always begin 
			#5000 clk = ~clk;  // flips the clock value every 5 counts to simulate clock 
			
					counter <= counter + 1;

					case (state)
						0: begin // idle state
							rf <= 0;
							if (counter >= 1000) begin
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
							if (counter >= 1000) begin
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
							if (counter >= 1000) begin
								counter <= 0;
								state <= 5;
							end
						end
						5: begin // final pulse state
							rf <= 1;
							if (counter >= 333) begin
							  counter <= 0;
							  state <= 0;
							end
						end
				endcase
		end
	

		reg[7:0] r_state = 0;
		reg[31:0] r_counter = 0;
		reg[31:0] pulse_length = 10;

		always begin // probably dont need a pin to select the rabi script, just use trigger pin 
			#100000 rabi_trig = ~rabi_trig;
				case (r_state)
					0: begin // idle state
						$display("rabi idle");
						rabi <= 0; 
						if (rabi_trig) begin // when pulse release pin is trigd, should only need a fixed trigger pulse length as should run till pulse is ended 
							r_state <= 1;
						end
					end
					1: begin // pulse state 
						$display("rabi pulse");
						r_counter <= r_counter + 1; // increment r_counter when trig pin is high
						rabi <= 1; // set high 
						if (r_counter >= (pulse_length - 10)) begin
							pulse_length <= pulse_length + 10; // increase pulse length with each pulse
							r_counter <= 0; // reset counter
							r_state <= 2; // reset state, change this to 2 if we add delay after
						end
					end
					2: begin // wait state
						if (rabi_trig == 0) begin 
							r_state <= 0; // only go back to state 0 when trig is off
						end 
						else begin
							r_counter <= r_counter + 1;
						end
					end 
					// could add 3rd state to add short interval after pulses to account for arduino delay in changing pin state.
				endcase
		end	

		
	initial begin 
		$monitor("Time =%0t clk = %0d rf = %0d counter = %0d", $time, clk, rf, counter);
		rf = 0;
		counter = 0;
		clk = 0;
		
		pi_2 = 10;
		interval = 20;
		pi = 20;
		mz_start_time = 10;

		//reg[7:0] pi_start;
		pi_start = mz_start_time + pi_2 + interval; // 30
		interval_2_start = mz_start_time + pi_2 + interval + pi; // 50
		second_pi_2_start = mz_start_time + pi_2 + pi + (2 * interval); // 70
		end_time = second_pi_2_start + pi_2;
		$display("interval 2 start = %0d, pi start = %0d, second pi_2 start= %0d", interval_2_start, pi_start, second_pi_2_start);
		
		
		#100 rabi_trig = 1;
		#1000 rabi_trig = 0;
		#100 rabi_trig = 1;
		#1000 rabi_trig = 0;
		#100 rabi_trig = 1;
		#1000 rabi_trig = 0;
	end
	

endmodule