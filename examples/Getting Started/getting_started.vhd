-- Generated using pyhdl2 version 0.2a on 01/04/2022 at 20:12:32 

library IEEE;
use IEEE.std_logic_1164.all;

entity ExampleEntity is
	 port (clk : in std_logic;
		   output : out std_logic);
end entity ExampleEntity;

architecture rtl of ExampleEntity is

	signal sig1 : std_logic := '0';

begin
	my_process: process (clk)
	begin 
	
		my_if: if clk = '0' then 
			output <= sig1;else if clk = '1' then 
			output <= '0';
		else if clk = '0' then 
			output <= '0';
		else  
			output <= sig1;end if my_if;
	end process;
end architecture rtl;