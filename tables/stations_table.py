from dbtable import *
import functions

class StationTable(DbTable):
    '''
    Это класс для таблиц 
    '''
    def table_name(self):
        '''
        Это метод для названия таблицы
        '''
        return self.dbconn.prefix + "stations"

    def columns(self):
        return {"id": ["serial", "PRIMARY KEY"],
                "st_name": ["varchar(60)", "NOT NULL"],
                "tarrif_zone_id": ["integer", "NOT NULL"],
                "st_index": ["integer", "NOT NULL"]}

    def table_constraint(self):
        return ['CONTRAINT "Name" UNIQUE (st_name)']
    
    def find_by_position(self, num):
        sql = "SELECT * FROM " + self.table_name()
        sql += " ORDER BY "
        sql += ", ".join(self.primary_key())
        sql += " LIMIT 1 OFFSET %(offset)s"
        cur = self.dbconn.conn.cursor()
        cur.execute(sql, {"offset": num - 1})
        return cur.fetchone()   
    
    def delete(self, val):
        par_sql = f"DELETE FROM stations WHERE st_name = '{val[0]}';"
        cur = self.dbconn.conn.cursor()
        cur.execute(par_sql)
        self.dbconn.conn.commit()
        
    def insert(self):
        while True:
            st_name = input('Введите название добавляемой станции (enter - отмена): ').strip()
            if len(st_name) > 60:
                print('Недопустмая длина названия станции')
            elif st_name == '':
                return "1"
            else:
                break
        tarrif_zone_id = functions.validate_input('Введите номер тарифной зоны: ', 0, 7)
        if(tarrif_zone_id==-1):
            return "1"
        st_index = functions.validate_input('Введите индекс добавляемой станции: ', 0, 100)
        if(st_index==-1):
            return "1"
        insert = [st_index, st_name, tarrif_zone_id]
        self.insert_one(insert)
            

    def update(self, old):
        """Функция для обновления категории
        """      
        print(f'''Выбрана станция для изменения: {old[0]}''')
        cur = self.dbconn.conn.cursor()
        while True:
            data = input("Введите название (enter - отмена): ").strip()
            if(len(data.strip()) > 60):
                data = input("Название слишком длинное! Введите название заново (enter - отмена):").strip()
            elif(self.check_by_name(data.strip())):
                data = input("Такое название уже существует. Введите новое (enter - отмена):").strip()
            elif(data==''): return 
            else:
                param_sql = f"UPDATE {self.table_name()} SET st_name = '{data}' WHERE st_name = '{old[0]}';"
                cur.execute(param_sql)
                self.dbconn.conn.commit()
                return
    
    def check_by_name(self, value): 
        sql = f"SELECT * FROM {self.table_name()} WHERE st_name='{value}'"  
        cur = self.dbconn.conn.cursor() 
        cur.execute(sql) 
        result = cur.fetchone() 
        cur.close() 
        if result: 
            return True 
        else: 
            return False

    def find_by_name(self, name):
        cur = self.dbconn.conn.cursor()
        param_query = "SELECT id FROM Stations WHERE st_name = %s;"
        # sql_sel = "SELECT id FROM " + self.table_name()
        # sql_sel += " WHERE cath_name = " + "'" + name + "'" + ";"
        cur.execute(param_query, (name,))           
        ret = cur.fetchone()
        return  list(ret)[0] 
    
    def name_by_id(self, id):
        cur = self.dbconn.conn.cursor()
        query = "SELECT st_name FROM Stations WHERE id = %s;"
        cur.execute(query, str(id))
        return cur.fetchone()

    def index_by_id(self,id):
        cur = self.dbconn.conn.cursor()
        query = "SELECT st_index FROM Stations WHERE id = %s;"
        cur.execute(query, str(id))
        return cur.fetchone()
    
    def example_insert(self):
        self.insert_one([1, "Нахабино", 1])
        self.insert_one([2, "Стрешнево", 2])
        self.insert_one([2, "Царицыно", 2])
        self.insert_one([3, "Яуза", 3])
        self.insert_one([2, "Щукинская", 3])
        self.insert_one([4, "Москва-Курская", 4])
        self.insert_one([4, "Дмитровская", 4])
        self.insert_one([4, "Остафьево", 4])
        self.insert_one([4, "Подольск", 4])
        return
