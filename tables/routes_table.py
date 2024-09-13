from tables.stations_table import *
from dbtable import *
import functions

class RoutesTable(DbTable):
    def table_name(self):
        return self.dbconn.prefix + "routes"

    def columns(self):
        return {"id": ["serial", "PRIMARY KEY"],
                "first_st_id": ["integer", "NOT NULL", "REFERENCES stations(id) ON DELETE CASCADE"],
                "last_st_id": ["integer", "NOT NULL", "REFERENCES stations(id) ON DELETE CASCADE"]}
    
    def primary_key(self):
        return ['id']    

    '''def table_constraints(self):
        return ["PRIMARY KEY(route_id)"]'''

                
    def all_by_st_id(self, pid, t):
        if(t == 1):
            sql = f"""SELECT * FROM {self.table_name()} WHERE first_st_id = {str(pid)} ORDER BY {", ".join(self.primary_key())};"""
        else:
            sql = f"""SELECT * FROM {self.table_name()} WHERE last_st_id = {str(pid)} ORDER BY {", ".join(self.primary_key())};"""
        cur = self.dbconn.conn.cursor()
        cur.execute(sql)
        return cur.fetchall()      
    
    def delete(self, val):
        par_sql = "DELETE FROM routes WHERE st_name = %s"
        cur = self.dbconn.conn.cursor()
        value = "".join(val)
        cur.execute(par_sql, (value,))
        self.dbconn.conn.commit()
        
    def insert(self, max_index):
        while True:
            first_st_id = functions.validate_input('Введите номер добавляемой начальной станции (0 - для отмены): ', 0, max_index)
            if(first_st_id == -1): return "1"
            last_st_id = functions.validate_input('Введите номер добавляемой конечной станции (0 - для отмены): ', 0, max_index)
            if(last_st_id == -1): return "1"
            t1 = StationTable().index_by_id(first_st_id)
            t2 = StationTable().index_by_id(last_st_id)
            if t1>t2:
                print('Нельзя добавить такой маршрут')
            else:
                insert = [first_st_id, last_st_id]
                self.insert_one(insert)
                return
        
    def update(self, max_index):
        while True:
            t = functions.validate_input('Изменить маршрут по:\
            \n1 - начальной станции;\
            \n2- конечной станции;\n', 0, 2)
            if(t==1):
                n1 = functions.validate_input('Введите номер начальной станции, который вы хотите заменить (0 - для отмены): ', 0, max_index)
                if(n1 == -1): return "1"
                n2 = functions.validate_input('Введите номер, на который вы хотите поменять (0 - для отмены): ', 0, max_index)
                if(n2 == -1): return "1"
                if n1 != n2:
                    sql = f"""UPDATE {self.table_name()} SET first_st_id = '{n2}' WHERE first_st_id = '{n1}';"""
                    # sql2 = f"""UPDATE stations SET id = '{n2}' WHERE id = '{n1}';"""
                    break
                else:
                    print('Невозможно поменять на такой номер')
            elif(t==2):
                n1 = functions.validate_input('Введите номер конечной станции, который вы хотите заменить (0 - для отмены): ', 0, max_index)
                if(n1 == -1): return "1"
                n2 = functions.validate_input('Введите номер, на который вы хотите поменять (0 - для отмены): ', 0, max_index)
                if(n2 == -1): return "1"
                if n1 != n2:
                    sql = f"""UPDATE {self.table_name()} SET last_st_id = '{n2}' WHERE last_st_id = '{n1}';"""
                    # sql2 = f"""UPDATE stations SET id = '{n2}' WHERE id = '{n1}';"""
                    break
                else:
                    print('Невозможно поменять на такой номер')
        cur = self.dbconn.conn.cursor()
        cur.execute(sql)
        self.dbconn.conn.commit()
        return
    
    def example_insert(self):
        self.insert_one([1,2])
        self.insert_one([1,6])
        self.insert_one([1,7])
        self.insert_one([1,8])
        self.insert_one([1,9])
        self.insert_one([1,6])
        return
