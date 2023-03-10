import yaml
from pathlib import Path
import sys
class Reg:
    """ fields were like <name:[begin:end]>"""
    def __init__(self,name,fields:dict):
        self.fields = fields
        self.reg = name

def store_yaml(file_name,mcu, ver, typ, registers):
    data = {"MCU":mcu, "version":ver, "type":typ, "registers":registers}
    prj_dir = str(Path(__file__).parent.parent)
    with open(prj_dir+"/cnf/"+file_name,'w') as f:
        yaml.dump(data,f)
    content=[]    
    with open(prj_dir+"/cnf/"+file_name,'r') as f:
        content = f.readlines()
    for idx, line in enumerate(content):
        if "- !!" in  line:
            content[idx]="-\n"        
    with open(prj_dir+"/cnf/"+file_name,'w') as f:
        f.writelines(content)
    

def test_write():
    prj_dir = str(Path(__file__).parent.parent)
    data = {"MCU":"stm32","version":"8964","type":"u32",
    "registers":[
       {"reg":"UUCC", 
       "fields":[
           {"field":"x1", "pos":[0,1]}
       ]
       },
    ]}
    
    with open(prj_dir+"/cnf/test_cnf.yaml",'w') as f:
        yaml.dump(data,f)
        
def test_write_serialization():
    r = Reg("AA",{"s1":[2,3],"s2":[4,5]})
    r1 = Reg("AA",{"s1":[2,3],"s2":[4,5]})
    regs = [r,r1]
    store_yaml("test_cnf.yaml","MPC5744","0.1.1","u32",regs)

if __name__ == '__main__':
    test_write_serialization()
    