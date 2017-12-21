#!/bin/bash
#######################################################################
	#'''	
	#> File Name: run.sh
	#> Author: cyf
	#> Mail: XXX@qq.com
	#> Created Time: 2017年09月28日 星期四 10时06分23秒
	#'''	
#######################################################################
#set -x
start_time=`date +%s`
CUR=$(cd `dirname $0`;pwd)
#global var
. ${CUR}/../conf/global.conf
#数据处理
log_info "对语音和流量表进行过滤，过滤掉month_id和开始时间不对应的数据"
hive --database $DATABASE -S -e "create table tmp_dwd_d_use_cb_sms_filter_$MONTH as select * from $DWD_D_USE_CB_SMS where month_id=substring(apply_time, 0, 6);"
hive --database $DATABASE -S -e "create table tmp_dwd_d_use_cb_voice_filter_$MONTH as select * from $DWD_D_USE_CB_VOICE where month_id=substring(start_time, 0, 6);"
hive --database $DATABASE -S -e "create table tmp_dwd_d_use_cb_flux_filter_$MONTH as select * from $DWD_D_USE_CB_FLUX where month_id=substring(start_time, 0, 6);"
log_info "########################user telephone info#####################################"
log_info "移网用户自然月内的漫游天数"
hive --database $DATABASE -e "create table tmp_dwd_d_use_cb_flux_manyou_days_$MONTH as select user_id, month_id, count(distinct day_id) as times from tmp_dwd_d_use_cb_flux_filter_$MONTH where roam_type<>'01AA'  group by user_id, month_id;"
log_info "用户当月通话次数"
hive --database $DATABASE -e "create table tmp_current_calling_times_$MONTH as select user_id, month_id, count(*) as times from tmp_dwd_d_use_cb_voice_filter_$MONTH group by user_id, month_id;"
log_info "用户当月主叫通话次数"
hive --database $DATABASE -e "create table tmp_current_calling_zhu_$MONTH as select user_id, month_id, count(*) as times from tmp_dwd_d_use_cb_voice_filter_$MONTH where call_type='01' or call_type='03' group by user_id, month_id;"
log_info "用户当月被叫对方号码个数oppose_number"
hive --database $DATABASE -e "create table tmp_current_calling_bei_nums_$MONTH as select user_id, month_id, count(distinct oppose_number) as times from tmp_dwd_d_use_cb_voice_filter_$MONTH where call_type='02' or call_type='04' group by user_id, month_id;"
hive --database $DATABASE -e "create table tmp_current_calling_bei_$MONTH as select user_id, month_id, count(*) as times from tmp_dwd_d_use_cb_voice_filter_$MONTH where call_type='02' or call_type='04' group by user_id, month_id;"
log_info "当月累计-使用天数（含语音、流量、短信)"
hive --database $DATABASE -e "create table tmp_using_voice_days_$MONTH as select user_id, month_id, day_id, 0 as using_type from tmp_dwd_d_use_cb_voice_filter_$MONTH;"
hive --database $DATABASE -e "create table tmp_using_sms_days_$MONTH as select user_id, month_id, day_id, 1 as using_type from tmp_dwd_d_use_cb_sms_filter_$MONTH;"
hive --database $DATABASE -e "create table tmp_using_flux_days_$MONTH as select user_id, month_id, day_id, 2 as using_type from tmp_dwd_d_use_cb_flux_filter_$MONTH;"
hive --database $DATABASE -e "create table tmp_using_merge_$MONTH as select * from tmp_using_voice_days_$MONTH;"
hive --database $DATABASE -e "insert into tmp_using_merge_$MONTH select * from tmp_using_sms_days_$MONTH;"
hive --database $DATABASE -e "insert into tmp_using_merge_$MONTH select * from tmp_using_flux_days_$MONTH;"
hive --database $DATABASE -e "create table tmp_using_days_$MONTH as select user_id, month_id, count(distinct day_id) as days from tmp_using_merge_$MONTH group by user_id, month_id;"
log_info "当月累计-未产生话单天数"
hive --database $DATABASE -e "create table tmp_calling_days_$MONTH as select user_id, month_id, count(distinct day_id) as calling_days from tmp_dwd_d_use_cb_voice_filter_$MONTH group by user_id, month_id;"
hive --database $DATABASE -e "create table tmp_no_calling_days_$MONTH as select user_id, month_id, (31-cast(calling_days as bigint)) as no_calling_days from tmp_calling_days_$MONTH;"
log_info "创建user_id，cust_id， month_id"
hive --database $DATABASE -e "create table tmp_user_cust_$MONTH as select user_id,cust_id, month_id from $DWA_V_M_CUS_CB_USER_INFO where month_id='$MONTH';"
hive --database $DATABASE -e "create table tmp_all_merge_$MONTH as SELECT a.user_id,a.cust_id,a.month_id, b.times AS roaming_days,c.times AS call_times,d.times AS originate_times,e.times AS destination_phone_numbers,f.no_calling_days,g.days AS using_days FROM tmp_user_cust_$MONTH a LEFT JOIN tmp_dwd_d_use_cb_flux_manyou_days_$MONTH b ON a.user_id = b.user_id and a.month_id=b.month_id LEFT JOIN tmp_current_calling_times_$MONTH c ON a.user_id = c.user_id and a.month_id=c.month_id LEFT JOIN tmp_current_calling_zhu_$MONTH d ON a.user_id = d.user_id and a.month_id=d.month_id LEFT JOIN tmp_current_calling_bei_nums_$MONTH e ON e.user_id = a.user_id and a.month_id=e.month_id LEFT JOIN tmp_no_calling_days_$MONTH f ON f.user_id = a.user_id and a.month_id=f.month_id LEFT JOIN tmp_using_days_$MONTH g ON g.user_id = a.user_id and a.month_id=g.month_id;"
log_info "创建all_merge_with_cust_sex"
hive --database $DATABASE -e "CREATE TABLE tmp_all_merge_with_cust_sex_$MONTH as SELECT a.user_id,a.cust_id,a.month_id,a.roaming_days,a.call_times,a.originate_times,a.destination_phone_numbers,a.no_calling_days,a.using_days,b.CUST_SEX,b.CONSTELLATION_DESC,b.CUST_BIRTHDAY,b.CERT_AGE FROM tmp_all_merge_$MONTH a,$DWA_V_M_CUS_RNS b WHERE a.cust_id=b.CUST_ID and a.month_id=b.MONTH_ID;"
log_info "#################################base_info########################################"
log_info "转换user_id=>dwa_v_m_cus_nm_charge_010"
hive --database $DATABASE -e "create table tmp_dwa_v_m_cus_nm_charge_a_$MONTH as  SELECT MONTH_ID,PROV_ID,substring(USER_ID, 2,16) as USER_ID,SERVICE_TYPE,DEVICE_NUMBER,CUST_ID,IS_ACCT,NORMAL_BILL_FEE,TOTAL_FEE,BASE_RENT_FEE,DINNER_RENT_FEE,FUNCATION_RENT_FEE,OTHER_RENT_FEE,BASE_CALL_FEE,COUN_LONG_LFEE,INTER_LONG_LFEE,GAT_LONG_LFEE,COUN_ROAM_BFEE,INTER_ROAM_BFEE,GAT_RAOM_BFEE,OTHER_CALL_LFEE,P2P_FEE,LTZX_FEE,RBT_FEE,FUNCATION_FEE,NICAM_FEE,MMS_FEE,OTHER_INCR_FEE,MOBILE_NET_FEE,MOBILE_TV_FEE,MOBILE_PAPER_FEE,MOBILE_MUSIC_FEE,MOBILE_EMAIL_FEE,INSTANT_MESSAGE_FEE,MOBILE_SEARCH_FEE,WIDEBRAND_FEE,OTHER_NET_FEE,OTHER_INTERNET_FEE,WIRLESS_CARD_FEE,WLAN_FEE,CHARGE_FAV_FEE,ADJUST_FEE,DISCOUNT_FEE,GRANT_FEE,RECOVER_FEE,OTHER_FEE,PROV_LONG_FEE,VP_FEE,INFO_MMS_FEE,USER_ID_OLD FROM $DWA_V_M_CUS_NM_CHARGE;"
log_info "转换user_id=>dwa_v_m_cus_nm_sing_flux_010"
hive --database $DATABASE -e "create table tmp_dwa_v_m_cus_nm_sing_flux_a_$MONTH as  SELECT MONTH_ID,PROV_ID,SERVICE_TYPE,substring(USER_ID,2,16) as USER_ID,DEVICE_NUMBER,FLUX_NUM,FREE_NUM,BILL_NUM,LOCAL_NUM,ROAM_PROV_NUM,ROAM_CONT_NUM,ROAM_GAT_NUM,ROAM_INT_NUM,TOTAL_FLUX,FREE_FLUX,BILL_FLUX,UP_FLUX,UP_LOCAL_FLUX,UP_ROAM_PROV_FLUX,UP_ROAM_CONT_FLUX,UP_ROAM_GAT_FLUX,UP_ROAM_INT_FLUX,DOWN_FLUX,DOWN_LOCAL_FLUX,DOWN_ROAM_PROV_FLUX,DOWN_ROAM_CONT_FLUX,DOWN_ROAM_GAT_FLUX,DOWN_ROAM_INT_FLUX,TOTAL_DURA,FREE_DURA,BILL_DURA,TOTAL_FEE,PROD_IN_LOCAL_FLUX,PROD_IN_ROAM_CONT_FLUX,PROD_IN_ROAM_GAT_FLUX,PROD_IN_ROAM_INT_FLUX,USER_ID_OLD FROM $DWA_V_M_CUS_NM_SING_FLUX;"
log_info "base_info"
hive --database $DATABASE -e "CREATE TABLE tmp_base_info_$MONTH AS SELECT UI.USER_ID,UI.MONTH_ID,UI.DEVICE_NUMBER,UI.BRAND_ID,UI.INNET_DATE,UI.CHANNEL_ID,UI.AREA_ID,UI.IS_LOST,UI.IS_THIS_BREAK,UI.CREDIT_CLASS,MC.TOTAL_FEE MONTH_FEE,MSF.TOTAL_FLUX MONTH_FlUX,TW.USER_3WU_FLAG FROM $DWA_V_M_CUS_CB_USER_INFO UI LEFT JOIN TMP_DWA_V_M_CUS_NM_CHARGE_a_$MONTH MC ON UI.USER_ID = MC.USER_ID AND UI.MONTH_ID = MC.MONTH_ID LEFT JOIN TMP_DWA_V_M_CUS_NM_SING_FLUX_a_$MONTH MSF ON UI.USER_ID = MSF.USER_ID AND UI.MONTH_ID = MSF.MONTH_ID LEFT JOIN $DWA_V_M_CUS_CB_USER_3WU TW ON UI.USER_ID = TW.USER_ID AND UI.MONTH_ID = TW.MONTH_ID;"

