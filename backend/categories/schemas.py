import pydantic


class CategoryBase(pydantic.BaseModel):
    name: str


class CategoryCreate(CategoryBase):
    user: int


class CategoryEnhanced(CategoryCreate):
    category_id: int


class CategoryBind(pydantic.BaseModel):
    category_id: int
    wish: int


class WishId(pydantic.BaseModel):
    wish: int
