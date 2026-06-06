#!/usr/bin/env python3
"""
分析 Serenity 推文数据集的脚本
"""

import csv
import pandas as pd
from collections import Counter
import re
from datetime import datetime

def analyze_serenity_dataset(csv_path):
    """分析 Serenity 推文数据集"""
    
    print("🔍 开始分析 Serenity 数据集...")
    
    # 读取数据
    try:
        df = pd.read_csv(csv_path, encoding='utf-8')
        print(f"✅ 成功读取数据集，共 {len(df)} 条推文")
    except Exception as e:
        print(f"❌ 读取失败: {e}")
        return
    
    # 基本信息
    print(f"\n📊 数据集基本信息:")
    print(f"   列数: {len(df.columns)}")
    print(f"   列名: {list(df.columns)}")
    
    # 检查关键列
    if 'created_at' in df.columns:
        # 转换日期
        df['created_at'] = pd.to_datetime(df['created_at'], errors='coerce')
        date_range = df['created_at'].dropna()
        if len(date_range) > 0:
            print(f"\n📅 时间范围:")
            print(f"   最早: {date_range.min()}")
            print(f"   最晚: {date_range.max()}")
            print(f"   时间跨度: {(date_range.max() - date_range.min()).days} 天")
    
    # 分析文本内容
    if 'text' in df.columns:
        print(f"\n📝 文本分析:")
        
        # 推文长度
        df['text_length'] = df['text'].astype(str).apply(len)
        print(f"   平均推文长度: {df['text_length'].mean():.0f} 字符")
        print(f"   最长推文: {df['text_length'].max():.0f} 字符")
        print(f"   最短推文: {df['text_length'].min():.0f} 字符")
        
        # 语言分布
        if 'language' in df.columns:
            lang_counts = df['language'].value_counts()
            print(f"\n🌐 语言分布:")
            for lang, count in lang_counts.head(5).items():
                print(f"   {lang}: {count} 条 ({count/len(df)*100:.1f}%)")
        
        # 提取股票代码
        print(f"\n💹 提到的股票代码:")
        stock_pattern = r'\$[A-Z]{1,5}'
        all_stocks = []
        for text in df['text'].astype(str):
            stocks = re.findall(stock_pattern, text)
            all_stocks.extend(stocks)
        
        stock_counter = Counter(all_stocks)
        print(f"   共提到 {len(stock_counter)} 种股票代码")
        print(f"   最常提到的股票:")
        for stock, count in stock_counter.most_common(10):
            print(f"     {stock}: {count} 次")
        
        # 提取关键词
        print(f"\n🔑 高频关键词:")
        # 简单分词（按空格分割）
        all_words = []
        for text in df['text'].astype(str):
            words = text.lower().split()
            all_words.extend([w for w in words if len(w) > 3])
        
        word_counter = Counter(all_words)
        print(f"   最常提到的词汇:")
        for word, count in word_counter.most_common(15):
            print(f"     {word}: {count} 次")
    
    # 互动数据
    print(f"\n❤️ 互动数据分析:")
    for col in ['favorite_count', 'retweet_count', 'reply_count', 'view_count']:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
            print(f"   {col}: 平均 {df[col].mean():.1f}, 最大 {df[col].max():.0f}")
    
    # 推文类型
    if 'type' in df.columns:
        type_counts = df['type'].value_counts()
        print(f"\n📱 推文类型分布:")
        for ttype, count in type_counts.items():
            print(f"   {ttype}: {count} 条 ({count/len(df)*100:.1f}%)")
    
    print(f"\n✅ 分析完成！")

def extract_sample_tweets(csv_path, n=5):
    """提取样本推文"""
    print(f"\n📄 样本推文（前{n}条）:")
    try:
        df = pd.read_csv(csv_path, encoding='utf-8', nrows=n)
        for i, row in df.iterrows():
            text_preview = str(row.get('text', ''))[:200]
            print(f"\n--- 推文 {i+1} ---")
            print(f"内容: {text_preview}...")
            if 'created_at' in row:
                print(f"时间: {row['created_at']}")
            if 'favorite_count' in row:
                print(f"喜欢: {row['favorite_count']}")
    except Exception as e:
        print(f"❌ 提取样本失败: {e}")

if __name__ == "__main__":
    csv_path = "/root/serenity.csv"
    analyze_serenity_dataset(csv_path)
    extract_sample_tweets(csv_path, n=3)