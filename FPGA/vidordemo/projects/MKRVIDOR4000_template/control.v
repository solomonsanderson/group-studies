module control(trig, clk, rf);
  
input trig; // trigger input
input clk; // fpga clock as input
output rf; // outputs to rf controller


integer counter = 0; 
integer pi_2 = 333;  // this changes the frequency, it is the number of clock cycles for which the pin is low or high. 
integer pi; // sets pi pulse to be twice the length of the pi over 2 
assign pi = pi_2 * 2;

integer square_count = 0; // counts the number of switches between high and low. 
integer short_counter = 0;
integer interval_count = 0;
integer pi_count = 0; 

always @(posedge clk) begin

	// pi/2 pulse
	if (square_count == 0) begin // if at zero generate pi/2 pulse
		
		if (short_counter == 0) begin  // if the counter for the pi/2 pulse is zero, flip. 
			rf <= 1'b1; // flip to high 
		end
		
		else if (short_counter == pi_2) begin //when at pi_2 length flip and increment squares
			rf <= 1'b0;  // flip to low 
			short_counter <= 0; // reset the short counter			
			square_count <= square_count + 1; // increment count of squares
		end
		
		else begin //incrementing
			short_counter <= short_counter + 1;
		end 
	end
		
	// interval
	else if ( 0 < square_count < 201) begin
		rf <= 1'b0;
		if (interval_count == pi_2) begin
			// rf <= ~rf; // should already be low
			square_count <= square_count + 1;
			interval_count <= 0; // reset when one square is complete
		
		end else begin
			interval_count <= interval_count + 1; //counting to make square
		end 
		
	end
	
	
	
	// pi pulse
	else if (square_count == 201) begin
		if (pi_count == 0) begin
		rf <= 1'b1;
		end
		else if (pi_count == pi) begin
			rf <= 1'b0;
			square_count <= square_count + 2; //we add 2 as the pi pulse is twice the length of our normal pulses
			pi_count = 0;
		end else begin 
			pi_count <= pi_count + 1; 
		end
		
		
	end
	
	
	// interval

	
	// pi/2 pulse
	
	//else if
	

end
endmodule

