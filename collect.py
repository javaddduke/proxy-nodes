#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import requests
import base64
import time
from urllib.parse import urlparse

# ================= 配置区域 =================
OUTPUT_FILE = "nodes.txt"  # 输出的文件名
# ============================================

def decode_base64(data):
    """尝试解码Base64，失败就返回原字符串"""
    try:
        # 补足填充字符
        padding = 4 - len(data) % 4
        if padding != 4:
            data += '=' * padding
        return base64.b64decode(data).decode('utf-8', errors='ignore')
    except:
        return data

def extract_links_from_text(text):
    """从文本中提取所有代理链接"""
    patterns = [
        r'vmess://[a-zA-Z0-9+/=]+',
        r'vless://[a-zA-Z0-9\-_.~%]+',
        r'ss://[a-zA-Z0-9\-_.~%]+',
        r'trojan://[a-zA-Z0-9\-_.~%]+',
        r'ssr://[a-zA-Z0-9\-_]+',  # SSR是Base64编码
    ]
    
    links = []
    for pattern in patterns:
        found = re.findall(pattern, text)
        links.extend(found)
    return links

def fetch_from_url(url, headers=None):
    """从URL获取内容"""
    if headers is None:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    try:
        resp = requests.get(url, headers=headers, timeout=15)
        if resp.status_code == 200:
            return resp.text
    except Exception as e:
        print(f"  [错误] 获取 {url} 失败: {e}")
    return ""

def fetch_from_url_base64(url):
    """从URL获取Base64编码的内容（常见的订阅格式）"""
    text = fetch_from_url(url)
    if text:
        return decode_base64(text)
    return ""

def main():
    print("=" * 50)
    print("节点采集脚本开始运行")
    print("=" * 50)
    
    all_links = set()  # 用set自动去重
    
    # ============ 数据源列表（你可以自行添加/修改） ============
    sources = [
        # 方式1：直接抓取网页，从中提取节点链接
        {
            "type": "html",
            "url": "https://example-proxy-site-1.com/free",  # 这里替换成你的目标网站
            "note": "示例网站1"
        },
        # 方式2：抓取Base64编码的订阅链接
        {
            "type": "base64",
            "url": "https://example-subscribe.com/sub",  # 这里替换成你的订阅地址
            "note": "示例订阅1"
        },
        # 方式3：抓取GitHub上的订阅文件
        {
            "type": "text",
            "url": "https://raw.githubusercontent.com/某用户/某仓库/main/sub.txt",
            "note": "GitHub源1"
        },
    ]
    # =======================================================
    
    for source in sources:
        print(f"\n📡 正在抓取: {source['note']}")
        print(f"    URL: {source['url']}")
        
        if source['type'] == 'html':
            content = fetch_from_url(source['url'])
            links = extract_links_from_text(content)
            print(f"    ✅ 提取到 {len(links)} 个链接")
            all_links.update(links)
            
        elif source['type'] == 'base64':
            content = fetch_from_url_base64(source['url'])
            links = extract_links_from_text(content)
            print(f"    ✅ 解码后提取到 {len(links)} 个链接")
            all_links.update(links)
            
        elif source['type'] == 'text':
            content = fetch_from_url(source['url'])
            links = extract_links_from_text(content)
            print(f"    ✅ 提取到 {len(links)} 个链接")
            all_links.update(links)
        
        # 礼貌性延迟，避免被反爬
        time.sleep(1)
    
    # 写入文件
    final_links = list(all_links)
    print(f"\n📊 去重后共有 {len(final_links)} 个节点")
    
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        for link in final_links:
            f.write(link + '\n')
    
    print(f"✅ 已写入 {OUTPUT_FILE}")
    
    # 打印前5个作为预览
    print("\n📝 前5个节点预览:")
    for i, link in enumerate(final_links[:5]):
        print(f"  {i+1}. {link[:80]}...")
    
    print("\n" + "=" * 50)
    print("采集完成")

if __name__ == "__main__":
    main()
