from tkinter import messagebox, ttk
import tkinter
from DataAccess.db import db

class user_edit(tkinter.Toplevel):
    def __init__(self, parent, user_data=None):
        super().__init__(parent)
        self.db=db()
        self.parent = parent
        self.user_data=user_data

        self.title("Редактирование пользователя")
        self.geometry("350x400")
        self.minsize(300,350)
        self.grab_set()
        self.setup_edit()
        self.fill_data()

    def setup_edit(self):
        tkinter.Label(self, text = "ID: ").pack(pady=(10, 0))
        self.ID_entry = tkinter.Entry(self, font = ("Areal", 12))
        self.ID_entry.pack(padx=20, fill=tkinter.X)

        tkinter.Label(self, text ="Логин: ").pack(pady = (10, 0))
        self.login_entry = tkinter.Entry(self, font = ("Areal", 12))
        self.login_entry.pack(padx = 20, fill = tkinter.X)

        tkinter.Label(self, text = "Пароль: ").pack(pady=(10, 0))
        self.password_entry = tkinter.Entry(self, font = ("Areal", 12))
        self.password_entry.pack(padx=20, fill = tkinter.X)

        tkinter.Label(self, text = "Роли: ").pack(pady=(10, 0))
        self.roles_db = self.db.get_role()
        role_name = [role[1] for role in self.roles_db]
        self.roles_combobox = ttk.Combobox(self, values=role_name, state="readonly", font = ("Areal", 12))
        self.roles_combobox.pack(padx=20, fill=tkinter.X)

        self.var_block = tkinter.IntVar(self)
        self.check_block = tkinter.Checkbutton(self, text = "Заблокирован", variable = self.var_block)
        self.check_block.pack(pady = 10)

        button_save = tkinter.Button(self, text = "СОхранить", command = self.save_click)
        button_save.pack(pady = 20)

    def fill_data(self):
        if self.user_data:
            self.login_entry.insert(0,self.user_data[1])
            self.password_entry.insert(0,self.user_data[4])
            self.roles_combobox.set(self.user_data[2])
            role_id = int(self.user_data[2])
            for role in self.roles_db:
                if role[0] == role_id:
                    self.roles_combobox.set(role[1])
                    break

            block_value = str(self.user_data[3]).strip().lower()
            if block_value in ['true', '1']:
                self.var_block.set(1)
            else:
                self.var_block.set(0)


    def save_click (self):
        user_id = self.ID_entry.get().strip()
        login = self.login_entry.get().strip()
        password = self.password_entry.get().strip()
        block = bool(self.var_block.get())
        if not login or not password:
            messagebox.showwarning("Ошибка", "Введите все данные")
            return
        select_role_name = self.roles_combobox.get()
        id_role = 4
        for role in self.roles_db:
            if role[1] == select_role_name:
                id_role = role[0]
                break
        if self.user_data is None:
            if self.db.check_user_exist(login):
                messagebox.showwarning("Внимание", "Пользователь с таким логином уже существует")
                return
            self.db.add_user(user_id, login, password, id_role)
            messagebox.showinfo("Успех", "Пользователь добавлен")
        else:
            user_id = self.user_data[0]
            self.db.update_user(user_id, login, password, id_role, block)
            messagebox.showinfo("Успех", "Пользователь обновлен.")

        self.parent.load_users()
        self.destroy()




