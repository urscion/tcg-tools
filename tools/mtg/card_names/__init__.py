from flask import Blueprint

mtg_card_names_bp = Blueprint(
    "card-names",
    __name__,
    url_prefix="/card-names",
    template_folder="templates",
)

# Import tool routes so they register onto this blueprint
from . import routes  # noqa
