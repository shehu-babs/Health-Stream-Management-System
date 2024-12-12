class Config():
    domain = 'groupsix.edu'
    smtp_username=""
    smtp_password=""
    db_host = '000.000.00.00'
    user='root'
    password='mypass'
    database ='BIS698W_29'


    @classmethod
    def get_domain(cls):
        return cls.domain
