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
CUR=`pwd`
#global var
. ${CUR}/../conf/global.conf

log_info "将最后的数据导入mysql"
cat $LOCAL_DIR_3G/0000* > $LOCAL_DIR_3G/final
#3G
sql="CREATE TABLE $MYSQL_DB_NAME.qinghai_3g_5_9 (user_id varchar(200) ,month_id varchar(200) ,service_type varchar(200) ,channel_type varchar(200) ,device_number varchar(200) ,chnl_id varchar(200) ,chnl_kind_id varchar(200) ,area_id varchar(200) ,pay_mode varchar(200) ,cust_sex varchar(200) ,cert_age varchar(200) ,constellation_desc varchar(200) ,call_fee double ,voice_call_duration double ,bill_times double ,voice_cdr_nums double ,voice_doubleroam_num double ,total_bytes double ,flux_call_duration double ,flux_cdr_nums double ,flux_doubleroam_num double ,total_fee double ,use_months double ,sms_nums double ,flux_strem double ,call_nums double ,out_call_nums double ,pkg_prod_class varchar(200) ,break varchar(200) ,user_3wu_flag varchar(200));"
mysqlCMD="mysql -h${MYSQL_HOST} -P${MYSQL_PORT} -u${MYSQL_USER} -p${MYSQL_PASS}"
LOADSQL="LOAD DATA LOCAL INFILE '$LOCAL_DIR_3G/final' REPLACE INTO TABLE $MYSQL_DB_NAME.qinghai_3g_5_9 FIELDS TERMINATED BY '|';"
log_info "create table"
echo $sql | $mysqlCMD
log_info "import data"
echo $LOADSQL | $mysqlCMD
