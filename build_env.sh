#!/bin/bash


# 判断当前用户是否为root
if [ $UID -ne 0 -a $USER != 'root' ]
then
	echo "Current user is not root, stop building environment!"
	echo "Rerun this script by root!"
	exit 1
else
	echo "Current user is root，Continue building environment"
fi

# 获取脚本所在的目录
project_root_dir=$(cd "$(dirname "$0")"; pwd)
package_abs_path=${project_root_dir}"/redis_analysis_env.tar.gz"
#echo $project_root_dir

# 检查当前目录是否有redis_analysis_env.tar.gz
if [ -f $package_abs_path -a -s $package_abs_path ]
then
    echo "found $package_abs_path"
    echo "start building all-in-one environment......"
else
    echo "file miss or broken: $package_abs_path"
    exit 1
fi

# 开始复制和解压环境包
# cp $package_abs_path /opt/
cd /opt/ && tar -zxvf /opt/redis_analysis_env.tar.gz