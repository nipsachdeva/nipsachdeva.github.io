import os
import json
import datetime
from openai import OpenAI

# ---------- CONFIG ----------
BLOG_DIR = "blog/posts"
POSTS_INDEX = f"{BLOG_DIR}/posts.json"

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

today = datetime.date.today()
date_str = today.isoformat()

slug = f"{date_str}-real-world-data-systems"
filename = f"{slug}.md"
filepath = f"{BLOG_DIR}/{filename}"

# ---------- PROMPT ----------
prompt = f"""
You are Nipun Sachdeva, a senior data practitioner.

Write a 900–1200 word blog post.

Audience:
- Data scientists
- Data engineers
- Engineering leaders

Tone:
- Practical
- Opinionated
- Business-aware
- No buzzwords

Topics (choose one naturally):
- Forecasting in real-world supply chains
- Data engineering tradeoffs
- Automation and RPA in production
- Why most data projects fail operationally

Structure:
- Strong opening opinion
- Real examples from industry
- Clear takeaways
"""

# ---------- GENERATE ----------
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": prompt}],
)

content = response.choices[0].message.content.strip()

title = content.split("\n")[0].replace("#", "").strip()

# ---------- WRITE MARKDOWN ----------
markdown = f"""---
title: {title}
date: {date_str}
excerpt: Practical lessons from building and operating real-world data systems.
---

{content}
"""

os.makedirs(BLOG_DIR, exist_ok=True)

with open(filepath, "w", encoding="utf-8") as f:
    f.write(markdown)

# ---------- UPDATE posts.json ----------
post_entry = {
    "title": title,
    "date": date_str,
    "excerpt": "Practical lessons from building and operating real-world data systems.",
    "url": f"./posts/{filename}"
}

posts = []

if os.path.exists(POSTS_INDEX):
    try:
        with open(POSTS_INDEX, "r", encoding="utf-8") as f:
            raw = f.read().strip()
            if raw:
                posts = json.loads(raw)
    except Exception:
        posts = []

posts.append({
    "title": title,
    "date": date_str,
    "excerpt": "Practical lessons from building real-world data systems.",
    "url": filename
})


with open(POSTS_INDEX, "w", encoding="utf-8") as f:
    json.dump(posts, f, indent=2)


print("✅ Blog post generated:", filepath)
