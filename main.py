import sys
import functions
sys.path.append('tables')

from project_config import *
from dbconnection import *
from tables.stations_table import *
from tables.routes_table import *

class Main:

    config = ProjectConfig()
    connection = DbConnection(config)

    def __init__(self):
        DbTable.dbconn = self.connection
        return

    def db_init(self):
        st = StationTable()
        rt = RoutesTable()
        st.create()
        rt.create()
        return

    def db_insert_somethings(self):
        st = StationTable()
        rt = RoutesTable()
        
        st.example_insert()
        rt.example_insert()
        
    def db_drop(self):
        rt = RoutesTable()
        st = StationTable()
        rt.drop()
        st.drop()
        return

            
    def show_main_menu(self):
        menu = """Добро пожаловать! 
Основное меню (выберите цифру в соответствии с необходимым действием): 
    1 - просмотр станций;
    2 - сброс и инициализация таблиц;
    10 - выход."""
        print(menu)
        return

    def read_next_step(self):
        return input("=> ").strip()

    def after_main_menu(self, next_step):
        if next_step == "2":
            self.db_drop()
            self.db_init()
            self.db_insert_somethings()
            print("Таблицы созданы заново!")
            return "0"
        elif next_step != "1" and next_step != "10":
            print("Выбрано неверное число! Повторите ввод!")
            return "0"
        else:
            return next_step
            
    def show_stations(self):
        self.st_id = -1
        self.st_arr = []
        self.max_name_len = 0
        lst = StationTable().all()
        self.max_st_index = len(lst)
        for i in lst:
            self.st_arr.append([str(i[2]), str(i[3]), str(i[1])])
            self.max_name_len = max(self.max_name_len, len(str(i[2])))
        
        menu = f"""Просмотр списка станций.
№\tНазвание {" "*(self.max_name_len-4)}Тарифная зона{" " *3}Индекс\n\
----------------------------------------------------------------"""
        print(menu)
        for i in range(len(lst)):
            txt = str(i+1) + "\t"
            txt += self.st_arr[i][0] + " "*(4+self.max_name_len-len(self.st_arr[i][0]))
            txt += self.st_arr[i][1] + " "*(13 - len(self.st_arr[i][1]) + 3) + self.st_arr[i][2]
            print(txt)
        menu = """Дальнейшие операции: 
    0 - возврат в главное меню;
    4 - удаление станции;
    5 - добавление станции;
    6 - изменение названия станций;
    7 - просмотр маршрутов;
    9 - добавление маршрута(с использованием станций);
    10 - выход."""
        print(menu)
        return

    def after_show_stations(self, next_step):
        while True:
            if next_step == "4":#delete station
                x = functions.validate_input('Введите номер удаляемой станции (0 - для отмены): ', 0, self.max_st_index)
                if(x!=-1):
                    StationTable().delete(self.st_arr[int(x)-1])
                    print('Станция успешно удалена')
                return "1"

            elif next_step == "5":#insert station
                StationTable().insert()
                print('Станция успешно добавлена')
                return "1"
            
            elif next_step == "6":#update station
                x = functions.validate_input('Введите номер изменяемой станции (0 - для отмены): ', 0, self.max_st_index)
                if(x!=-1):
                    StationTable().update(self.st_arr[int(x)-1])
                    print('Станция успешно изменена')
                return "1"
            
            elif(next_step == "8"): # delete route
                if(self.st_id != -1):
                    x = functions.validate_input('Введите номер удаляемого маршрута (0 - для отмены): ', 0, self.max_rt_index)
                    if(x!=-1):
                        RoutesTable().delete(self.rt_arr[int(x)-1])
                        print('Маршрут успешно удален')
                    else:
                        next_step = "7"
                        return "1"
                else:
                    print("Необходимо выбрать станцию")
                    return "1"
                
                
            elif next_step == "7":#show routes
                self.show_routes_with_station()
        
            elif next_step == "9":#insert route
                RoutesTable().insert(self.max_st_index)
                print('Маршрут успешно добавлен')
                return "1"
                
            elif next_step != "0" and next_step != "10":
                print("Выбрано неверное число! Повторите ввод!")
                return "1"
            else:
                return next_step
            
            
    def show_routes_with_station(self):
        """Вывод всех маршрутов по введенной станции
        """       
        self.routes_arr = []
        if self.st_id == -1:
            while True:
                t = functions.validate_input('Вывести маршрут по:\
            \n1 - начальной станции;\
            \n2 - конечной станции;\n', 0, 2)
                if t == 1:
                    x = functions.validate_input('Выберите номер интересуемой строки с начальной станцией (0 - отмена): ', 0, self.max_st_index)
                    if(x==-1):
                        return
                    else:
                        self.st_id = StationTable().find_by_name(self.st_arr[x-1][0])
                        self.st_obj = self.st_arr[x-1][0]
                    lst = RoutesTable().all_by_st_id(self.st_id, 1)
                    self.max_rt_index = len(lst)
                    if lst == []:
                        print('Нет маршрута с такой начальной станцией')
                    else:
                        print("Выбрана station: " + self.st_obj)
                        print("Маршруты:")
                        print("№\tНомер маршрута\tВыбранная станция\tКонечная станция\
                                \n--------------------------------------------------------")
                        for i in lst:
                            self.routes_arr.append([str(i[0]), str(i[2]), i[1]])
                                
                        for i in range(len(self.routes_arr)):
                            output = f"""{str(i+1)}\t{str(self.routes_arr[i][2])} \t\t\
        {self.st_obj}\t\t{str(StationTable().name_by_id(self.routes_arr[i][1])[0])}"""
                            print(output)
                        menu = """Дальнейшие операции:
0 - возврат в главное меню;
1 - возврат в просмотр станций;
8 - удаление маршрута;
10 - выход."""
                        print(menu)
                        return self.read_next_step()
                
                elif t == 2:
                    x = functions.validate_input('Выберите номер интересуемой строки с конечной станцией (0 - отмена): ', 0, self.max_st_index)
                    if(x==0):
                        return
                    else:
                        self.st_id = StationTable().find_by_name(self.st_arr[x-1][0])
                        self.st_obj = self.st_arr[x-1][0]
                    lst = RoutesTable().all_by_st_id(self.st_id, 2)
                    self.max_rt_index = len(lst)
                    if lst == []:
                        print('Нет маршрута с такой конечной станцией')
                    else:
                        print("Выбрана station: " + self.st_obj)
                        print("Маршруты:")
                        print("№\tНомер маршрута\tВыбранная станция\tНачальная станция\
                                \n--------------------------------------------------------")
                        for i in lst:
                            self.routes_arr.append([str(i[0]), str(i[2]), i[1]])
                                
                        for i in range(len(self.routes_arr)):
                            output = f"""{str(i+1)}\t{str(self.routes_arr[i][1])} \t\t\
        {self.st_obj}\t\t{str(StationTable().name_by_id(self.routes_arr[i][0])[0])}"""
                            print(output)
                        
                        menu = """Дальнейшие операции:
            0 - возврат в главное меню;
            1 - возврат в просмотр станций;
            8 - удаление маршрута;
            10 - выход."""
                        print(menu)
                        return self.read_next_step()
                else:
                    print("Неверный ввод!")
        
    def main_cycle(self):
        current_menu = "0"
        next_step = None
        while(current_menu != "10"):
            if current_menu == "0":
                self.show_main_menu()
                next_step = self.read_next_step()
                current_menu = self.after_main_menu(next_step)
                
            elif current_menu == "1":
                self.show_stations()
                next_step = self.read_next_step()
                current_menu = self.after_show_stations(next_step)
                
            # elif current_menu == "2":
            #     self.show_main_menu()
            #     current_menu = "1"
                
        print("До свидания!")    
        return

    def test(self):
        DbTable.dbconn.test()

m = Main()
# Откоментируйте эту строку и закоментируйте следующую для теста
# соединения с БД
# m.test()
m.main_cycle()
    
