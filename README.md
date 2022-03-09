# gpun
Grapheme Parser and unicode normalization work

# Environment Setup

**python requirements**

* **pip requirements**: ```pip install -r requirements.txt``` 

> Its better to use a virtual environment 
> OR use conda-

* **conda**: use environment.yml: ```conda env create -f environment.yml```

**LOCAL ENVIRONMENT: Experimentation Environment**  
```python
OS          : Ubuntu 20.04.3 LTS       
Memory      : 23.4 GiB 
Processor   : Intel® Core™ i5-8250U CPU @ 1.60GHz × 8    
Graphics    : Intel® UHD Graphics 620 (Kabylake GT2)  
Gnome       : 3.36.8
```


# Batch Execution
* run **script.sh** (change execution mode if needed: ```sudo chmod +x script.sh```)
* set the **DATA_DIR** variable to a location to save the processed data

### Separate Execution
* ```python download.py -h```

```python
usage: Oscar Data Download script [-h] [--chunk_size CHUNK_SIZE] data_dir

positional arguments:
  data_dir              Path to save the oscar data as csv

optional arguments:
  -h, --help            show this help message and exit
  --chunk_size CHUNK_SIZE
                        number of data to store in one csv : default=50000
```
* ```python words.py -h```

```python
usage: Oscar Data Word conversion script [-h] [--chunk_size CHUNK_SIZE] data_dir

positional arguments:
  data_dir              Path where oscar data is saved as csv: The data folder should contain sub-folders as described in readme

optional arguments:
  -h, --help            show this help message and exit
  --chunk_size CHUNK_SIZE
                        number of data to tokenize in a chunk : default=5000

```


# Adding a new language
* change ```languages.py``` with the 
    * ```oscar language code``` as a new key and 
    * ```regex pattern of unicode blocks for the language``` as value: 

```python
#---------------------------------------------------------------
# language
#---------------------------------------------------------------
languages={}
languages["bn"]=u'[\u0980-\u09FF]+'
languages["hi"]=u'[\u0900-\u097F]+'
languages["ml"]=u'[\u0D00-\u0D7F]+'
languages["gu"]=u'[\u0A80-\u0AFF]+'
languages["ta"]=u'[\u0B80—\u0BFF]+'
languages["pa"]=u'[\u0A00—\u0A7F]+'
languages["or"]=u'[\u0B00-\u0B7F]+'
```