#!/bin/bash
#######################################################################
	#'''	
	#> File Name: merge_3_months.sh
	#> Author: cuiyufei
	#> Mail: XXX@qq.com
	#> Created Time: 2017年09月28日 星期四 10时06分23秒
	#'''	
#######################################################################
#set -x
start_time=`date +%s`
CUR=$(cd `dirname $0`;pwd)
#global var
. ${CUR}/../conf/global.conf
TABLE1=qinghai_201708
TABLE2=qinghai_201710
TABLE3=qinghai_201711

log_info "merge three month"
hive --database $DATABASE -e "create table final_tmp0_$MONTH as select a.user_id, a.month_id, a.device_number,a.brand_id, a.innet_date, a.channel_id, a.area_id, a.cust_sex, a.constellation_desc, a.cust_birthday, a.cert_age as cert_age_0, a.credit_class as credit_class_0, a.roaming_days as roaming_days_0, a.call_times as call_times_0, a.originate_times as originate_times_0, a.destination_phone_numbers as destination_phone_numbers_0,a.no_calling_days as no_calling_days_0, a.using_days as using_days_0, a.is_lost as is_lost_0,a.is_this_break as is_this_break_0, a.user_3wu_flag as user_3wu_flag_0,a.yue as yue_0, a.recv_fee as recv_fee_0, b.cert_age as cert_age_1, b.credit_class as credit_class_1, b.roaming_days as roaming_days_1, b.call_times as call_times_1, b.originate_times as originate_times_1, b.destination_phone_numbers as destination_phone_numbers_1,b.no_calling_days as no_calling_days_1, b.using_days as using_days_1, b.is_lost as is_lost_1,b.is_this_break as is_this_break_1, b.user_3wu_flag as user_3wu_flag_1,b.yue as yue_1, b.recv_fee as recv_fee_1 from $TABLE1 a left join $TABLE2 b on a.user_id=b.user_id;"
log_info "one"
hive --database $DATABASE -e "create table final_tmp1_$MONTH as select b.user_id, b.month_id, b.device_number,b.brand_id, b.innet_date, b.channel_id, b.area_id, b.cust_sex, b.constellation_desc, b.cust_birthday, b.cert_age as cert_age_0, b.credit_class as credit_class_0, b.roaming_days as roaming_days_0, b.call_times as call_times_0, b.originate_times as originate_times_0, b.destination_phone_numbers as destination_phone_numbers_0,b.no_calling_days as no_calling_days_0, b.using_days as using_days_0, b.is_lost as is_lost_0,b.is_this_break as is_this_break_0, b.user_3wu_flag as user_3wu_flag_0,b.yue as yue_0, b.recv_fee as recv_fee_0, a.cert_age as cert_age_1, a.credit_class as credit_class_1, a.roaming_days as roaming_days_1, a.call_times as call_times_1, a.originate_times as originate_times_1, a.destination_phone_numbers as destination_phone_numbers_1,a.no_calling_days as no_calling_days_1, a.using_days as using_days_1, a.is_lost as is_lost_1,a.is_this_break as is_this_break_1, a.user_3wu_flag as user_3wu_flag_1,a.yue as yue_1, a.recv_fee as recv_fee_1 from $TABLE2 a left join $TABLE1 b on a.user_id=b.user_id;"
log_info "two"
hive --database $DATABASE -e "insert into final_tmp0_$MONTH select * from final_tmp1_$MONTH;"
log_info "three"
hive --database $DATABASE -e "create table final_merge_1_$MONTH as select distinct * from final_tmp0_$MONTH;"
log_info "four"
hive --database $DATABASE -e "create table final_tmp2_$MONTH as select a.*, b.cert_age as cert_age_2, b.credit_class as credit_class_2, b.roaming_days as roaming_days_2, b.call_times as call_times_2, b.originate_times as originate_times_2, b.destination_phone_numbers as destination_phone_numbers_2,b.no_calling_days as no_calling_days_2, b.using_days as using_days_2, b.is_lost as is_lost_2,b.is_this_break as is_this_break_2, b.user_3wu_flag as user_3wu_flag_2,b.yue as yue_2, b.recv_fee as recv_fee_2 from final_merge_1_$MONTH a left join $TABLE3 b on a.user_id=b.user_id;"
log_info "five"
hive --database $DATABASE -e "create table final_tmp3_$MONTH as select b.*, a.cert_age as cert_age_2, a.credit_class as credit_class_2, a.roaming_days as roaming_days_2, a.call_times as call_times_2, a.originate_times as originate_times_2, a.destination_phone_numbers as destination_phone_numbers_2,a.no_calling_days as no_calling_days_2, a.using_days as using_days_2, a.is_lost as is_lost_2,a.is_this_break as is_this_break_2, a.user_3wu_flag as user_3wu_flag_2,a.yue as yue_2, a.recv_fee as recv_fee_2 from $TABLE3 a left join final_merge_1_$MONTH b on a.user_id=b.user_id;"
hive --database $DATABASE -e "insert into final_tmp2_$MONTH as select * from final_tmp3_$MONTH;"
hive --database $DATABASE -e "create table final_merge_2_$MONTH as select distinct * from final_tmp2_$MONTH;"
hive --database $DATABASE -e "alter table final_merge_2_$MONTH rename to qinghai_8_10;"

log_info "rm tmp 表"
hive --database $DATABASE -e "drop table final_merge_1_$MONTH;"
hive --database $DATABASE -e "drop table final_tmp0_$MONTH;"
hive --database $DATABASE -e "drop table final_tmp1_$MONTH;"
hive --database $DATABASE -e "drop table final_tmp2_$MONTH;"
hive --database $DATABASE -e "drop table final_tmp3_$MONTH;"

end_time=`date +%s`
diff=$[ end_time - start_time ]
log_info "程序执行成功!用时:$diff seconds"
