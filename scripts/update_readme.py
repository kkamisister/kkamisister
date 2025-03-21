import feedparser
from datetime import datetime

# 블로그 RSS 피드 주소
BLOGS = {
    "Velog": "https://v2.velog.io/rss/kkamisister",
    "Tistory": "https://kkamisister1207.tistory.com/rss",
    "Naver Blog": "https://rss.blog.naver.com/yooondooong.xml"
}

def fetch_feed(feed_url, max_items=5):
    feed = feedparser.parse(feed_url)
    return [(entry.title, entry.link) for entry in feed.entries[:max_items]]

def generate_blog_md():
    sections = ["### 🧾 최신 블로그 글\n"]
    for blog_name, url in BLOGS.items():
        entries = fetch_feed(url)
        section = f"#### 📌 {blog_name}\n"
        for title, link in entries:
            section += f"- [{title}]({link})\n"
        sections.append(section + "\n")
    return "\n".join(sections)

def update_readme():
    with open("README.md", "r", encoding="utf-8") as f:
        content = f.read()

    start_tag = "<!-- BLOG-POST-LIST:START -->"
    end_tag = "<!-- BLOG-POST-LIST:END -->"
    start = content.find(start_tag)
    end = content.find(end_tag)

    if start == -1 or end == -1:
        print("Tags not found in README.md")
        return

    new_content = content[:start + len(start_tag)] + "\n" + generate_blog_md() + content[end:]
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(new_content)

if __name__ == "__main__":
    update_readme()
