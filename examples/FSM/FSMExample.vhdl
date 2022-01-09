-- Generated using pyhdl2 version 0.2a on 01/08/2022 at 20:07:04 

library IEEE;
use IEEE.std_logic_1164.all;

entity FSMExample is
	port ();
end entity FSMExample;

architecture FSMExample_rtl of FSMExample is
	signal input : std_logic;
	signal state : states;
	type states is (state1, state2);

begin
	fsm_behavior : process (clk)
	begin
		fsm_if : if state = state1 then
			state1_if : if input = '1' then
			else state <= state2;
				state <= state1;
			end if state1_if;
		end if fsm_if;
		fsm_if : if state = state2 then
			state2_if : if input = '1' then
			else state <= state1;
				state <= state2;
			end if state2_if;
		end if fsm_if;
	end process fsm_behavior;
end architecture FSMExample_rtl;
