import psycopg2

class DbConnection:
    '''config это класс, который находится в файле config.yaml'''
    def __init__(self, config):
        '''это метод, который вызывается при создании объекта на основе класса DbConnection, 
            и в нём задаются все ключевые параметры'''
        self.dbname = config.dbname
        self.user = config.user
        self.password = config.password
        self.host = config.host
        self.prefix = config.dbtableprefix
        ''' conn - это переменная/атрибут'''
        ''' self.conn - это мы создаем атрибутт conn для ЭТОГО объекта и он хранит информацию о соединении с бд'''
        self.conn = psycopg2.connect(dbname = self.dbname,
                                    user = self.user, 
                                    password = self.password,
                                    host = self.host)

    def __del__(self):
        if self.conn:
            self.conn.close()

    # def dif_stations(self):
    #     '''cursor - это посредник между питоном и бд'''
    #     cur = self.conn.cursor()
    #     cur.execute("DROP TABLE IF EXISTS stations CASCADE")
    #     cur.execute("CREATE TABLE stations(st_id serial, st_name varchar(60), tarrif_zone_id integer, st_index integer)")
    #     cur.execute("INSERT INTO stations(st_id, st_name, tarrif_zone_id, st_index) VALUES(1, 'Нахабино', 1,1)")
    #     self.conn.commit()
    #     cur.execute("SELECT * FROM stations")
    #     result = cur.fetchall()
    #     cur.execute("DROP TABLE stations")
    #     self.conn.commit()
    #     return (result[0][0] == 1)

    # def dif_routes(self):
    #     cur = self.conn.cursor()
    #     cur.execute("DROP TABLE IF EXISTS routes CASCADE")
    #     cur.execute("CREATE TABLE routes(route_id serial, first_st_id integer, last_st_id integer)")
    #     cur.execute("INSERT INTO routes(route_id, first_st_id, last_st_id) VALUES(1,1,2)")
    #     self.conn.commit()
    #     cur.execute("SELECT * FROM routes")
    #     result = cur.fetchall()
    #     cur.execute("DROP TABLE routes")
    #     self.conn.commit()
    #     return (result[0][0] == 1)
        
    def test(self):
        '''cursor - это посредник между питоном и бд'''
        cur = self.conn.cursor()
        cur.execute("DROP TABLE IF EXISTS test CASCADE")
        cur.execute("CREATE TABLE test(test integer)")
        cur.execute("INSERT INTO test(test) VALUES(1)")
        self.conn.commit()
        cur.execute("SELECT * FROM test")
        result = cur.fetchall()
        # cur.execute("DROP TABLE test")
        self.conn.commit()
        return (result[0][0] == 1)
        
