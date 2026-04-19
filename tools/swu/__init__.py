from flask import Blueprint

from .picklist import swu_picklist_bp

swu_bp = Blueprint(
    "swu",
    __name__,
    template_folder="templates",
)

swu_bp.register_blueprint(swu_picklist_bp)
