from datetime import datetime
from sqlalchemy import BigInteger, LargeBinary, DateTime, Integer
from sqlalchemy.orm import Mapped, mapped_column

from database import db

class Print(db.Model):
    __tablename__ = "prints"
    id: Mapped[int] = mapped_column(BigInteger,primary_key=True)
    raster_data: Mapped[bytes] = mapped_column(LargeBinary,nullable=False)
    image_width: Mapped[int] = mapped_column(Integer,nullable=False)
    image_height: Mapped[int] = mapped_column(Integer,nullable=False)
    printed_at: Mapped[datetime] = mapped_column(DateTime,nullable=True)