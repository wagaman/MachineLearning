CREATE TABLE IF NOT EXISTS DWD_M_ACC_CB_PAYLOG_201708 (MONTH_ID string,DAY_ID string,PROV_ID string,CHARGE_ID string,AREA_ID string,AREA_ID_CBSS string,CITY_ID string,CITY_ID_CBSS string,CUST_ID string,USER_ID string,SERIAL_NUMBER string,NET_TYPE_CBSS string,ACCT_ID string,CHANNEL_ID string,PAYMENT_ID int,PAY_FEE_MODE int,PAYMENT_OP int,PAY_METHOD string,RECV_FEE double,LIMIT_MONEY double,RECV_TIME string,RECV_AREA_ID string,RECV_AREA_ID_CBSS string,RECV_CITY_ID string,RECV_CITY_ID_CBSS string,RECV_DEPART_ID string,RECV_STAFF_ID string,PAYMENT_REASON_CODE int,INPUT_NO string,INPUT_MODE int,OUTER_TRADE_ID string,ACT_FLAG string,IS_EXTEND string,ACTION_CODE int,ACTION_EVENT_ID int,PAYMENT_RULE_ID int,CANCEL_FLAG string,CANCEL_STAFF_ID string,CANCEL_DEPART_ID string,CANCEL_CITY_ID string,CANCEL_CITY_ID_CBSS string,CANCEL_AREA_ID string,CANCEL_AREA_ID_CBSS string,CANCEL_TIME string,CANCEL_CHARGE_ID int,STANDARD_KIND_CODE string,ACCT_BALANCE_TYPE string,ACCT_BALANCE_TYPE_CBSS string,PART_ID string) row format delimited fields terminated by '\001' stored as textfile;