from cmd2 import Cmd
from cmd2 import style
from cmd2 import Fg,Bg
from core import ParserReg,Calculator
from pathlib import Path
import os

class App(Cmd):
    def __init__(self) -> None:
        super().__init__()
        self.cc = style("this is the command line tool of calculator register content",
                           fg=Fg.RED,bg=Bg.WHITE,bold=True)
        self.cnf_no_exist_msg = style("cnf folder were not exist ./cnf or ../cnf where is it? pls check you setup",fg=Fg.RED,bold=True)

        self.cnf_file_no_exist_msg = style("u specified file were not exist",fg=Fg.RED,bold=True)
        
        self.cnf_parse_succeed_msg = style("the cnfiguration file load succeed",fg=Fg.GREEN,bold=True)

        self.regs_empty_msg= style("the the registers were empty pls consider ldcnf file",fg=Fg.RED,bold=True)

        self.intro = style("workflow\n \
                           1. list configuration file by lscnf\n \
                           2. load configuration file by ldcnf file_name\n \
                           3. fuzzy search register name by sech register_name\n \
                           4. choose the register and use calc register_name rawvalue to see the field value\n\
                            4.1 example input calc FUE 0x19890604\n \
                           ",fg=Fg.GREEN,bold=True)
        
        self.parser = ParserReg()
        self.calculator = Calculator()
        self.cnf_dir = Path()
        
    # list configuration file command
    def do_lscnf(self,_):
        script_path = Path(__file__).parent
        # lev1 and lev2 means we have 2 way to store configuration files
        lev1_path = script_path.joinpath("cnf")
        lev2_path = script_path.parent.joinpath("cnf")

        if(lev1_path.exists()):
            self.cnf_dir = lev1_path
            for item in os.listdir(lev1_path):
                print(item)
        elif(lev2_path.exists()):
            self.cnf_dir = lev2_path
            for item in os.listdir(lev2_path):
                print(item)
        else:
            self.poutput(self.cnf_no_exist_msg)

    # load configuration command
    def do_ldcnf(self,arg):
        cnf_file=self.cnf_dir.joinpath(arg)
        if(cnf_file.exists()):
            if(self.parser.parse_file(cnf_file)):
                self.poutput(self.cnf_parse_succeed_msg)
        else:
            self.poutput(self.cnf_file_no_exist_msg)
    
    def do_lsreg(self,_):
        if(len(self.parser.registers)!=0):
            self.parser.ls_regs()
        else:
            self.poutput(self.regs_empty_msg)
    
    # fuzzy search command
    def do_fuzzy(self,arg):
        pass
    # calc command 
    def do_calc(self,arg):
        pass
    
    
if __name__ == '__main__':
    app = App()
    app.cmdloop()