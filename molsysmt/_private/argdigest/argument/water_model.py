from molsysmt._private.smonitor import ArgumentError

from ._attribute_query import digest_query_flag


def digest_water_model(water_model, caller=None):

    if caller == "molsysmt.build.solvate.solvate" and isinstance(water_model, str):
        key = (
            water_model.upper()
            .replace("-", "")
            .replace("/", "")
            .replace("_", "")
            .replace(" ", "")
        )
        aliases = {
            "SPCE": "SPC/E",
            "TIP4PEW": "TIP4P-EW",
            "TIP3PFB": "TIP3P-FB",
            "TIP4PFB": "TIP4P-FB",
        }
        if key in aliases:
            return aliases[key]

    if caller == "molsysmt.basic.get.get":
        return digest_query_flag("water_model", water_model, caller=caller)

    if isinstance(water_model, str):
        from molsysmt.attribute import attributes

        values = attributes["water_model"]["values"]
        for value in values:
            if water_model.lower() == value.lower():
                return value
    elif water_model is None:
        return None

    raise ArgumentError("water_model", value=water_model, caller=caller, message=None)
