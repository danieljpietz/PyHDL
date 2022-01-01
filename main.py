from pyhdl2 import Module
from MyPYHDLProject import MyEntity, MyArchitecture


M = Module(MyEntity, MyArchitecture, "test_project.vhd")

M.writeout()

