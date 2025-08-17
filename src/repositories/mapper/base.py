from pydantic import BaseModel


class BaseMapper:
    db_model = None
    schema: BaseModel = None

    @classmethod
    def map_to_schemas_object(cls, data):
        return cls.schema.model_validate(data, from_attributes=True)

    @classmethod
    def map_to_alchemy_object(cls, data: BaseModel):
        return cls.db_model(**data.model_dump())
