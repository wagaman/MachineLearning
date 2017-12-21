#!/bin/bash
#######################################################################
	#'''	
	#> File Name: load_data_to_mysql.sh
	#> Author: cyf
	#> Mail: XXX@qq.com
	#> Created Time: 2017年10月09日 星期一 13时45分30秒
	#'''	
#######################################################################
#set -x
CUR=$(cd `dirname $0`;pwd)
#global var
. ${CUR}/../conf/global.conf

log_info "将最后的数据导入mysql"
cat $LOCAL_DIR_2G/0000* > $LOCAL_DIR_2G/final
#2G
sql="CREATE TABLE $MYSQL_DB_NAME.qinghai_2g_$MONTH (user_id varchar(200) ,month_id varchar(201) ,user_status varchar(202) ,chnl_id varchar(203) ,chnl_kind_id varchar(204) ,area_id varchar(205) ,pay_mode varchar(206) ,cust_sex varchar(207) ,cert_age varchar(208) ,constellation_desc varchar(209) ,service_type varchar(210) ,call_fee double ,voice_call_duration double ,bill_times double ,voice_cdr_nums double ,voice_doubleroam_num double ,total_bytes double ,flux_call_duration double ,flux_cdr_nums double ,flux_doubleroam_num double ,total_fee double ,break varchar(200));"
mysqlCMD="mysql -h${MYSQL_HOST} -P${MYSQL_PORT} -u${MYSQL_USER} -p${MYSQL_PASS}"
LOADSQL="LOAD DATA LOCAL INFILE '$LOCAL_DIR_2G/final' REPLACE INTO TABLE $MYSQL_DB_NAME.qinghai_2g_5_9 FIELDS TERMINATED BY '|';"
log_info "create table"
echo $sql | $mysqlCMD
log_info "import data"
echo $LOADSQL | $mysqlCMD
