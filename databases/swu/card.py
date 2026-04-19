from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto
from typing import Any, Literal, Sequence, override

from ..models import Card as CardBase


class Aspect(Enum):
    VIGILANCE = auto()
    COMMAND = auto()
    AGGRESSION = auto()
    CUNNING = auto()
    HEROISM = auto()
    VILLAINY = auto()

    @property
    def short_name(self) -> str:
        if self == Aspect.VIGILANCE:
            return "B"
        elif self == Aspect.COMMAND:
            return "G"
        elif self == Aspect.AGGRESSION:
            return "R"
        elif self == Aspect.CUNNING:
            return "Y"
        elif self == Aspect.HEROISM:
            return "W"
        elif self == Aspect.VILLAINY:
            return "K"
        else:
            raise NotImplementedError(
                f"{self.name} does not have an aspect color implemented!"
            )

    @staticmethod
    def short(aspects: Sequence[Aspect]) -> str:
        if not aspects:
            return "N"
        return "/".join([a.short_name for a in aspects])


ASPECT_COMBOS = (
    (Aspect.VIGILANCE, Aspect.VILLAINY),
    (Aspect.VIGILANCE, Aspect.HEROISM),
    (Aspect.VIGILANCE, Aspect.VIGILANCE),
    (Aspect.VIGILANCE,),
    (Aspect.COMMAND, Aspect.VILLAINY),
    (Aspect.COMMAND, Aspect.HEROISM),
    (Aspect.COMMAND, Aspect.COMMAND),
    (Aspect.COMMAND,),
    (Aspect.AGGRESSION, Aspect.VILLAINY),
    (Aspect.AGGRESSION, Aspect.HEROISM),
    (Aspect.AGGRESSION, Aspect.AGGRESSION),
    (Aspect.AGGRESSION,),
    (Aspect.CUNNING, Aspect.VILLAINY),
    (Aspect.CUNNING, Aspect.HEROISM),
    (Aspect.CUNNING, Aspect.CUNNING),
    (Aspect.CUNNING,),
    (Aspect.VILLAINY,),
    (Aspect.HEROISM,),
    (),
)


"""
Example card data
{
    "Set": "JTL",
    "Number": "012",
    "Name": "Luke Skywalker",
    "Subtitle": "Hero of Yavin",
    "Type": "Leader",
    "Aspects": [
        "Aggression",
        "Heroism"
    ],
    "Traits": [
        "FORCE",
        "REBEL",
        "PILOT"
    ],
    "Arenas": [
        "Ground"
    ],
    "Cost": "6",
    "Power": "5",
    "HP": "6",
    "FrontText": "Action [Exhaust]: If you attacked with a Fighter unit this phase, deal 1 damage to a unit.",
    "EpicAction": "Epic Action: If you control 6 or more resources, choose one:\nDeploy this leader.\nDeploy this leader as an upgrade on a friendly Vehicle unit without a Pilot on it.",
    "DoubleSided": true,
    "BackArt": "https://cdn.swu-db.com/images/cards/JTL/012-b.png",
    "BackText": "This upgrade can't be defeated by enemy card abilities.\nAttached unit is a leader unit. If it's a Fighter, it gains: \"On Attack: You may deal 3 damage to a unit.\"",
    "Rarity": "Common",
    "Unique": true,
    "Artist": "Renaud Scheidt",
    "VariantType": "Normal",
    "MarketPrice": "0.09",
    "FoilPrice": "",
    "FrontArt": "https://cdn.swu-db.com/images/cards/JTL/012.png",
    "LowPrice": "0.04"
}
"""


@dataclass
class SwuCard(CardBase):
    aspects: list[Aspect]
    """Aspects."""

    type: str
    """Type (e.g. Leader, Unit, Upgrade, Action)."""

    variant: Literal["Normal", "Hyperspace", "Showcase"]
    """Variant."""

    subtitle: str = ""
    """Subtitle."""

    @classmethod
    @override
    def from_dict(cls, d: dict[str, Any]) -> SwuCard:
        if "Aspects" in d:
            aspects = [Aspect[a.upper()] for a in d["Aspects"]]
        else:
            aspects = []

        return cls(
            set_code=d["Set"],
            number=d["Number"],
            name=d["Name"],
            aspects=aspects,
            type=d["Type"],
            variant=d["VariantType"],
            rarity=d["Rarity"],
            subtitle=d.get("Subtitle", ""),
        )

    @property
    def full_name(self) -> str:
        if self.subtitle:
            return f"{self.name} - {self.subtitle}"
        return self.name

    @property
    def uid(self) -> str:
        return f"{self.set_code}_{self.number}"

    @property
    def aspect(self) -> str:
        """The combined aspects of the card.

        If no aspects, returns "NEUTRAL".
        """
        if not self.aspects:
            return "NEUTRAL"
        return "+".join([a.name for a in self.aspects])

    @property
    def rarity_code(self) -> str:
        """Code for the rarity.

        The first letter of the rarity
        """
        return self.rarity[0]

    @property
    def aspect_short(self) -> str:
        return Aspect.short(self.aspects)

    def __str__(self) -> str:
        return f"{self.name} ({self.set_code}) {self.number}"
