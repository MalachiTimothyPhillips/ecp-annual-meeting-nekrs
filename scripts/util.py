import glob
import os
import re
import numpy as np
def field_by_regex(regex,log_file_name, fieldnum = 0, returnType = float):
    with open(log_file_name) as log_file:
        content =log_file.readlines()
    content = [x.strip() for x in content]
    field=[]
    for line in content:
        m = re.search(regex,line)
        if m:
            #print(m.groups())
          try:
            field.append(returnType(m.groups()[fieldnum]))
          except:
            pass
    return field
