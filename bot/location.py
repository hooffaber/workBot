from geopy import Nominatim
from datetime import datetime, time
from timezonefinder import TimezoneFinder
import pytz

USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0"


def get_location(lat, long):
    geolocator = Nominatim(user_agent=USER_AGENT)
    location = geolocator.reverse(f'{lat}, {long}')

    return str(location)


async def get_current_time(lat, long):
    tf = TimezoneFinder()
    timezone_str = tf.timezone_at(lat=lat, lng=long)
    timezone = pytz.timezone(timezone_str)
    current_time = datetime.now(pytz.utc).astimezone(timezone)

    return current_time


async def get_times(lat, long):
    tf = TimezoneFinder()
    local_timezone_str = tf.timezone_at(lat=lat, lng=long)
    if local_timezone_str is None:
        raise RuntimeError("Timezone could not be found for the given coordinates.")

    local_timezone = pytz.timezone(local_timezone_str)

    moscow_timezone = pytz.timezone("Europe/Moscow")

    today_local = datetime.now(local_timezone).date()

    datetime_8_am_local = local_timezone.localize(datetime.combine(today_local, time(8, 0)))
    datetime_4_40_pm_local = local_timezone.localize(datetime.combine(today_local, time(16, 50)))

    datetime_8_am_moscow = datetime_8_am_local.astimezone(moscow_timezone)
    datetime_4_40_pm_moscow = datetime_4_40_pm_local.astimezone(moscow_timezone)

    return datetime_8_am_moscow, datetime_4_40_pm_moscow


