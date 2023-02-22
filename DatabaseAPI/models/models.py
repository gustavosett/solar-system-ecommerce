from sqlalchemy import Column, Integer, String, ForeignKey, Float, Boolean, DateTime, Numeric, Date
from sqlalchemy.orm import relationship, backref
from database import Base
from datetime import datetime


class Role(Base):
    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True)
    role_name = Column(String(15))
    permissions = Column(Integer)

    users = relationship("User", back_populates="role")

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    role_id = Column(Integer, ForeignKey('roles.id'), nullable=False, index=True)
    cpf = Column(String(14))
    first_name = Column(String(50))
    last_name = Column(String(50))
    phone = Column(String(20))
    email = Column(String(100))
    password = Column(String(128))
    birth_date = Column(Date)
    created_at = Column(DateTime, default=datetime.now)
    status = Column(String(20), default="Active")
    last_email_modification = Column(DateTime, nullable=True)
    last_password_modification = Column(DateTime, nullable=True)
    last_activity = Column(DateTime, default=datetime.now)

    addresses = relationship('Address', backref=backref('user', uselist=False))
    role = relationship("Role", back_populates="users")

class Address(Base):
    __tablename__ = 'addresses'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    street = Column(String(100))
    number = Column(String(10))
    complement = Column(String(50))
    city = Column(String(50))
    state = Column(String(50))
    zip_code = Column(String(10))
    is_primary = Column(Boolean)

class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    value = Column(Numeric(precision=10, scale=2))
    name = Column(String(100))
    description1 = Column(String(500))
    photos = Column(String(500))
    description2 = Column(String(1000))
    tags = relationship('ProductTagAssociation', backref='product')
    in_promotion = Column(Boolean, default=False)
    promotion_value = Column(Numeric(precision=10, scale=2))
    final_value = Column(Numeric(precision=10, scale=2))
    related_products = relationship('Product', secondary='product_related_association',
                                     primaryjoin='Product.id==ProductRelatedAssociation.product_id',
                                     secondaryjoin='Product.id==ProductRelatedAssociation.related_product_id')

class Tag(Base):
    __tablename__ = 'tags'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))

class ProductTagAssociation(Base):
    __tablename__ = 'product_tag_association'
    product_id = Column(Integer, ForeignKey('products.id'), primary_key=True)
    tag_id = Column(Integer, ForeignKey('tags.id'), primary_key=True)

class ProductRelatedAssociation(Base):
    __tablename__ = 'product_related_association'
    product_id = Column(Integer, ForeignKey('products.id'), primary_key=True)
    related_product_id = Column(Integer, ForeignKey('products.id'), primary_key=True)

class Cart(Base):
    __tablename__ = 'carts'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    cart_items = relationship('CartItem', backref='cart')
    coupons = relationship('Coupon', backref='cart')
    shipping_value = Column(Float)
    subtotal_value = Column(Float)
    total_value = Column(Float)

class CartItem(Base):
    __tablename__ = 'cart_items'
    id = Column(Integer, primary_key=True)
    cart_id = Column(Integer, ForeignKey('carts.id'))
    product_id = Column(Integer, ForeignKey('products.id'))
    quantity = Column(Integer)

class Coupon(Base):
    __tablename__ = 'coupons'
    id = Column(Integer, primary_key=True)
    code = Column(String(50))
    discount_value = Column(Float)
    cart_id = Column(Integer, ForeignKey('carts.id'))

class Wishlist(Base):
    __tablename__ = 'wishlists'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    wishlist_items = relationship('WishlistItem', backref='wishlist')

class WishlistItem(Base):
    __tablename__ = 'wishlist_items'
    id = Column(Integer, primary_key=True)
    wishlist_id = Column(Integer, ForeignKey('wishlists.id'))
    product_id = Column(Integer, ForeignKey('products.id'))

class Checkout(Base):
    __tablename__ = 'checkouts'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    first_name = Column(String(50))
    last_name = Column(String(50))
    company_name = Column(String(100))
    email = Column(String(100))
    phone = Column(String(20))
    street = Column(String(100))
    number = Column(String(10))
    complement = Column(String(50))
    city = Column(String(50))
    state = Column(String(50))
    zip_code = Column(String(10))
    is_primary = Column(Boolean)