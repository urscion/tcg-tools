from __future__ import annotations

import json
from pathlib import Path
from typing import Any, override

import requests

from ..models import Database
from .card import SwuCard

# SETS_FILE = Path(__file__).parent / "sets.json"

SET_CARDS_BASE_URL = "https://api.swu-db.com/cards"
"""Base URL for querying cards in a set."""

SET_QUERY_URL = "https://api.swu-db.com/cards/search?q=type:Base"
"""Query used to determine available sets."""

CACHE_DIRECTORY = Path.home() / ".cache" / "tcg-tools" / "swu-db"


class SwuDatabase(Database[SwuCard]):
    def __init__(self):
        super().__init__(SwuCard)

    @override
    def load(self) -> dict[str, Any]:
        data: dict[str, Any] = {}

        self.build_cache()

        for set_cache_file in CACHE_DIRECTORY.glob("*.json"):
            set_code = set_cache_file.stem.upper()
            data[set_code] = json.loads(set_cache_file.read_text())

        return data

    def online_set_codes(self) -> set[str]:
        """Get the set codes from online database."""
        response = requests.get(SET_QUERY_URL)
        response.raise_for_status()
        data = response.json()
        set_codes: set[str] = set()
        for card in data["data"]:
            if "Set" in card:
                set_code = card["Set"].upper()
                if set_code not in set_codes:
                    print(f"Found set code {set_code} from online database.")
                    set_codes.add(set_code)

        return set_codes

    def build_cache(self) -> None:
        """Build the cache from the online database."""

        CACHE_DIRECTORY.mkdir(parents=True, exist_ok=True)

        for set_code in self.online_set_codes():
            set_cache_file = CACHE_DIRECTORY / f"{set_code}.json"
            if set_cache_file.exists():
                continue

            # Create the cache
            print(f"Building cache for set {set_code}...")
            response = requests.get(f"{SET_CARDS_BASE_URL}/{set_code}")
            response.raise_for_status()
            set_cache_file.write_text(response.text)
