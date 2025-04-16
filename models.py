from pydantic import BaseModel

class DataModel(BaseModel):
    id: str
    title: str
    abstract: str
    domains: list
    keywords: list

class DataModel2(BaseModel):
    abstract: str

class AbstractModel(BaseModel):
    abstract: str
    title: str
    domain: list
    keywords: list
