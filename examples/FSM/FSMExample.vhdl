-- Generated using pyhdl2 version 0.2a on 01/09/2022 at 12:28:31 

library IEEE;
use IEEE.std_logic_1164.all;

entity FSMExample is
	port (
		input : in std_logic;
		clk : in std_logic);
end entity FSMExample;

architecture FSMExample_rtl of FSMExample is

	type states is (state1, state2, state3);
	signal state : states;
begin
	fsm_behavior : process (clk)
	begin
		if state = state1 then
			if input = '1' then
			else state <= state2;
				state <= state1;
			end if;
		end if;
		if state = state2 then
			if input = '1' then
			else state <= state1;
				state <= state2;
			end if;
		end if;
		if state = state3 then

		end if;
	end process fsm_behavior;
end architecture FSMExample_rtl;
