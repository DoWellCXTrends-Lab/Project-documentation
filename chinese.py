import numpy as np
import pandas as pd
import os
import json
import matplotlib
import seaborn as sns
import matplotlib.pyplot as plt
from tqdm import tqdm_notebook
%matplotlib inline 
from wordcloud import WordCloud, STOPWORDS
from joblib import Parallel, delayed
import tqdm
import jieba
import time
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import SVC
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.metrics import confusion_matrix, classification_report, roc_auc_score, f1_score, recall_score

data_df = pd.read_csv("./chinese_news.csv")
print(f"Rows: {data_df.shape[0]}, Cols: {data_df.shape[1]}")
print(f"Samples with content null: {data_df.loc[data_df['content'].isnull()].shape[0]}")
print(f"Samples with headline null: {data_df.loc[data_df['headline'].isnull()].shape[0]}")
data_df = data_df.loc[~data_df['content'].isnull()]
print(f"New data shape: {data_df.shape}")

'''
!wget https://github.com/adobe-fonts/source-han-sans/raw/release/SubsetOTF/SourceHanSansCN.zip
!unzip -j "SourceHanSansCN.zip" "SourceHanSansCN/SourceHanSansCN-Regular.otf" -d "."
!rm SourceHanSansCN.zip
!ls
'''


import matplotlib.font_manager as fm
font_path = './SourceHanSansCN-Regular.otf'
prop = fm.FontProperties(fname=font_path)
def plot_count(feature, title, df, font_prop=prop, size=1):
    f, ax = plt.subplots(1,1, figsize=(4*size,4))
    total = float(len(df))
    g = sns.countplot(df[feature], order = df[feature].value_counts().index[:20], palette='Set3')
    g.set_title("Number and percentage of {}".format(title))
    if(size > 2):
        plt.xticks(rotation=90, size=8)
    for p in ax.patches:
        height = p.get_height()
        ax.text(p.get_x()+p.get_width()/2.,
                height + 3,
                '{:1.2f}%'.format(100*height/total),
                ha="center") 
    ax.set_xticklabels(ax.get_xticklabels(), fontproperties=font_prop);
    plt.show()  
    
plot_count('tag', 'tag (all data)', font_prop=prop, df=data_df,size=1.2)

data_df['datetime'] = data_df['date'].apply(lambda x: pd.to_datetime(x))
data_df['year'] = data_df['datetime'].dt.year
data_df['month'] = data_df['datetime'].dt.month
data_df['dayofweek'] = data_df['datetime'].dt.dayofweek


def jieba_cut(x, sep=' '):
    return sep.join(jieba.cut(x, cut_all=False))

print('raw', data_df['headline'][0])
print('cut', jieba_cut(data_df['headline'][0], ', '))


%%time
data_df['headline_cut'] = Parallel(n_jobs=4)(
    delayed(jieba_cut)(x) for x in tqdm.tqdm_notebook(data_df['headline'].values)
)

%%time
data_df['content_cut'] = Parallel(n_jobs=4)(
    delayed(jieba_cut)(x) for x in tqdm.tqdm_notebook(data_df['content'].values)
)

prop = fm.FontProperties(fname=font_path, size=20)

stopwords = set(STOPWORDS)

def show_wordcloud(data, font_path=font_path, title = None):
    wordcloud = WordCloud(
        background_color='white',
        stopwords=stopwords,
        font_path=font_path,
        max_words=50,
        max_font_size=40, 
        scale=5,
        random_state=1
    ).generate(str(data))

    fig = plt.figure(1, figsize=(10,10))
    plt.axis('off')
    if title: 
        prop = fm.FontProperties(fname=font_path)
        fig.suptitle(title, fontsize=40, fontproperties=prop)
        fig.subplots_adjust(top=2.3)

    plt.imshow(wordcloud)
    
    
    
show_wordcloud(data_df['headline_cut'], font_path, title = 'Prevalent words in headline, all data')