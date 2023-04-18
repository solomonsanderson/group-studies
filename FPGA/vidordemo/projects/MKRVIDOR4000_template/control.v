module control(trig, clk, rf);
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
	//output clock;
	//output counter;
	input wire trig;
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
	
	// square wave generation.
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
	
	
	/*always @(posedge clk) begin 
		if (count == 17895697)
			begin 
				count <= 0; 
				rf <= ~rf; 
			end
		else
			begin
				count <= count + 1;
				rf <= rf;
			end
	end
	*/
	
	/*
	always @(posedge clk) begin
		case(counter)
		((mz_start_time <= counter) & (counter < (pi_2 + mz_start_time))) : rf  = 1; // first pi/2 pulse
		(( pi_start <= counter) & (counter < interval_2_start)) : rf = 1; // pi pulse
		((second_pi_2_start <= counter) & (counter < end_time)) : rf = 1; //second pi/2 pulse
		default : rf = 0;
		endcase
		counter = counter + 1; 
	end
	*/
	/*
	always @(posedge clk) begin
		counter <= counter + 1;
		if (counter == START ) begin
			rf <= 1;
		end
		if (counter == (START + PI_2)) begin 
			rf <= 0; 
		end 
	
		if (counter == (START + PI_2 + WAIT)) begin
			rf <= 1; 
		end
		
		if (counter == (START + PI_2 + WAIT + PI)) begin
			rf <= 0;
		end 
	end */ 
	
	//generating 5mus pulses every 1ms
	/*
	always @(posedge clk) begin
		if (trig == 1) begin
			counter <= counter + 1;
			if (counter == WAIT - PI) begin
				rf <= 1;
			end
			else if (counter == WAIT) begin
				rf <= 0;
				counter <= 0;
			end

	
			long_counter <= long_counter + 1;
			if (long_counter == WAIT - PI_2) begin
				rf <= 1;
			end
			else if (long_counter == WAIT) begin
				rf <= 0;
				long_counter <= 0;
			end
		end
	end*/
	/*
	always @(posedge clk) begin
		counter <= counter + 1;
	*/
	
	reg[3:0] state = 0;
	reg[31:0] counter = 0; // need this to be at least 17 bit as wait for intervals is larger than 16 bit number 
	
	always @(posedge clk) begin
    if (counter == 33) begin
        counter <= 0;
        rf <= ~ rf;
    end else begin
        counter <= counter + 1;
    end
	end
	
	/*
	always @(posedge clk) begin
		if (trig == 1) begin
			counter <= counter + 1;
			case (state)
				0: begin // idle state
					rf <= 0;
					if (counter >= 33300) begin
						counter <= 0;
						state <= 1;
					end
				end
				1: begin // first pulse state
					rf <= 1;
					if (counter >= 240) begin
						counter <= 0;
						state <= 2;
					end
				end
				2: begin // pause state
					rf <= 0;
					if (counter >= 48000) begin
						counter <= 0;
						state <= 3;
					end
				end
				3: begin // second pulse state
					rf <= 1;
					if (counter >= 480) begin
						counter <= 0;
						state <= 4;
					end
				end
				4: begin // third pulse state
					rf <= 0;
					if (counter >= 48000) begin
						counter <= 0;
						state <= 5;
					end
				end
				5: begin // final pulse state
					rf <= 1;
					if (counter >= 240) begin
					  rf <= 0;
					  state <= 6;
					  counter <= 0;
					end
					end
				6: begin // end delay to allow arduino pin to change
						if (counter >= 24000) begin
							rf <= 0; 
							state <= 0;
							counter <= 0;
						end
					end
			endcase
	 //end else begin
		//counter<=0;
	end 
end
*/	
	initial begin 
		//$monitor("Time =%0t clk = %0d rf = %0d counter = %0d", $time, clk, rf, counter);
		rf <= 0;
		counter <= 0;
		long_counter <= HALF_WAIT;
		//clk = 0;
		//clock = 0;
		//pi_2 <= 1;
		//interval <= 1;
		//pi <= pi_2 * 2;
		//mz_start_time <= 0;
		
		//out = 0;

		//reg[7:0] pi_start;
		pi_start = mz_start_time + PI_2 + interval; // 30
		interval_2_start = mz_start_time + PI_2 + interval + PI; // 50
		second_pi_2_start = mz_start_time + PI_2 + PI + (2 * interval); // 70
		end_time = second_pi_2_start + PI_2;
		//$display("interval 2 start = %0d, pi start = %0d, second pi_2 start= %0d", interval_2_start, pi_start, second_pi_2_start);
	end



endmodule
	



