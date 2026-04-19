#!/usr/bin/env python3

# Copyright 2025, Peter Clay (pwclay@gmail.com), All Rights Reserved

"""SWU Tools

TODO:
- Add sort by button (quantity, name, set, rarity, aspect, type)
  - with asc/dsc
- toggle to include sideboard
  - toggle to include column if Deck or Sideboard or Maybeboard (only show if sideboard is enabled)
- toggle to include subtitle column
"""

import json
from dataclasses import dataclass

from flask import Flask, render_template, request

from databases.swu.card import SwuCard
from databases.swu.database import SwuDatabase as SwuDb
from parsers import DeckParser, SWUDBApiParser, SWUDBJsonParser

app = Flask(__name__)

swudb = SwuDb()


@dataclass
class DisplayOptions:
    use_quantity_wide_checkboxes: bool = False
    """If set, the number of spaces in the checkbox is the quantity."""

    use_header: bool = False
    """Include a header"""


def to_picklist(parser: DeckParser, options: DisplayOptions) -> str:
    deck = parser.deck()

    max_card_count_in_deck = 0

    # Populate the card name, if missing
    for card in deck.cards:
        if not card.full_name:
            card.full_name = swudb.card(card.set_code, card.number).full_name
        max_card_count_in_deck = max(max_card_count_in_deck, card.count)

    deck_card_names = set([card.full_name.lower() for card in deck.cards])
    deck_card_count = {card.full_name.lower(): card.count for card in deck.cards}

    card_buffer_size = 0
    # Set the card name buffer size
    for set_code in swudb.sets():
        for set_card in swudb.cards(set_code=set_code):
            if (
                set_card.full_name.lower() in deck_card_names
                and set_card.variant == "Normal"
            ):
                card_buffer_size = max(card_buffer_size, len(str(set_card.name)))

    header_printed = False  # Laziness to keep output all together
    output = ""
    cards_added: set[str] = set()
    # Sort by set first, then by aspect
    for set_code in swudb.sets():
        deck_cards_in_set: list[SwuCard] = []

        # Add card if in deck and is Normal
        for set_card in swudb.cards(set_code=set_code):
            if (
                set_card.full_name.lower() in deck_card_names
                and set_card.variant == "Normal"
            ):
                deck_cards_in_set.append(set_card)

        # If no deck cards in this set, skip it
        if not deck_cards_in_set:
            print(f"No cards found for set {set_code}.")
            continue

        # Order by number
        for card in sorted(deck_cards_in_set, key=lambda x: int(x.number)):
            # Always print this card's set code first
            other_sets_for_card = set(
                [
                    c.set_code
                    for c in swudb.cards(full_name=card.full_name)
                    if c.set_code != card.set_code
                ]
            )
            all_sets_for_card_str = ",".join(other_sets_for_card)

            # Create checkbox
            if card.name not in cards_added:
                spaces_for_quantity = (
                    " " * deck_card_count[card.full_name.lower()]
                    if options.use_quantity_wide_checkboxes
                    else " "
                )
                card_checkbox = f"[{spaces_for_quantity}]"
            else:
                card_checkbox = "   "
            card_checkbox_spacing = (
                max_card_count_in_deck + 2
                if options.use_quantity_wide_checkboxes
                else 3
            )

            # Output
            if options.use_header and not header_printed:
                output += (
                    f"{'CHK':<{card_checkbox_spacing}s} {'QNTY':>4s} {'CARD NAME':<{card_buffer_size}s}"
                    f" | SET"
                    f" | NMBR"
                    f" | R"
                    f" | {'OTHER SETS':11s}"
                    f" | {'ASPECT':6s}"
                    f" | {'TYPE':7s}\n"
                )
                header_printed = True

            output += (
                f"{card_checkbox:<{card_checkbox_spacing}s} {deck_card_count[card.full_name.lower()]:>3d}x {str(card.name):<{card_buffer_size}s}"
                f" | {card.set_code}"
                f" | #{card.number}"
                f" | {card.rarity_code}"
                f" | {all_sets_for_card_str:11s}"
                f" | {card.aspect_short:6s}"
                f" | {card.type:7s}\n"
            )
            cards_added.add(card.name)

    return output


@app.route("/", methods=["GET", "POST"])
def index():
    converted_text = ""
    if request.method == "POST":
        input_swudb_json = request.form["input_swudb_json"]
        input_swudb_url = request.form["input_swudb_url"]

        # Create display options
        display_options = DisplayOptions()
        display_options.use_quantity_wide_checkboxes = bool(
            request.form.get("toggle_quantity_wide_checkboxes")
        )
        display_options.use_header = bool(request.form.get("toggle_header"))

        # Create correct type of parser
        try:
            if input_swudb_json:
                parser = SWUDBJsonParser(json.loads(input_swudb_json))
            elif input_swudb_url:
                parser = SWUDBApiParser.from_url(input_swudb_url)
            else:
                # Do nothing
                return render_template("index.html")
        except Exception:
            return render_template("index.html")

        converted_text = to_picklist(parser, display_options)
    return render_template("index.html", converted_text=converted_text)


# app.run() not needed as on PythonAnywhere as it's handled by their server.
