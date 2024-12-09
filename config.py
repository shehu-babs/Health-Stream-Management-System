class Config():
    domain = 'groupsix.edu'
    smtp_username=""
    smtp_password=""
    db_host = '141.209.241.57'
    user='shehu1i'
    password='mypass'
    database ='BIS698W_29'


    @classmethod
    def get_domain(cls):
        return cls.domain