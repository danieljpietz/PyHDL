-- Generated using pyhdl2 version 0.2a on 01/07/2022 at 22:00:20 

library IEEE;
use IEEE.std_logic_1164.all;
library work;
use work.MyPackage.all;

entity GettingStarted is
	port (
		clk : in std_logic;
		output : out std_logic);
end entity GettingStarted;

architecture GettingStarted_rtl of GettingStarted is
	signal record_signal : MyRecord := (v => '1', rst => '0');
	signal sig1 : std_logic := '0';
	constant my_other_const : std_logic := '1';
begin
	my_process : process (clk)
	begin
		my_if : if rising_edge(clk);
			then
			 sig1 <= MyConstant;
			output <= sig1;

		end if my_if;
	end process my_process;
end architecture GettingStarted_rtl;
