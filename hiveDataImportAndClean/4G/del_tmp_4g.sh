#!/bin/bash
#######################################################################
	#'''	
	#> File Name: del_tmp_4g.sh
	#> Author: cyf
	#> Mail: XXX@qq.com
	#> Created Time: 2017年11月27日 星期一 17时12分33秒
	#'''	
#######################################################################
#set -x
start_time=`date +%s`
CUR=$(cd `dirname $0`;pwd)
#global var
. ${CUR}/../conf/global.conf
log_info "删除tmp表"
hive --database $DATABASE -e "drop table tmp_all_merge_$MONTH;"
hive --database $DATABASE -e "drop table tmp_all_merge_with_cust_sex_$MONTH;"
hive --database $DATABASE -e "drop table tmp_base_info_$MONTH;"
hive --database $DATABASE -e "drop table tmp_calling_days_$MONTH;"
hive --database $DATABASE -e "drop table tmp_current_calling_bei_$MONTH;"
hive --database $DATABASE -e "drop table tmp_current_calling_bei_nums_$MONTH;"
hive --database $DATABASE -e "drop table tmp_current_calling_times_$MONTH;"
hive --database $DATABASE -e "drop table tmp_current_calling_zhu_$MONTH;"
hive --database $DATABASE -e "drop table tmp_dwa_v_m_cus_nm_charge_a_$MONTH;"
hive --database $DATABASE -e "drop table tmp_dwa_v_m_cus_nm_sing_flux_a_$MONTH;"
hive --database $DATABASE -e "drop table tmp_dwd_d_use_cb_flux_filter_$MONTH;"
hive --database $DATABASE -e "drop table tmp_dwd_d_use_cb_flux_manyou_days_$MONTH;"
hive --database $DATABASE -e "drop table tmp_dwd_d_use_cb_sms_filter_$MONTH;"
hive --database $DATABASE -e "drop table tmp_dwd_d_use_cb_voice_filter_$MONTH;"
hive --database $DATABASE -e "drop table tmp_no_calling_days_$MONTH;"
hive --database $DATABASE -e "drop table tmp_user_cust_$MONTH;"
hive --database $DATABASE -e "drop table tmp_using_days_$MONTH;"
hive --database $DATABASE -e "drop table tmp_using_flux_days_$MONTH;"
hive --database $DATABASE -e "drop table tmp_using_merge_$MONTH;"
hive --database $DATABASE -e "drop table tmp_using_sms_days_$MONTH;"
hive --database $DATABASE -e "drop table tmp_using_voice_days_$MONTH;"

hive --database $DATABASE -e "drop table tmp_dwd_m_acc_cb_acct_deposit_yue_$MONTH;"
hive --database $DATABASE -e "drop table tmp_dwd_m_acc_cb_acct_deposit_yue_sum_$MONTH;"
hive --database $DATABASE -e "drop table tmp_dwd_m_acc_cb_paylog_recv_fee_$MONTH;"
hive --database $DATABASE -e "drop table tmp_dwd_m_acc_yue_fee_$MONTH;"
hive --database $DATABASE -e "drop table tmp_qinghai_$MONTH;"
end_time=`date +%s`
diff=$[ end_time - start_time ]
log_info "程序执行成功!用时:$diff seconds"
