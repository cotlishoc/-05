import psycopg2
from Models.user import user
class db:
    def __init__(self):
        self.db_param = {
            "dbname":"production",
            "user":"postgres",
            "password":"88888888",
            "host":"localhost",
            "port":"5432"
        }

    def connection(self):
        return psycopg2.connect(**self.db_param)

    def get_user_by_login(self,login):
        try:
            conn=self.connection()
            cursor=conn.cursor()

            cursor.execute(
                """select id_user, login, id_role, block, failed_pass, password_hach FROM users WhERE login = %s""", (login,)
            )

            row=cursor.fetchone()

            if row:
                user_n = user(
                    id_user = row[0],
                    login = row[1],
                    id_role = row[2],
                    block = row[3],
                    failed_pass=row[4]
                )
                password_hach = row[5]

                cursor.close()
                conn.close()
                return user_n, password_hach

            else:
                cursor.close()
                conn.close()
                return None, None

        except Exception as e:
            print(e)
            return None, None

    def get_all_users(self):
        conn=self.connection()
        cursor=conn.cursor()
        cursor.execute("""select id_user, login, id_role, block, password_hach from users order by id_user""")
        rows = cursor.fetchall()

        cursor.close()
        conn.close()

        return rows

    def get_role(self):
        conn=self.connection()
        cursor = conn.cursor()
        cursor.execute("""select id_role, role_name from roles""")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return rows

    def check_user_exist(self, login):
        conn = self.connection()
        cursor = conn.cursor()
        cursor.execute("""select count(*) from users where login = %s""", (login,))
        count = cursor.fetchone()[0]
        return count > 0

    def add_user(self, id_user, login, password, id_role):
        conn = self.connection()
        cursor = conn.cursor()
        cursor.execute("""insert into users(id_user, login, password_hach, id_role) values(%s, %s, %s, %s)""",(id_user, login, password, id_role))
        conn.commit()
        cursor.close()
        conn.close()

    def update_user(self, id_user, login, password, id_role, block):
        conn = self.connection()
        cursor = conn.cursor()

        if not block:
            cursor.execute("""update users set block =%s, login=%s, password_hach = %s, id_role = %s, failed_pass = 0 where id_user =%s """, (block, login, password, id_role, id_user))
        else:
            cursor.execute("""update users set login=%s, password_hach=%s, id_role=%s, block = %s where id_user =%s """, (login, password, id_role, block, id_user))
        conn.commit()
        cursor.close()
        conn.close()

