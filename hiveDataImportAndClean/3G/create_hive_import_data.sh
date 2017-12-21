#!/bin/bash
#######################################################################
	#'''	
	#> File Name: create_hive_import_data.sh
	#> Author: cyf
	#> Mail: XXX@qq.com
	#> Created Time: 2017年10月19日 星期四 14时10分41秒
	#'''	
#######################################################################
#set -x
start_time=`date +%s`
CUR=$(cd `dirname $0`;pwd)
#global var
. ${CUR}/../conf/global.conf
#判断源数据文件的文件夹是否存在
hdfs dfs -ls $SOURCE_DIR > /dev/null 2>&1
if [ $? -ne 0 ]
then
	log_info "the diretory of $SOURCE_DIR  not exists!"
	exit 1
fi
#创建表格，并导入数据
for file in `hdfs dfs -ls $SOURCE_DIR|grep $INPUT_DATE|awk '{print $8}'|awk -F '/' '{print $NF}'`
do
	source_file=$SOURCE_DIR/$file
	file_transfer=`echo $file|sed "s/\~/\_/g"`
	file_time=${file_transfer:5:6}
	tmp_name=${file_transfer#*_}
	table_name_010=${tmp_name%_*}
	table_name=`echo $table_name_010|grep -oE '^([a-zA-Z_23]+)+'`
	table_name_month=${table_name}${MONTH}
	#创建hive表格
	log_info "开始创建表格..."
	#默认分隔符为\001
	#python $CUR/../script/qinghai.py $table_name $SEP
	python $CUR/../script/qinghai.py $table_name_month 
	if [ $? -eq 0 ]
	then
		log_info "创建表格${table_name_month}的sql文件成功！"
	else
		log_error "创建表格${table_name_month}的sql文件失败！"
		exit 1
	fi
	hive --database $DATABASE -f $CUR/../sql/${table_name_month}.sql
	if [ $? -eq 0 ]
	then
		log_info "hive创建表格${table_name_month}成功！"
	else
		log_error "hive创建表格${table_name_month}失败！"
		exit 1
	fi
	#导入数据
	hive --database $DATABASE -e "load data inpath '$source_file' into table $table_name_month;"
	if [ $? -eq 0 ]
	then
		log_info "hive导入数据$source_file=>${table_name_month}成功！"
	else
		log_error "hive导入数据$source_file=>${table_name_month}失败！"
		exit 1
	fi
done
end_time=`date +%s`
program_time=$[ end_time - start_time ]
log_info "数据处理完毕--用时:$program_time"
