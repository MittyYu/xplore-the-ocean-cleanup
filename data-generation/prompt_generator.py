from datetime import date, timedelta
from dataclasses import dataclass, field
import numpy as np


@dataclass
class PromptGenerator:

    loc_list: tuple
    item_list: tuple
    org_list: tuple
    type_list: tuple = ('press release', 'instagram caption')
    loc_probs: list = None
    item_probs: list = None
    org_probs: list = None
    type_probs: list = None
    max_items: int = 0
    split_prob: float = 0.5
    weight_range: tuple = (0, 10000)
    rounding_range: tuple = (-2, 2)
    unit_list: tuple = ('kgs', 'lbs', 'kilograms', 'pounds')
    date_range: list = (date(2015, 1, 1), date.today())

    def __post_init__(
        self,
    ):
        self.loc, self.org, self.items, self.weight, self.unit, self.date = [None] * 6
        self.loc_probs = np.ones(len(self.loc_list)) / len(self.loc_list) if self.loc_probs is None else self.loc_probs
        self.item_probs = np.ones(len(self.item_list)) / len(self.item_list) if self.item_probs is None else self.item_probs
        self.org_probs = np.ones(len(self.org_list)) / len(self.org_list) if self.org_probs is None else self.org_probs
        self.type_probs = np.ones(len(self.type_list)) / len(self.type_list) if self.type_probs is None else self.type_probs


    def sample_items(self):
        self.weight = self.sample_weight()
        self.unit = np.random.choice(self.unit_list, replace=False)

        n = np.random.randint(self.max_items+1)
        if n == 0:
            return '%s %s of trash' % (self.weight, self.unit)
        items = list(np.random.choice(self.item_list, n, replace=False, p=self.item_probs))

        if n == 1:
            item = items[0]
        elif n == 2:
            if np.random.rand() < self.split_prob:
                self.weight = tuple(self.sample_weight() for _ in range(n))
            else:
                item = " and ".join(items)
        else:
            items[-1] = ("and " + items[-1])
            item = ", ".join(items)

        if type(self.weight) == int:
            return "%s %s of %s" % (self.weight, self.unit, item)
        else:
            return "%s %s of %s and %s %s of %s" % (self.weight[0], self.unit, items[0],
                    self.weight[1], self.unit, items[1])



    def sample_weight(self):
        precision = np.random.randint(*self.rounding_range)
        return int(round(np.random.rand() * (self.weight_range[1] - self.weight_range[0]) + self.weight_range[0], precision))


    def sample(self):
        self.loc = np.random.choice(self.loc_list, replace=False, p=self.loc_probs)
        self.org = np.random.choice(self.org_list, replace=False, p=self.org_probs)
        self.type = np.random.choice(self.type_list, replace=False, p=self.type_probs)
        self.items = self.sample_items()
        self.date = self.date_range[0] + timedelta(days=np.random.randint(
                    (self.date_range[1] - self.date_range[0]).days
                )
            )


    def build_prompt(self):
        prompt = "Generate a%s %s for a beach cleanup where %s was cleaned.\nOrganization: %s\nDate: %s\nLocation: %s" % (
                'n' if self.type[0] in 'aeiou' else '',
                self.type,
                self.items,
                self.org,
                self.date,
                self.loc,
            )
        return prompt
