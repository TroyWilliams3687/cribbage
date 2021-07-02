#!/usr/bin/env python3
# -*- coding:utf-8 -*-

# -----------
# SPDX-License-Identifier: MIT
# Copyright (c) 2021 Troy Williams

# uuid:   060527ea-d69c-11eb-87bb-1b4177236484
# author: Troy Williams
# email:  troy.williams@bluebill.net
# date:   2021-06-26
# -----------

"""
"""

# ------------
# System Modules - Included with Python

from pathlib import Path

# ------------
# 3rd Party - From pip

import click

# ------------
# Custom Modules


# ------------


@click.group()
@click.version_option()
@click.pass_context
def main(*args, **kwargs):
    """ """

    # Initialize the shared context object to a dictionary and configure it for the app
    ctx = args[0]
    ctx.ensure_object(dict)

    ctx.obj["paths"] = common_paths()


# -----------
# Add the child menu options

# main.add_command(save)
# main.add_command(restore)
