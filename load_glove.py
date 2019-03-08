import numpy as np
import pickle
import argparse
from tqdm import tqdm

from transformer import Constants

def load_glove(glove_path, vocab=set([])):
    ''' Loads GloVe embeddings '''

    word2emb = {}
    with open(glove_path,'r', encoding="utf-8") as f:
        for line in tqdm(f):
            split_line = line.split()
            word = split_line[0]
            if word in vocab:
                word2emb[word] = np.array([float(val) for val in split_line[1:]])

    return word2emb

def create_glove_emb_table(word2idx, split_name, glove_path='data/glove/glove.6B.300d.txt', glove_size=300):
    ''' Creates GloVe embedding table and changes word2idx '''

    #- Disregard special tokens when looking for glove pairs
    word2idx.pop(Constants.PAD_WORD, None)
    word2idx.pop(Constants.UNK_WORD, None)
    word2idx.pop(Constants.BOS_WORD, None)
    word2idx.pop(Constants.EOS_WORD, None)

    #- Load GloVe model
    print("[Info] Load GloVe model.")
    word2emb = load_glove(glove_path, set(word2idx.keys()))

    #- Create embedding table and new vocab, randomly initialize special tokens
    word2idx = {
        Constants.BOS_WORD: Constants.BOS,
        Constants.EOS_WORD: Constants.EOS,
        Constants.PAD_WORD: Constants.PAD,
        Constants.UNK_WORD: Constants.UNK}

    emb_table = np.zeros(shape=(len(word2emb) + 4, glove_size))
    emb_table[Constants.PAD] = np.random.randn(glove_size)
    emb_table[Constants.UNK] = np.random.randn(glove_size)
    emb_table[Constants.BOS] = np.random.randn(glove_size)
    emb_table[Constants.EOS] = np.random.randn(glove_size)
    for idx, (word, emb) in enumerate(word2emb.items(), 4):
        emb_table[idx] = emb
        word2idx[word] = idx

    print('[Info] Final {} vocabulary size: {}'.format(split_name, len(word2idx)))

    return word2idx, emb_table
