import os
import openai

from prompt_generator import PromptGenerator


# OPENAI_KEY = "" # INSERT OPENAI KEY HERE


# openai.api_key = OPENAI_KEY
# openai.Model.list()


if __name__=="__main__":
    gen = PromptGenerator(
            loc_list = ["testloc1", "testloc2"],
            item_list = ["a", "b", "c", "d", "e", "f", "g"],
            org_list = ["testorg3", "testorg4"],
            max_items=3,
        )
    for _ in range(10):
        gen.sample()
        print(gen.build_prompt())
