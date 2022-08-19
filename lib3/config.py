#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import platform
import logging
import sys

os_type = platform.platform()
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
redis_cli_path = None
if os_type.startswith("Windows"):
    redis_cli_path = os.path.join(project_root,"tools","redis-cli.exe")
elif os_type.startswith("Linux"):
    redis_cli_path = os.path.join(project_root,"tools","redis-cli")
else:
    logging.error(f"platform not support: {os_type}")
    sys.exit(1)



