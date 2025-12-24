from datetime import datetime
from sqlalchemy import BigInteger, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from database import db

class Token(db.Model):
    __tablename__ = "tokens"
    id: Mapped[int] = mapped_column(BigInteger,primary_key=True)
    value: Mapped[str] = mapped_column(String(255),unique=True,nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime,nullable=False)
    
db.Index("unique_token_value", Token.value, unique=True)