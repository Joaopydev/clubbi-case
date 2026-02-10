from pydantic import BaseModel


class ProductSchema(BaseModel):
    id: int
    ean: str
    name: str
    items_per_box: int

    class Config:
        from_attributes = True