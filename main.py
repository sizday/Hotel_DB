from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import pymysql.cursors


class Main(Frame):

    def connect(self):
        self.connection = pymysql.connect(host='localhost',
                                     user='root',
                                     password='dionis0799',
                                     db='qwe',
                                     charset='utf8')

        print("connect successful!!")

    def operation(self, sql):
        print(sql)
        with self.connection.cursor() as cursor:
            cursor.execute(sql)
            rows = cursor.fetchall()
            for row in rows:
                print("{0}".format(row[0]))

    def create_db(self):
        self.connection.cursor().execute(f"call CreateDB('{self.name_db.get()}')")
        self.list_db()
        self.bd_menu = OptionMenu(self, self.choice_db, *self.db)
        self.bd_menu.grid(row=3, column=0, padx=5, pady=10)

    def delete_db(self):
        self.connection.cursor().execute(f"call dropDB('{self.name_db.get()}')")
        self.list_db()
        self.bd_menu = OptionMenu(self, self.choice_db, *self.db)
        self.bd_menu.grid(row=3, column=0, padx=5, pady=10)
        
    def list_db(self):
        self.db = []
        with self.connection.cursor() as cursor:
            cursor.execute("show databases")
            rows = cursor.fetchall()
            for row in rows:
                if row[0] != 'information_schema' and row[0] != 'mysql' and \
                        row[0] != 'performance_schema' and row[0] != 'practice1' and row[0] != "qwe":
                    self.db.append(row[0])
        print(self.db)

    def list_tables(self):
        self.tb = []
        with self.connection.cursor() as cursor:
            cursor.execute("show tables")
            rows = cursor.fetchall()
            for row in rows:
                if row[0] != 'information_schema' and row[0] != 'mysql' and \
                        row[0] != 'performance_schema' and row[0] != 'practice1':
                    self.tb.append(row[0])
        print(self.tb)

    def list_columns(self, table):
        self.cl = []
        with self.connection.cursor() as cursor:
            cursor.execute(f"show columns from {table}")
            rows = cursor.fetchall()
            for row in rows:
                self.cl.append(row[0])
        print(self.cl)

    def column_answer_check(self):
        if self.search.get() == "roomtype":
            self.column_answer.config(text="Количество мест")
        elif self.search.get() == "room":
            self.column_answer.config(text="Тип номера")
        elif self.search.get() == "reservation":
            self.column_answer.config(text="Дата приезда")
        elif self.search.get() == "client":
            self.column_answer.config(text="Полное имя")
        else:
            self.column_answer.config(text="Название статуса")

    def table_answer_check(self):
        if self.add_var.get() == "roomtype":
            self.column1.config(text="typeId")
            self.column2.config(text="title")
            self.column3.config(text="numOfSeats")
            self.column4.config(text="area")
            self.column5.config(text="animals")
            self.column6.config(text="price")
        elif self.add_var.get() == "room":
            self.column1.config(text="roomID")
            self.column2.config(text="room")
            self.column3.config(text="typeID")
            self.column4.config(text="None")
            self.column5.config(text="None")
            self.column6.config(text="None")
        elif self.add_var.get() == "reservation":
            self.column1.config(text="reservID")
            self.column2.config(text="roomID")
            self.column3.config(text="clientID")
            self.column4.config(text="arrivalDate")
            self.column5.config(text="numOfDays")
            self.column6.config(text="total")
        elif self.add_var.get() == "client":
            self.column1.config(text="clientID")
            self.column2.config(text="fullName")
            self.column3.config(text="statusID")
            self.column4.config(text="None")
            self.column5.config(text="None")
            self.column6.config(text="None")
        else:
            self.column1.config(text="statusID")
            self.column2.config(text="stat")
            self.column3.config(text="discount")
            self.column4.config(text="None")
            self.column5.config(text="None")
            self.column6.config(text="None")

    def table_answer_check2(self):
        if self.select_var.get() == "roomtype":
            self.list_columns("roomtype")
        elif self.select_var.get() == "room":
            self.list_columns("room")
        elif self.select_var.get() == "reservation":
            self.list_columns("reservation")
        elif self.select_var.get() == "client":
            self.list_columns("client")
        else:
            self.list_columns("stat")
        self.tree.config(column=self.cl)
        for i in range(len(self.cl)):
            self.tree.heading(self.cl[i], text=self.cl[i])
            self.tree.column(self.cl[i], width=int(385/len(self.cl)))
        self.select()

    def search_fun(self):
        sql = ""
        with self.connection.cursor() as cursor:
            if self.search.get() == "roomtype":
                sql = f"call findTable1({self.search_message.get()})"
                cursor.execute(sql)
            elif self.search.get() == "room":
                sql = f"call findTable2({self.search_message.get()})"
                cursor.execute(sql)
            elif self.search.get() == "reservation":
                sql = f"call findTable3('{self.search_message.get()}')"
                cursor.execute(sql)
            elif self.search.get() == "client":
                sql = f"call findTable4('{self.search_message.get()}')"
                cursor.execute(sql)
            elif self.search.get() == "stat":
                sql = f"call findTable5('{self.search_message.get()}')"
                cursor.execute(sql)
            else:
                print("ошибка")
            rows = cursor.fetchall()
            print(sql)
            for row in rows:
                self.result_list.insert(0, row)
                print(row)

    def delete_type(self):
        if self.type_var.get() == "все таблицы":
            self.where_menu['state'] = 'disabled'
            self.where_button['state'] = 'disabled'
            self.delete_entry['state'] = 'disabled'
        elif self.type_var.get() == "одна таблица":
            self.where_menu['state'] = 'normal'
            self.where_button['state'] = 'normal'
            self.delete_entry['state'] = 'disabled'
        else:
            self.where_menu['state'] = 'normal'
            self.where_button['state'] = 'normal'
            self.delete_entry['state'] = 'normal'

    def where_delete(self):
        if self.type_var.get() == "одна таблица":
            self.change_label['text'] = self.where_var.get()
        elif self.type_var.get() == "запись по ID":
            if self.where_var.get() == "roomtype":
                self.change_label['text'] = "typeID"
            elif self.where_var.get() == "room":
                self.change_label['text'] = "roomID"
            elif self.where_var.get() == "reservation":
                self.change_label['text'] = "reservID"
            elif self.where_var.get() == "client":
                self.change_label['text'] = "clientID"
            else:
                self.change_label['text'] = "statusID"
        elif self.type_var.get() == "запись":
            if self.where_var.get() == "roomtype":
                self.change_label['text'] = "numOfSeats"
            elif self.where_var.get() == "room":
                self.change_label['text'] = "typeID"
            elif self.where_var.get() == "reservation":
                self.change_label['text'] = "arrivalDate"
            elif self.where_var.get() == "client":
                self.change_label['text'] = "fullName"
            else:
                self.change_label['text'] = "stat"

    def delete_fun(self):
        sql = ""
        if self.type_var.get() == "одна таблица":
            if self.where_var.get() == "roomtype":
                sql = "call deleteTable1"
            elif self.where_var.get() == "room":
                sql = "call deleteTable2"
            elif self.where_var.get() == "reservation":
                sql = "call deleteTable3"
            elif self.where_var.get() == "client":
                sql = "call deleteTable4"
            elif self.where_var.get() == "stat":
                sql = "call deleteTable5"
        elif self.type_var.get() == "запись по ID":
            if self.where_var.get() == "roomtype":
                sql = f"call deleteIDTable1({self.delete_message.get()})"
            elif self.where_var.get() == "room":
                sql = f"call deleteIDTable2({self.delete_message.get()})"
            elif self.where_var.get() == "reservation":
                sql = f"call deleteIDTable3({self.delete_message.get()})"
            elif self.where_var.get() == "client":
                sql = f"call deleteIDTable4({self.delete_message.get()})"
            elif self.where_var.get() == "stat":
                sql = f"call deleteIDTable5({self.delete_message.get()})"
        elif self.type_var.get() == "запись":
            if self.where_var.get() == "roomtype":
                sql = f"call deleteStrTable1({self.delete_message.get()})"
            elif self.where_var.get() == "room":
                sql = f"call deleteStrTable2({self.delete_message.get()})"
            elif self.where_var.get() == "reservation":
                sql = f"call deleteStrTable3('{self.delete_message.get()}')"
            elif self.where_var.get() == "client":
                sql = f"call deleteStrTable4('{self.delete_message.get()}')"
            elif self.where_var.get() == "stat":
                sql = f"call deleteStrTable5('{self.delete_message.get()}')"
        elif self.type_var.get() == "все таблицы":
            sql = "call deleteAll"
        else:
            print("ошибка")
        self.connection.cursor().execute(sql)
        print(sql)
        self.connection.commit()

    def add_func(self):
        if self.add_var.get() == "roomtype":
            sql = "call insertTable1({}, '{}', {}, {}, {}, {})".format(
                self.column_answer1.get(), self.column_answer2.get(), self.column_answer3.get(),
                self.column_answer4.get(), self.column_answer5.get(), self.column_answer6.get())
            self.connection.cursor().execute(sql)
        elif self.add_var.get() == "room":
            sql = "call insertTable2({}, {}, {})".format(
                self.column_answer1.get(), self.column_answer2.get(), self.column_answer3.get())
            self.connection.cursor().execute(sql)
        elif self.add_var.get() == "reservation":
            sql = "call insertTable3({}, {}, {}, '{}', {}, {})".format(
                self.column_answer1.get(), self.column_answer2.get(), self.column_answer3.get(),
                self.column_answer4.get(), self.column_answer5.get(), self.column_answer6.get())
            self.connection.cursor().execute(sql)
        elif self.add_var.get() == "client":
            sql = "call insertTable4({}, '{}', {})".format(
                self.column_answer1.get(), self.column_answer2.get(), self.column_answer3.get())
            self.connection.cursor().execute(sql)
        elif self.add_var.get() == "stat":
            sql = "call insertTable5({}, '{}', {})".format(
                self.column_answer1.get(), self.column_answer2.get(), self.column_answer3.get())
            self.connection.cursor().execute(sql)
        else:
            sql = "ошибка"
        print(sql)
        self.connection.commit()

    def update_func(self):
        if self.add_var.get() == "roomtype":
            sql = "call upgradeTable1({}, '{}', {}, {}, {}, {})".format(
                self.column_answer1.get(), self.column_answer2.get(), self.column_answer3.get(),
                self.column_answer4.get(), self.column_answer5.get(), self.column_answer6.get())
            self.connection.cursor().execute(sql)
        elif self.add_var.get() == "room":
            sql = "call upgradeTable2({}, {}, {})".format(
                self.column_answer1.get(), self.column_answer2.get(), self.column_answer3.get())
            self.connection.cursor().execute(sql)
        elif self.add_var.get() == "reservation":
            sql = "call upgradeTable3({}, {}, {}, '{}', {}, {})".format(
                self.column_answer1.get(), self.column_answer2.get(), self.column_answer3.get(),
                self.column_answer4.get(), self.column_answer5.get(), self.column_answer6.get())
            self.connection.cursor().execute(sql)
        elif self.add_var.get() == "client":
            sql = "call upgradeTable4({}, '{}', {})".format(
                self.column_answer1.get(), self.column_answer2.get(), self.column_answer3.get())
            self.connection.cursor().execute(sql)
        elif self.add_var.get() == "stat":
            sql = "call upgradeTable5({}, '{}', {})".format(
                self.column_answer1.get(), self.column_answer2.get(), self.column_answer3.get())
            self.connection.cursor().execute(sql)
        else:
            sql = "ошибка"
        print(sql)
        self.connection.commit()

    def select(self):
        with self.connection.cursor() as cursor:
            if self.select_var.get() == "roomtype":
                cursor.execute("call showTable1")
            elif self.select_var.get() == "room":
                cursor.execute("call showTable2")
            elif self.select_var.get() == "reservation":
                cursor.execute("call showTable3")
            elif self.select_var.get() == "client":
                cursor.execute("call showTable4")
            else:
                cursor.execute("call showTable5")
            rows = cursor.fetchall()
            for row in rows:
                print(row)
                self.tree.insert('', 'end', values=row)

    def close_app(self):
        if self.window == "option":
            self.delete_option()
            self.init_main()
        elif self.window == "add":
            self.delete_add()
            self.init_option()
        elif self.window == "search":
            self.delete_search()
            self.init_option()
        elif self.window == "update":
            self.delete_update()
            self.init_option()
        elif self.window == "delete":
            self.delete_delete()
            self.init_option()
        elif self.window == "select":
            self.delete_select()
            self.init_option()

    def execute_file_scripts(self):
        fd = open("hostel.txt", 'r')
        sqlFile = fd.read()
        fd.close()
        sqlCommands = sqlFile.split('//')

        cursor = self.connection.cursor()
        for command in sqlCommands:
            if command.strip() != '':
                    cursor.execute(command)

    # init
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.connect()
        self.parent = parent
        self.window = ""
        self.color = "black"
        self.bg = "white"
        self.fgr_bg = "white"
        self.brush_size = 5
        self.init_main()

    def init_main(self):
        self.master.title("Hostel")
        self.pack(fill=BOTH, expand=1)
        self.list_db()
        self.window = "main"
        self.set_main()

    def init_option(self):
        self.master.title("Hostel")
        self.pack(fill=BOTH, expand=1)
        name = self.choice_db.get()
        self.window = "option"
        self.set_option(name)

    def init_search(self):
        self.master.title("Search")
        self.pack(fill=BOTH, expand=1)
        name = self.choice_db.get()
        self.window = "search"
        self.set_search(name)

    def init_add(self):
        self.master.title("Add")
        self.pack(fill=BOTH, expand=1)
        name = self.choice_db.get()
        self.window = "add"
        self.set_add(name)

    def init_delete(self):
        self.master.title("Delete")
        self.pack(fill=BOTH, expand=1)
        name = self.choice_db.get()
        self.window = "delete"
        self.set_delete(name)

    def init_update(self):
        self.master.title("Update")
        self.pack(fill=BOTH, expand=1)
        name = self.choice_db.get()
        self.window = "update"
        self.set_update(name)

    def init_select(self):
        self.master.title("Select")
        self.pack(fill=BOTH, expand=1)
        name = self.choice_db.get()
        self.window = "select"
        self.set_select(name)

    # use
    def use_bd(self):
        self.delete_main()
        self.init_option()
        self.operation(f"use {self.choice_db.get()}")
        self.execute_file_scripts()
        self.operation("call createTable1")
        self.operation("call createTable2")
        self.operation("call createTable5")
        self.operation("call createTable4")
        self.operation("call createTable3")

    def use_search(self):
        self.delete_option()
        self.list_tables()
        self.init_search()

    def use_add(self):
        self.delete_option()
        self.list_tables()
        self.init_add()

    def use_delete(self):
        self.delete_option()
        self.list_tables()
        self.init_delete()

    def use_update(self):
        self.delete_option()
        self.list_tables()
        self.init_update()

    def use_select(self):
        self.delete_option()
        self.list_tables()
        self.init_select()

    # set
    def set_option(self, name):
        self.columnconfigure(2, weight=1)
        self.rowconfigure(7, weight=1)
        self.back_button = Button(self, font="Arial 10", background="white", text="назад",
                                  justify=RIGHT, command=self.close_app)
        self.back_button.grid(row=1, column=1, padx=5, sticky=E)
        self.name_label = Label(self, text=name, font="Arial 48", justify=CENTER)
        self.name_label.grid(row=0, column=0, columnspan=2)
        self.output_button = Button(self, width=16, height=1, font="12",
                               background="white", text="вывод", command=self.use_select)
        self.output_button.grid(row=2, column=1, padx=5, pady=10)
        self.delete_button = Button(self, width=16, height=1, font="12",
                               background="white", text="удалить", command=self.use_delete)
        self.delete_button.grid(row=3, column=1, padx=5, pady=10)
        self.search_button = Button(self, width=16, height=1, font="12",
                               background="white", text="поиск", command=self.use_search)
        self.search_button.grid(row=4, column=1, padx=5, pady=10)
        self.update_button = Button(self, width=16, height=1, font="12",
                               background="white", text="обновить", command=self.use_update)
        self.update_button.grid(row=5, column=1, padx=5, pady=10)
        self.add_button = Button(self, width=16, height=1, font="12",
                                    background="white", text="добавить", command=self.use_add)
        self.add_button.grid(row=6, column=1, padx=5, pady=10)
        size = (40, 40)
        self.img1 = ImageTk.PhotoImage(Image.open("output.png").resize(size))
        self.output_logo = Label(self, justify=CENTER, image=self.img1)
        self.output_logo.grid(row=2, column=0, padx=70)
        self.img2 = ImageTk.PhotoImage(Image.open("delete.png").resize(size))
        self.delete_logo = Label(self, justify=CENTER, image=self.img2)
        self.delete_logo.grid(row=3, column=0, padx=70)
        self.img3 = ImageTk.PhotoImage(Image.open("search.png").resize(size))
        self.search_logo = Label(self, justify=CENTER, image=self.img3)
        self.search_logo.grid(row=4, column=0, padx=70)
        self.img4 = ImageTk.PhotoImage(Image.open("update.png").resize(size))
        self.update_logo = Label(self, justify=CENTER, image=self.img4)
        self.update_logo.grid(row=5, column=0, padx=70)
        self.img5 = ImageTk.PhotoImage(Image.open("add.png").resize(size))
        self.add_logo = Label(self, justify=CENTER, image=self.img5)
        self.add_logo.grid(row=6, column=0, padx=70)

    def set_main(self):
        self.columnconfigure(2, weight=1)
        self.rowconfigure(4, weight=1)
        self.bg_label = Label(self, text="Hostel", font="Arial 48", justify=CENTER)
        self.bg_label.grid(row=0, column=0, columnspan=2)
        self.bd_label = Label(self, text="название БД", font="Arial 16", justify=CENTER)
        self.bd_label.grid(row=1, column=0)
        self.name_db = StringVar()
        self.bd_entry = Entry(self, textvariable=self.name_db, font="16", width=15)
        self.bd_entry.grid(row=1, column=1, padx=10, pady=10)
        self.delete_button = Button(self, width=16, height=2, font="12",
                                    background="white", text="Удалить", command=self.delete_db)
        self.delete_button.grid(row=2, column=1, padx=5, pady=10)
        self.new_button = Button(self, width=16, height=2, font="12",
                            background="white", text="Создать", command=self.create_db)
        self.new_button.grid(row=2, column=0, padx=5, pady=10)
        self.choice_db = StringVar(self)
        self.choice_db.set("выберете")
        self.bd_menu = OptionMenu(self, self.choice_db, *self.db)
        self.bd_menu.grid(row=3, column=0, padx=5, pady=10)
        self.use_button = Button(self, width=16, height=2, font="12", background="white",
                            text="Использовать", command=self.use_bd)
        self.use_button.grid(row=3, column=1, padx=5, pady=10)

    def set_search(self, name):
        self.columnconfigure(3, weight=1)
        self.rowconfigure(6, weight=1)
        self.back_button = Button(self, font="Arial 10", background="white", text="назад",
                                  justify=RIGHT, command=self.close_app)
        self.back_button.grid(row=1, column=2, padx=5, sticky=E)
        self.name_label = Label(self, text="Search in " + name, font="Arial 24", justify=CENTER)
        self.name_label.grid(row=0, column=0, columnspan=3)
        self.table_label = Label(self, text="Таблица", font="Arial 14", justify=CENTER)
        self.table_label.grid(row=2, column=0)
        self.column_label = Label(self, text="Столбец", font="Arial 14", justify=CENTER)
        self.column_label.grid(row=3, column=0)
        self.search_label = Label(self, text="Что искать?", font="Arial 14", justify=CENTER)
        self.search_label.grid(row=4, column=0)
        self.search_button = Button(self, width=8, height=1, font="12", background="white",
                                    text="Принять", command=self.column_answer_check)
        self.search_button.grid(row=2, column=2, padx=10, pady=10)
        self.search = StringVar(self)
        self.search.set("выберете")
        self.table_menu = OptionMenu(self, self.search, *self.tb)
        self.table_menu.grid(row=2, column=1, padx=10, pady=10)
        self.column_answer = Label(self, text="column", font="Arial 10", justify=CENTER)
        self.column_answer.grid(row=3, column=1, padx=10, pady=10)
        self.search_message = StringVar()
        self.text_entry = Entry(self, textvariable=self.search_message)
        self.text_entry.grid(row=4, column=1, padx=10, pady=10)
        self.search_button = Button(self, width=12, height=2, font="12", background="white",
                                    text="Поиск", command=self.search_fun)
        self.search_button.grid(row=4, column=2, padx=10, pady=10)
        self.result_list = Listbox(width=40, height=8, font="Arial 12")
        self.result_list.pack()

    def set_add(self, name):
        self.columnconfigure(3, weight=1)
        self.rowconfigure(6, weight=1)
        self.back_button = Button(self, font="Arial 10", background="white", text="назад",
                                  justify=RIGHT, command=self.close_app)
        self.back_button.grid(row=1, column=2, padx=5, sticky=E)
        self.name_label = Label(self, text="Add to " + name, font="Arial 24", justify=CENTER)
        self.name_label.grid(row=0, column=0, columnspan=3)
        self.table_label = Label(self, text="Таблица", font="Arial 14", justify=CENTER)
        self.table_label.grid(row=2, column=0)
        self.add_var = StringVar(self)
        self.add_var.set("выберете")
        self.table_menu = OptionMenu(self, self.add_var, *self.tb)
        self.table_menu.grid(row=2, column=1, padx=10, pady=10)
        self.check_button = Button(self, width=8, height=1, font="12", background="white",
                                    text="Принять", command=self.table_answer_check)
        self.check_button.grid(row=2, column=2, padx=10, pady=10)
        self.column1 = Label(self, text="column1", font="Arial 14", justify=CENTER)
        self.column1.grid(row=3, column=0)
        self.column2 = Label(self, text="column2", font="Arial 14", justify=CENTER)
        self.column2.grid(row=4, column=0)
        self.column3 = Label(self, text="column3", font="Arial 14", justify=CENTER)
        self.column3.grid(row=5, column=0)
        self.column4 = Label(self, text="column4", font="Arial 14", justify=CENTER)
        self.column4.grid(row=6, column=0)
        self.column5 = Label(self, text="column5", font="Arial 14", justify=CENTER)
        self.column5.grid(row=7, column=0)
        self.column6 = Label(self, text="column6", font="Arial 14", justify=CENTER)
        self.column6.grid(row=8, column=0)
        self.column_answer1 = StringVar()
        self.column_answer2 = StringVar()
        self.column_answer3 = StringVar()
        self.column_answer4 = StringVar()
        self.column_answer5 = StringVar()
        self.column_answer6 = StringVar()
        self.entry1 = Entry(self, textvariable=self.column_answer1)
        self.entry1.grid(row=3, column=1, padx=10, pady=10)
        self.entry2 = Entry(self, textvariable=self.column_answer2)
        self.entry2.grid(row=4, column=1, padx=10, pady=10)
        self.entry3 = Entry(self, textvariable=self.column_answer3)
        self.entry3.grid(row=5, column=1, padx=10, pady=10)
        self.entry4 = Entry(self, textvariable=self.column_answer4)
        self.entry4.grid(row=6, column=1, padx=10, pady=10)
        self.entry5 = Entry(self, textvariable=self.column_answer5)
        self.entry5.grid(row=7, column=1, padx=10, pady=10)
        self.entry6 = Entry(self, textvariable=self.column_answer6)
        self.entry6.grid(row=8, column=1, padx=10, pady=10)
        self.add_button = Button(self, width=12, height=2, font="12", background="white",
                                    text="Добавить", command=self.add_func)
        self.add_button.grid(row=7, column=2, padx=10, pady=10, rowspan=2)

    def set_delete(self, name):
        self.columnconfigure(3, weight=1)
        self.rowconfigure(6, weight=1)
        self.back_button = Button(self, font="Arial 10", background="white", text="назад",
                                  justify=RIGHT, command=self.close_app)
        self.back_button.grid(row=1, column=2, padx=5, sticky=E)
        self.name_label = Label(self, text="Delete in " + name, font="Arial 24", justify=CENTER)
        self.name_label.grid(row=0, column=0, columnspan=3)
        self.type_label = Label(self, text="Тип удаления:", font="Arial 14", justify=CENTER)
        self.type_label.grid(row=2, column=0)
        self.where_label = Label(self, text="Откуда удалять?", font="Arial 14", justify=CENTER)
        self.where_label.grid(row=3, column=0)
        self.field_label = Label(self, text="Поле удаления", font="Arial 14", justify=CENTER)
        self.field_label.grid(row=4, column=0)
        self.what_label = Label(self, text="Что удалять?", font="Arial 14", justify=CENTER)
        self.what_label.grid(row=5, column=0)
        self.type_var = StringVar(self)
        self.type_var.set("тип")
        self.type_menu = OptionMenu(self, self.type_var, "все таблицы", "одна таблица", "запись по ID", "запись")
        self.type_menu.grid(row=2, column=1, padx=10, pady=5)
        self.where_var = StringVar(self)
        self.where_var.set("таблица")
        self.where_menu = OptionMenu(self, self.where_var, *self.tb)
        self.where_menu.grid(row=3, column=1, padx=10, pady=5)
        self.change_label = Label(self, text="None", font="Arial 14", justify=CENTER)
        self.change_label.grid(row=4, column=1)
        self.delete_message = StringVar()
        self.delete_entry = Entry(self, textvariable=self.delete_message)
        self.delete_entry.grid(row=5, column=1, padx=10, pady=5)
        self.type_button = Button(self, width=12, height=2, font="12", background="white",
                                    text="Принять", command=self.delete_type)
        self.type_button.grid(row=2, column=2, padx=10, pady=5)
        self.where_button = Button(self, width=12, height=2, font="12", background="white",
                                    text="Принять", command=self.where_delete)
        self.where_button.grid(row=3, column=2, padx=10, pady=5)
        self.delete_button = Button(self, width=12, height=2, font="12", background="white",
                                    text="Удалить", command=self.delete_fun)
        self.delete_button.grid(row=5, column=2, padx=10, pady=5)

    def set_update(self, name):
        self.columnconfigure(3, weight=1)
        self.rowconfigure(6, weight=1)
        self.back_button = Button(self, font="Arial 10", background="white", text="назад",
                                  justify=RIGHT, command=self.close_app)
        self.back_button.grid(row=1, column=2, padx=5, sticky=E)
        self.name_label = Label(self, text="Delete in " + name, font="Arial 24", justify=CENTER)
        self.name_label.grid(row=0, column=0, columnspan=3)
        self.table_label = Label(self, text="Таблица", font="Arial 14", justify=CENTER)
        self.table_label.grid(row=2, column=0)
        self.add_var = StringVar(self)
        self.add_var.set("выберете")
        self.table_menu = OptionMenu(self, self.add_var, *self.tb)
        self.table_menu.grid(row=2, column=1, padx=10, pady=10)
        self.check_button = Button(self, width=8, height=1, font="12", background="white",
                                   text="Принять", command=self.table_answer_check)
        self.check_button.grid(row=2, column=2, padx=10, pady=10)
        self.column1 = Label(self, text="column1", font="Arial 14", justify=CENTER)
        self.column1.grid(row=3, column=0)
        self.column2 = Label(self, text="column2", font="Arial 14", justify=CENTER)
        self.column2.grid(row=4, column=0)
        self.column3 = Label(self, text="column3", font="Arial 14", justify=CENTER)
        self.column3.grid(row=5, column=0)
        self.column4 = Label(self, text="column4", font="Arial 14", justify=CENTER)
        self.column4.grid(row=6, column=0)
        self.column5 = Label(self, text="column5", font="Arial 14", justify=CENTER)
        self.column5.grid(row=7, column=0)
        self.column6 = Label(self, text="column6", font="Arial 14", justify=CENTER)
        self.column6.grid(row=8, column=0)
        self.column_answer1 = StringVar()
        self.column_answer2 = StringVar()
        self.column_answer3 = StringVar()
        self.column_answer4 = StringVar()
        self.column_answer5 = StringVar()
        self.column_answer6 = StringVar()
        self.entry1 = Entry(self, textvariable=self.column_answer1)
        self.entry1.grid(row=3, column=1, padx=10, pady=10)
        self.entry2 = Entry(self, textvariable=self.column_answer2)
        self.entry2.grid(row=4, column=1, padx=10, pady=10)
        self.entry3 = Entry(self, textvariable=self.column_answer3)
        self.entry3.grid(row=5, column=1, padx=10, pady=10)
        self.entry4 = Entry(self, textvariable=self.column_answer4)
        self.entry4.grid(row=6, column=1, padx=10, pady=10)
        self.entry5 = Entry(self, textvariable=self.column_answer5)
        self.entry5.grid(row=7, column=1, padx=10, pady=10)
        self.entry6 = Entry(self, textvariable=self.column_answer6)
        self.entry6.grid(row=8, column=1, padx=10, pady=10)
        self.add_button = Button(self, width=12, height=2, font="12", background="white",
                                 text="Обновить", command=self.update_func)
        self.add_button.grid(row=7, column=2, padx=10, pady=10, rowspan=2)

    def set_select(self, name):
        self.columnconfigure(3, weight=1)
        self.rowconfigure(6, weight=1)
        self.back_button = Button(self, font="Arial 10", background="white", text="назад",
                                  justify=RIGHT, command=self.close_app)
        self.back_button.grid(row=1, column=2, padx=5, sticky=E)
        self.name_label = Label(self, text="Select in " + name, font="Arial 24", justify=CENTER)
        self.name_label.grid(row=0, column=0, columnspan=3)
        self.table_label = Label(self, text="Таблица", font="Arial 14", justify=CENTER)
        self.table_label.grid(row=2, column=0)
        self.select_var = StringVar(self)
        self.select_var.set("выберете")
        self.table_menu = OptionMenu(self, self.select_var, *self.tb)
        self.table_menu.grid(row=2, column=1, padx=10, pady=10)
        self.check_button = Button(self, width=8, height=1, font="12", background="white",
                                   text="вывести", command=self.table_answer_check2)
        self.check_button.grid(row=2, column=2, padx=10, pady=10)
        self.tree = ttk.Treeview(self, columns=('', '', ''), height=15, show='headings')
        self.tree.grid(row=3, column=0, padx=10, pady=10, columnspan=3)

    # delete
    def delete_main(self):
        self.bg_label.destroy()
        self.bd_label.destroy()
        self.new_button.destroy()
        self.delete_button.destroy()
        self.bd_menu.destroy()
        self.use_button.destroy()
        self.bd_entry.destroy()
        self.bd_menu.destroy()

    def delete_option(self):
        self.name_label.destroy()
        self.delete_button.destroy()
        self.output_button.destroy()
        self.search_button.destroy()
        self.update_button.destroy()
        self.output_logo.destroy()
        self.delete_logo.destroy()
        self.search_logo.destroy()
        self.update_logo.destroy()
        self.add_button.destroy()
        self.add_logo.destroy()
        self.back_button.destroy()

    def delete_search(self):
        self.name_label.destroy()
        self.table_label.destroy()
        self.column_label.destroy()
        self.search_label.destroy()
        self.table_menu.destroy()
        self.column_answer.destroy()
        self.text_entry.destroy()
        self.search_button.destroy()
        self.back_button.destroy()
        self.result_list.destroy()

    def delete_add(self):
        self.name_label.destroy()
        self.table_label.destroy()
        self.table_menu.destroy()
        self.check_button.destroy()
        self.column1.destroy()
        self.column2.destroy()
        self.column3.destroy()
        self.column4.destroy()
        self.column5.destroy()
        self.column6.destroy()
        self.entry1.destroy()
        self.entry2.destroy()
        self.entry3.destroy()
        self.entry4.destroy()
        self.entry5.destroy()
        self.entry6.destroy()
        self.add_button.destroy()
        self.back_button.destroy()

    def delete_delete(self):
        self.name_label.destroy()
        self.type_label.destroy()
        self.where_label.destroy()
        self.field_label.destroy()
        self.what_label.destroy()
        self.type_menu.destroy()
        self.where_menu.destroy()
        self.change_label.destroy()
        self.delete_entry.destroy()
        self.type_button.destroy()
        self.where_button.destroy()
        self.delete_button.destroy()
        self.back_button.destroy()

    def delete_update(self):
        self.name_label.destroy()
        self.table_label.destroy()
        self.table_menu.destroy()
        self.check_button.destroy()
        self.column1.destroy()
        self.column2.destroy()
        self.column3.destroy()
        self.column4.destroy()
        self.column5.destroy()
        self.column6.destroy()
        self.entry1.destroy()
        self.entry2.destroy()
        self.entry3.destroy()
        self.entry4.destroy()
        self.entry5.destroy()
        self.entry6.destroy()
        self.add_button.destroy()
        self.back_button.destroy()

    def delete_select(self):
        self.back_button.destroy()
        self.name_label.destroy()
        self.table_label.destroy()
        self.table_menu.destroy()
        self.check_button.destroy()
        self.tree.destroy()


def main():
    root = Tk()
    root.geometry("400x400")
    Main(root)
    root.mainloop()


if __name__ == '__main__':
    main()