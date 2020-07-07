'''
@version: Python 3.7.3
@Author: Louis
@Date: 2020-07-07 14:53:45
@LastEditors: Louis
@LastEditTime: 2020-07-07 16:43:31
'''
import os
import sys
import json

import pandas as pd


def get_cy_dt(cy_path=os.path.join(sys.path[0], "conf\\idiom.json")):
    with open(cy_path, "r", encoding="utf-8") as fp:
        dt = json.load(fp)
    return dt

def deal_outliers(df):
    df.loc[df["word"]=="鸡犬之声相闻，老死不相往来", "pinyin"] = "jī quǎn zhī shēng xiāng wén lǎo sǐ bù xiāng wǎng lái"
    df.loc[df["word"]=="各人自扫门前雪，莫管他家瓦上霜", "pinyin"] = "gè rén zì sǎo mén qián xuě mò guǎn tā jiā wǎ shàng shuāng"
    df.loc[df["word"]=="抓耳搔腮", "pinyin"] = "zhuā ěr sāo sāi"
    df.loc[df["word"]=="只许州官放火，不许百姓点灯", "pinyin"] = "zhǐ xǔ zhōu guān fàng huǒ，bù xǔ bǎi xìng diǎn dēng"
    return df

def get_head_tail(df):
    tmp_df = df["pinyin"].str.split(n=-1, expand=True)
    df["head"] = tmp_df[0]
    df["tail"] = tmp_df[3]
    return df

def wash_df(df):
    df = df[["word", "head", "tail"]]
    df = df.sort_values("head").reset_index(drop=True)
    return df

def get_cy_df(cy_json):
    df = pd.DataFrame(cy_json)
    df = deal_outliers(df)
    df = get_head_tail(df)
    df = wash_df(df)
    df = df[["word", "head", "tail"]]
    assert df[df["head"].str.len()>6].empty  # to make sure no outliers 
    return df

def dump_df(df, df_path):
    if not os.path.isdir(os.path.basename(df_path)):
        os.mkdir(os.path.basename(df_path))
    df.to_csv(df_path, index=False)
    print(f"[Data Generated]: {df_path}")

def main():
    dt = get_cy_dt()
    df = get_cy_df(dt)
    dump_df(df, os.path.join(sys.path[0], "data\\full_cy.csv"))
    dump_df(df[df["word"].str.len()==4], os.path.join(sys.path[0], "data\\four_cy.csv"))

if __name__ == "__main__":
    main()
