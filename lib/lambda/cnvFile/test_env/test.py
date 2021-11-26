import calculation as clc
import os


def test():
    dl_path = './test.png'
    up_path = './out.png'
    clc.call_by_object(up_path, dl_path)
    
    return


test()

