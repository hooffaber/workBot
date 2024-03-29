from geopy import Nominatim

USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0"


def get_location(lat, long):
    geolocator = Nominatim(user_agent=USER_AGENT)
    location = geolocator.reverse(f'{lat}, {long}')

    return str(location)
