import sys

__author__ = 'sss'
import psycopg2

def getDegree(num):
    degree = len(num)

if __name__ == '__main__':

    print(getDegree(1234567))

    try:
        con = psycopg2.connect(host='127.0.0.1', database='postgres', user='postgres', password='root', port="5432")
        cur = con.cursor()
        cur.execute('select * from test_1.relate_2')
        ver = cur.fetchone()
        print(ver)
    except psycopg2.DatabaseError as e:
        print('Error %s' % e)
        sys.exit(1)
    finally:
        if con:
            con.close()