#!/bin/bash
#######################################################################
	#'''	
	#> File Name: run.sh
	#> Author: cyf
	#> Mail: XXX@qq.com
	#> Created Time: Wed 10 May 2017 07:50:24 PM PDT
	#'''	
#######################################################################
#set -x

table_name=$1
if [ "X${table_name}" = "X" ]
then
    table_name=TF_F_USER_PURCHASE
fi
#将配置文件引入
CUR_DIR=`pwd`
source $CUR_DIR/../conf/local.conf


#创建日志文件
#@input:log_file  NOTICE log_module file msg
#@outpu: 0
LOG()
{
	local log_notice=$1/access.log
	local log_error=$1/error.log
	local log_type=$2
	local log_module=$3
	local file=$4
	local msg=$5
	local log_form="[$2] `date '+%Y-%m-%d %H:%M:%S'` [$log_module] file [$file] msg [$msg] "
	if ! test -e $log_notice
	then
		touch $log_notice
	fi
	if ! test -e $log_error
	then
		touch $log_error
	fi
	case $2 in
		INFO)
			echo $log_form >> $log_notice
			;;
		ERROR)
			echo $log_form >> $log_error
			;;
		?)
			echo "echo input error."
			;;
	esac
}
#执行sqlldr
#@input:dataPath endType code table_name ctlDIR
#@outpu: 0
SQLLDR()
{
	local dataPath=$1
	local endType=$2
	local code=$3
	local table_name=$4
	local ctlDIR=$5

	cd ${dataPath}
	for filename in `ls|grep "${endType}$"|grep $code`
	do
	    sqlldr ${user}/${password}@//${host}:${port}/${connection_string} control=${ctlDIR}/${table_name}.ctl bad=${log_sqlldr}/${table_name}.bad log=${log_sqlldr}/${table_name}.log data=${dataPath}/${filename} direct=true parallel=true streamsize=20971520 readsize=20971520 bindsize=20971520 errors=10000000 > /dev/null
	    if [ $? -eq 0  ]
	    then
	    	LOG $log_shell INFO $table_name $filename SUCCESS
	    	echo "数据导入成功"
	    else
	    	LOG $log_shell ERROR $table_name $filename FAIL
	    	echo "数据导入失败"
	    fi
	done
}



#本地创建控制文件和远程服务器创建oracle表
echo "创建表格和与之对应的数据库表..."
python dataAnalysis.py $table_name 
if [ $? -eq 0 ]
then
	LOG $log_shell INFO dataAnalysis $table_name  SUCCESS
        echo "创建控制文件与数据表成功"
else
	LOG $log_shell ERROR dataAnalysis $table_name FAIL
        echo "创建控制文件与数据表失败"
fi

#获取表格的接口号
echo "获取表格的接口号:${table_name}..."
code=`python getCode.py hb ${table_name}`
if [ "X$code" = "X" ]
then
	LOG $log_shell ERROR getCode $table_name FAIL
        echo "获取接口号失败"
else
	LOG $log_shell INFO getCode $table_name  $code
        echo "获取表格接口号成功,表格:${table_name} 接口号:$code"
fi

#将数据导入数据库
echo "数据导入数据库:${table_name}..."
SQLLDR ${dataHB} 018 $code $table_name $ctlDIR
if [ $? -eq 0 ]
then
	LOG $log_shell INFO SQLLDR_HB $table_name  SUCCESS
else
	LOG $log_shell ERROR SQLLDR_HB $table_name FAIL
fi

SQLLDR ${dataSD} 017 $code $table_name $ctlDIR
if [ $? -eq 0 ]
then
	LOG $log_shell INFO SQLLDR_SD $table_name  SUCCESS
else
	LOG $log_shell ERROR SQLLDR_SD $table_name FAIL     
fi

