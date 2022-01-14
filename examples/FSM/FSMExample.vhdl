-- Generated using pyhdl2 version 0.2a on 01/14/2022 at 15:52:30 

library IEEE;
use IEEE.std_logic_1164.all;

entity FSMExample is
	port (clk : in std_logic);
end entity FSMExample;

architecture FSMExample_rtl of FSMExample is

	type states is (state1, state2, state3);
	signal state : states;
begin
	fsm_behavior : process (clk)
	begin
	if state = state1 then
	end if;
	if state = state2 then
	end if;
	if state = state3 then
	end if;
end process fsm_behavior;
end architecture FSMExample_rtl;

