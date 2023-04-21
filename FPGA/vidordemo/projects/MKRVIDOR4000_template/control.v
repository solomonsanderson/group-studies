module control(trig, rabi_trig, clk, rf, rabi);
/* a module for generion of a raman pulse scan and pi and pi/2 pulses with an arduino MKR Vidor development board in a TE2V atom interferometer
-> when digital pin 1 is high the mach zehnder pulses are released.
-> when digital pin 3 is high the raman pulse scan is released
-> the rabi output is the raman scan and is output to digital pin 7
-> the rf output is the mach zehnder output and is output to digital pin 6
 */

	output rf;
	output rabi;
	input wire trig;
	input wire rabi_trig;
	input wire clk;

	reg count;
	reg out;
	reg rf;


	
	// square wave generation, for testing.
	/*
	integer N = 50;
	integer pulses = 0;

	always @(posedge clk) begin
		if ((counter == N)) begin
        counter <= 0;
        rf = ~ rf;
		  pulses += 1; 
		end else begin
        counter <= counter + 1;
		end
	end 
	*/


// mach zehnder pulses settings 
	reg[3:0] state = 0;
	reg[31:0] counter = 0; // need this to be at least 17 bit as wait for intervals is larger than 16 bit number 
	
	reg[31:0] before_interval = 33300; // sets the wait time after trigger to emit
	reg[31:0] interval = 33300; // change integer here to set interval between pulses, T. 
	reg[31:0] pi_pulse = 666; // change this integer to set the length of the pi pulse, pi_2 is calculated automatically
	reg[31:0] pi_2_pulse; // automatically calculated
	reg[31:0] after_interval = 33300; // sets the time for which nothing happens after the sequence
	
	
// raman pulse scan sequence settings 
	reg[31:0] pulse_length = 66; // sets the initial pulse length for the raman pulse scan to start at
	reg[32:0] pulse_increment =66; // amount to increment pulse by each time
	reg[31:0] r_counter;
	reg[7:0] r_state = 0;
	
	always @(posedge clk) begin
		if (trig == 1) begin // if the trigger pin (digital pin 7) is high the sequence runs 
			counter <= counter + 1;
			case (state)
				0: begin // idle state
					rf <= 0;
					if (counter >= before_interval) begin // change 33300 to change length of interval, this is approx 5 micro seconds
						counter <= 0;
						state <= 1;
					end
				end
				1: begin // first pulse state
					rf <= 1;
					if (counter >= pi_2_pulse) begin // change integer here to set length of pulse
						counter <= 0;
						state <= 2;
					end
				end
				2: begin // pause state
					rf <= 0;
					if (counter >= interval) begin 
						counter <= 0;
						state <= 3;
					end
				end
				3: begin // second pulse state
					rf <= 1;
					if (counter >= pi_pulse) begin 
						counter <= 0;
						state <= 4;
					end
				end
				4: begin // third pulse state
					rf <= 0;
					if (counter >= interval) begin
						counter <= 0;
						state <= 5;
					end
				end
				5: begin // final pulse state
					rf <= 1;
					if (counter >= pi_2_pulse) begin
					  rf <= 0;
					  state <= 6;
					  counter <= 0;
					end
				end
				6: begin // end delay to allow arduino pin to change
						if (counter >= after_interval) begin
							rf <= 0; 
							state <= 0;
							counter <= 0;
						end
					end
			endcase
	end else if (rabi == 1) begin
	 // probably dont need a pin to select the rabi script, just use trigger pin 
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
						if (r_counter >= (pulse_length)) begin
							pulse_length <= pulse_length + 66; // increase pulse length with each pulse
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
				endcase
		end
	end
	initial begin 
		// mach zehnder initial state
		rf <= 0;
		counter <= 0;
		pi_2_pulse <= pi_pulse/2;
		
		
	end
endmodule
	



