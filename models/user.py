from sqlalchemy import Column, INTEGER, String, DateTime, text, LargeBinary

from utils import database


class User(database.Model):
    __tablename__ = 'users'

    id = Column(INTEGER(), primary_key=True)
    login = Column(String(255, 'utf8mb4_unicode_ci'), nullable=False, unique=True)
    password = Column(LargeBinary, nullable=False)
    token = Column(String(255, 'utf8mb4_unicode_ci'), nullable=False)
    token_expired_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    created_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
