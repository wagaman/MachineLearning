SELECT DISTINCT month_id FROM DWD_M_ACC_CB_PAYLOG LIMIT 10
SELECT user_id,COUNT(*) FROM DWD_M_ACC_CB_PAYLOG GROUP BY user_id HAVING COUNT(*)>1

CREATE TABLE lyh_tmp_paylog_merge AS
SELECT a.*,COUNT(b.PAYMENT_ID)/4 paytimes FROM final_merge_10 a, DWD_M_ACC_CB_PAYLOG b
WHERE a.user_id = b.user_id 
GROUP BY b.user_id

CREATE TABLE lyh_tmp_paylog AS
SELECT user_id,COUNT(*)/4 avepaytimes,SUM(RECV_FEE)/4 avepayfee FROM  DWD_M_ACC_CB_PAYLOG
GROUP  BY user_id

CREATE TABLE lyh_tmp_paylog_merge AS
SELECT a.*,b.avepaytimes FROM final_merge_10 a, lyh_tmp_paylog b
WHERE a.user_id = b.user_id 

SELECT * FROM lyh_tmp_paylog LIMIT 1000

SELECT * FROM DWD_M_ACC_CB_PAYLOG WHERE user_id='7014033124181733'


CREATE TABLE lyh_paylog_merge AS 
SELECT a.*,b.avepaytimes,b.avepayfee
FROM lyh_tmp_paylog b
LEFT JOIN final_merge_10 a ON a.user_id = b.user_id


CREATE INDEX lyh_index_pylog ON qinghai.lyh_tmp_paylog(USER_ID)

CREATE TABLE lyh_tmp_remove AS 
SELECT user_id,COUNT(*),MIN(cert_age) FROM lyh_paylog_merge GROUP BY user_id  HAVING COUNT(*)>1;

SELECT * FROM lyh_paylog_merge WHERE  user_id='7014041424183080'


DESCRIBE lyh_paylog_merge

SELECT * FROM lyh_tmp_remove LIMIT 2
SELECT  * FROM lyh_paylog_merge LIMIT 2
SELECT ISNULL(user_id) FROM lyh_paylog_merge LIMIT 10

DELETE FROM lyh_paylog_merge WHERE ISNULL(user_id)=1
DELETE FROM lyh_tmp_remove WHERE ISNULL(user_id)=1


CREATE INDEX inx_user_merge ON lyh_paylog_merge(user_id);
CREATE INDEX inx_user_tmp ON lyh_tmp_remove(user_id);


DELETE lyh_paylog_merge FROM lyh_paylog_merge , lyh_tmp_remove  WHERE lyh_paylog_merge.user_id = lyh_tmp_remove.user_id AND lyh_paylog_merge.cert_age = lyh_tmp_remove.`min(cert_age)`


SELECT COUNT(*) FROM lyh_paylog_merge

SELECT COUNT(*) FROM lyh_paylog_merge GROUP BY user_id HAVING COUNT(*) >1
#SELECT user_id FROM final_merge_10 GROUP BY user_id  HAVING COUNT(*)>1;
#select * from final_merge_10 where user_id = '7014100624796401'

DESCRIBE lyh_paylog_merge