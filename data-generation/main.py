import os
import openai

from prompt_generator import PromptGenerator


# OPENAI_KEY = "" # INSERT OPENAI KEY HERE


# openai.api_key = OPENAI_KEY
# openai.Model.list()


if __name__=="__main__":
    gen = PromptGenerator(["testloc1", "testloc2"], ["a", "b", "c", "d", "e", "f", "g"],  ["testorg3", "testorg4"], 3)
    for _ in range(10):
        gen.sample()
        print(gen.build_prompt())
