
module adder (
	input logic clk, // clock signal
    input logic resetn, // reset signal
	input logic [31:0] in_a, // 32 bit wide first operant
	input logic [31:0] in_b, // 32 bit wide second operant
	input logic i_valid, // indicate the validity of the operant
	output logic o_valid, // indicate the validity of the sum
 	output logic [31:0] sum // contain the result of adder
);
	// defing all the state in localparam
	localparam IDEL = 2'h0,
			   READY = 2'h1, 
			   COMPUTE = 2'h2, 
			   SHOW = 2'h3;
	
	// state mcahine internla veriable
	reg [1:0] state_reg = IDEL, state_next = IDEL;
	
	// temprary veriables
	reg [31:0] tmp_a, tmp_b, tmp_sum;
    reg tmp_vld;

	// state machine's sequentional part
	always @(posedge clk) begin
		if (resetn == 1) 
			state_reg <= IDEL;
		else
			state_reg <= state_next;
	end

	// transition logic
	always @(*) begin
		case (state_reg)
			// after deserting reset machine state change from idel to ready 
			IDEL: state_next = resetn == 1'b1 ? IDEL : READY;
			// if input_valid signal asserted mcahine change from ready to compute
			READY: state_next = i_valid == 1'b1 ? COMPUTE : READY;
			// this state just take one cycle to compute result
			COMPUTE: state_next = SHOW;
			// this state just take one cycle ouput result
			SHOW: state_next = READY;
		endcase
	end

	//output logic
	always @(*) begin
		case (state_reg)
			// on idel state output valid deaserted
			IDEL: begin
				tmp_vld = 1'b0;
				tmp_sum = 0;
			end
			// on ready state if i_valid asserted then save in_a and in_b in
			// relevent temp veriables
			READY: begin
				tmp_vld = 1'b0;
				if (i_valid == 1'b1) begin
					tmp_a = in_a;
					tmp_b = in_b;
				end
			end
			// save sum reult of tmp_a and tmp_b in tmp_sum
			COMPUTE: begin
				tmp_vld = 1'b1;
				tmp_sum = tmp_a + tmp_b; 
			end

		endcase
	end
    assign sum = state_reg == SHOW ? tmp_sum : 0; 
    assign o_valid = state_reg == SHOW ? tmp_vld : 1'b0; 

    initial begin
        $dumpfile("wave.vcd");
        $dumpvars(0, adder);
    end
endmodule
