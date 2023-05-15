from lxml import etree,objectify
from pathlib import Path
import yaml


class Reg:
    """ fields were like <name:[begin:end]>"""
    def __init__(self,name,fields:dict):
        self.fields = fields
        self.reg = name

def store_yaml(file_name,mcu, ver, typ, registers):
    #the yaml file is a abstraction of dictionary
    data = {"MCU":mcu, "version":ver, "type":typ, "registers":registers}
    prj_dir = str(Path(__file__).parent.parent)
    # store the dictionary to yaml 
    with open(prj_dir+"/cnf/"+file_name,'w') as f:
        yaml.dump(data,f)
    content=[]    
    # exlude the the useless message in primary yaml file
    with open(prj_dir+"/cnf/"+file_name,'r') as f:
        content = f.readlines()
    for idx, line in enumerate(content):
        if "- !!" in  line:
            content[idx]="-\n"        
    with open(prj_dir+"/cnf/"+file_name,'w') as f:
        f.writelines(content)

def get_stm32L0_peripharals():
    fp=Path(__file__).parent
    fp=fp.joinpath("stm32L0").joinpath("STM32L0x0.svd")
    with open(fp,'r') as f:
        svd_data = f.read()
    root = objectify.fromstring(svd_data.encode('utf-8'))
    peripharals = [p for p in root.peripherals.getchildren() if hasattr(p,"registers")]
    return peripharals
def get_field_dic(fields):
    f_dic = {}
    for field in fields:
        name = str(field.name)
        pos_begin = int(field.bitOffset)
        pos_end = int(pos_begin+field.bitWidth-1)
        f_dic.update({name:[pos_begin,pos_end]})
    return f_dic

def sniff_svd_file():
    reg_list=[]
    peripharals = get_stm32L0_peripharals()
    for p in peripharals:
        for r in p.registers.getchildren():
            reg =p.name+"_"+r.name
            fields_dic = get_field_dic(r.fields.getchildren())
            # print("===============================================")
            # print(reg)
            # print(fields_dic)
            reg_list.append(Reg(reg,fields_dic))
    return reg_list
def parse_store_svd_file():
    regs = sniff_svd_file()
    store_yaml("stm32L0.yaml","stm32L0","0.0.1","u32",regs)
            

        

if __name__ == '__main__':
    parse_store_svd_file()

    