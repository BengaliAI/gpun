#---------------------------
# imports
#---------------------------
import re
import os
from glob import glob
import pandas as pd
from tqdm.auto import tqdm
tqdm.pandas()
#---------------------------
# csv
#---------------------------
def reset(df):
    df.dropna(inplace=True)
    df.reset_index(drop=True,inplace=True) 
    return df

def de_emojify(text):
    regrex_pattern = re.compile(pattern = "["u"\U0001F600-\U0001F64F"  # emoticons
                                             u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                                             u"\U0001F680-\U0001F6FF"  # transport & map symbols
                                             u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                                            "]+", flags = re.UNICODE)
    return regrex_pattern.sub(r'',text)

def clean(text):
    text=str(text)
    text = re.sub("[a-zA-Z0-9]+", "",text)
    if len(text)==0:
        return None
    else:
        text=de_emojify(text)
        if len(text)>0:
            return text
        else:
            return None

if __name__=="__main__":
    for lang in ["bn","hi","ml","gu","ta","pa","or"]:
        print(lang)
        data_dir=f"/backup/Oscar/words/{lang}/"
        csvs=[csv for csv in glob(os.path.join(data_dir,"*.csv"))]
        dfs=[pd.read_csv(csv) for csv in tqdm(csvs)]
        df=pd.concat(dfs,ignore_index=True)
        df=reset(df)
        df["word"]=df["word"].progress_apply(lambda x:clean(x))
        df=reset(df)
        # group
        df_new = df.groupby(df['word']).aggregate({"count":"sum"})
        df_new = df_new.sort_values(by='count', ascending=False)
        # new
        df=pd.DataFrame({})
        df["word"]=df_new.index.tolist()
        df["count"]=df_new["count"].tolist()
        df["count"]=df["count"].progress_apply(lambda x:int(x))
        df.to_csv(os.path.join("/backup/Oscar/words/",f"{lang}.csv"))