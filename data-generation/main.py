import glob
import os
import openai
import pandas as pd

from prompt_generator import PromptGenerator


def get_openai_key(fname="./.OPENAI_KEY"):
    with open(fname, "r") as f:
        key = f.readline().strip()
    return key


def read_locations(loc_folder="./data/locations"):
    dfs = []

    for f in glob.glob("%s/*.xml" % loc_folder):
        dfs += [pd.read_xml(f)]
    df = pd.concat(dfs)

    return list(df.toponymName.unique())


def read_orgs(org_file="./data/orgs/orgs.txt"):
    with open(org_file, 'r') as f:
        orgs = [l.strip() for l in f]

    return orgs


def read_materials(mat_file="./data/materials/materials.txt"):
    with open(mat_file, 'r') as f:
        mats = [l.strip() for l in f]
    return mats


def save_data(df, outfile):
    df.to_pickle(outfile)


def generate_data(generator, n, outfile=None, call_api=False, save_every=100, write_csv=True):
    data = []
    if outfile is None:
        outfile = 'data/generated/data_{}.pkl'.format(pd.datetime.today().strftime('%y%m%d-%H%M%S'))

    for i in range(n):
        gen.sample()
        row = gen.get_data()
        row['prompt'] = gen.build_prompt()

        if call_api:
            row['text'] = openai.Completion.create(
                engine="text-davinci-003",
                prompt=row['prompt'],
                max_tokens=256,
                temperature=0.7
            )['choices'][0]['text']
        else:
            row['text'] = "Text not generated"

        data += [row]
        if i % save_every == 0:
            pd.DataFrame(data).to_pickle(outfile)

    df = pd.DataFrame(data)
    df.to_pickle(outfile)
    if write_csv:
        df.to_csv(outfile[:-4]+".csv", index=False)


if __name__=="__main__":
    OPENAI_KEY = get_openai_key()

    openai.api_key = OPENAI_KEY
    locations = read_locations()
    orgs = read_orgs()
    mats = read_materials()

    gen = PromptGenerator(
            loc_list = locations,
            item_list = mats,
            org_list = orgs,
            max_items=3,
        )

    generate_data(gen, 1, call_api=True)
