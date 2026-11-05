from buddy import Buddy

b = Buddy(log=True)

print("Запрос: alloc P1 200")
ok = b.alloc("P1", 200)

print("Выделено:", ok)
print("Свободные блоки:", {s: a for s, a in sorted(b.free.items()) if a})
print("Занятые блоки:", b.owned)

total, largest, internal = b.stats()
print("Свободно:", total)
print("Максимальный свободный блок:", largest)
print("Внутренняя фрагментация:", internal)

assert ok
assert b.owned["P1"] == (0, 256, 200)
assert (total, largest, internal) == (768, 512, 56)
print("Проверка пройдена")
