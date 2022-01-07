-- Generated using pyhdl2 version 0.2a on 01/06/2022 at 19:24:21 

library work;
use work.MyPackage.all;
library IEEE;
use IEEE.std_logic_1164.all;

entity GettingStarted is
	port (
		clk : in std_logic;
		output : out std_logic);
end entity GettingStarted;

architecture rtl of GettingStarted is

	signal record_signal : MyRecord := (v => '1', rst => '0');
	signal sig1 : std_logic := '0';
	constant my_other_const : std_logic := '1';

begin
	Test : process (clk)
	begin
		my_if : if clk = '1' then
			sig1 <= MyConstant;
			output <= sig1;
		end if my_if;
	end process;
end architecture rtl;
