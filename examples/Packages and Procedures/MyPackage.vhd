package MyPackage is
	procedure MyProcedure (a : in std_logic;
	b : in std_logic;
	c : out std_logic) is
	signal sig : std_logic;
begin
	my_if : if a then
		 c <= a and b;
	else c <= a or b;
	end if my_if;
end procedure MyProcedure;

function myFunction (arg1 : std_logic) return std_logic is
begin
	return arg1;
end myFunction;
end package MyPackage;
