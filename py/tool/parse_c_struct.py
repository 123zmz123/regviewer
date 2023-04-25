from pkg_resources import fixup_namespace_packages
import yaml
from pathlib import Path
import sys
import re
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
    
# this is the entry to convert firmware to a dictionary 
# that contains the register defines
#@parameter p = the c files folder that contains the reg definitions
# we use the official firmware to generate the yaml configraution file,
# attention the developer should use this type of method to generate all the regs defines
# enjoy it! 
def conv_tc_xxx_to_dict(p,):
    pass

def exlude_comments(p):
    content=[]
    n_content=[]
    with open(p,'r') as f:
        content = f.readlines()
    n_content = map(clear_comment_tc27x,content)
    cc = [item for item in list(n_content) if item != ""]
    s = "".join(cc)
    s = s.replace("\n","")
    return s
    
# clear comment for each line
# only used to exclude tc27x official documents
def clear_comment_tc27x(line:str):
    import re
    #line start with /*
    res = re.match('^\/\*.*',line)
    if (res is not None):
        cmt = res.group(0)
        line = line.replace(cmt,"").strip()
        return line
    # line start with *
    res = re.match('^ \*.*',line)
    if (res is not None):
        cmt = res.group(0)
        line = line.replace(cmt,"").strip()
        return line
    # exclude \*xxxxx*\
    res = re.search('\/\*.*\*\/',line) 
    if(res is not None):
        cmt = res.group(0)
        line = line.replace(cmt,"").strip()    
        return line
    return line.strip()
    
def match_reg_defs_tc27D(origin_str):
    import re
    # in tc27D inf the register structs were like such pattern
    structs = re.findall('typedef struct.*?Bits;',origin_str) # .*? is the non greedy match
    if (structs.count==0): return None
    for struct_item in structs:
        # print(struct_item)
        reg = get_reg_tc27D(struct_item)
        print(reg)
        
# the function try to get reg name from the splitted strings
def get_reg_tc27D(_str):
    res = re.search('[^_]Ifx.*?Bits;',_str)
    return res.group(0)[5:-6] # delete the Ifx_ and _Bits


# the function try to get reg fields from the splitted strings
def get_fields_tc27D(_str):
    fields = re.findall('int.*?:\d+',_str)
    
    

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

def test_clear_comment():
    line = "   unsigned int U;                         /**< \brief Unsigned access */"
    clear_comment_tc27x(line)
def test_exlude_comments():
    pth= str(Path(__file__).parent)+"/tc27D/IfxEth_regdef.h"
    content = exlude_comments(pth)
    match_reg_defs_tc27D(content)
    # with open(str(Path(__file__).parent)+"/uncomment_file.h",'w') as f:
    #     f.writelines(content)
if __name__ == '__main__':
    test_exlude_comments()
    