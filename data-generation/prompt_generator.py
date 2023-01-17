from datetime import date, timedelta
import numpy as np


class PromptGenerator:
    def __init__(
        self,
        loc_list,
        item_list,
        org_list,
        max_items=0, # TODO: make stochastic
        weight_range=(0, 10000),
        unit_list=['kgs', 'lbs'],
        date_range=(date(2015, 1, 1), date.today()),
    ):
        # TODO: add randomness: press release v insta 
        self.loc_list = loc_list
        self.org_list = org_list

        # setting 0 max_items labels everything as trash
        if max_items:
            self.max_items = max_items
            self.item_list = item_list
        else:
            self.max_items = 1
            self.item_list = ['trash']

        self.weight_range = weight_range
        self.unit_list = unit_list
        self.date_range = date_range

        self.loc, self.org, self.items, self.weight, self.unit, self.date = [None] * 6


    def sample_items(self):
        items = list(np.random.choice(self.item_list, self.max_items, replace=False))
        if self.max_items == 1:
            return items
        elif self.max_items == 2:
            return " and ".join(items)
        else:
            items[-1] = ("and " + items[-1])
            return ", ".join(items)


    def sample(self):
        self.loc = np.random.choice(self.loc_list, replace=False)
        self.org = np.random.choice(self.org_list, replace=False)
        self.items = self.sample_items()
        self.weight = np.random.rand() * (self.weight_range[1] - self.weight_range[0]) + \
            self.weight_range[0]
        self.unit = np.random.choice(self.unit_list, replace=False)
        self.date = self.date_range[0] + timedelta(days=np.random.randint(
                    (self.date_range[1] - self.date_range[0]).days
                )
            )

    def build_prompt(self):
        prompt = "Generate a press release for %s about a cleanup on %s at %s where %s %s of %s was cleaned" % (
                self.org,
                self.date,
                self.loc,
                self.weight,
                self.unit,
                self.items
            )
        return prompt
