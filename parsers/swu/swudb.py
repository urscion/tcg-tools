# Need to return Name and count.
# Optionally the set and card number

from __future__ import annotations

from typing import Any

import requests

from ..models import DeckCard, DeckParser
from .parser import SwuDeck

CARD_SET_KEY = "defaultExpansionAbbreviation"
CARD_NUMBER_KEY = "defaultCardNumber"


class SWUDBApiParser(DeckParser):
    """Parser for the deck API endpoint (json).

    e.g. https://swudb.com/api/deck/ABCD1234
    """

    def __init__(self, data: Any):
        self.data = data

    @classmethod
    def from_url(cls, url: str) -> DeckParser:
        deck_id = url.split("/")[-1]
        api_url = f"https://swudb.com/api/deck/{deck_id}"
        response = requests.get(api_url, timeout=(2, 5))
        response.raise_for_status()

        return cls(response.json())

    def deck(self) -> SwuDeck:
        cards: list[DeckCard] = []
        sideboard_cards: list[DeckCard] = []

        for deck_item in self.data["shuffledDeck"]:
            deck_item_card = deck_item["card"]
            deck_count = int(deck_item["count"])
            sideboard_count = int(deck_item["sideboardCount"])
            card_name = (
                f"{deck_item_card['cardName']} - {deck_item_card['title']}"
                if deck_item_card["title"]
                else deck_item_card["cardName"]
            )
            # Add to deck
            if deck_count > 0:
                deck_card = DeckCard(
                    full_name=card_name,
                    count=deck_count,
                )
                if CARD_SET_KEY in deck_item_card:
                    deck_card.set_code = deck_item_card[CARD_SET_KEY].upper()
                if CARD_NUMBER_KEY in deck_item_card:
                    deck_card.number = deck_item_card[CARD_NUMBER_KEY]
                cards.append(deck_card)
            # Add to sideboard
            if sideboard_count > 0:
                deck_card = DeckCard(
                    full_name=card_name,
                    count=sideboard_count,
                )
                if CARD_SET_KEY in deck_item_card:
                    deck_card.set_code = deck_item_card[CARD_SET_KEY].upper()
                if CARD_NUMBER_KEY in deck_item_card:
                    deck_card.number = deck_item_card[CARD_NUMBER_KEY]
                sideboard_cards.append(deck_card)

        return SwuDeck(leaders=[], cards=cards, sideboard=sideboard_cards)


class SWUDBJsonParser(DeckParser):
    """Parser for exported JSON data."""

    def __init__(self, data: dict[str, Any]):
        self.data = data

    def deck(self) -> SwuDeck:
        cards: list[DeckCard] = []
        sideboard_cards: list[DeckCard] = []

        def get_card(obj: Any) -> DeckCard:
            card_set_code, card_number = obj["id"].split("_")
            return DeckCard(
                count=int(
                    obj["count"],
                ),
                set_code=card_set_code.upper(),
                number=card_number,
            )

        for deck_card in self.data["deck"]:
            cards.append(get_card(deck_card))
        for deck_card in self.data["sideboard"]:
            sideboard_cards.append(get_card(deck_card))
        return SwuDeck(leaders=[], cards=cards, sideboard=[])
