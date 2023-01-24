import json
import numpy as np
import pandas as pd

def clean_materials(fname="./data/materials/taco_annotations.json",
                    out="./data/materials/materials.txt"):
    '''Using annotations from https://github.com/pedropro/TACO to create a list of
    reasonable trash categories. TOC data too messy to use for now'''
    with open(fname) as f:
        data = json.load(f)

    df = pd.DataFrame(data['categories'])


    items = [i+'s' for i in np.concatenate((df.supercategory.unique(), df.name.unique()))
                    if i[-1]!='s']

    with open(out, 'w') as f:
        for i in items:
            f.write(i.replace("glooves", "gloves").lower()) # checking for a typo noticed
            f.write("\n")

if __name__=="__main__":
    clean_materials()
