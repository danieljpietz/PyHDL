-- Generated using pyhdl2 version 0.2a on 01/11/2022 at 08:01:10 

library IEEE;
use IEEE.std_logic_1164.all;

entity FSMExample is
	port (
		input : in std_logic;
		clk : in std_logic);
end entity FSMExample;

architecture FSMExample_rtl of FSMExample is

	type states is (state1);
	signal signal1 : std_logic_vector (0 to 100);
	signal state : states;
begin
	fsm_behavior : process (clk)
	begin
		if state = state1 then
			if function(); then
				signal1(0) <= '1';
				signal1(1) <= '1';
				signal1(2) <= '1';
				signal1(3) <= '1';
				signal1(4) <= '1';
				signal1(5) <= '1';
				signal1(6) <= '1';
				signal1(7) <= '1';
				signal1(8) <= '1';
				signal1(9) <= '1';
				signal1(10) <= '1';
				signal1(11) <= '1';
				signal1(12) <= '1';
				signal1(13) <= '1';
				signal1(14) <= '1';
				signal1(15) <= '1';
				signal1(16) <= '1';
				signal1(17) <= '1';
				signal1(18) <= '1';
				signal1(19) <= '1';
				signal1(20) <= '1';
				signal1(21) <= '1';
				signal1(22) <= '1';
				signal1(23) <= '1';
				signal1(24) <= '1';
				signal1(25) <= '1';
				signal1(26) <= '1';
				signal1(27) <= '1';
				signal1(28) <= '1';
				signal1(29) <= '1';
				signal1(30) <= '1';
				signal1(31) <= '1';
				signal1(32) <= '1';
				signal1(33) <= '1';
				signal1(34) <= '1';
				signal1(35) <= '1';
				signal1(36) <= '1';
				signal1(37) <= '1';
				signal1(38) <= '1';
				signal1(39) <= '1';
				signal1(40) <= '1';
				signal1(41) <= '1';
				signal1(42) <= '1';
				signal1(43) <= '1';
				signal1(44) <= '1';
				signal1(45) <= '1';
				signal1(46) <= '1';
				signal1(47) <= '1';
				signal1(48) <= '1';
				signal1(49) <= '1';
				signal1(50) <= '1';
				signal1(51) <= '1';
				signal1(52) <= '1';
				signal1(53) <= '1';
				signal1(54) <= '1';
				signal1(55) <= '1';
				signal1(56) <= '1';
				signal1(57) <= '1';
				signal1(58) <= '1';
				signal1(59) <= '1';
				signal1(60) <= '1';
				signal1(61) <= '1';
				signal1(62) <= '1';
				signal1(63) <= '1';
				signal1(64) <= '1';
				signal1(65) <= '1';
				signal1(66) <= '1';
				signal1(67) <= '1';
				signal1(68) <= '1';
				signal1(69) <= '1';
				signal1(70) <= '1';
				signal1(71) <= '1';
				signal1(72) <= '1';
				signal1(73) <= '1';
				signal1(74) <= '1';
				signal1(75) <= '1';
				signal1(76) <= '1';
				signal1(77) <= '1';
				signal1(78) <= '1';
				signal1(79) <= '1';
				signal1(80) <= '1';
				signal1(81) <= '1';
				signal1(82) <= '1';
				signal1(83) <= '1';
				signal1(84) <= '1';
				signal1(85) <= '1';
				signal1(86) <= '1';
				signal1(87) <= '1';
				signal1(88) <= '1';
				signal1(89) <= '1';
				signal1(90) <= '1';
				signal1(91) <= '1';
				signal1(92) <= '1';
				signal1(93) <= '1';
				signal1(94) <= '1';
				signal1(95) <= '1';
				signal1(96) <= '1';
				signal1(97) <= '1';
				signal1(98) <= '1';
				signal1(99) <= '1';
			end if;
		end if;
	end process fsm_behavior;
end architecture FSMExample_rtl;
