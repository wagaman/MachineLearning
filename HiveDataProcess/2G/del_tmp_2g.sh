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
hive --database $DATABASE -e "drop table tmp_dwa_v_m_cus_2g_imei_flux_use_$MONTH;"
hive --database $DATABASE -e "drop table tmp_dwa_v_m_cus_2g_imei_flux_$MONTH;"
hive --database $DATABASE -e "drop table tmp_dwa_v_m_cus_2g_imei_voice_$MONTH;"
hive --database $DATABASE -e "drop table tmp_dwa_v_m_cus_2g_imei_voice_use_$MONTH;"
end_time=`date +%s`
diff=$[ end_time - start_time ]
log_info "程序执行成功!用时:$diff seconds"
