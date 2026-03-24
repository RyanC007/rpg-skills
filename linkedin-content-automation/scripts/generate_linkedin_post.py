#!/usr/bin/env python3
"""
LinkedIn Post Generator
Generates LinkedIn post drafts using AI based on Ryan's writing style and knowledge base.
"""

import sys
import json
import os
from datetime import datetime
from openai import OpenAI

def load_knowledge_base(knowledge_dir):
    """Load all knowledge base files from the knowledge directory."""
    knowledge_content = []
    knowledge_path = os.path.expanduser(knowledge_dir)
    
    if not os.path.exists(knowledge_path):
        print(f"Warning: Knowledge directory not found at {knowledge_path}")
        return ""
    
    for file in os.listdir(knowledge_path):
        file_path = os.path.join(knowledge_path, file)
        if os.path.isfile(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    knowledge_content.append(f"--- {file} ---\n{f.read()}\n")
            except Exception as e:
                print(f"Warning: Could not read {file}: {e}")
    
    return "\n".join(knowledge_content)

def load_writing_style(style_file):
    """Load Ryan's writing style analysis."""
    try:
        with open(style_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Warning: Could not load writing style file: {e}")
        return {}

def generate_post(knowledge_dir, style_file, topic=None, post_type="standard"):
    """
    Generate a LinkedIn post draft.
    
    Args:
        knowledge_dir: Directory containing knowledge base files
        style_file: Path to Ryan's writing style analysis JSON
        topic: Optional specific topic to write about
        post_type: Type of post (standard, infographic, question)
    """
    client = OpenAI()
    
    # Load knowledge base and writing style
    knowledge = load_knowledge_base(knowledge_dir)
    style = load_writing_style(style_file)
    
    # Build the prompt
    system_prompt = f"""You are a LinkedIn content creator writing as Ryan Cunningham.

WRITING STYLE GUIDELINES:
- Tone: Direct, conversational, strategic, focused on practical application
- Topics: AI automation, brand building, knowledge building, neural nets, marketing for small business founders, "Founders Flywheel" framework
- Structure: Medium-length posts (150-250 words)
- Always end with an engaging question to drive comments
- Use RPG brand voice: direct, anti-BS, empathetic, educational but not preachy
- Avoid corporate jargon, hyperbole, and flowery language
- Use contractions naturally
- Focus on practical value and real results
- Incorporate the Gen X narrative: victims of corporate culling 2023/2024, delivering what corporate never does

RYAN'S WRITING STYLE ANALYSIS:
{json.dumps(style, indent=2)}

KNOWLEDGE BASE:
{knowledge[:3000] if knowledge else "No knowledge base loaded yet."}

POST TYPE: {post_type}
{"TOPIC: " + topic if topic else "Choose a relevant topic from Ryan's focus areas."}

Generate a LinkedIn post that matches Ryan's voice and provides genuine value to small business founders."""

    user_prompt = f"""Create a LinkedIn post for today ({datetime.now().strftime('%B %d, %Y')}).

Requirements:
1. Medium length (150-250 words)
2. Start with a hook that grabs attention
3. Provide practical, actionable insight
4. End with an engaging question
5. Include 3-5 relevant hashtags
6. Match Ryan's authentic voice

{f"Focus on this topic: {topic}" if topic else "Choose a timely, relevant topic."}
{f"This is an {post_type} post." if post_type != "standard" else ""}"""

    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.8,
            max_tokens=500
        )
        
        post_content = response.choices[0].message.content
        
        # Save the generated post
        output = {
            "generated_date": datetime.now().isoformat(),
            "topic": topic or "auto-selected",
            "post_type": post_type,
            "content": post_content,
            "status": "draft"
        }
        
        return output
        
    except Exception as e:
        print(f"Error generating post: {e}")
        return None

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python generate_linkedin_post.py <knowledge_dir> <style_file> [topic] [post_type]")
        sys.exit(1)
    
    knowledge_dir = sys.argv[1]
    style_file = sys.argv[2]
    topic = sys.argv[3] if len(sys.argv) > 3 else None
    post_type = sys.argv[4] if len(sys.argv) > 4 else "standard"
    
    result = generate_post(knowledge_dir, style_file, topic, post_type)
    
    if result:
        print(json.dumps(result, indent=2))
    else:
        print("Failed to generate post")
        sys.exit(1)
