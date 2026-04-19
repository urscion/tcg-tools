from dataclasses import dataclass

from ..models import Deck as DeckBase
from ..models import DeckCard


@dataclass
class SwuDeck(DeckBase):
    leaders: list[DeckCard]
    """Leaders for the deck."""
