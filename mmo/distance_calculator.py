from math import sqrt, radians, atan, sin, cos

EARTH_RADIUS_KM = 6371


def calculate_distance(height_m, degrees_below_horizon):
    """
    References:
    http://www.afsc.noaa.gov/nmml/software/downloads/geofunc.txt
    http://www.afsc.noaa.gov/nmml/software/excelgeo.php
    :return: Distance in km
    """
    height_km = height_m / 1000.0
    distance_to_horizon_km = sqrt(2 * EARTH_RADIUS_KM * height_km + height_km ** 2)
    if degrees_below_horizon < 0:
        return None
    if degrees_below_horizon == 0.0:
        return distance_to_horizon_km
    radians_below_horizon = radians(degrees_below_horizon)
    angle = atan(distance_to_horizon_km / EARTH_RADIUS_KM)
    distance = ((EARTH_RADIUS_KM + height_km) * sin(angle + radians_below_horizon) -
                sqrt(EARTH_RADIUS_KM ** 2 - ((EARTH_RADIUS_KM + height_km) * cos(angle + radians_below_horizon)) ** 2))
    return distance