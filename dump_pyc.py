import marshal
import dis
import types

with open(r"dispatch\__pycache__\views.cpython-314.pyc", "rb") as f:
    f.read(16)
    code = marshal.load(f)

for item in code.co_consts:
    if isinstance(item, types.CodeType):
        print()
        print("=" * 70)
        print(f"FUNCTION: {item.co_name}")
        print("=" * 70)
        dis.dis(item)
