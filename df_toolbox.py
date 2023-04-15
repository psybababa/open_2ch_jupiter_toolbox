from collections import Counter as ct
from datetime import date
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import string
import sudachipy as sp

class Convert:
    def __init__(self):
        self.files = [
            {
                "fname": "comments",
                "encoding": "utf_8_sig",
                "mode": "a"
            },
            {
                "fname": "threads",
                "encoding": "utf_8_sig",
                "mode": "a"
            },
            {"fname": "titles",
             "encoding": "utf_8_sig",
             "mode": "a"
            },
        ]

    def convfile(self, finfo):
        df = pd.read_pickle(f"./data/{finfo['fname']}.pkl")
        df.to_csv(f"./data/{finfo['fname']}.csv", encoding=finfo["encoding"], mode=finfo["mode"])

    def convall(self):
        for finfo in self.files:
            self.convfile(finfo)

class process:
    dparam = {
        'date': date.today(), #日付を単位での検索用
        'time':None,#時間単位での検索用
        'id':None, #追跡したい特定のidがいればここに入力
        'num':None, #調べたいデータの数を入力すればよし
        'thread':None, #特定のスレッド内で検索したければここにurlを入力すればいいです
        }
    
    def __init__(self):
        mode = sp.Tokenizer.SplitMode.C
        self.tokenizer = sp.Dictionary().create(mode)
        self.tokenizer.set_option("emoji", True)      
        
    def mergeparam(self,param):
        if param:
            self.dparam.update(param)
    
    def cleanfile(self, finfo):
        df = pd.read_pickle(f"./data/{finfo['fname']}.pkl")
        df['comment'] = df['comment'].replace('\n',' ')
        df['comment'] = df['comment'].translate(str.maketrans('','',string.punctuation))
        df['date'] = df['date'].replace('/','-')
        date_str = f"{df['date']}{df['timetable']}"
        df.drop(['date','timetable'],axis=1,inplace=True)
        df['datetime'] = pd.to_datetime(date_str)
        df.dropna(inplace=True, subset=['title', 'link'])
        df.drop_duplicates(subset='title', inplace=True)
        df = df.reindex(columns = ['comment','datetime','id','title','link'])
        df.to_pickle(f"./data/{finfo['fname']}_clean.pkl")
    
    def tokenize(self,txt):          
        tokens = self.tokenizer.tokenize(txt)
        return [(t.surface(), t.part_of_speech()) for t in tokens]
    
    def ntokenize(self,txt):           
        tokens = self.tokenizer.tokenize(txt)
        return [(t.normalized_form(), t.part_of_speech()) for t in tokens]
    
    def countid(self,finfo,n):
        df = pd.read_pickle(f"./data/{finfo['fname']}.pkl")
        cid = ct(df['id'])
        mcid = cid.most_common(n)
        return mcid
    
    def countwords(self,finfo,n):
        comments = pd.read_pickle(f"./data/{finfo['fname']}.pkl")['comment']
        wds = [t[0] for comment in comments for t in [self.ntokenize(comment)] if t[1] in ['名詞','動詞','形容詞','固有名詞','emoji']]
        cwds = ct(wds)
        return cwds.most_common(n)
    
    def purseid(self,finfo,id,date):
        df = pd.read_pickle(f"./data/{finfo['fname']}.pkl")
        idf = pd.DataFrame((df['datetime'].dt.day == date) & (df['id'] == id))
        return idf
    
class visualize:
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    