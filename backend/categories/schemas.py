import pydantic


class CategoryBase(pydantic.BaseModel):
    name: str


class CategoryCreate(CategoryBase):
    user: int
