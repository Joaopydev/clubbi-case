from pydantic import BaseModel


class CustomerSchema(BaseModel):
    id: int
    name: str
    cnpj: str
    address: str

    class Config:
        from_attribute = True