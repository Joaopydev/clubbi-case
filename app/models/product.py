from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String

from app.db.base import Base

class Product(Base):

    __tablename__ = "products"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    ean: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    items_per_box: Mapped[int] = mapped_column(Integer, nullable=False)