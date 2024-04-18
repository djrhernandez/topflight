# schema.py

import graphene
from graphene import relay, ObjectType, Schema
from graphene_sqlalchemy import SQLAlchemyConnectionField
from graphene_sqlalchemy import SQLAlchemyObjectType

from .models import Hotels as HotelModel
from .models import Owners as OwnerModel


class Hotels(SQLAlchemyObjectType):
    class Meta:
        model = HotelModel
        interfaces = (relay.Node, )


class HotelConnection(relay.Connection):
    class Meta:
        node = Hotels


class Owners(SQLAlchemyObjectType):
    class Meta:
        model = OwnerModel
        interfaces = (relay.Node, )


class OwnerConnection(relay.Connection):
    class Meta:
        node = Owners


class Query(ObjectType):
    node = relay.Node.Field()
    all_hotels = SQLAlchemyConnectionField(HotelConnection)    
    all_owners = SQLAlchemyConnectionField(OwnerConnection)

    hotels = graphene.List(Hotels)
    def resolve_hotels(self, info):
        query = Hotels.get_query(info)
        return query.all()
    
    owners = graphene.List(Owners)
    def resolve_owners(self, info):
        query = Owners.get_query(info)
        return query.all()


schema = Schema(query=Query, types=[Hotels, Owners])