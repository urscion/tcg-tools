from flask import Blueprint

swu_picklist_bp = Blueprint(
    "picklist",
    __name__,
    url_prefix="/picklist",
    template_folder="templates",
)

# Import tool routes so they register onto this blueprint
from . import routes  # noqa
