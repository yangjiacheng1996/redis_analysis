#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import subprocess
import time
import logging
import pprint

class TimeoutError(Exception):
    def __init__(self, message):
        Exception.__init__(self, message)

def command(cmd, timeout=60):
    """执行命令cmd，返回命令输出的内容。
    如果超时将会抛出TimeoutError异常。
    cmd - 要执行的命令
    timeout - 最长等待时间，单位：秒
    return code is not 0
    """
    logging.info("run command: %s"%cmd)
    p = subprocess.Popen(cmd, stderr=subprocess.STDOUT, stdout=subprocess.PIPE, shell=True)
    begin = time.time()
    while True:
        # p.poll() return None if it's not finish
        if p.poll() is not None:
            if p.returncode == 0:
                break
            else:
                error = p.stdout.read()
                raise Exception("Run %s error: %s" % (cmd, error))
        take_time = time.time() - begin
        if take_time > timeout:
            p.terminate()
            raise TimeoutError("Run %s timeout" % (cmd))
        time.sleep(0.01)
    # 注意，不要打印p.stdout，否则return出来的命令输出就会缺少信息,print多少，少多少。
    return p.stdout.readlines()
    # return p.stdout.read()
