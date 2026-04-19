from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Type


@dataclass(kw_only=True)
class Card(ABC):
    set_code: str
    """Set Code"""

    name: str
    """Name."""

    rarity: str
    """Rarity."""

    number: str = ""
    """Number in set. Many, but not all, TCGs implement this."""

    @classmethod
    @abstractmethod
    def from_dict(cls, d: dict[str, Any]) -> Card:
        """Create a card from a dict.

        Args:
            d: A dict representing the card. The keys and values depend on the implementation.
        """

    @property
    def full_name(self) -> str:
        """The full display name of the card."""
        return self.name

    @property
    def uid(self) -> str:
        """A unique ID for the card."""
        return f"{self.set_code}_{self.name}"

    @property
    def rarity_short(self) -> str:
        """Short rarity.

        Returns the first letter of the rarity.
        """
        return self.rarity[0].upper()

    def __str__(self) -> str:
        return f"{self.name} ({self.set_code}) {self.number}"


class Database[T: Card]:
    def __init__(self, card_type: Type[T]):
        self._sets: list[str] = []
        self._cards: dict[str, T] = {}

        data = self.load()
        for set_data in data:
            self._sets.append(set_data)
            for card_dict in data[set_data]["data"]:
                card = card_type.from_dict(card_dict)
                self._cards[card.uid] = card

    @abstractmethod
    def load(self) -> dict[str, Any]:
        """Load the database.

        Returns:
            Dict with the set codes as keys. Each set value should be a dict with "total_cards", and "data" (containing the card data).
        """

    def sets(self) -> list[str]:
        return self._sets

    def card(self, set_code: str, number: str) -> T:
        """Find a single card by set code and number.

        Args:
            set_code: Set code
            number: Card number within set
        Raises:
            KeyError: If no card is found with the given set code and number.
        Returns:
            The card with the given set code and number.
        """
        for card in self._cards.values():
            if card.set_code == set_code and card.number == number:
                return card
        raise KeyError(f"Card with set code {set_code} and number {number} not found!")

    def cards(self, full_name: str = "", set_code: str = "") -> list[T]:
        """Find cards.

        Args:
            full_name: Full name of cards (returns all versions)
            set_code: Set code
        """
        cards: list[T] = []
        for card in self._cards.values():
            if set_code and card.set_code != set_code:
                continue
            if full_name and card.full_name != full_name:
                continue
            cards.append(card)
        return cards
