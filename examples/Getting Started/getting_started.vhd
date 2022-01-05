-- Generated using pyhdl2 version 0.2a on 01/05/2022 at 11:56:15 

library IEEE;
use IEEE.std_logic_1164.all;

entity ExampleEntity is
	port (
		clk : in std_logic;
		output : out std_logic);
end entity ExampleEntity;

architecture rtl of ExampleEntity is

	type MyRecord is record
		v : std_logic;
		rst : std_logic;
	end record MyRecord;

	signal record_signal : MyRecord := (v => '1', rst => '0');
	signal sig1 : std_logic := '0';

begin
	my_process : process (clk)
	begin

		my_if : if clk = '1' then
			sig1 <= not sig1;
			output <= sig1;
		end if my_if;
	end process;
end architecture rtl;
