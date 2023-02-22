from typing import Optional, List
from pydantic import BaseModel
from datetime import date, datetime


class RoleBase(BaseModel):
    role_name: str
    permissions: int


class Role(RoleBase):
    id: int
    class Config:
        orm_mode = True



class UserBase(BaseModel):
    role_id: int
    cpf: str
    first_name: str
    last_name: str
    phone: str
    email: str
    birth_date: date
    password: str
    created_at: datetime = datetime.now()


class UserCreate(UserBase):
    confirm_password: str


class User(UserBase):
    id: int
    status: str
    last_email_modification: Optional[datetime]
    last_password_modification: Optional[datetime]
    last_activity: datetime = datetime.now()
    addresses: List['Address'] = []

    class Config:
        orm_mode = True


class AddressBase(BaseModel):
    street: str
    number: str
    complement: Optional[str]
    city: str
    state: str
    zip_code: str
    is_primary: bool


class AddressCreate(AddressBase):
    pass


class Address(AddressBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True


class ProductBase(BaseModel):
    value: float
    name: str
    description1: Optional[str]
    photos: Optional[str]
    description2: Optional[str]
    in_promotion: Optional[bool] = False
    promotion_value: Optional[float]
    final_value: Optional[float]


class ProductCreate(ProductBase):
    tags: Optional[List[int]] = []


class Product(ProductBase):
    id: int
    tags: List['Tag'] = []
    related_products: List['Product'] = []

    class Config:
        orm_mode = True


class TagBase(BaseModel):
    name: str


class TagCreate(TagBase):
    pass


class Tag(TagBase):
    id: int

    class Config:
        orm_mode = True


class CartBase(BaseModel):
    user_id: int
    shipping_value: Optional[float] = 0.0
    subtotal_value: Optional[float] = 0.0
    total_value: Optional[float] = 0.0


class CartCreate(CartBase):
    pass


class Cart(CartBase):
    id: int
    cart_items: List['CartItem'] = []
    coupons: List['Coupon'] = []

    class Config:
        orm_mode = True


class CartItemBase(BaseModel):
    cart_id: int
    product_id: int
    quantity: int


class CartItemCreate(CartItemBase):
    pass


class CartItem(CartItemBase):
    id: int

    class Config:
        orm_mode = True


class CouponBase(BaseModel):
    code: str
    discount_value: float
    cart_id: int


class CouponCreate(CouponBase):
    pass


class Coupon(CouponBase):
    id: int

    class Config:
        orm_mode = True


class WishlistBase(BaseModel):
    user_id: int


class WishlistCreate(WishlistBase):
    pass


class Wishlist(WishlistBase):
    id: int
    wishlist_items: List['WishlistItem'] = []

    class Config:
        orm_mode = True


class WishlistItemBase(BaseModel):
    wishlist_id: int
    product_id: int


class WishlistItemCreate(WishlistItemBase):
    pass


class WishlistItem(WishlistItemBase):
    id: int

    class Config:
        orm_mode = True


class CheckoutBase(BaseModel):
    user_id: int
    first_name: str
    last_name: str
    company_name: Optional[str]
    email: str
    phone: str
    street: str
    number: str
    complement: Optional[str]
    city: str
    state: str
    cep_code: str
    is_primary: bool


class CheckoutCreate(CheckoutBase):
    pass


class Checkout(CheckoutBase):
    id: int

    class Config:
        orm_mode = True

