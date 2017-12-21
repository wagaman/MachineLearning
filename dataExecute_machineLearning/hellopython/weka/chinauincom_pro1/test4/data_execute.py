import sys

__author__ = 'sss'
import psycopg2

def getDegree(num):
    degree = len(num)

if __name__ == '__main__':

    try:
        con = psycopg2.connect(host='127.0.0.1', database='postgres', user='postgres', password='root', port="5432")
        cur = con.cursor()
        cur.execute('SELECT t1."USERID",t1."BRAND", t1."TIME",  t2."BRAND",t2."TIME" FROM "test_1"."user_brand" t1,"test_1"."user_brand" t2 where t1."USERID" = t2."USERID" and t1."TIME" < t2."TIME"ORDER BY t1."USERID", t1."TIME"')
        ver = cur.fetchall()


        tmp_userid = ''
        tmp_timestamp = None
        for change in ver:
            if change[0] != tmp_userid and change[2] != tmp_timestamp:
                print(1)
                tmp_userid = change[0]
                tmp_timestamp = change[2]
                cur.execute('update test_1.user_brand set "NEXT_BRAND" = \''+change[3]+'\' where "USERID" = \''+change[0]+'\' and "TIME" = \''+change[2]+'\'')
                con.commit()
            elif change[0] == tmp_userid and change[2] != tmp_timestamp:
                print(1)
                tmp_userid = change[0]
                tmp_timestamp = change[2]
                cur.execute('update test_1.user_brand set "NEXT_BRAND" = \''+change[3]+'\' where "USERID" = \''+change[0]+'\' and "TIME" = \''+change[2]+'\'')
                con.commit()
            else:
                print(2)

        print(ver)
    except psycopg2.DatabaseError as e:
        print('Error %s' % e)
        sys.exit(1)
    finally:
        if con:
            con.close()