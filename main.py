from tkinter import *
from PIL import Image, ImageTk
import pymysql.cursors


class Main(Frame):

    def connect(self):
        self.connection = pymysql.connect(host='localhost',
                                     user='root',
                                     password='dionis0799',
                                     db='qwe',
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)

        print("connect successful!!")

    def operation(self, sql):
        print(sql)
        self.connection.cursor().execute(sql)

    def createDB(self, sql):
        print(sql)
        self.connection.cursor().execute("call createDB('{sql}')")

    # init
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.connect()
        self.parent = parent
        self.color = "black"
        self.bg = "white"
        self.fgr_bg = "white"
        self.brush_size = 5
        self.init_main()

    def init_main(self):
        self.master.title("Hostel")
        self.pack(fill=BOTH, expand=1)
        self.set_main()

    def init_option(self):
        self.master.title("Hostel")
        self.pack(fill=BOTH, expand=1)
        name = self.variable.get()
        self.set_option(name)

    def init_search(self):
        self.master.title("Search")
        self.pack(fill=BOTH, expand=1)
        name = self.variable.get()
        self.set_search(name)

    # use
    def use_bd(self):
        self.delete_main()
        self.init_option()

    def use_search(self):
        self.delete_option()
        self.init_search()

    # set
    def set_option(self, name):
        self.columnconfigure(2, weight=1)
        self.rowconfigure(5, weight=1)
        self.name_label = Label(self, text=name, font="Arial 48", justify=CENTER)
        self.name_label.grid(row=0, column=0, columnspan=2)
        self.delete_button = Button(self, width=16, height=2, font="12",
                               background="white", text="вывод")
        self.delete_button.grid(row=1, column=1, padx=5, pady=10)
        self.output_button = Button(self, width=16, height=2, font="12",
                               background="white", text="удалить")
        self.output_button.grid(row=2, column=1, padx=5, pady=10)
        self.search_button = Button(self, width=16, height=2, font="12",
                               background="white", text="поиск", command=self.use_search)
        self.search_button.grid(row=3, column=1, padx=5, pady=10)
        self.update_button = Button(self, width=16, height=2, font="12",
                               background="white", text="обновить")
        self.update_button.grid(row=4, column=1, padx=5, pady=10)
        size = (40, 40)
        self.img1 = ImageTk.PhotoImage(Image.open("output.png").resize(size))
        self.output_logo = Label(self, justify=CENTER, image=self.img1)
        self.output_logo.grid(row=1, column=0, padx=70)
        self.img2 = ImageTk.PhotoImage(Image.open("delete.png").resize(size))
        self.delete_logo = Label(self, justify=CENTER, image=self.img2)
        self.delete_logo.grid(row=2, column=0, padx=70)
        self.img3 = ImageTk.PhotoImage(Image.open("search.png").resize(size))
        self.search_logo = Label(self, justify=CENTER, image=self.img3)
        self.search_logo.grid(row=3, column=0, padx=70)
        self.img4 = ImageTk.PhotoImage(Image.open("update.png").resize(size))
        self.update_logo = Label(self, justify=CENTER, image=self.img4)
        self.update_logo.grid(row=4, column=0, padx=70)

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
                                    background="white", text="Удалить")
        self.delete_button.grid(row=2, column=1, padx=5, pady=10)
        self.new_button = Button(self, width=16, height=2, font="12",
                            background="white", text="Создать", command=self.createDB(self.name_db.get()))
        self.new_button.grid(row=2, column=0, padx=5, pady=10)
        self.variable = StringVar(self)
        self.variable.set("выберете")
        self.bd_menu = OptionMenu(self, self.variable, "First BD", "Second BD")
        self.bd_menu.grid(row=3, column=0, padx=5, pady=10)
        self.use_button = Button(self, width=16, height=2, font="12", background="white",
                            text="Использовать", command=self.use_bd)
        self.use_button.grid(row=3, column=1, padx=5, pady=10)

    def set_search(self, name):
        self.columnconfigure(2, weight=1)
        self.rowconfigure(5, weight=1)
        self.name_label = Label(self, text="Search in " + name, font="Arial 24", justify=CENTER)
        self.name_label.grid(row=0, column=0, columnspan=2)
        self.table_label = Label(self, text="Таблица", font="Arial 14", justify=CENTER)
        self.table_label.grid(row=1, column=0)
        self.column_label = Label(self, text="Столбец", font="Arial 14", justify=CENTER)
        self.column_label.grid(row=2, column=0)
        self.search_label = Label(self, text="Что искать?", font="Arial 14", justify=CENTER)
        self.search_label.grid(row=3, column=0)
        self.variable1 = StringVar(self)
        self.variable1.set("выберете")
        self.variable2 = StringVar(self)
        self.variable2.set("выберете")
        self.table_menu = OptionMenu(self, self.variable1, "first table", "second table")
        self.table_menu.grid(row=1, column=1, padx=10, pady=10)
        self.column_menu = OptionMenu(self, self.variable2, "first column", "second column")
        self.column_menu.grid(row=2, column=1, padx=10, pady=10)
        self.message = StringVar()
        self.text_entry = Entry(self, textvariable=self.message)
        self.text_entry.grid(row=3, column=1, padx=10, pady=10)
        self.search_button = Button(self, width=12, height=2, font="12",
                                 background="white", text="Поиск")
        self.search_button.grid(row=4, column=1, padx=10, pady=10)

    # delete
    def delete_main(self):
        self.bg_label.destroy()
        self.new_button.destroy()
        self.delete_button.destroy()
        self.bd_menu.destroy()
        self.use_button.destroy()

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

    def delete_search(self):
        self.name_label.destroy()
        self.table_label.destroy()
        self.column_label.destroy()
        self.search_label.destroy()
        self.table_menu.destroy()
        self.column_menu.destroy()
        self.text_entry.destroy()
        self.search_button.destroy()


def main():
    root = Tk()
    root.geometry("400x400")
    Main(root)
    root.mainloop()


if __name__ == '__main__':
    main()