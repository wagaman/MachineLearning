CREATE TABLE IF NOT EXISTS DWD_M_ACC_CB_ACCT_DEPOSIT_201708 (MONTH_ID string,PROV_ID string,ACCT_BALANCE_ID string,ACCT_ID string,USER_ID string,DEPOSIT_CODE string,DEPOSIT_MONEY double,INIT_MONEY double,ODD_MONEY double,EVEN_MONEY double,LIMIT_MONEY double,LIMIT_MODE string,LIMIT_LEFT double,INVOICE_FEE double,PRINT_FEE double,START_CYCLE_ID string,END_CYCLE_ID string,START_DATE string,END_DATE string,OWE_FEE double ,VALID_FLAG string,FREEZE_FEE double,PRIVATE_FLAG string,AREA_ID string,AREA_ID_CBSS string,BACKUP_INFO string,ROLL_BACK_INFO string,VERSION_NO int,ACTION_CODE string,OPEN_CYCLE_ID int,UPDATE_TIME string,ACTIVE_TIME string,DRECV_FEE1 double,DRECV_FEE2 double) row format delimited fields terminated by '\001' stored as textfile;