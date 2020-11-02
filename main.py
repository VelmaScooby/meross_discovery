#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# PYTHON_ARGCOMPLETE_OK

"""
Locates a configures a Meross IoT device
"""

import sys

import meross_discovery.command_line as command_line


if __name__ == "__main__":
    opts, subcommands = command_line.arguments()
    if opts.subcommand is None:
        sys.exit("Missing sub-command, expecting one of:"
                 " {}".format(", ".join(sorted(subcommands.keys()))))
    try:
        subcommands[opts.subcommand].go(opts)
    except KeyboardInterrupt:
        pass
