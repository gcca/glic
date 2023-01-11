# gcca
from typing import Optional, Sequence

import argparse
import contextlib
import pathlib


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        prog="glic",
        description="GLic: License header code formatter",
        epilog="(gcca 🄯)",
    )
    parser.add_argument("filenames", nargs="*", help="Filenames to fix")
    args = parser.parse_args(argv)
    config = ReadConfig()
    code = 0

    for filename in args.filenames:
        filepath = pathlib.Path(filename)

        key = filepath.suffix[1:]
        try:
            block = config[key]
        except KeyError:
            continue

        file = filepath.open()

        headlines = []
        line = file.readline()
        for blockline in block:
            if line != blockline:
                break
            headlines.append(line)
            line = file.readline()

        body = file.read()
        file.close()
        formatted = []

        if block != headlines:
            formatted.append(filename)
            code = 1
            file = filepath.open("w")
            file.writelines(block)
            if len(line) > 1:
                file.write("\n")
            file.write(line)
            file.write(body)
            file.close()

        if code:
            for filename in formatted:
                print(filename)

    return code


def ReadConfig():
    with open(".glic") as glicfile:
        lines = glicfile.readlines()
    blocks = []
    keys = ["default"]
    block = []
    for line in lines:
        if len(line) == 1:
            continue

        if not line.startswith("["):
            block.append(line)
            continue

        blocks.append(block)
        block = []
        keys.append(line[1:-2])
    blocks.append(block)
    return dict(zip(keys, blocks))


if "__main__" == __name__:
    raise SystemExit(main())
