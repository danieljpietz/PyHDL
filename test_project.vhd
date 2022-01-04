-- Generated using pyhdl2 version 0.1a on 01/03/2022 at 11:48:31 

library IEEE;
use IEEE.std_logic_1164.all;

entity MyEntity is
	 port (clk : in std_logic;
		   input : in std_logic;
		   output : out std_logic);
end entity MyEntity;

architecture rtl of MyEntity is

	signal sig_vec : std_logic_vector (4 downto 0);

begin
	my_process: process (clk)
	begin 
	
		first_if: if clk then 
			sig_vec(0) <= sig_vec(3);
			sig_vec(1) <= sig_vec(0);
			sig_vec(2) <= sig_vec(1);
			sig_vec(3) <= input; 
			end if first_if;
	end process;
end architecture rtl;