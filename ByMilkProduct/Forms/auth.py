import tkinter
from DataAccess.db import db
from tkinter import messagebox
from Forms.captcha import captcha


class auth(tkinter.Tk):
    def __init__ (self):
        super().__init__()
        self.db=db()
        self.title("Вход")
        self.geometry("400x400")
        self.minsize(400,400)
        self.failed_pass = 0
        self.setup()

    def setup(self):
        lb_log = tkinter.Label(self, text = "Логин")
        lb_log.pack(pady=( 20,5))

        self.entry_login=tkinter.Entry(self, font = ("Areal", 12))
        self.entry_login.pack()

        lb_password = tkinter.Label(self, text = "Пароль")
        lb_password.pack(pady=(15, 5))

        self.entry_password = tkinter.Entry(self, font = ("Areal", 12), show="*")
        self.entry_password.pack()

        bt_login = tkinter.Button(self, text ="Войти", command = self.login_click)
        bt_login.pack(pady = (20))

        self.captcha_widget = None

    def login_click(self):
        login=self.entry_login.get().strip()
        password=self.entry_password.get().strip()

        if not login or not password:
            messagebox.showwarning("Внимание", "Поля Логин и Пароль не могут быть пустыми")
            return

        user_name, bd_password = self.db.get_user_by_login(login)

        if user_name is None:
            messagebox.showwarning("Внимание", "Неверно введен логи или пароль")
            return

        if user_name.block:
            messagebox.showwarning("Внимание", "Ваша учетная запись заблокирована, обратитесь к администратору")
            return

        if password == bd_password:
            self.show_captcha(login, user_name)


        else:
            self.handle_fail(login)
            messagebox.showwarning("Внимание", "Неверно введен пароль")

    def show_captcha(self, login, user_name):
        if self.captcha_widget is None:
            self.captcha_widget = captcha(self)
            self.captcha_widget.pack(pady=10)
        btn_check = tkinter.Button(self, text="Проверить",command=lambda: self.check_captcha(login, user_name))
        btn_check.pack()

    def check_captcha(self, login, user_name):
        if self.captcha_widget.current == self.captcha_widget.correct:
            messagebox.showinfo("Успех", "Вы успешно авторизовались!")
            self.reset_attempts(login)
            self.destroy()
            if user_name.id_role == 3:
                from Forms.admin_desk import admin_desk
                admin_window = admin_desk()
                admin_window.mainloop()
            else:
                user_win = tkinter.Tk()
                user_win.title("Рабочий стол пользователя")
                user_win.geometry("400x400")
                user_win.minsize(400,400)
                tkinter.Label(user_win, text ="Добро пожаловать в систему").pack(expand = True)
                user_win.mainloop()

        else:
            self.handle_fail(login)

    def reset_attempts(self, login):
        conn = self.db.connection()
        cursor = conn.cursor()

        cursor.execute("update users set failed_pass = 0 where login = %s", (login,))
        conn.commit()

    def handle_fail(self, login):
        self.failed_pass+=1
        user, _ = self.db.get_user_by_login(login)
        new_filed = user.failed_pass+1

        conn = self.db.connection()
        cursor = conn.cursor()

        if new_filed >=3:
            cursor.execute("update users set block = true, failed_pass = %s where login = %s", (new_filed, login))
            conn.commit()
            messagebox.showwarning("Блокировка", "Вы заблокированы. Обратитесь к администратору")
            return
        else:
            cursor.execute("update users set failed_pass = %s WHERE login = %s",(new_filed, login))
            conn.commit()
            messagebox.showwarning("Неверно", "Повторите попытку")


