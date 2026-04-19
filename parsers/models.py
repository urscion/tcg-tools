from abc import ABC, abstractmethod
from dataclasses import dataclass

"""Abstract interfaces for Deck Parsers."""


@dataclass
class DeckCard:
    """Represent a card as listed in a deck.

    Name or set+number MUST be set.
    """

    count: int

    full_name: str = ""
    """Full name/title of the card. Includes subtitles."""

    set_code: str = ""
    """Set code."""

    number: str = ""
    """Card number (within set)."""

    def __post_init__(self):
        if not self.full_name and (not self.set_code and not self.number):
            raise Exception("Deck Card Name or Set+Number MUST be set!")


@dataclass
class Deck:
    cards: list[DeckCard]
    """Cards in the main deck."""

    sideboard: list[DeckCard]
    """Sideboard cards for the deck."""


class DeckParser(ABC):
    @abstractmethod
    def deck(self) -> Deck:
        pass
