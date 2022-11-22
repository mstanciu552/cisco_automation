#!/usr/bin/env python
import argparse
import base64
from util import get_diff


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("filename1")
    parser.add_argument("filename2")
    args = parser.parse_args()

    f1 = base64.b64decode(args.filename1).decode("utf-8")
    f2 = base64.b64decode(args.filename2).decode("utf-8")

    print(get_diff(f1, f2))


if __name__ == "__main__":
    main()
