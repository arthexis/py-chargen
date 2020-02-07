import sys
import logging
from random import Random
from collections import defaultdict

import names
from nested_lookup import (
    nested_lookup, nested_update, nested_delete
)

from . import data
from .traits import Trait

logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
logger = logging.getLogger('generators')


__all__ = [
    "Generator",
    "CoDGen",
    "Requiem2Gen",
    "Awakening2Gen",
]


def make_pool(traits, *keys):
    """Add the dots for all the specified keys in traits."""

    pool = 0
    for key in keys:
        values = nested_lookup(document=traits, key=key)
        assert len(values) == 1
        pool += values[0]
    return pool


class Generator(Random):
    """Skeleton generator for all character types."""

    RULES = "base"

    def __init__(self, seed=None):
        super().__init__(seed)
        logger.debug(f"Initialize RNG with {seed=}")
        self._seed = seed

    @classmethod
    def from_rules(cls, rules, seed=None):
        """Return an instance of a Generator for the specified rules."""

        for subclass in cls.__subclasses__():
            if subclass.RULES == rules:
                logger.debug(f"Using {subclass=}")
                return subclass(seed)
            if generator := subclass.from_rules(rules, seed):
                return generator

    def flip(self):
        return bool(self.getrandbits(1))

    def chance(self, percent):
        assert 0 > percent < 100
        return self.randint(1, 100) <= percent

    def spread(self, size, dots, base=0, limit=5):
        """Randomly distribute dots to a tuple of specified size."""
        if limit:
            assert size * limit >= dots
        dist = [Trait(base, limit)] * size
        while dots > 0:
            n = self.randint(0, size - 1)
            if limit and dist[n] >= limit:
                continue
            dist[n] += 1
            dots -= 1
        return dist

    def shuffled(self, *seq):
        """Return a shuffled sequence (no change to the original)."""
        return self.sample(seq, len(seq))

    def spend(self, keys, dots, groups=1, base=0, limit=None):
        """Randomly spend dots over a fixed list of key traits."""
        assert groups > 0 and len(keys) % groups == 0
        size = len(keys) // groups
        iterkeys = iter(keys)
        traits = {}
        for total in self.shuffled(*dots):
            for dots in self.spread(size, dots=total, base=base, limit=limit):
                traits[next(iterkeys)] = dots
        return traits

    def choice_under(self, seq, n):
        """Randomly choose an item for seq that is less than n."""

        if min(seq) > n:
            raise ValueError("Impossible choice")
        while True:
            if (q := self.choice(seq)) <= n:
                return q

    def roll(self, dice, again=(10,)):
        """Roll the specified number of d10s."""

        successes = 0
        repeat = 0
        for die in range(dice):
            if (result := self.randint(1, 10)) >= 8:
                successes += 1
                repeat += 1 if result in again else 0
        if repeat:
            successes += self.roll(repeat)
        return successes

    def generate(self, **traits):
        """Generate a skeleton that can be used by subclasses."""
        return {
            "metadata": {
                "rules": self.RULES,
                "seed": self._seed,
            },
            "names": [names.get_full_name()],
            "traits": {**traits},
            "hooks": []
        }


