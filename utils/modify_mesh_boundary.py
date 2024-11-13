import re
import sys
from typing import NamedTuple
from dataclasses import dataclass
# s_without_cmnt = re.sub(r"(\/\*(.|\n)*\*\/)|(\/\/.*\n)", "", s)
r0 = r"\d[\n\S]+\([\n\S\s]*\)"
r1 = r"(?:(\S*)\n*.*{((?:[\s\n]*(?:\S+)\s+(?:[\S]+);)+[\s\n]*)})"
r2 = r"(?:[\s\n]*(\S+)\s+([\S]+);)"
@dataclass
class Property:
    name: str
    value: str
    def __str__(self):
        return f"{self.name}    {self.value};"
@dataclass
class Data:
    name: str
    properties: list[Property]
    def __str__(self):
        return f"{self.name}\n" + "{\n" +  "".join([" "*4 + str(i) + "\n"  for i in self.properties]) + "}\n"
def modify(d: Data) -> Data:
    if "wedge" in d.name:
        for p in d.properties:
            if p.name in ["type", "physicalType"]:
                p.value = "wedge"
    elif "wall" in d.name:
        for p in d.properties:
            if p.name in ["type", "physicalType"]:
                p.value = "wall"
    elif "empty" in d.name:
        for p in d.properties:
            if p.name in ["type", "physicalType"]:
                p.value = "empty"
    else:
        pass
    return d

def main():
    # s = sys.stdin.read()
    fname = sys.argv[1]
    s = open(fname, "r").read()
    lst = re.findall(r0, s)[0]
    drvs = [Data(i.groups()[0], [Property(*j.groups()) for j in list(re.finditer(r2, i.groups()[1]))]) for i in list(re.finditer(r1, lst))]
    drvs2 = [modify(d) for d in drvs]
    asd = "\n\n"+ f"{len(drvs2)}\n(\n" +"\n".join([str(i) for i in drvs2]) + "\n)\n"
    out = re.sub(r0, "", s)
    out += asd
    open(fname, "w").write(out)

if __name__ == "__main__":
    main()