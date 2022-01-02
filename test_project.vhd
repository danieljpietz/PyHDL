-- Generated using pyhdl2 version 0.1a on 01/02/2022 at 11:48:20 

library IEEE;
use IEEE.std_logic_1164.all;

entity MyEntity is
	 port (clk : in std_logic;
		   output : out std_logic);
end entity MyEntity;

architecture rtl of MyEntity is

	type MyArray is array of integer (5 downto 0);

	signal sig : integer;
	signal sig2 : integer;
	signal sig_vec : std_logic_vector (4 downto 0);
	signal custom : MyArray (5 downto 0);

begin
	my_process: process (clk)
	begin 
		sig <= sig;
		custom(0) <= custom(1);
	end process;
end architecture rtl;