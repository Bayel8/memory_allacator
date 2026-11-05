from buddy import Buddy
from memsim import load

b = Buddy(log=True)

for n, (cmd, pid, *rest) in enumerate(load("ops1.txt")[:6], 1):
    if cmd == "alloc":
        ok = b.alloc(pid, rest[0])
        result = f"блок {b.owned[pid][1]}" if ok else "ОТКАЗ"
        print(f"{n}. alloc {pid} {rest[0]} → {result}")
    else:
        b.release(pid)
        print(f"{n}. free {pid}")

    print("Свободные блоки:",
          {s: a for s, a in sorted(b.free.items()) if a})
    print("Внутренняя фрагментация:", b.stats()[2])

assert b.refused == 1
assert b.stats() == (512, 512, 162)
assert "P4" not in b.owned

print("\nПроверяем полное слияние:")
b.release("P1")
b.release("P3")

assert b.stats() == (1024, 1024, 0)
assert b.free[1024] == [0]
assert not b.owned
print("Вся память свободна: {1024: [0]}")
print("Проверка пройдена")
