-- Generated using pyhdl2 version 0.2a on 01/07/2022 at 13:09:10 

entity EnumExample is
	port ();
end entity EnumExample;

architecture EnumExample_rtl of EnumExample is
	signal sig : EnumType := Option1;
	type EnumType is (Option1, Option2, Option3);

begin
	my_process : process
	begin
		state_check : if sig = Option1 then
			 sig <= Option2;

		end if state_check;
	end process my_process;
end architecture EnumExample_rtl;
