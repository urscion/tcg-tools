import csv
import io
import itertools
import tempfile
from pathlib import Path

import scrython
from flask import render_template, request, send_file

from tools.mtg.card_names import mtg_card_names_bp


def save_to_csv() -> Path:
    cards = set(scrython.catalogs.CardNames().data)
    cards = sorted(cards)

    file_path = Path(tempfile.gettempdir()) / "mtg_card_names.csv"

    with open(file_path, "w", newline="\n") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(
            itertools.zip_longest(
                cards,
                [
                    "",
                ],
            )
        )

    return file_path


@mtg_card_names_bp.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        return send_file(
            io.BytesIO(save_to_csv().read_bytes()),
            mimetype="text/csv",
            as_attachment=True,
            download_name="mtg_card_names.csv",
        )
    return render_template("mtg/card-names/index.html")
