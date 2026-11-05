"""Сравнение трёх стратегий со слиянием и buddy system."""
import argparse
from pathlib import Path
from memsim import MemoryManager, load
from buddy import Buddy


def simulate(ops, make, alloc, free, stats):
    m, ext, internal = make(), [], []
    for cmd, pid, *rest in ops:
        alloc(m, pid, rest[0]) if cmd == "alloc" else free(m, pid)
        total, largest, extra = stats(m)
        ext.append(1 - largest / total if total else 0)
        internal.append(extra)
    count = len(ops)
    return (m.refused, sum(ext) / count if count else 0,
            sum(internal) / count if count else 0)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("file", type=Path, nargs="?", default=Path(__file__).with_name("ops2.txt"))
    ops = load(parser.parse_args().file)
    print(f"Операций: {len(ops)}. Фрагментация усреднена после каждой операции.")
    print(f"{'подход':<16}{'отказов':>8}{'внешняя фр.':>13}{'внутренняя':>12}")
    for strategy in ("first", "best", "worst"):
        r, e, i = simulate(ops, lambda: MemoryManager(strategy, coalesce=True),
                           MemoryManager.alloc, MemoryManager.free,
                           lambda m: (*m.stats()[:2], 0))
        print(f"{strategy + ' +merge':<16}{r:>8}{e:>13.4f}{i:>12.2f}")
    r, e, i = simulate(ops, Buddy, Buddy.alloc, Buddy.release, Buddy.stats)
    print(f"{'buddy':<16}{r:>8}{e:>13.4f}{i:>12.2f}")


if __name__ == "__main__":
    main()
