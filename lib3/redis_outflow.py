#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import redis
from pprint import pprint
from typing import List

from redis_client import Client
from run_commnad import command

class Counter:
    @staticmethod
    def fit_line(x1: float, y1: float, x2: float, y2: float, x=None, y=None):
        k = (y2 - y1) / (x2 - x1)  # 斜率
        b = y1 - k * x1  # 截距
        if not x and not y:
            raise ValueError("x和y至少给一个，给x求y，给y求x。")
        elif x and y:
            raise ValueError("x和y不能全给")
        elif not x:  # x是None，给了y
            x = (y - b) / k
            return x
        elif not y:  # y是None，给了x
            y = k * x + b
            return y

    @staticmethod
    def counter_to_qps(counter: int, factor=1):
        """
        # +--------+------------+------------+------------+------------+------------+
        # | factor | 100 hits   | 1000 hits  | 100K hits  | 1M hits    | 10M hits   |
        # +--------+------------+------------+------------+------------+------------+
        # | 0      | 104        | 255        | 255        | 255        | 255        |
        # +--------+------------+------------+------------+------------+------------+
        # | 1      | 18         | 49         | 255        | 255        | 255        |
        # +--------+------------+------------+------------+------------+------------+
        # | 10     | 10         | 18         | 142        | 255        | 255        |
        # +--------+------------+------------+------------+------------+------------+
        # | 100    | 8          | 11         | 49         | 143        | 255        |
        # +--------+------------+------------+------------+------------+------------+
        """
        # counter本来是关于qps的复杂的对数函数，qps是自变量，counter是因变量。但是无法用一个对数去拟合这些点，所以就用分段直线代替。
        if factor == 1:
            qps_x = [0, 50, 500, 50000]
            counter_y = [0, 18, 49, 255]
        elif factor == 10:
            qps_x = [0, 50, 500, 50000, 500000]
            counter_y = [0, 10, 18, 142, 255]
        elif factor == 100:
            qps_x = [0, 50, 500, 50000, 500000, 5000000]
            counter_y = [0, 8, 11, 49, 143, 255]
        else:
            raise ValueError("factor must equal to 1 or 10 or 100")
        if counter == 0:
            qps = 0
        elif counter > 0:
            counter_tag = counter_y[-1]
            for c in counter_y:
                if counter < c:
                    counter_tag = c
                    break
            index_y = counter_y.index(counter_tag)
            qps = Counter.fit_line(x1=qps_x[index_y - 1], y1=counter_y[index_y - 1], x2=qps_x[index_y],
                                   y2=counter_y[index_y], y=counter)
        else:
            raise ValueError("minus counter? system down.")
        return int(qps * 1.05)  # log对数函数上任取两个点连线，所连成的线段永远在曲线的下方，所以为了接近真实的结果，在直线的基础上乘以1.05


