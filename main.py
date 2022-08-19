#!/usr/bin/env python
# -*- coding: utf-8 -*-

# standard library
import logging
import logging.handlers
import os
import sys
from pprint import pprint

# modules
import lib3.file_system as fs
from lib3.redis_bigkey import Bigkey
from lib3.redis_outflow import Outflow
from lib3.config import project_root

# secondary packages
import click

# environment variety
BIGKEY_LOGFILE_NAME = "bigkey.log"
HOTKEY_LOGFILE_NAME = "hotkey.log"
OUTFLOW_LOGFILE_NAME = "outflow.log"


@click.group()
def main():
    # each feature build a logger

    # hotkey logger
    hotkey_logger = logging.getLogger("HotkeyLogger")
    hotkey_handler = logging.handlers.RotatingFileHandler(HOTKEY_LOGFILE_NAME,maxBytes=1048576,backupCount=10)
    hotkey_logger.setLevel(logging.INFO)
    hotkey_logger.addHandler(hotkey_handler)


    # 创建分析结果文件夹
    project_father_dir = os.path.dirname(project_root)
    result_dir = os.path.join(project_father_dir, "results")
    fs.recursive_delete_path(result_dir)
    try:
        os.mkdir(result_dir)
    except:
        print("Can't create results folder, somethine wrong")
        print(f"path: {result_dir}")
        sys.exit(1)

@click.command()
@click.option("-h","--host",help="redis instance connect address",required=True)
@click.option("-p","--port",help="redis exposed port",default="6379")
@click.option("-a","--password",help="redis login password",required=True)
@click.option("-n","--dbnumber",help="select a db that you want to check,"
            "default is all redis db.",default="-1")
def bigkeys(host:str,port:str,password:str,dbnumber:str):
    # bigkey logger
    bigkey_logger = logging.getLogger("BigkeyLogger")
    bigkey_handler = logging.handlers.RotatingFileHandler(BIGKEY_LOGFILE_NAME, maxBytes=1048576, backupCount=10)
    bigkey_logger.setLevel(logging.INFO)
    bigkey_logger.addHandler(bigkey_handler)
    # create an object and run function
    if not port.isdigit():
        bigkey_logger.error("-p or --port must be an int number,system down!")
        sys.exit(1)
    bk = Bigkey(host=host,port=int(port),password=password)
    bk.bigkeys(int(dbnumber))

@click.command()
@click.option("-h","--host",help="redis instance connect address",required=True)
@click.option("-p","--port",help="redis exposed port",default="6379")
@click.option("-a","--password",help="redis login password",required=True)
@click.option("-n","--dbnumber",help="select a db that you want to check,"
            "default is all redis db.",default="-1")
def hotkeys(host:str,port:str,password:str,dbnumber:str):
    return None


@click.command()
@click.option("-h","--host",help="redis instance connect address",required=True)
@click.option("-p","--port",help="redis exposed port",default="6379")
@click.option("-a","--password",help="redis login password",required=True)
@click.option("-n","--dbnumber",help="select a db that you want to check,"
            "default is all redis db.",default="-1")
def outflow(host,port,password,dbnumber):
    # outflow logger
    outflow_logger = logging.getLogger("OutflowLogger")
    outflow_handler = logging.handlers.RotatingFileHandler(OUTFLOW_LOGFILE_NAME,maxBytes=1048576,backupCount=10)
    outflow_logger.setLevel(logging.INFO)
    outflow_logger.addHandler(outflow_handler)
    # get top 10 keys which occupy redis node network bandwidth
    ofo = Outflow(host=host,port=port,password=password)
    # to be continued


