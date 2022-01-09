-- Generated using pyhdl2 version 0.2a on 01/07/2022 at 08:36:59 

entity Array2DExample is
	port ();
end entity Array2DExample;

architecture Array2DExample_rtl of Array2DExample is
	signal sig1 : matrix_3x3;
	signal sig2 : matrix_3x3;
	signal tensor : tensor_3x2x3;
	signal sig3 : matrix_3x3;
	type tensor_3x2x3 is array of matrix_3x2 (3 downto 0);
	type matrix_3x3 is array of vector3 (3 downto 0);
	type matrix_3x2 is array of vector3 (2 downto 0);
	type vector3 is array of integer (3 downto 0);

begin
	tensor(0)(0)(0) <= sig1(0)(0);
	tensor(0)(0)(1) <= sig1(0)(1);
	tensor(0)(0)(2) <= sig1(0)(2);
	tensor(0)(1)(0) <= sig2(0)(0);
	tensor(0)(1)(1) <= sig2(1)(0);
	tensor(0)(1)(2) <= sig2(2)(0);
	tensor(1)(0)(0) <= sig1(1)(0);
	tensor(1)(0)(1) <= sig1(1)(1);
	tensor(1)(0)(2) <= sig1(1)(2);
	tensor(1)(1)(0) <= sig2(0)(1);
	tensor(1)(1)(1) <= sig2(1)(1);
	tensor(1)(1)(2) <= sig2(2)(1);
	tensor(2)(0)(0) <= sig1(2)(0);
	tensor(2)(0)(1) <= sig1(2)(1);
	tensor(2)(0)(2) <= sig1(2)(2);
	tensor(2)(1)(0) <= sig2(0)(2);
	tensor(2)(1)(1) <= sig2(1)(2);
	tensor(2)(1)(2) <= sig2(2)(2);
end architecture Array2DExample_rtl;
