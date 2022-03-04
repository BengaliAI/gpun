#---------------------------
# imports
#---------------------------
import os
from glob import glob
import pandas as pd
from collections import Counter
from tqdm.auto import tqdm
tqdm.pandas()
#---------------------------
# helpers
#---------------------------
punctuations           =    ['!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', 
                            '/', ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`',
                            '{', '|', '}', '~', '।', '॥','“','”'] 
def reset(df):
    df.dropna(inplace=True)
    df.reset_index(drop=True,inplace=True) 
    return df

def get_words(text):
    if text.strip():
        for punct in punctuations+["\n"]:
            text=text.replace(punct," ")
        words=[word for word in text.split(" ") if word.strip()]
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

def process_csv(csv,didx,words_dir):
    df=pd.read_csv(csv)
    df=reset(df)
    df["words"]=df.text.progress_apply(lambda x:get_words(x))
    df=reset(df)
    chunks=split_dataframe(df)
    for cidx,df in enumerate(chunks):
        data=Counter()
        for idx in tqdm(range(len(df))):
            data+=df.iloc[idx,-1]
        data=cvtCounter(data)
        _csv=os.path.join(words_dir,f"{didx}_{cidx}.csv")
        data.to_csv(_csv,index=False) 

if __name__=="__main__":
    for lang in ["bn","hi","ml","gu","ta","pa","or"]:
        data_dir=f"/backup/Oscar/data/{lang}"
        words_dir=f"/backup/Oscar/words/{lang}/"
        if not os.path.exists(words_dir):
            os.mkdir(words_dir)
            
        csvs=[csv for csv in glob(os.path.join(data_dir,"*.csv"))]
        for didx,csv in enumerate(csvs):
            print(lang,didx)
            process_csv(csv,didx,words_dir)