class Outflow(Client):
    def __init__(self, host: str, port: int, password: str):
        self.redis_host = host
        self.redis_port = port
        self.redis_password = password
        self.connection = self.create_connection(self.redis_host, self.redis_port, self.redis_password)

    def describe_instance_info(self):
        '''
        函数返回：
        {'redis_version': '5.0.5', 'tcp_port': 6379, 'uptime_in_seconds': 5342760, 'uptime_in_days': 61,
        'hz': 10, 'lru_clock': 1263998, 'connected_clients': 9, 'blocked_clients': 0, 'used_memory': 793531672,
        'used_memory_human': '756.77M', 'used_memory_rss': 765480960, 'used_memory_rss_human': '730.02M',
        'used_memory_peak': 1138412424, 'used_memory_peak_human': '1.06G', 'used_memory_overhead': 617209188,
        'used_memory_overhead_human': '588.62M', 'used_memory_startup': 333150272, 'used_memory_startup_human': '317.72M',
        'used_memory_dataset': 176322484, 'used_memory_dataset_human': '168.15M', 'used_memory_lua': 303104,
        'used_memory_lua_human': '296.00K', 'maxmemory': 17179869184, 'maxmemory_human': '16.00G',
        'maxmemory_policy': 'allkeys-lfu', 'mem_fragmentation_ratio': 0.95, 'mem_allocator': 'jemalloc-5.1.0',
        'active_defrag_running': 0, 'lazyfree_pending_objects': 0, 'total_connections_received': 206029142,
        'total_commands_processed': 2525486632, 'instantaneous_ops_per_sec': 463, 'total_net_input_bytes': 4021694274375,
        'total_net_output_bytes': 292131750841244, 'instantaneous_input_kbps': 26, 'instantaneous_output_kbps': 23447,
        'rejected_connections': 0, 'sync_full': 8, 'sync_partial_ok': 0, 'sync_partial_err': 0, 'expired_keys': 50488217,
        'evicted_keys': 0, 'keyspace_hits': 1423340149, 'keyspace_misses': 115968057, 'pubsub_channels': 0,
        'pubsub_patterns': 0, 'latest_fork_usec': 4789, 'migrate_cached_sockets': 0, 'role': 'master',
        'connected_slaves': 1, 'master_replid': 'e203b5a52d54f1a982bba78f07b6ccf995d7515f', 'master_replid2': 0,
        'master_repl_offset': 14771357017, 'second_repl_offset': -1, 'repl_backlog_active': 1,
        'repl_backlog_size': 33554432, 'repl_backlog_first_byte_offset': 14737802586, 'repl_backlog_histlen': 33554432,
        'used_cpu_sys': 208438.33, 'used_cpu_user': 268779.84, 'used_cpu_sys_children': 258.01,
        'used_cpu_user_children': 309.67, 'cluster_enabled': 0, 'databases': 256, 'nodecount': 8,
        'db3': {'keys': 16, 'expires': 0, 'avg_ttl': 0},
        'db6': {'keys': 6, 'expires': 1, 'avg_ttl': 312675374250},
        'db0': {'keys': 84785, 'expires': 84455, 'avg_ttl': 18693467},
        'db1': {'keys': 65, 'expires': 1, 'avg_ttl': 300840255850}}
        '''
        return self.connection.info()

    def __list_node_keys(self, node_num: int) -> list:
        """
        功能：本函数执行iscan命令获取某个数据节点上的key，所以只适用于redis集群版实例，获取某个节点的全部key name到文件里
        时间复杂度：O(N^2) ， 这个算法对CPU的要求比较高，因为是N平方的算法。
        空间复杂度: O(10N), 因为while循环每次执行iscan命令都只获取10个key，所有key都进一个列表，所以是10N的算法，内存无压力。
        """
        cursor = 0
        keys_list = []
        while True:
            # print(cursor)
            tmp_stdout = self.connection.execute_command("iscan", str(node_num), str(cursor))
            new_cursor, key_list = tmp_stdout[0], tmp_stdout[1]
            it = iter(key_list)
            while True:
                try:
                    keys_list.append(str(next(it), encoding="utf-8"))
                except StopIteration:
                    break
            cursor = str(new_cursor, encoding="utf-8")  # 每次执行iscan都返回两个只，1. 新的cursor用于下次迭代，2. 列表，包含10个key
            if cursor == "0":
                break
        return keys_list

    def __get_key_memory_size(self, key_name: str, db=0) -> dict:
        """
        函数功能： 执行redis-memory-for-key命令(这个命令是redis的依赖库，已经安装好了)，获取某个key的内存信息，然后整理到一个字典里
        redis-memory-for-key  -s r-uf63g3f5ge8l7qjs8m.redis.rds.aliyuncs.com -p 6379
        -a uxfhe%5^0aWeWa#afPEYRLdhAUQndoM4  -d 0 ORDER_POS_RELATION
        Key				ORDER_POS_RELATION
        Bytes				3439508.0
        Type				hash
        Encoding			hashtable
        Number of Elements		34305
        Length of Largest Element	35
        """
        one_key_info = {}
        stdout = command(
            f"redis-memory-for-key -s {self.redis_host} -p {self.redis_port} -a {self.redis_password} -d {str(db)} {key_name}")
        # print(len(stdout)) # 4行
        for line in stdout:
            line = str(line, encoding="utf-8").rstrip()
            # print("line",line)
            one_key_info[line.split("\t")[0]] = line.split("\t")[-1]
        return one_key_info

    def list_node_keys_size(self, node_num: int, db=0) -> list:
        key_list = self.__list_node_keys(node_num)
        result = []
        for i in key_list:
            try:
                one_key_size = self.__get_key_memory_size(i, db)
                result.append(one_key_size)
            except Exception as e:
                continue  # 因为获取key名称和读取他们的内存大小之间有时间间隔，所以有的key可能已经不存在了，不存在就不获取。
        return result

    def get_several_key_size(self, key_list, db=0) -> List[dict]:
        """
        功能：传入一个包含key名字的列表，返回这些key的大小信息列表，如果中途有的 key不存在了，则跳过
        """
        result = []
        for i in key_list:
            try:
                one_key_size = self.__get_key_memory_size(i, db)
                result.append(one_key_size)
            except Exception as e:
                continue
        return result

    def get_instance_hotkeys_counter(self):
        """
        redis-cli --hotkeys命令返回大致是这样：
        """
        instance_info = self.describe_instance_info()
        if instance_info.get("maxmemory_policy") not in ("allkeys-lfu", "volatile-lfu"):
            raise EnvironmentError("获取redis实例当前的hotkey需要提前设置redis的LFU淘汰机制，但是检查了您的redis实例，并没有设置LFU。\n"
                                   "设置LFU的方法：进入阿里云实例，参数设置--修改maxmemory-policy，\n"
                                   "也可以进入redis后通过命令行设置：\n"
                                   "config set maxmemory-policy allkeys-lfu或者config set maxmemory-policy volatile-lfu")
        output = command(f"redis-cli -h {self.redis_host} -p {str(self.redis_port)} -a {self.redis_password} --hotkeys")
        # 转化output中的b字符串为utf-8格式
        output = [str(i, encoding="utf-8").rstrip() for i in output]
        # print(output)
        # 去掉output的#开头的行
        # output = [i for i in output if not i.startswith("#")]
        summary = [i for i in output if "--- summary ---" in i][0]
        summary_index = output.index(summary)
        before_summary = output[:summary_index]
        # after_summary = output[summary_index+1:]
        hotkeys_name_and_counter = {}
        pattern = re.compile("(\[\d{2}\.\d{2}%]) Hot key '(.*)' found so far with counter (\d+)")
        for line in before_summary:
            groups = pattern.match(line)
            if not groups:  # 和正则表达式不匹配的行全部忽略
                continue
            key_name, counter = groups[2], groups[3]
            hotkeys_name_and_counter[key_name] = counter
        return hotkeys_name_and_counter  # {'keyname1':'255' , 'keyname2': '49'}

    def get_node_hot_key_outflow(self, node_num: int, db=0) -> list:  # 这是一个价值连城，连阿里云都做不到的函数！
        """
        功能：获取redis集群版实例的热key和读取流量。
        """
        # 第一步，获取redis实例的全部热key和热key的counter
        hotkeys_counter = self.get_instance_hotkeys_counter() # 性能好，10s内完成
        # print("hotkey and counter",hotkeys_counter)
        # 第二步，获取redis某个数据节点node上的全部key的name
        node_keys_name = self.__list_node_keys(node_num) # 性能好，5s内完成
        # 第三步，获取某个数据节点node的热key
        node_hotkey_name = [h for h in hotkeys_counter.keys() if h in node_keys_name]
        print("node_hotkey_name",node_hotkey_name,"\n")
        if not node_hotkey_name:
            print("恭喜你，这个redis实例的数据分片%d没有热key，停止检查redis。"%node_num)
            return []
        node_hotkey_counter = {}
        for h in node_hotkey_name:
            node_hotkey_counter.setdefault(h,hotkeys_counter[h])
        # print("node_hotkey_counter:",node_hotkey_counter)
        # 第四步，将counter转化成qps
        node_hotkey_qps = {}
        for k, v in node_hotkey_counter.items():
            node_hotkey_qps.setdefault(k,Counter.counter_to_qps(int(v),factor=1))
        # print("node_hotkey_qps",node_hotkey_qps)
        # 第五步，获取每个热key的 name+内存大小+类型+qps+长度。
        node_hotkeys_size = self.get_several_key_size(node_hotkey_qps.keys(), db)
        # print("node_hotkeys_size",node_hotkeys_size)
        result = []
        for nhs in node_hotkeys_size:
            nhs["Qps"] = node_hotkey_qps[nhs["Key"]]
            result.append(nhs)
        return result
        # [{"Key": "OPEN_ORDER:2022022487895833004116", "Bytes": "1360", "Type": "string","Qps":"1234"},
        # {"Key": "USER:271492", "Bytes": "1380.0", "Type": "hash", "Encoding": "hashtable", "Number of Elements": "4",
        # "Length of Largest Element": "571","Qps":"2345"}]
