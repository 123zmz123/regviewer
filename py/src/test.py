from core import Reg
from core import Calculator


def test_field_gen():
    fields_def = {
        "f0":[0,2],
        "f1":[3,7],
        "f2":[8,11],
        "reserved":[12,63],
    }
    
    reg1 = Reg("SSPN","u32",fields_def)
    
    calc = Calculator()
    calc.setup(0x00002367,reg1)
    
    print(calc.to_bin())
    for showit in calc.calc():
        print(showit) 
    


    


if __name__ == '__main__':
    test_field_gen()
    