class user:
    def __init__ (self, id_user, login, id_role, block, failed_pass):
        self.id_user=id_user
        self.login=login
        self.id_role=id_role
        self.block=block
        self.failed_pass=failed_pass