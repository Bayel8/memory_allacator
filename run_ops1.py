import argparse
from pathlib import Path
from memsim import load, run


def main():
    parser = argparse.ArgumentParser(description="Симулятор распределения памяти")
    parser.add_argument("strategy", choices=("first", "best", "worst"), nargs="?", default="first")
    parser.add_argument("--merge", action="store_true", help="сливать соседние дыры")
    parser.add_argument("--file", type=Path, default=Path(__file__).with_name("ops1.txt"))
    args = parser.parse_args()
    mm = run(load(args.file), args.strategy, coalesce=args.merge, verbose=True)
    total, largest, holes = mm.stats()
    print(f"свободно={total} макс. дыра={largest} дыр={holes} отказов={mm.refused}")
    print(f"внешняя фрагментация={mm.fragmentation():.4f} ({mm.fragmentation():.2%})")


if __name__ == "__main__":
    main()
