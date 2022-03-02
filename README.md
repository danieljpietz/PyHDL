# PyHDL
![Tests](https://github.com/mCodingLLC/SlapThatLikeButton-TestingStarterProject/actions/workflows/tests.yml/badge.svg)

PyHDL aims to **_Accelerate_** the hardware design process by providing high-level Python objects to represent constructs in HDL's.

These objects can then be operated on in Python to produce an HDL output.

## Examples

### Creating a basic project

To start a project, import pyhdl2 into your enviroment and create an object that inherits **Module** and is decorated by _module_. We can use the _write_out_ function to produce the a VHDL output.


<table>
<tr>
<th>PyHDL</th>
<th>VHDL</th>
</tr>
<tr>
<td>

``` python
from pyhdl2 import *

@module
class GettingStarted(Module):
    pass

write_out("getting_started.vhd", GettingStarted)

```
</td>
<td>

``` vhdl
-- Generated using pyhdl2 version 0.2a on 03/02/2022 at 09:19:07 

entity GettingStarted is
end entity GettingStarted;

architecture GettingStarted_rtl of GettingStarted is

begin

end architecture GettingStarted_rtl;

```

</td>
</tr>
</table>


### Ports and Signals

Ports and signals can be added to a module by giving our class **PortSignal** and **Signal** properties.

<table>
<tr>
<th>PyHDL</th>
<th>VHDL</th>
</tr>
<tr>
<td>

``` python
from pyhdl2 import *

@module
class GettingStarted(Module):
    clk = PortSignal('clk', std_logic, Direction.In)
    output = PortSignal('output', std_logic, Direction.Out)
    my_signal = Signal('my_signal', std_logic)

write_out("getting_started.vhd", GettingStarted)

```
</td>
<td>

``` vhdl
-- Generated using pyhdl2 version 0.2a on 03/02/2022 at 09:31:50 

library IEEE;
use IEEE.std_logic_1164.all;

entity GettingStarted is
	port (
		clk : in std_logic;
		output : out std_logic);
end entity GettingStarted;

architecture GettingStarted_rtl of GettingStarted is
	signal my_signal : std_logic;
begin

end architecture GettingStarted_rtl;

```

</td>
</tr>
</table>

When using types from an external library, PyHDL will manage library management.

### Concurrent Statements and Processes

Processes can be included by adding functions to our class that have the _process_ decorator. Edge detection can be done using either an PyHDL if statement or the _RISING_EDGE_ decorator macro that has been included for convenience.

<table>
<tr>
<th>PyHDL</th>
<th>VHDL</th>
</tr>
<tr>
<td>

``` python
from pyhdl2 import *


@module
class GettingStarted(Module):
    clk = PortSignal("clk", std_logic, Direction.In)
    output = PortSignal("output", std_logic, Direction.Out)
    my_signal = Signal("my_signal", std_logic)
    vector = Signal("vector", std_logic_vector(0, 10))

    @process(clk)
    def my_process(self):
        @IF(rising_edge(self.clk))
        def my_if():
            self.my_signal.next = self.clk

    @RISING_EDGE(clk)
    def my_other_process(self):
        for item in self.vector:
            item.next = self.clk


write_out("getting_started.vhd", GettingStarted)
```
</td>
<td>

``` vhdl
-- Generated using pyhdl2 version 0.2a on 03/02/2022 at 09:35:38 

-- Generated using pyhdl2 version 0.2a on 03/02/2022 at 09:39:30 

library IEEE;
use IEEE.std_logic_1164.all;

entity GettingStarted is
	port (
		clk : in std_logic;
		output : out std_logic);
end entity GettingStarted;

architecture GettingStarted_rtl of GettingStarted is
	signal my_signal : std_logic;
	signal vector : std_logic_vector (0 to 10);
begin
	my_process : process (clk)
	begin
		if rising_edge(clk) then
			 my_signal <= clk;
		end if;
	end process my_process;
	my_other_process : process (clk)
	begin
		if rising_edge(clk) then
			vector(0) <= clk;
			vector(1) <= clk;
			vector(2) <= clk;
			vector(3) <= clk;
			vector(4) <= clk;
			vector(5) <= clk;
			vector(6) <= clk;
			vector(7) <= clk;
			vector(8) <= clk;
			vector(9) <= clk;
			vector(10) <= clk;
		end if;
	end process my_other_process;
end architecture GettingStarted_rtl;



```

</td>
</tr>
</table>

Code Beautifier adapted from https://github.com/g2384/VHDLFormatter
