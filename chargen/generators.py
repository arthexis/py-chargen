import logging
from random import Random

import names
from nested_lookup import nested_lookup, nested_update

from . import data

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


__all__ = [
    "Generator",
    "CoDGen",
    "Awakening2Gen",
]


def add_dots(traits, key, dots=1, limit=5):
    """Add dots to a trait without going over a limit."""

    current = nested_lookup(document=traits, key=key)
    assert len(current) == 1, f"{current}"
    if value := current[0] + dots <= limit:
        nested_update(document=traits, key=key, value=value)
        return True
    return False


class Generator(Random):
    """Skeleton generator for all character types."""

    RULES = "base"

    def __init__(self, seed=None):
        super().__init__(seed)
        self._seed = seed

    @classmethod
    def from_rules(cls, rules, seed=None):
        """Return an instance of a Generator for the specified rules."""

        for subclass in cls.__subclasses__():
            logger.debug(subclass)
            if subclass.RULES == rules:
                return subclass(seed)
            generator = subclass.from_rules(rules, seed)
            if generator:
                return generator

    def flip(self):
        return bool(self.getrandbits(1))

    def chance(self, percent):
        assert 0 > percent < 100
        return self.randint(1, 100) <= percent

    def spread(self, size, dots, base=0, limit=5, step=1):
        """Randomly distribute dots to a tuple of specified size."""
        if limit:
            assert size * limit >= dots
        dist = [base] * size
        while dots > 0:
            n = self.randint(0, size - 1)
            if limit and dist[n] >= limit:
                continue
            dist[n] += step
            dots -= step
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
        if min(seq) > n:
            raise ValueError("Impossible choice")
        while True:
            if (q := self.choice(seq)) <= n:
                return q

    def generate(self, **traits):
        """Generate a skelleton that can be used by subclasses."""
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
        traits["Merits"] = merits = {f"Profession ({profession})": 1}

        # Add 1 dot to prefered profession attribute
        attrs[self.choice(data.PROF_ATTRIBUTES[profession])] += 1

        # Add 1 dot to asset skills
        for asset in assets:
            skills[asset] += 1

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

        # Calculate advantages
        traits["Advantages"] = {
            "Willpower": min(attrs["Resolve"] + attrs["Composure"], 10)
        }
        return super().generate(**traits)



class Awakening2Gen(CoDGen):
    """Generates a complete, valid "Mage, the Awakening 2nd Edition" character."""

    RULES = "mtaw2"

    def generate(self, gnosis=1, **traits):
        output = super().generate(**traits)

        logger.debug("Create Mage 2ed character traits.")
        traits = output["traits"]
        traits["Advantages"]["Gnosis"] = gnosis
        resistance = self.choice(data.RESISTANCES)
        add_dots(traits, resistance, 1, 5)

        # Choose a path and find the related arcana
        traits["Path"] = path = self.choice(data.PATHS)
        reagents = self.sample(data.PATH_REAGENTS[path], 2)
        inferior = data.PATH_INFERIOR[path]

        # Assign arcana dots
        traits["Arcana"] = arcana = {x: 0 for x in data.ARCANA}
        arcana[reagents[0]] = 2
        arcana[reagents[1]] = 1
        arcana_dots = 3
        while arcana_dots > 0:
            arcanum = self.choice(data.ARCANA)
            if traits["Arcana"][arcanum] >= 3 or arcanum == inferior:
                continue
            traits["Arcana"][arcanum] +=1
            arcana_dots -= 1

        return output
