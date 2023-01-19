
# the abstraction of each register.
from unicodedata import name


class Reg:
    """ fields were like <name:[begin:end]>"""
    def __init__(self,name,types,fields:dict):
        self.name = name
        self.types = types
        self.fields = fields



# parse the yaml file
class Parser:
    pass

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
        pass
        
        

    def calc(self):
        """generate each field value of each regsister"""
        bin_list = self.bin_format()
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
    b = ['1','1','0','1'] 
    print(b[0:1])
    

