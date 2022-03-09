#-*- coding: utf-8 -*-
"""
@author:MD.Nazmuddoha Ansary
"""
from __future__ import print_function
#---------------------------
# imports
#---------------------------
from datasets import load_dataset
import pandas as pd
from tqdm.auto import tqdm
import os
import argparse
from utils import *
from languages import languages
#---------------------------
# execution
#---------------------------
def main(args):
    # args
    data_dir=args.data_dir
    max_len =args.chunk_size
    
    for lang in languages.keys():
        LOG_INFO(f"Downloading:{lang}")
        dataset = load_dataset("oscar", f"unshuffled_deduplicated_{lang}")
        dir=create_dir(data_dir,lang)
        LOG_INFO(f"Creating Chunks:{lang}")
        for _,idx in enumerate(tqdm(range(0,dataset["train"].num_rows,max_len))):
            df=pd.DataFrame({})
            df["text"]=dataset["train"]["text"][idx:idx+max_len]
            df.to_csv(os.path.join(dir,f"{idx}.csv"),index=False)

if __name__=="__main__":
    '''
        parsing and execution
    '''
    parser = argparse.ArgumentParser("Oscar Data Download script")
    parser.add_argument("data_dir", help="Path to save the oscar data as csv")
    parser.add_argument("--chunk_size",required=False,default=50000,help ="number of data to store in one csv : default=50000")
    args = parser.parse_args()
    main(args)