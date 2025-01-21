import pydantic


class CategoryBase(pydantic.BaseModel):
    name: str


class CategoryCreate(CategoryBase):
    user: int


class CategoryBind(pydantic.BaseModel):
    category_id: int
    wish: int