log_info "==================start====================="
log_info "yue and fee"
hive --database $DATABASE -e "CREATE TABLE TMP_DWD_M_ACC_CB_ACCT_DEPOSIT_YUE_$MONTH AS SELECT USER_ID,MONTH_ID,sum(ODD_MONEY) AS ODD_MONEY,sum(EVEN_MONEY) AS EVEN_MONEY FROM $DWD_M_ACC_CB_ACCT_DEPOSIT GROUP BY USER_ID,MONTH_ID;"
hive --database $DATABASE -e "CREATE TABLE TMP_DWD_M_ACC_CB_ACCT_DEPOSIT_YUE_SUM_$MONTH AS SELECT USER_ID,MONTH_ID,(ODD_MONEY+EVEN_MONEY) as YUE FROM TMP_DWD_M_ACC_CB_ACCT_DEPOSIT_YUE_$MONTH;"
hive --database $DATABASE -e "CREATE TABLE TMP_DWD_M_ACC_CB_PAYLOG_RECV_FEE_$MONTH AS SELECT USER_ID,MONTH_ID,sum(RECV_FEE) AS RECV_FEE FROM $DWD_M_ACC_CB_PAYLOG GROUP BY USER_ID,MONTH_ID;"
hive --database $DATABASE -e "CREATE TABLE tmp_dwd_m_acc_yue_fee_$MONTH AS SELECT a.USER_ID,a.MONTH_ID,a.YUE,b.RECV_FEE FROM TMP_DWD_M_ACC_CB_ACCT_DEPOSIT_YUE_SUM_$MONTH a,TMP_DWD_M_ACC_CB_PAYLOG_RECV_FEE_$MONTH b WHERE a.USER_ID = b.USER_ID AND a.MONTH_ID = b.MONTH_ID"
log_info "==================end====================="

