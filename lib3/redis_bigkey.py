#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import sys

from redis_client import Client
from config import redis_cli_path
from run_commnad import command


"""
methods to manually show big key 

"""
class Bigkey(Client):
    def __init__(self,host:str,port:int,password:str):
        self.host = host
        self.port = port
        self.password = password
        self.connection = self.create_connection(host,port,password)
        self.redis_info = self.redis_info()

    def bigkeys(self,db:int):
        if db == -1:
            cmd = f"{redis_cli_path} -h {self.host} -p {self.port} -a {self.password} --bigkeys"
        elif db not in range(256):
            logging.error("db out of range,the number of db must within 0-255")
            return None
        else:
            cmd = f"{redis_cli_path} -h {self.host} -p {self.port} -a {self.password} --bigkeys -n {db}"
        output = command(cmd)
        return output


if __name__ == "__main__":
    bk = Bigkey(host="hahaha",port=6379,password="hahaha")
    print(bk.bigkeys(0))
    #print(int("-1"))
