#!/bin/bash
#######################################################################
	#'''	
	#> File Name: clean_2g.sh
	#> Author: cyf
	#> Mail: XXX@qq.com
	#> Created Time: 2017年11月28日 星期二 09时05分15秒
	#'''	
#######################################################################
#set -x
start_time=`date +%s`
CUR=$(cd `dirname $0`;pwd)
#global var
. ${CUR}/../conf/global.conf
log_info "================2g数据处理========================="

log_info "3g flux tmp"
hive --database $DATABASE -e "create table tmp_dwa_v_m_cus_3g_imei_flux_$MONTH as select subs_instance_id as user_id, month_id, total_bytes, call_duration, cdr_nums, flux_doubleroam_num, total_fee from dwa_v_m_cus_3g_imei_flux_$MONTH;"

log_info "3g flux use"
hive --database $DATABASE -e "create table tmp_dwa_v_m_cus_3g_imei_flux_use_$MONTH as select user_id, month_id, sum(total_bytes) as total_bytes, sum(call_duration) as call_duration, sum(cdr_nums) as cdr_nums, sum(flux_doubleroam_num) as flux_doubleroam_num, sum(total_fee) as total_fee from tmp_dwa_v_m_cus_3g_imei_flux_$MONTH group by user_id,month_id;"

log_info "3g voice tmp"
hive --database $DATABASE -e "create table tmp_dwa_v_m_cus_3g_imei_voice_$MONTH as select user_id, month_id, call_fee, call_duration, bill_times, cdr_nums, doubleroam_num from dwa_v_m_cus_3g_imei_voice_$MONTH;"

log_info "3g voice use"
hive --database $DATABASE -e "create table tmp_dwa_v_m_cus_3g_imei_voice_use_$MONTH as select user_id, month_id, sum(call_fee) as call_fee, sum(call_duration) as call_duration, sum(cdr_nums) as cdr_nums, sum(bill_times) as bill_times,sum(doubleroam_num) as doubleroam_num from tmp_dwa_v_m_cus_3g_imei_voice_$MONTH group by user_id,month_id;"

log_info "qinghai 3g"
hive --database $DATABASE -e "create table qinghai_3g_$MONTH as SELECT a.SUBS_INSTANCE_ID as USER_ID,a.MONTH_ID,a.SERVICE_TYPE,a.CHANNEL_TYPE,a.DEVICE_NUMBER,a.USER_STATUS,a.CHNL_ID,a.CHNL_KIND_ID,a.AREA_ID,a.PAY_MODE,a.CUST_SEX,a.CERT_AGE,a.CONSTELLATION_DESC,b.CALL_FEE,b.CALL_DURATION as VOICE_CALL_DURATION,b.BILL_TIMES,b.CDR_NUMS as VOICE_CDR_NUMS,b.doubleROAM_NUM as voice_doubleroam_num,c.TOTAL_BYTES,c.CALL_DURATION as FLUX_CALL_DURATION,c.CDR_NUMS as FLUX_CDR_NUMS,c.FLUX_doubleROAM_NUM,c.TOTAL_FEE,d.use_months,d.sms_nums,d.flux_strem,d.call_nums,d.out_call_nums,d.pkg_prod_class,a.IS_THIS_BREAK AS BREAK,d.user_3wu_flag FROM dwa_v_m_cus_3g_rns_wide_$MONTH a LEFT JOIN TMP_DWA_V_M_CUS_3G_IMEI_VOICE_$MONTH b on a.SUBS_INSTANCE_ID=b.user_id and a.MONTH_ID=b.MONTH_ID LEFT JOIN TMP_DWA_V_M_CUS_3G_IMEI_FLUX_use_$MONTH c on a.SUBS_INSTANCE_ID=c.USER_ID and a.MONTH_ID=c.MONTH_ID left join dwa_v_m_cus_3g_user_3wu_$MONTH d on a.SUBS_INSTANCE_ID=d.subs_instance_id and a.month_id=d.month_id;"

log_info "导出数据到本地"
hive --database $DATABASE -e "INSERT OVERWRITE LOCAL DIRECTORY '$LOCAL_DIR_3G' ROW FORMAT DELIMITED FIELDS TERMINATED BY '|' select * from qinghai_3g_$MONTH;"
end_time=`date +%s`
diff=$[ end_time - start_time ]
log_info "程序执行成功!用时:$diff seconds"
