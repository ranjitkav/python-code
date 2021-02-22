import json
import yaml
import os

# remove any blanklines in file
def removeblanklines(file):
  outfile = "C:\\python\\my-python\\test4.yaml"   # change this to the output file name
  with open(file,"r+") as fd:
      with open(outfile,"w+") as fout:
         line = fd.readline()
         while line:
            if not line.isspace() and "'" not in line:
              fout.write(line)
            line = fd.readline()
      fd.close()
      os.remove(file)
      os.rename("C:\\python\\my-python\\test4.yaml", "C:\\python\\my-python\\test3.yaml")  # change this

def json2yaml(file):
    outfile = "C:\\python\\my-python\\test3.yaml"  # change this
    with open(outfile,"w+") as fd:
        fd.write(yaml.safe_dump(json.load(file),default_flow_style=False))
        fd.close()
        removeblanklines(outfile)

# to control execution of code
if __name__ == "__main__":
    with open("C:\\python\\my-python\\cloudformation.json", "r") as fd:  # input json
       json2yaml(fd)