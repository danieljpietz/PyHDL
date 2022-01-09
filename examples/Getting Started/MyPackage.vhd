package MyPackage is
	type MyRecord is record v : std_logic;
		rst : std_logic;
	end record MyRecord;
	type MyArray is array of std_logic (0 to 3);
	constant MyConstant : MyRecord := (v => '1', rst => '0');

end package MyPackage;
