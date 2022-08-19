# -*- coding: utf-8 -*-
"""
Created on Tue Aug  9 11:03:15 2022

@author: github.com/yangjiacheng1996
"""
import redis


class Client:
    def create_connection(self, host: str, port: int, password: str):
        self.__connection = redis.StrictRedis(host=host, port=port, password=password)
        return self.__connection

    def redis_info(self):
        return self.__connection.info()
    """
    阿里云集群版
    {'active_defrag_running': 0,
     'blocked_clients': 0,
     'cluster_enabled': 0,
     'connected_clients': 8,
     'connected_slaves': 1,
     'databases': 256,
     'db0': {'avg_ttl': 17998489, 'expires': 93922, 'keys': 94328},
     'db1': {'avg_ttl': 286244048050, 'expires': 1, 'keys': 65},
     'db3': {'avg_ttl': 0, 'expires': 0, 'keys': 16},
     'db6': {'avg_ttl': 312338422550, 'expires': 1, 'keys': 151},
     'evicted_keys': 0,
     'expired_keys': 133081895,
     'hz': 10,
     'instantaneous_input_kbps': 37,
     'instantaneous_ops_per_sec': 351,
     'instantaneous_output_kbps': 2759,
     'keyspace_hits': 2960302345,
     'keyspace_misses': 287862648,
     'latest_fork_usec': 8831,
     'lazyfree_pending_objects': 0,
     'lru_clock': 15860206,
     'master_repl_offset': 39872610003,
     'master_replid': 'e203b5a52d54f1a982bba78f07b6ccf995d7515f',
     'master_replid2': 0,
     'maxmemory': 17179869184,
     'maxmemory_human': '16.00G',
     'maxmemory_policy': 'allkeys-lfu',
     'mem_allocator': 'jemalloc-5.1.0',
     'mem_fragmentation_ratio': 0.93,
     'migrate_cached_sockets': 0,
     'nodecount': 8,
     'pubsub_channels': 0,
     'pubsub_patterns': 0,
     'redis_version': '5.0.5',
     'rejected_connections': 0,
     'repl_backlog_active': 1,
     'repl_backlog_first_byte_offset': 39839055572,
     'repl_backlog_histlen': 33554432,
     'repl_backlog_size': 33554432,
     'role': 'master',
     'second_repl_offset': -1,
     'sync_full': 26,
     'sync_partial_err': 16,
     'sync_partial_ok': 0,
     'tcp_port': 6379,
     'total_commands_processed': 6407106005,
     'total_connections_received': 685597269,
     'total_net_input_bytes': 13502558491640,
     'total_net_output_bytes': 509555680292796,
     'uptime_in_days': 230,
     'uptime_in_seconds': 19938968,
     'used_cpu_sys': 602010.82,
     'used_cpu_sys_children': 1027.64,
     'used_cpu_user': 817949.15,
     'used_cpu_user_children': 1088.69,
     'used_memory': 843742120,
     'used_memory_dataset': 227004904,
     'used_memory_dataset_human': '216.49M',
     'used_memory_human': '804.66M',
     'used_memory_lua': 303104,
     'used_memory_lua_human': '296.00K',
     'used_memory_overhead': 616737216,
     'used_memory_overhead_human': '588.17M',
     'used_memory_peak': 3494104696,
     'used_memory_peak_human': '3.25G',
     'used_memory_rss': 808591360,
     'used_memory_rss_human': '771.13M',
     'used_memory_startup': 333150272,
     'used_memory_startup_human': '317.72M'}

    """


