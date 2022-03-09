#-*- coding: utf-8 -*-
"""
@author:MD.Nazmuddoha Ansary
"""
from __future__ import print_function
#---------------------------
# imports
#---------------------------
import os
import re
from glob import glob
import pandas as pd
from collections import Counter
from tqdm.auto import tqdm
tqdm.pandas()
import argparse
from utils import *
from languages import languages
#---------------------------
# helpers
#---------------------------

def get_words(text,pattern):
    if text.strip():
        words=re.findall(pattern, text)
        return Counter(words)
    else:
        return None

def cvtCounter(counter):
    df = pd.DataFrame.from_dict(counter, orient='index').reset_index()
    df = df.rename(columns={'index':'word', 0:'count'})
    return df

def split_dataframe(df, chunk_size = 5000): 
    chunks =[]
    num_chunks = len(df) // chunk_size + 1
    for i in range(num_chunks):
        chunks.append(df[i*chunk_size:(i+1)*chunk_size])
    return chunks

def process_csv(csv,didx,words_dir,pattern,chunk_size):
    df=pd.read_csv(csv)
    df=reset(df)
    df["words"]=df.text.progress_apply(lambda x:get_words(x,pattern))
    df=reset(df)
    chunks=split_dataframe(df,chunk_size=chunk_size)
    for cidx,df in enumerate(chunks):
        data=Counter()
        for idx in tqdm(range(len(df))):
            data+=df.iloc[idx,-1]
        data=cvtCounter(data)
        _csv=os.path.join(words_dir,f"{didx}_{cidx}.csv")
        data.to_csv(_csv,index=False) 

def main(args):
    data_dir=args.data_dir
    chunk_size=args.chunk_size
    save_dir  =create_dir(data_dir,"splits")
    stats_dir =create_dir(data_dir,"data")
    for lang in languages.keys():
        # unicode patterns
        pattern  =languages[lang]
        # lang dir
        lang_dir =create_dir(data_dir,lang)
        # splits dir
        splits_dir=create_dir(save_dir,lang)
        # process splits 
        csvs=[csv for csv in glob(os.path.join(lang_dir,"*.csv"))]
        LOG_INFO(f"Found {len(csvs)} csv files for {lang}")
        for didx,csv in enumerate(csvs):
            LOG_INFO(f"Language:{lang} CSV:{csv}")
            process_csv(csv,didx,splits_dir,pattern,chunk_size)
        
        # merge splits
        csvs=[csv for csv in glob(os.path.join(splits_dir,"*.csv"))]
        LOG_INFO(f"Found {len(csvs)} splits for {lang}")
        ## read 
        dfs=[pd.read_csv(csv) for csv in tqdm(csvs)]
        ## concat
        df=pd.concat(dfs,ignore_index=True)
        df=reset(df)
        ## group
        df_new = df.groupby(df['word']).aggregate({"count":"sum"})
        df_new = df_new.sort_values(by='count', ascending=False)
        ## form stats 
        df=pd.DataFrame({})
        df["word"]=df_new.index.tolist()
        df["count"]=df_new["count"].tolist()
        df["count"]=df["count"].progress_apply(lambda x:int(x))
        ## save
        df.to_csv(os.path.join(stats_dir,f"{lang}.csv"),index=False)



if __name__=="__main__":
    '''
        parsing and execution
    '''
    parser = argparse.ArgumentParser("Oscar Data Word conversion script")
    parser.add_argument("data_dir", help="Path where oscar data is saved as csv: The data folder should contain sub-folders as described in readme")
    parser.add_argument("--chunk_size",required=False,default=5000,help ="number of data to tokenize in a chunk : default=5000")
    args = parser.parse_args()
    main(args)

            
    