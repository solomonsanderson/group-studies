 	module simulation(rf, counter);
/*	initial begin
		control_testbench(trig, clk, rf);
	end
	
	output rf;
	input clk;
	input trig;
*/
		output rf;
		output counter;
		reg trig;
		reg clk;
		reg rf;
		integer counter; 
		integer pi_2;
		integer interval;
		integer pi;
		
		integer mz_start_time;
		integer pi_start;
		integer interval_2_start;
		integer second_pi_2_start;
		integer end_time;
		parameter PULSE_LENGTH = 10;
		
		//reg[7:0] pi_start
		
		
		
		
		always begin 
			#5000 clk = ~clk;  // flips the clock value every 5 counts to simulate clock 
			//counter = counter + 1;
			
			/*
			
			if ((mz_start_time <= counter) & (counter < (pi_2 + mz_start_time))) begin // first pi/2 pulse
				$display("pi/2 1");
				rf = 1;
			end
		

			else if (( pi_start <= counter) & (counter < interval_2_start)) begin // pi pulse
				$display("pi");
				rf = 1; 
			end
			
			
			else if ((second_pi_2_start <= counter) & (counter < end_time)) begin// second pi/2 plse
				$display("pi/2 2");
				rf = 1;
			end
			
			else begin 
				rf = 0;
			end
			*/
				counter <= counter + 1;
				if (counter == PULSE_LENGTH - 2) begin
					rf <= 1;
				end
				else if (counter == PULSE_LENGTH) begin
					rf <= 0;
					counter <= 0;
				end
			end 
	
			
			/*
			$display((1 <= counter) & (counter <= pi_2));
			if ((1 <= counter) & (counter <= pi_2)) begin
				$display("pi/2");
				rf = 1;
			end
			else begin 
				rf = 0;
			end
		end
		*/
		
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

	end
	

endmodule