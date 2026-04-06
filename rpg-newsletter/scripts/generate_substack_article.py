#!/usr/bin/env python3
"""
Substack Article Generator
Generates Substack article drafts using AI based on Ryan's writing style and knowledge base.
"""
import sys
import json
import os
from datetime import datetime
from openai import OpenAI

def load_knowledge_base(knowledge_dir):
    knowledge_content = []
    knowledge_path = os.path.expanduser(knowledge_dir)
    if not os.path.exists(knowledge_path):
        return ""
    for file in os.listdir(knowledge_path):
        file_path = os.path.join(knowledge_path, file)
        if os.path.isfile(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    knowledge_content.append(f"--- {file} ---\n{f.read()}\n")
            except Exception:
                pass
    return "\n".join(knowledge_content)

def load_writing_style(style_file):
    try:
        with open(style_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return {}

def generate_article(knowledge_dir, style_file, topic=None):
    client = OpenAI()
    knowledge = load_knowledge_base(knowledge_dir)
    style = load_writing_style(style_file)
    
    system_prompt = f"""You are a Substack newsletter creator writing as Ryan Cunningham.
WRITING STYLE GUIDELINES:
- Tone: Direct, conversational, anti-BS, empathetic, educational but not preachy
- Structure: Long-form article (500-800 words)
- Use short paragraphs (2-3 sentences max)
- Use Markdown formatting (headers, bold text, bullet points)
- Avoid corporate jargon, hyperbole, and flowery language
- No em dashes (use periods or commas)
- Focus on practical value and real results
- Incorporate the Gen X narrative: victims of corporate culling 2023/2024, delivering what corporate never does
- Always include an "Actionable Takeaway" section at the end
- Always end with a question to drive replies

RYAN'S WRITING STYLE ANALYSIS:
{json.dumps(style, indent=2)}

KNOWLEDGE BASE:
{knowledge[:4000] if knowledge else "No knowledge base loaded yet."}

Generate a Substack article that matches Ryan's voice and provides genuine value to small business founders."""

    user_prompt = f"""Create a Substack article for this week.
Requirements:
1. Catchy subject line/title
2. Greeting: "Hey [First Name],"
3. Strong opening hook
4. 3 main points or lessons
5. "Your Actionable Takeaway" section
6. Sign off: "Ryan"
7. P.S. section teasing next week
{f"Focus on this topic: {topic}" if topic else "Choose a timely, relevant topic from the knowledge base."}"""

    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7,
            max_tokens=1500
        )
        
        article_content = response.choices[0].message.content
        
        output = {
            "generated_date": datetime.now().isoformat(),
            "topic": topic or "auto-selected",
            "content": article_content,
            "status": "draft"
        }
        return output
    except Exception as e:
        print(f"Error generating article: {e}")
        return None

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python generate_substack_article.py <knowledge_dir> <style_file> [topic]")
        sys.exit(1)
    
    knowledge_dir = sys.argv[1]
    style_file = sys.argv[2]
    topic = sys.argv[3] if len(sys.argv) > 3 else None
    
    result = generate_article(knowledge_dir, style_file, topic)
    if result:
        print(json.dumps(result, indent=2))
    else:
        sys.exit(1)
