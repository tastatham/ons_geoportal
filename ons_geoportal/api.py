from requests import get
import geopandas


def get_boundaries(
    geom_type="lsoa",
    layer_type="full clipped",
    cols="all",
    where="st_area(shape) > 282152900",
    crs=27700,
    precision=5,
):
    """
    Get boundaries from Office of National Statistics Open Geography Portal API
    These can be downloaded in bulk from https://geoportal.statistics.gov.uk/

    Parameters
    ----------
    geom_type : str
        geometry type
    layer_type: str
        how the boundary layers are returned
    cols: str or list (default: all)
        str or list of columns or attributes to include
    where : str
        sql like statement to filter geometries and attributes
    crs : int (default: British National Grid)
        epsg codes to transform and extract geometries
    precision: int
         number of digits past the decimal point are to be used

    Returns
    -------
    geopandas.GeoDataFrame
        GeoDataFrame containing attribute and geometry values
    """

    census_types = ["lsoa"]

    admin_types = ["lad"]

    epsg = [4326, 3857, 27700]

    if geom_type in census_types:
        boundary, geom, fields = _get_census_boundaries(geom_type)
    elif geom_type in admin_types:
        boundary, geom, fields = _get_admin_boundaries(geom_type)
    else:
        raise ValueError(f"Only the following census types: {census_types} \
            and administrative types: {admin_types} are supported")

    layer = _check_layer_types(layer_type)

    if crs not in epsg:
        raise ValueError(f"Only the following {epsg} codes are supported")

    if precision not in range(1, 8):
        raise ValueError(
                "Geometry precisions only accepts values between 1 and 8"
            )

    response = get(
        url=(
            "https://ons-inspire.esriuk.com/arcgis/rest/services/"
            f"{boundary}"
            f"{geom}"
            f"MapServer/{layer}/query"
        ),
        params=_format_params(cols, fields, where, crs, precision)
    )

    response.raise_for_status()

    return geopandas.GeoDataFrame.from_features(
        response.json()["features"],
        crs=crs
    )


def get_postcodes():
    """"""


def get_lookups():
    """"""


def get_products():
    """"""


def get_uprns():
    """"""


def _check_layer_types(layer_type):
    """Function checks boundary layer type"""

    layer_types = [
        "full clipped",
        "full extent",
        "generalised clipped",
        "super generalised clipped",
    ]

    if layer_type == layer_types[0]:
        layer = 0
    elif layer_type == layer_types[1]:
        layer = 1
    elif layer_type == layer_types[2]:
        layer = 2
    elif layer_type == layer_types[3]:
        layer = 3
    else:
        raise ValueError(f"Only layer types {layer_types} are supported")

    return layer


def _get_census_boundaries(geom_type):
    """Function returns boundary type,
    census boundary type and list of columns"""

    boundary = "Census_Boundaries/"

    geom_types = [
        "lsoa",
    ]

    fields = [
        "objectid",
        "lsoa11cd",
        "lsoa11nm",
        "shape",
        "st_area",
        "st_length",
    ]

    if geom_type == "lsoa":
        geom = "Lower_Super_Output_Areas_December_2011_Boundaries/"
    else:
        raise ValueError(f"Only {geom_types} are supported")

    return boundary, geom, fields


def _get_admin_boundaries(geom_type):
    """Function returns boundary type,
    admin boundary type and list of columns"""

    boundary = "Administrative_Boundaries/"

    geom_types = [
        "lad",
    ]

    fields = [
        "objectid",
        "lad18cd",
        "lad18nm",
        "shape",
        "st_area",
        "st_length",
    ]

    if geom_type == "lad":
        geom = "Local_Authority_Districts_December_2018_Boundaries_UK_BGC/"
    else:
        raise ValueError(f"Only {geom_types} are supported")

    return boundary, geom, fields


def _format_params(cols, fields, where, crs, precision):
    """
    Transform parameters into a query input for ESRIs feature service:
    The feature service allows users to query & edit feature geoms & attributes

    A breakdown of the ESRIs feature service:
        https://developers.arcgis.com/rest/services-reference/enterprise/feature-service.htm

    Parameters
    ----------
    cols: str or list (default: 'all')
        str list of columns or attributes to include
    fields: list
        list of fields supported by the boundary
    where : str
        sql like statement to filter geometries and attributes
    crs : int (default: British National Grid)
        epsg codes to transform and extract geometries
    precision: int
         number of digits past the decimal point are to be used

    Returns
    -------
    dict:
        dictionary containing query inputs for ESRIs feature service
    """

    if isinstance(cols, str):
        cols = cols.lower()
        if cols == "all":
            cols = "*"

    if isinstance(cols, list):
        cols = [col.lower() for col in cols]

        if all(elem in fields for elem in cols) is not True:
            raise ValueError(f"Only {fields} are supported for geometry type")
        cols = ", ".join(cols)

    return {
        "outFields": f"{cols}",
        "where": f"{where}",
        "outSR": crs,
        "f": "geojson",
        "geometryPrecision": f"{precision}",
    }

