from flask import Blueprint

from .card_names import mtg_card_names_bp

mtg_bp = Blueprint(
    "mtg",
    __name__,
    template_folder="templates",
)

mtg_bp.register_blueprint(mtg_card_names_bp)
