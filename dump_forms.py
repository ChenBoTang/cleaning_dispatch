import marshal
import dis
import types

path = r"dispatch\__pycache__\forms.cpython-314.pyc"

with open(path, "rb") as f:
    f.read(16)
    code = marshal.load(f)

print("=" * 80)
print("MODULE NAMES")
print("=" * 80)
print(code.co_names)

print("\n" + "=" * 80)
print("MODULE DISASSEMBLY")
print("=" * 80)
dis.dis(code)

for const in code.co_consts:
    if isinstance(const, types.CodeType):
        print("\n" + "=" * 80)
        print("FUNCTION / CLASS CODE:", const.co_name)
        print("=" * 80)
        print("NAMES:", const.co_names)
        print("VARNAMES:", const.co_varnames)
        dis.dis(const)