class CoDGen(Generator):
    """Generates a complete, valid CoD character."""

    RULES = "cod"

    def generate(self, **traits):
        logger.debug("Create CoD character traits.")

        # Assign base attributes nd sills
        traits["Attributes"] = attrs = self.spend(
            data.ATTRIBUTES, dots=(5, 4, 3), groups=3, base=1, limit=4)
        traits["Skills"] = skills = self.spend(
            data.SKILLS, dots=(11, 7, 4), groups=3, base=0, limit=4)

        # Choose professional training (1 dot)
        profession = self.choice(data.PROFESSIONS)
        traits["Asset Skills"] = assets = self.sample(data.PROF_SKILLS[profession], 2)

        # Add 1 dot to asset skills
        for asset in assets:
            skills[asset] += self.choice((0, 1, 2, 2))

        # Add 1 dot to preferred profession attribute
        attrs[self.choice(data.PROF_ATTRIBUTES[profession])] += 1

        # Update the profession Merit based on specific profession
        profession = f"Profession ({profession})"
        traits["Merits"] = merits = {profession: 1}

        # You get 2 dots of contacts with professional training
        for contact in self.sample(data.CONTACTS, 2):
            merits[f"Contacts ({contact})"] = 1

        # Personality traits
        traits["Anchors"] = anchors = {
            "Virtue": self.choice(data.VIRTUES),
            "Vice": self.choice(data.VICES)
        }

        # Assign mundane Merits
        merit_dots = 7
        while merit_dots > 0:
            try:
                merit = self.choice(data.MERITS)
                opts = data.MERIT_DOTS[merit]
                dots = max([
                    self.choice_under(opts, merit_dots),
                    self.choice_under(opts, merit_dots)
                ])
            except ValueError:
                continue
            merits[merit] = dots
            merit_dots -= dots

        # Initial integrity
        integrity = Trait(7)
        pool = make_pool(traits, "Resolve", "Composure")
        while integrity > 1 and not self.roll(pool):
            integrity -= 1
        traits["Integrity"] = integrity

        # Calculate advantages
        traits["Advantages"] = {
            "Willpower": min(attrs["Resolve"] + attrs["Composure"], 10)
        }
        return super().generate(**traits)


class Requiem2Gen(CoDGen):
    """Generates a complete, valid "Vampire, the Requiem 2nd Ed" character."""

    RULES = "vtr2"

    def generate(self, blood_potency=1, **traits):
        output = super().generate(**traits)
        traits = output["traits"]

        logger.debug("Create Vampire, the Requiem 2ed character traits.")
        traits["Advantages"]["Blood Potency"] = Trait(blood_potency, 10)

        # Choose a clan and initial disciplines
        traits["Clan"] = clan = self.choice(data.CLANS)
        traits["Disciplines"] = disciplines = defaultdict(Trait)
        for i in range(3):
            discipline = self.choice(data.CLAN_DISCIPLINES[clan])
            disciplines[discipline] += 1

        return output


class Awakening2Gen(CoDGen):
    """Generates a complete, valid "Mage, the Awakening 2nd Edition" character."""

    RULES = "mtaw2"

    def generate(self, gnosis=1, **traits):
        output = super().generate(**traits)

        logger.debug("Create Mage 2ed character traits.")
        traits = output["traits"]
        traits["Advantages"]["Gnosis"] = Trait(gnosis, 10)
        resistance = self.choice(data.RESISTANCES)
        traits["Attributes"][resistance] += 1
        traits["Skills"]["Occult"] += 1

        # Choose a path and find the related arcana
        traits["Path"] = path = self.choice(data.PATHS)
        reagents = self.sample(data.PATH_REAGENTS[path], 2)
        inferior = data.PATH_INFERIOR[path]

        # Assign arcana dots
        traits["Arcana"] = arcana = {x: 0 for x in data.ARCANA}
        arcana[reagents[0]] = Trait(2)
        arcana[reagents[1]] = Trait(1)
        arcana_dots = 3
        while arcana_dots > 0:
            arcanum = self.choice(data.ARCANA)
            if traits["Arcana"][arcanum] >= 3 or arcanum == inferior:
                continue
            traits["Arcana"][arcanum] +=1
            arcana_dots -= 1

        # Assign Mage merits
        merits = traits["Merits"]
        lost_merit = self.choice(merits.keys())
        nested_delete(traits, lost_merit, in_place=True)
        merits["High Speech"] = Trait(1)

        # Set initial wisdom
        nested_delete(traits, "Integrity", in_place=True)
        wisdom = 7
        traits["Wisdom"] = wisdom

        return output
