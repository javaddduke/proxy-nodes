#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import requests
import base64
import time

OUTPUT_FILE = "nodes.txt"

def decode_base64(data):
    try:
        data = data.strip()
        padding = 4 - len(data) % 4
        if padding != 4:
            data += '=' * padding
        return base64.b64decode(data).decode('utf-8', errors='ignore')
    except:
        return data

def extract_links(text):
    patterns = [
        r'(vmess://[a-zA-Z0-9+/=]+)',
        r'(vless://[^\s<>\"\']+)',
        r'(ss://[^\s<>\"\']+)',
        r'(trojan://[^\s<>\"\']+)',
        r'(ssr://[a-zA-Z0-9\-_/+=]+)',
        r'(hysteria2?://[^\s<>\"\']+)',
        r'(tuic://[^\s<>\"\']+)',
    ]
    links = []
    for p in patterns:
        found = re.findall(p, text)
        links.extend(found)
    return links

def fetch(url, is_base64=False):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    try:
        r = requests.get(url, headers=headers, timeout=30)
        if r.status_code == 200:
            text = r.text.strip()
            if is_base64:
                text = decode_base64(text)
            return text
        else:
            print(f"  ⚠️ HTTP {r.status_code}")
    except Exception as e:
        print(f"  ❌ 错误: {e}")
    return ""

def main():
    print("=" * 50)
    print("🚀 节点采集开始")
    print("=" * 50)

    all_links = set()

    # =====================================================
    #  真实数据源（全部来自 GitHub 公开仓库）
    #  如果某个源失效了（返回0），删掉换新的即可
    # =====================================================
    sources = [
        {
            "name": "mfuu/v2ray",
            "url": "https://raw.githubusercontent.com/mfuu/v2ray/master/v2ray",
            "base64": True
        },
        {
            "name": "peasoft/NoMoreWalls",
            "url": "https://raw.githubusercontent.com/peasoft/NoMoreWalls/master/list_raw.txt",
            "base64": True
        },
        {
            "name": "mahdibland/V2RayAggregator-1",
            "url": "https://raw.githubusercontent.com/mahdibland/V2RayAggregator/master/sub/sub_merge_base64.txt",
            "base64": True
        },
        {
            "name": "Pawdroid/Free-servers",
            "url": "https://raw.githubusercontent.com/Pawdroid/Free-servers/main/sub",
            "base64": True
        },
        {
            "name": "aiboboxx/v2rayfree",
            "url": "https://raw.githubusercontent.com/aiboboxx/v2rayfree/main/v2",
            "base64": True
        },
        {
            "name": "barry-far/V2ray-Configs-Sub1",
            "url": "https://raw.githubusercontent.com/barry-far/V2ray-Configs/main/Sub1.txt",
            "base64": False
        },
        {
            "name": "barry-far/V2ray-Configs-Sub2",
            "url": "https://raw.githubusercontent.com/barry-far/V2ray-Configs/main/Sub2.txt",
            "base64": False
        },
        {
            "name": "barry-far/V2ray-Configs-Sub3",
            "url": "https://raw.githubusercontent.com/barry-far/V2ray-Configs/main/Sub3.txt",
            "base64": False
        },
        {
            "name": "ermaozi/get_subscribe",
            "url": "https://raw.githubusercontent.com/ermaozi/get_subscribe/main/subscribe/v2ray.txt",
            "base64": True
        },
        {
            "name": "freefq/free",
            "url": "https://raw.githubusercontent.com/freefq/free/master/v2",
            "base64": True
        },
        {
            "name": "mianfeifq/share",
            "url": "https://raw.githubusercontent.com/mianfeifq/share/main/data2023315.txt",
            "base64": False
        },
        {
            "name": "Leon406/SubCrawler",
            "url": "https://raw.githubusercontent.com/Leon406/SubCrawler/master/sub/share/vless",
            "base64": True
        },
        {
            "name": "Leon406/SubCrawler-ss",
            "url": "https://raw.githubusercontent.com/Leon406/SubCrawler/master/sub/share/ss",
            "base64": True
        },
        {
            "name": "a2470982985/getNode",
            "url": "https://raw.githubusercontent.com/a2470982985/getNode/main/v2ray.txt",
            "base64": True
        },
    ]

    for src in sources:
        print(f"\n📡 [{src['name']}]")
        print(f"   {src['url']}")
        content = fetch(src["url"], is_base64=src["base64"])
        if content:
            links = extract_links(content)
            count = len(links)
            if count > 0:
                print(f"   ✅ 提取到 {count} 个节点")
            else:
                print(f"   ⚠️ 页面有内容但未提取到节点（格式可能变了）")
            all_links.update(links)
        else:
            print(f"   ❌ 获取失败或内容为空")
        time.sleep(1)

    # 保存
    final = sorted(all_links)
    print(f"\n{'=' * 50}")
    print(f"📊 去重后共计: {len(final)} 个节点")

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        for link in final:
            f.write(link + '\n')

    print(f"✅ 已写入 {OUTPUT_FILE}")

    if final:
        print(f"\n📝 前 5 个节点预览:")
        for i, l in enumerate(final[:5]):
            print(f"   {i+1}. {l[:80]}...")
    else:
        print("\n⚠️ 没有抓到任何节点！所有数据源可能都失效了")
        print("   请去 GitHub 搜索 'free v2ray nodes' 找新的源")

    print(f"\n🎉 采集完成")

if __name__ == "__main__":
    main()
