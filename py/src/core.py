
from os import curdir
from select import select
from tokenize import String
from unicodedata import name
import yaml
from fuzzywuzzy import fuzz
from pathlib import Path
# the abstraction of each register.

class Reg:
    """ fields were like <name:[begin:end]>"""
    def __init__(self,name,types,fields:dict):
        self.name = name
        self.types = types
        self.fields = fields


# parse the yaml file
class ParserReg:
    def __init__(self):
        self.MCU = "For mother 51"
        self.version = "8.9.6.4"
        self.type = '64'
        self.registers = {}
        pass
    def ls_regs(self):
        for name in self.registers.keys():
            print(name)
    
    # parse from yaml file to a dict
    # dict content were {"name": RegObject} 
    def parse_file(self,file_path):
        with open(file_path,'r') as f:
            data = yaml.load(f,yaml.FullLoader)
            self.MCU = data["MCU"]
            self.version = data["version"]
            self.type = data['type']
            for r_item in data["registers"]:
                reg_name = r_item['reg']
                # for f_item in r_item["fields"]:
                #     field_dict.update({f_item['field']:f_item['pos']})
                self.registers.update({reg_name:Reg(reg_name,self.type,r_item["fields"])})
                #print(self.registers)
                
                    
    # test func for understand how to use yaml

    # def test(self):
    #     prj_dir = Path(__file__).parent.parent
    #     with open(str(prj_dir)+"/cnf/xw32.yaml", 'r') as f:
    #         data = yaml.load(f,yaml.FullLoader)
    #         self.MCU = data["MCU"]
    #         self.version = data["version"]
    #         self.type = data['type']
    #         for reg in data["registers"]:
    #             field_dict={}
    #             reg_name = reg['reg']
    #             for item in reg["fields"]:
    #                 field_dict.update({item['field']:item['pos']})
    #             self.registers.update({reg_name:Reg(reg_name,self.type,field_dict)})
            
        
def fuzzy_search(name, regs:dict):
    print("SEARCH REGISTER | "+name)
    print("--------------------------------")
    # gen a  map of {reg:similar ratio} in dict
    reg_ratio_dic = {reg:fuzz.ratio(name,reg) for reg in regs.keys() if fuzz.ratio(name,reg)>60}
    # got the potential list of match our reg
    reg_p_list=sorted(reg_ratio_dic.items(),key=lambda x:x[1],reverse=True)
    print("OPTIONS         | ")
    for (reg,_) in reg_p_list:
        print("                |"+reg)

    
    
           
# calc reg and show the content.
class Calculator:
    def __init__(self):
        pass
    def setup(self, raw: int, regdef: Reg):
        self.regdef = regdef
        self.regval = raw
        self.res = []
        self.res.append("Register: "+ self.regdef.name+"\n")
    
    def show(self):
        print("Register--->"+ self.regdef.name)
        for msg in self.calc():
            print(msg) 

    def calc(self):
        """generate each field value of each regsister"""
        bin_list = self.bin_format() # convert the reg value to bin format
        for field_name, pos_def in self.regdef.fields.items():
            begin_pos = pos_def[0]
            end_pos = pos_def[1]+1
            bin_val = bin_list[begin_pos:end_pos]
            bin_val.reverse()
            bin_str="".join(bin_val)
            int_str= str(int(bin_str,2))
            hex_str = hex(int(bin_str,2))
            yield field_name+": 0d" + int_str + " " + hex_str + " 0b" + bin_str
    
    def to_bin(self):   
        return bin(self.regval)
    
    def bin_format(self):
        """generate a bin list to handle in the next phase """
        if self.regdef.types == "u32":
            s_list = [c for c in bin(self.regval)[2:].zfill(32)]
        elif self.regdef.types == "u64":
            s_list = [c for c in bin(self.regval)[2:].zfill(64)]
        else:
            raise Exception(self.regdef.types+ "were not support")
        s_list.reverse()
        return s_list

                


if __name__ == '__main__':
    file_path = str(Path(__file__).parent)
    
    p = ParserReg()
    c=Calculator()
    p.parse_file(file_path+"/../cnf/tc27x.yaml")
    print(p.registers["VADC_CLC"].fields)
    c.setup(0x102799,p.registers["VADC_CLC"])
    c.show()
    
    # p.test()
    # fuzzy_search("SP",p.registers)
    

