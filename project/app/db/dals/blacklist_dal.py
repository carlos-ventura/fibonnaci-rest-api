from sqlalchemy.orm import Session

class BlacklistDAL():
    def __init__(self, db_session: Session):
        self.db_session = db_session
