import pymysql


class mysqlhelper:
    '''
    helper for mysql
    '''

    __connstr__ = {}

    def __init__(self, host='localhost', user='root', passwd='test', db='test', port=3306, charset='utf8'):
        '''
        init,host(localhost),user(root),passwd(test),db(test),port(3306),charset(utf8)
        '''
        self.__connstr__['host'] = host
        self.__connstr__['user'] = user
        self.__connstr__['passwd'] = passwd
        self.__connstr__['db'] = db
        self.__connstr__['port'] = port
        self.__connstr__['charset'] = charset

    def select(self, cmd, param=tuple()):
        try:
            conn = pymysql.connect(**self.__connstr__)
            with conn.cursor() as cursor:
                cursor.execute(cmd, param)
                result = cursor.fetchall()
                return result
        except Exception as e:
            print("exception catched:" + e.message)
        finally:
            conn.close()

    def query(self, cmd, param=tuple()):
        try:
            conn = pymysql.connect(**self.__connstr__)
            cur = conn.cursor()
            cur.execute(cmd, param)
            result = cur.fetchall()
            conn.commit()
            return result
        except Exception as e:
            print('exception catched:' + e.message)
        finally:
            conn.close()

    def qselect(self, num=1, table='test', con="true"):
        try:
            conn = pymysql.connect(**self.__connstr__)
            with conn.cursor() as cursor:
                sql = 'select * from %s where %s limit %s' % (table, con, num)
                print(sql)
                cursor.execute(sql)
                result = cursor.fetchall()
                return result
        except Exception as e:
            print('exception catched:' + e.message)
        finally:
            conn.close()
