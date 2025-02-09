""" The Product model
"""

from sqlalchemy import (
    Column,
    String,
    Text,
    Numeric,
    ForeignKey,
    Integer,
    Enum as SQLAlchemyEnum,
    Boolean,
)
from api.v1.models.base_model import BaseTableModel
from sqlalchemy.orm import relationship
from enum import Enum


class ProductStatusEnum(Enum):
    in_stock = "in_stock"
    out_of_stock = "out_of_stock"
    low_on_stock = "low_on_stock"

class ProductFilterStatusEnum(Enum):
    published = "published"
    draft = "draft"

class Product(BaseTableModel):
    __tablename__ = "products"

    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    price = Column(Numeric, nullable=False)
    org_id = Column(
        String, ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False
    )
    category_id = Column(
        String, ForeignKey("product_categories.id", ondelete="CASCADE"), nullable=False
    )
    quantity = Column(Integer, default=0)
    image_url = Column(String, nullable=False)
    status = Column(
        SQLAlchemyEnum(ProductStatusEnum), default=ProductStatusEnum.in_stock
    )
    archived = Column(Boolean, default=False)
    filter_status = Column(
        SQLAlchemyEnum(ProductFilterStatusEnum), default=ProductFilterStatusEnum.published)

    variants = relationship(
        "ProductVariant", back_populates="product", cascade="all, delete-orphan"
    )
    organization = relationship("Organization", back_populates="products")
    category = relationship("ProductCategory", back_populates="products")

    def __str__(self):
        return self.name


class ProductVariant(BaseTableModel):
    __tablename__ = "product_variants"

    size = Column(String, nullable=False)
    stock = Column(Integer, default=1)
    price = Column(Numeric)
    product_id = Column(String, ForeignKey("products.id", ondelete="CASCADE"))
    product = relationship("Product", back_populates="variants")


class ProductCategory(BaseTableModel):
    __tablename__ = "product_categories"

    name = Column(String, nullable=False, unique=True)
    products = relationship("Product", back_populates="category")

    def __str__(self):
        return self.name
