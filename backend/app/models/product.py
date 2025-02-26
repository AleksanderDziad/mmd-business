from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
from app.models.user import User

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    price = Column(Float)
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="products")

User.products = relationship("Product", back_populates="owner")

