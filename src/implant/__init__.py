#!/usr/bin/env python3
"""Implant - a wrapper around magic-wormhole for secure file transfer."""

import argparse
import os
import sys
import tempfile
from pathlib import Path


def receive():
    """Receive a folder from sender and execute install.py."""
    print("Starting receiver...", flush=True)

    orig_dir = os.getcwd()
    with tempfile.TemporaryDirectory() as tmpdir:
        os.chdir(tmpdir)
        try:
            os.system("uvx --no-config magic-wormhole receive --no-listen --allocate --accept-file")

            received_items = list(Path(tmpdir).iterdir())
            if not received_items:
                print("Error: No files received", flush=True)
                sys.exit(1)

            received_path = received_items[0]
            print(f"Received: {received_path}", flush=True)

            install_script = (
                received_path / "install.py"
                if received_path.is_dir()
                else Path(tmpdir) / "install.py"
            )

            if not install_script.exists():
                print("Error: install.py not found in payload", flush=True)
                sys.exit(1)

            print("Running install.py with uv...", flush=True)
            os.system(f"uv run {install_script}")
        finally:
            os.chdir(orig_dir)


def send(folder_path, code):
    """Send a folder to receiver using provided code."""
    folder = Path(folder_path)
    if not folder.exists() or not folder.is_dir():
        print(
            f"Error: {folder_path} is not a valid directory",
            file=sys.stderr,
            flush=True,
        )
        sys.exit(1)

    install_script = folder / "install.py"
    if not install_script.exists():
        print("Error: install.py not found in folder", file=sys.stderr, flush=True)
        sys.exit(1)

    print(f"Sending {folder_path} to code {code}...", flush=True)
    os.chdir(folder)
    os.system(f"uvx --no-config magic-wormhole send . --code {code} --no-listen")


def main():
    parser = argparse.ArgumentParser(description="Implant - secure payload transfer")
    parser.add_argument("--send", metavar="FOLDER", help="Send folder to receiver")
    parser.add_argument(
        "--code", metavar="CODE", help="Code for receiver (used with --send)"
    )
    parser.add_argument(
        "--receive", action="store_true", help="Receive payload from sender"
    )

    args = parser.parse_args()

    if args.send:
        if not args.code:
            print(
                "Error: --code is required when using --send",
                file=sys.stderr,
                flush=True,
            )
            sys.exit(1)
        send(args.send, args.code)
    else:
        receive()


if __name__ == "__main__":
    main()
