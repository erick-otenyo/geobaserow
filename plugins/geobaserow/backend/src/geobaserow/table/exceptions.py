class UnsupportedGeoType(Exception):
    """
    Raised when the provided GeoJSON geometry type is not supported.
    """


class InvalidGeoJSONFeature(Exception):
    """
    Raised when the provided GeoJSON feature is invalid.
    """