log_info "##############################final_merge##########################################"
#final_merge
hive --database $DATABASE -e "create table tmp_qinghai_$MONTH as SELECT a.user_id,b.month_id,b.DEVICE_NUMBER,b.BRAND_ID,b.INNET_DATE,b.CHANNEL_ID,b.AREA_ID,a.CUST_SEX,a.CONSTELLATION_DESC,a.CUST_BIRTHDAY,a.CERT_AGE,b.CREDIT_CLASS,a.roaming_days,a.call_times,a.originate_times,a.destination_phone_numbers,a.no_calling_days,a.using_days,b.is_lost ,b.is_this_break,b.month_fee,b.month_flux,b.user_3wu_flag FROM tmp_all_merge_with_cust_sex_$MONTH a,tmp_base_info_$MONTH b WHERE a.user_id=b.user_id;"
log_info "==================start====================="
hive --database $DATABASE -e "create table qinghai_$MONTH as select a.*,b.YUE, b.RECV_FEE from tmp_qinghai_$MONTH a left join tmp_dwd_m_acc_yue_fee_$MONTH b on a.user_id=b.user_id;"
log_info "==================end====================="

log_info "将all_merge表格导出到本地"
hive --database $DATABASE -e "INSERT OVERWRITE LOCAL DIRECTORY '$LOCAL_DIR_4G' ROW FORMAT DELIMITED FIELDS TERMINATED BY '|' select * from qinghai_$MONTH;"



end_time=`date +%s`
diff=$[ end_time - start_time ]
log_info "程序执行成功!用时:$diff seconds"
