from ariadne import convert_kwargs_to_snake_case, ObjectType, QueryType

from ..utils import calculate_distance
from .models import Hotel

Query = QueryType()

@Query.field("hotels")
@convert_kwargs_to_snake_case
def resolve_hotels(
    obj, 
    info, 
    bldg_class = None, 
    borocode = None, 
    borough = None, 
    nta = None, 
    owner_name = None, 
    postcode = None, 
    tax_class = None, 
    tax_year = None):
    
    query = Hotel.query
    
    if bldg_class:
        query = query.filter(Hotel.bldg_class.in_(bldg_class))
    if borocode:
        query = query.filter(Hotel.borocode.in_(borocode))
    if borough:
        query = query.filter(Hotel.borough.in_(borough))
    if nta:
        query = query.filter(Hotel.nta.in_(nta))
    if owner_name:
        query = query.filter(Hotel.owner_name.in_(owner_name))
    if postcode:
        query = query.filter(Hotel.postcode.in_(postcode))
    if tax_class:
        query = query.filter(Hotel.tax_class.in_(tax_class))
    if tax_year:
        query = query.filter(Hotel.tax_year.in_(tax_year))

    return [hotel.to_dict() for hotel in query.all()] 


@Query.field("hotel")
@convert_kwargs_to_snake_case
def resolve_hotel(obj, info, owner_name):
    hotels = Hotel.query.filter_by(owner_name = owner_name).first()
    return [hotels.to_dict()]


@Query.field("hotelsByCouncilDistrict")
def resolve_hotels_by_council_district(obj, info, council_district = None):
    query = Hotel.query.filter(Hotel.council_district.in_(council_district))
    return [hotel.to_dict() for hotel in query.all()]


@Query.field("hotelsByParID")
def resolve_hotels_by_parid(obj, info, parid):
    hotels = Hotel.query.filter_by(parid = parid).first()
    return [hotels.to_dict()]


@Query.field("hotelsNearLocation")
@convert_kwargs_to_snake_case
def resolve_hotels_near_location(obj, info, latitude, longitude, radius):
    hotels = Hotel.query.all()
    nearby_hotels = []
    
    for hotel in hotels:
        hotel_lat = float(hotel.latitude)
        hotel_lon = float(hotel.longitude)
        distance = calculate_distance(latitude, longitude, hotel_lat, hotel_lon)
        
        if distance <= radius:
            nearby_hotels.append(hotel.to_dict())
    
    return nearby_hotels


query = ObjectType("Query")
query.set_field("hotel", resolve_hotel)
query.set_field("hotels", resolve_hotels)
query.set_field("hotelsByCouncilDistrict", resolve_hotels_by_council_district)
query.set_field("hotelsByParID", resolve_hotels_by_parid)
query.set_field("hotelsNearLocation", resolve_hotels_near_location)