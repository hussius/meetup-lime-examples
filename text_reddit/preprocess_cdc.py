#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul  5 09:03:17 2017

@author: mikaelhuss
"""

import pandas as pd
import json 
import numpy as np
import re

def majority_anno(annolist):
    annos = {}
    for anno in annolist:
        if anno['main_type'] in annos:
            annos[anno['main_type']] += 1
        else:
            annos[anno['main_type']] = 1
    return(max(annos, key=annos.get))

def get_all_threads(f):
    all_threads = [json.loads(line.strip()) for line in f]
    return(all_threads)

def get_posts_and_labels(threads, as_list=True):
    post_list=[]
    anno_list=[]
    for thread in threads:
        for post in thread['posts']:
            try:
                if as_list:
                    text = post['body'].lower().strip().split()
                    text = [re.sub(r'\W+', '', word) for word in text]
                    post_list.append(text)
                else:
                    text = post['body'].lower().strip()
                    text = [re.sub(r'\W+', '', word) for word in text]
                    post_list.append(text)
                anno_list.append(majority_anno(post['annotations']))
            except:
                pass #print(post)
    return(post_list, anno_list)

def get_posts_labels_and_depths(threads, as_list=True):
    post_list=[]
    anno_list=[]
    depth_list=[]
    for thread in threads:
        for post in thread['posts']:
            try:
                if as_list:
                    text = post['body'].lower().strip().split()
                    #text = [re.sub(r'\W+', '', word) for word in text]
                    post_list.append(text)
                else:
                    text = post['body'].lower().strip()
                    #text = [re.sub(r'\W+', '', word) for word in text]
                    post_list.append(text)
                anno_list.append(majority_anno(post['annotations']))
                if 'post_depth' in post:
                    depth_list.append(post['post_depth'])
                else:
                    assert('is_first_post' in post)
                    depth_list.append(0)
            except:
                pass #print(post)
    return(post_list, anno_list, depth_list)


def get_unique_words(post_list):
    all_words = [item for sublist in post_list for item in sublist]
    all_unique_words = list(set(all_words))
    return(all_unique_words)

def get_top_n_words(post_list, n):
    all_words = [item for sublist in post_list for item in sublist]
    wds = pd.Series(all_words)
    cts = wds.value_counts()
    return(cts[:n].index.values)

def subset_post_list(post_list, top_words):
    counter=0
    new_list = []
    for post in post_list:
        counter+=1
        if counter % 1000 == 0:
            print(counter)
        new_post=[w for w in post if w in top_words]
        new_list.append(new_post)
    return(new_list)
                
def create_word_mappings(all_unique_words):
    mapping=pd.factorize(all_unique_words)
    word_to_int = {}
    int_to_word = {}
    for i in range(len(mapping[0])):
        word_to_int[mapping[1][i]]=mapping[0][i]
        int_to_word[mapping[0][i]]=mapping[1][i]
    return(word_to_int, int_to_word)

def create_label_mappings():
    class_to_int = {'answer':0, 'question':1, 'agreement':2, 'announcement':3, 'appreciation':4, 'disagreement':5, 'elaboration':6, 'humor':7, 'negativereaction':8, 'other':9}
    int_to_class = {}
    for v, k in enumerate(class_to_int):
        int_to_class[v]=k
    return(class_to_int, int_to_class)

