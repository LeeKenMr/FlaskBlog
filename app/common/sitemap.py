
import xml.etree.ElementTree as ET
from xml.dom import minidom
import os
import env
from ..models import Article
# 单个URL的类
class URL:
    def __init__(self, loc, lastmod, changefreq, priority):
        self.loc = loc
        self.lastmod = lastmod
        self.changefreq = changefreq
        self.priority = priority
        
# 生成Sitemap.xml的类    
class Sitemap:
    def __init__(self, xmlns, urls):
        self.xmlns = xmlns
        self.urls = urls

# 生成Sitemap.xml函数
def sitemap():
    # 定义一个空列表，用于存放文章的URL
    urls = []
    
    # 加入单独页
    urls.append(URL(env.WEB_URL, "2024-03-28", "monthly", 0.6))
    urls.append(URL(f'{env.WEB_URL}/type/go/1', "2024-03-28", "monthly", 0.6))
    urls.append(URL(f'{env.WEB_URL}/type/py/1', "2024-03-28", "monthly", 0.6))
    urls.append(URL(f'{env.WEB_URL}/type/qd/1', "2024-03-28", "monthly", 0.6))
    urls.append(URL(f'{env.WEB_URL}/type/uni/1', "2024-03-28", "monthly", 0.6))
    urls.append(URL(f'{env.WEB_URL}/type/db/1', "2024-03-28", "monthly", 0.6))
    urls.append(URL(f'{env.WEB_URL}/type/ser/1', "2024-03-28", "monthly", 0.6))
    urls.append(URL(f'{env.WEB_URL}/type/ai/1', "2024-03-28", "monthly", 0.6))
    urls.append(URL(f'{env.WEB_URL}/type/chain/1', "2024-03-28", "monthly", 0.6))
    urls.append(URL(f'{env.WEB_URL}/type/tools/1', "2024-03-28", "monthly", 0.6))
    urls.append(URL(f'{env.WEB_URL}/us', "2024-03-28", "monthly", 0.6))
    # 获取所有文章
    articles = Article.select()
    for article in articles:
        # 将文章的URL加入到列表中
        urls.append(URL(f'{env.WEB_URL}/note/{article.id}', article.created_at.strftime("%Y-%m-%d"), "monthly", 0.8))
    # 合成成最终的sitemap文本
    sitemap = Sitemap("http://www.sitemaps.org/schemas/sitemap/0.9", urls)
    root = ET.Element("urlset", xmlns=sitemap.xmlns)
    for url in sitemap.urls:
        url_elem = ET.SubElement(root, "url")
        ET.SubElement(url_elem, "loc").text = url.loc
        ET.SubElement(url_elem, "lastmod").text = url.lastmod
        ET.SubElement(url_elem, "changefreq").text = url.changefreq
        ET.SubElement(url_elem, "priority").text = str(url.priority)

    # 将 ElementTree 转换为字符串
    xml_str = ET.tostring(root, encoding="utf-8", method="xml")

    # 使用 minidom 进行格式化
    parsed_str = minidom.parseString(xml_str)
    pretty_xml_str = parsed_str.toprettyxml(indent="  ", encoding="utf-8")

    # 确保目录存在
    os.makedirs("app/jingtai", exist_ok=True)

    # 写入格式化后的 XML 到文件
    with open("app/jingtai/sitemap.xml", "wb") as f:
        f.write(pretty_xml_str)
        print("Sitemap.xml生成成功")