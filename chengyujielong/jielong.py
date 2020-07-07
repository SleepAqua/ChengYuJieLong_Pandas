'''
@version: Python 3.7.3
@Author: Louis
@Date: 2020-07-07 15:42:30
@LastEditors: Louis
@LastEditTime: 2020-07-07 17:53:31
'''
import os
import sys
import argparse

import numpy as np
import pandas as pd
from pypinyin import pinyin


def get_df(mode):
    df = pd.read_csv(os.path.join(sys.path[0], f"data\\{mode}_cy.csv"))
    return df

def get_heads_idx(cy_df):
    cy_df = cy_df.reset_index()
    cy_df = cy_df.groupby("head").agg({"index": "first"})
    return cy_df["index"].to_dict()

def get_all(mode, word, verbose=False, *args):
    df = get_df(mode)
    heads_idx = get_heads_idx(df)
    last_pinyin = pinyin(word)[-1][0]
    if verbose:
        print(last_pinyin)
    if last_pinyin in heads_idx:
        sub_df = df.iloc[heads_idx[last_pinyin]:, :]
    else:
        print(f"[NO SUCH HEAD]: {last_pinyin}")
        return []
    sub_df = sub_df[sub_df["head"] == last_pinyin]
    if verbose:
        print(f"GET {sub_df.shape[0]} results:")
    return sub_df["word"].tolist()

def get_one(mode, word, verbose=False, *args):
    df = get_df(mode)
    heads_idx = get_heads_idx(df)
    last_pinyin = pinyin(word)[-1][0]
    if verbose:
        print(last_pinyin)
    sub_df = df.iloc[heads_idx[last_pinyin]:heads_idx[last_pinyin]+1, 0]
    return sub_df.to_string(header=False,index=False).strip()

def get_random_one(mode, word, verbose=False, *args):
    sub_df = get_all(mode, word, verbose)
    if not sub_df:
        return None
    return sub_df[np.random.randint(0, len(sub_df), dtype=np.int16)]

def get_seq(mode, word, verbose=False, max_len=5):
    word_lst = []
    for i in range(max_len):
        word = get_random_one(mode, word, verbose)
        if not word:
            print(f"[EARLY STOP]: {i+1}")
            break
        word_lst.append(word)
        if verbose:
            print(f"[ADDED]: {word}")
    return word_lst

def main(solution, mode, word, verbose, max_len):
    mode = "four" if not mode else mode
    max_len = 5 if not max_len else max_len

    sol_map = {"all": get_all, "one": get_one, "rand": get_random_one, "seq": get_seq}
    res = sol_map[solution](mode, word, verbose, max_len)
    print(res)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Give me a word, Gain a solution.")
    parser.add_argument("solution", help="""all: full words list \n \ 
                                            one: fixed one word \n \ 
                                            rand: random one word \n \ 
                                            seq: word sequence, --max_len shoule be given for this solution""")
    parser.add_argument("word", help="give me a word !-!")                       
    parser.add_argument("--mode", "-m", help="four/full")
    parser.add_argument('--verbose', '-v', action='count', default=0)
    parser.add_argument("--max_len", "-l", help="max length of the sequence")
    args = parser.parse_args()

    if args.solution == "seq":
        if not args.max_len :
            parser.error('--max_len not be set in seq solution.')

    main(args.solution, args.mode, args.word, args.verbose, int(args.max_len))
