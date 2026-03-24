from tkinter import messagebox, ttk
import tkinter
from DataAccess.db import db
from Forms.user_edit import user_edit

class admin_desk(tkinter.Tk):
    def __init__ (self):
        super().__init__()
        self.db=db()
        self.title("Молочный комбинат. Стол администратора")
        self.geometry("800x400")
        self.minsize(600,400)
        self.setup_desk()
        self.load_users()
    def setup_desk(self):
        tabel_frame = tkinter.Frame(self)
        tabel_frame.pack(fill=tkinter.BOTH, expand=True, padx=10, pady=5)
        columns = ("id", "login", "role", "block")
        self.tree=ttk.Treeview(tabel_frame, columns=columns, show="headings")

        self.tree.heading("id", text="ID")
        self.tree.heading("login", text="Логин")
        self.tree.heading("role", text="ID Роль")
        self.tree.heading("block", text = "Заблокирован")

        self.tree.pack(fill=tkinter.BOTH, expand=True)
        button_frame = tkinter.Frame(self)
        button_frame.pack(fill=tkinter.X, padx= 10, pady = 5)
        button_add = tkinter.Button(button_frame, text = "Добавить пользователя", command = self.add_user)
        button_add.pack(side=tkinter.LEFT, padx=10)
        button_edit = tkinter.Button(button_frame, text="Изменить данные", command = self.edit_user)
        button_edit.pack(side=tkinter.LEFT, padx=10)
        button_refrash = tkinter.Button(button_frame, text="Обновить", command = self.load_users)
        button_refrash.pack(side=tkinter.RIGHT, padx=10)

    def load_users(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        user_data = self.db.get_all_users()
        for user in user_data:
            id_user = user[0]
            login = user[1]
            role = user[2]
            block = user[3]
            password = user[4]
            self.tree.insert("", tkinter.END, values=(id_user, login, role, block, password))

    def add_user(self):
        windiw=user_edit(self, user_data=None)

    def edit_user(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Внимание", "Выберите пользователя в таблице")
            return
        item = self.tree.item(selected_item[0])
        user_data = item["values"]
        wimdow = user_edit(self, user_data=user_data)




