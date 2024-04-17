# schema.py

from graphene import relay, ObjectType, Schema
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from .models import Hotels as HotelModel
# from .models import Owners as OwnerModel
# from .models import Borough as BoroughModel
# from .models import Location as LocationModel
# from .models import Building as BuildingModel
# from .models import TaxInfo as TaxInfoModel
# from .models import CensusInfo as CensusInfoModel


class Hotel(SQLAlchemyObjectType):
    class Meta:
        model = HotelModel
        interfaces = (relay.Node, )


# class Owners(SQLAlchemyObjectType):
#     class Meta:
#         model = OwnerModel
#         interfaces = (relay.Node, )


# class Borough(SQLAlchemyObjectType):
#     class Meta:
#         model = BoroughModel
#         interfaces = (relay.Node, )


# class Location(SQLAlchemyObjectType):
#     class Meta:
#         model = LocationModel
#         interfaces = (relay.Node, )


# class Building(SQLAlchemyObjectType):
#     class Meta:
#         model = BuildingModel
#         interfaces = (relay.Node, )


# class TaxInfo(SQLAlchemyObjectType):
#     class Meta:
#         model = TaxInfoModel
#         interfaces = (relay.Node, )


# class CensusInfo(SQLAlchemyObjectType):
#     class Meta:
#         model = CensusInfoModel
#         interfaces = (relay.Node, )


class Query(ObjectType):
    node = relay.Node.Field()
    all_hotels = SQLAlchemyConnectionField(Hotel.connection, sort=Hotel.sort_argument())
    # all_owners = SQLAlchemyConnectionField(Owners.connection, sort=Owners.sort_argument())
    # all_boroughs = SQLAlchemyConnectionField(Borough.connection, sort=Borough.sort_argument())
    # all_locations = SQLAlchemyConnectionField(Location.connection)
    # all_buildings = SQLAlchemyConnectionField(Building.connection)
    # all_tax_info = SQLAlchemyConnectionField(TaxInfo.connection)
    # all_census_info = SQLAlchemyConnectionField(CensusInfo.connection)



schema = Schema(query=Query)