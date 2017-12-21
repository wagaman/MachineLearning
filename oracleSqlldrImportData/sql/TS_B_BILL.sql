CREATE TABLE TS_B_BILL (EPARCHY_CODE VARCHAR2(32) NULL,CITY_CODE VARCHAR2(32) NULL,NET_TYPE_CODE VARCHAR2(10) NULL,SERIAL_NUMBER VARCHAR2(64) NULL,BILL_ID VARCHAR2(20) NULL,ACCT_ID NUMBER(16) NULL,USER_ID NUMBER(16) NULL,CYCLE_ID NUMBER(8) NULL,INTEGRATE_ITEM_CODE VARCHAR2(10) NULL,FEE VARCHAR2(15) NULL,BALANCE VARCHAR2(15) NULL,PRINT_FEE NUMBER(15) NULL,B_DISCNT VARCHAR2(15) NULL,A_DISCNT VARCHAR2(15) NULL,ADJUST_BEFORE VARCHAR2(15) NULL,ADJUST_AFTER VARCHAR2(15) NULL,LATE_FEE VARCHAR2(15) NULL,LATE_BALANCE VARCHAR2(15) NULL,LATECAL_DATE DATE NULL,CANPAY_TAG VARCHAR2(4) NULL,PAY_TAG VARCHAR2(4) NULL,BILL_PAY_TAG VARCHAR2(32) NULL,DESC_OWE_TAG VARCHAR2(32) NULL,VERSION_NO NUMBER(9) NULL,UPDATE_TIME DATE NULL,UPDATE_DEPART_ID VARCHAR2(30) NULL,UPDATE_STAFF_ID VARCHAR2(20) NULL,CHARGE_ID VARCHAR2(40) NULL,WRITEOFF_FEE1 NUMBER(15) NULL,WRITEOFF_FEE2 NUMBER(15) NULL,WRITEOFF_FEE3 NUMBER(15) NULL,BACKUP_INFO VARCHAR2(60) NULL,ROLL_BACK_INFO VARCHAR2(60) NULL,RSRV_FEE1 NUMBER(15) NULL,RSRV_FEE2 NUMBER(15) NULL,RSRV_FEE3 NUMBER(15) NULL,RSRV_INFO1 VARCHAR2(40) NULL,RSRV_INFO2 VARCHAR2(40) NULL,ZK_FEE NUMBER(15) NULL,PROV_ID VARCHAR2(2) NULL,UNI_EPARCHY_CODE VARCHAR2(32) NULL,UNI_CITY_CODE VARCHAR2(32) NULL,UNI_BILL_PAY_TAG VARCHAR2(32) NULL,BALANCE_BACKUP_INFO1 NUMBER(15) NULL,BALANCE_BACKUP_INFO2 NUMBER(15) NULL,CREATE_CYCLE_ID NUMBER(6) NULL);
COMMENT ON COLUMN TS_B_BILL.EPARCHY_CODE IS '用户地市';COMMENT ON COLUMN TS_B_BILL.CITY_CODE IS '用户业务区编码';COMMENT ON COLUMN TS_B_BILL.NET_TYPE_CODE IS '用户网别';COMMENT ON COLUMN TS_B_BILL.SERIAL_NUMBER IS '用户号码';COMMENT ON COLUMN TS_B_BILL.BILL_ID IS '帐单标识';COMMENT ON COLUMN TS_B_BILL.ACCT_ID IS '帐户标识';COMMENT ON COLUMN TS_B_BILL.USER_ID IS '用户标识';COMMENT ON COLUMN TS_B_BILL.CYCLE_ID IS '帐务帐期标识';COMMENT ON COLUMN TS_B_BILL.INTEGRATE_ITEM_CODE IS '帐目编码';COMMENT ON COLUMN TS_B_BILL.FEE IS '帐目金额';COMMENT ON COLUMN TS_B_BILL.BALANCE IS '帐目余额';COMMENT ON COLUMN TS_B_BILL.PRINT_FEE IS '打印金额';COMMENT ON COLUMN TS_B_BILL.B_DISCNT IS '计费优惠金额';COMMENT ON COLUMN TS_B_BILL.A_DISCNT IS '帐务优惠金额';COMMENT ON COLUMN TS_B_BILL.ADJUST_BEFORE IS '帐前调整金额';COMMENT ON COLUMN TS_B_BILL.ADJUST_AFTER IS '帐后调整金额';COMMENT ON COLUMN TS_B_BILL.LATE_FEE IS '滞纳金金额';COMMENT ON COLUMN TS_B_BILL.LATE_BALANCE IS '滞纳金余额';COMMENT ON COLUMN TS_B_BILL.LATECAL_DATE IS '滞纳金结算时间';COMMENT ON COLUMN TS_B_BILL.CANPAY_TAG IS '帐单类型标志';COMMENT ON COLUMN TS_B_BILL.PAY_TAG IS '帐目销帐标志';COMMENT ON COLUMN TS_B_BILL.BILL_PAY_TAG IS '帐单销帐标志';COMMENT ON COLUMN TS_B_BILL.DESC_OWE_TAG IS '降欠标志';COMMENT ON COLUMN TS_B_BILL.VERSION_NO IS '版本号';COMMENT ON COLUMN TS_B_BILL.UPDATE_TIME IS '更新时间';COMMENT ON COLUMN TS_B_BILL.UPDATE_DEPART_ID IS '更新部门';COMMENT ON COLUMN TS_B_BILL.UPDATE_STAFF_ID IS '更新员工';COMMENT ON COLUMN TS_B_BILL.CHARGE_ID IS '最后一次缴费流水';COMMENT ON COLUMN TS_B_BILL.WRITEOFF_FEE1 IS '赠款销账金额';COMMENT ON COLUMN TS_B_BILL.WRITEOFF_FEE2 IS '销帐金额2';COMMENT ON COLUMN TS_B_BILL.WRITEOFF_FEE3 IS '销帐金额3';COMMENT ON COLUMN TS_B_BILL.BACKUP_INFO IS '一次抵扣后欠费备份';COMMENT ON COLUMN TS_B_BILL.ROLL_BACK_INFO IS '抵扣回滚信息';COMMENT ON COLUMN TS_B_BILL.RSRV_FEE1 IS '保留金额1';COMMENT ON COLUMN TS_B_BILL.RSRV_FEE2 IS '保留金额2';COMMENT ON COLUMN TS_B_BILL.RSRV_FEE3 IS '保留金额3';COMMENT ON COLUMN TS_B_BILL.RSRV_INFO1 IS '保留信息1';COMMENT ON COLUMN TS_B_BILL.RSRV_INFO2 IS '保留信息2';COMMENT ON COLUMN TS_B_BILL.ZK_FEE IS '赠款金额';COMMENT ON COLUMN TS_B_BILL.PROV_ID IS '省分标识';COMMENT ON COLUMN TS_B_BILL.UNI_EPARCHY_CODE IS '统一地市编码';COMMENT ON COLUMN TS_B_BILL.UNI_CITY_CODE IS '统一区县编码';COMMENT ON COLUMN TS_B_BILL.UNI_BILL_PAY_TAG IS '统一帐单销帐标志';COMMENT ON COLUMN TS_B_BILL.BALANCE_BACKUP_INFO1 IS '批量抵扣后欠费备份';COMMENT ON COLUMN TS_B_BILL.BALANCE_BACKUP_INFO2 IS '月底欠费备份';COMMENT ON COLUMN TS_B_BILL.CREATE_CYCLE_ID IS '费用生成账期';