import datetime, json, os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

today = datetime.date.today().isoformat()
slug = f"{today}-real-world-data-systems"

prompt = f"""
You are Nipun Sachdeva, a senior data practitioner.

Write a 900–1200 word blog post.
Audience: data scientists, engineers, tech leaders.
Tone: practical, opinionated, business-aware.
Topics: forecasting, data pipelines, automation, real-world tradeoffs.

Include:
- Strong opening opinion
- Real examples
- Clear takeaways
"""

resp = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": prompt}]
)

content = resp.choices[0].message.content

post = f"""---
title: Real-World Lessons from Production Data Systems
date: {today}
excerpt: Why building data systems is more about decisions than algorithms.
---

{content}
"""

path = f"blog/posts/{slug}.md"
with open(path, "w") as f:
    f.write(post)

print("Created:", path)
