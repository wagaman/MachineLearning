#/bin/bash
#######################################################################
    #'''   
    #> File Name: sftp.sh
    #> Author: cyf
    #> Mail: XXX@qq.com
    #> Created Time: 2017年11月29日 星期三 09时04分23秒
    #'''   
#######################################################################
#set -x
start_time=`date +%s`
CUR=$(cd `dirname $0`;pwd)
. $CUR/conf/global.conf

#local
LOCAL_DIR=$CUR/data
DONE=$CUR/tmp/done
UPDATE=$CUR/tmp/update
REMOTE_LIST=$CUR/tmp/list.txt
FINISH=$CUR/finish
TYPE_FILE=$CUR/tmp/type_file
UPDATE_DATE=`date`
HDFS_DIR=/user/cuiyufei/tmp
LOG_DIR=$CUR/log
HADOOP_EXC=/opt/hadoop-2.7.3/bin/hdfs
test -e $CUR/data||mkdir -p $CUR/data
test -e $CUR/tmp ||mkdir -p $CUR/tmp
test -e $FINISH || mkdir -p $FINISH


#获取列表
log_info "开始获取sftp文件列表..."
lftp -e 'ls;quit' sftp://$USER:$PASSWORD@$HOST/$REMOTE_DIR|sed '1,2d'|awk '{print $NF}' > $REMOTE_LIST
if [ $? -eq 0 ]
then
	log_info "sftp文件列表获取完成！"
else
	log_error "sftp文件列表获取失败!"
	exit 1
fi

#根据done生成 update
log_info "生成待更新列表..."
test -e $DONE||touch $DONE
test -e $UPDATE||touch $UPDATE
diff $DONE $REMOTE_LIST|grep ">"|awk '{print $NF}'>$UPDATE
log_info "待更新列表生成完成！"

if [ -s $UPDATE ]
then
	#更新数据到本地目录
	for file in `cat $UPDATE` 
	do
		log_info "get数据$file"
		lftp sftp://$USER:$PASSWORD@$HOST  -e "get $REMOTE_DIR/$file -o $LOCAL_DIR; bye"
		if [ $? -eq 0 ]
		then
			log_info "$file下载完成！"
		else
			log_error "$file下载失败！"
			#exit 1
		fi
	done
    #rm $UPDATE

	#将更新过的数据写入finished_file
	for file in `ls -l /$LOCAL_DIR|sed '1d'|awk '{print $NF}'`
	do
		echo $file >> $DONE
	done

	#将数据移动到finish
	mv $LOCAL_DIR/* $FINISH
	#计算数据量
	DATA_COUNT=`ls -l $FINISH|sed '1d'|wc -l`
	#计算数据大小
	DATA_ROOM=`du -h $FINISH|awk '{print $1}'`
	#删除md5文件
	rm $FINISH/*.*MD5

	#CRBLABLEC06001A171207011000000.091类型的文件一小时合并成一个文件
	for file in `ls -l $FINISH|sed '1d'|awk '{print $NF}'`
	do
		FILE_TYPE=${file:0:15}
		if [ "X${FILE_TYPE}" = "XCRBLABLEC06001A"  ] 
		then
			DATE_TYPE=${file:0:21}
			echo $DATE_TYPE >> $TYPE_FILE
		fi
	done

    for file in `cat $TYPE_FILE|sort -u|uniq`	
	do
		for ((i=0;i<=24;i++))
		do
			if [ $i -gt 9 ]
			then
				hour=$i
			else
				hour=0$i
			fi
			find $FINISH -type f|grep "$file$hour"
			if [  $? -eq 0 ]
			then
				cat $FINISH/$file$hour* > $FINISH/$file$hour
				find $FINISH -type f|grep -E "$file$hour[0-9]+.[0-9]+"|xargs rm -rf
			fi
		done
	done
	#删除类型文件
	rm -rf $TYPE_FILE
	#将数据put到hdfs上
	for file in `ls -l $FINISH|sed '1d'|awk '{print $NF}'`
	do
		log_info "hdfs put $file..."
		$HADOOP_EXC dfs -put $FINISH/$file $HDFS_DIR
	done

	#清空finish
	rm -rf $FINISH/*
	end_time=`date +%s`
	diff=$[ end_time - start_time  ]
	log_info "
*****************************************************************
*                                                               *
*               互联网运营部数据中心增量数据更新                *
*****************************************************************
		#更新时间:$UPDATE_DATE
		#数据数量:$DATA_COUNT
		#数据大小:$DATA_ROOM
		#用    时:$diff s
		#HDFS目录:$HDFS_DIR
		#日志文件:$LOG_DIR
**************************数据更新完成！*************************"
else
    #rm $UPDATE
	end_time=`date +%s`
	diff=$[ end_time - start_time  ]
	log_info "程序执行用时:$diff s。没有数据更新！"
fi
