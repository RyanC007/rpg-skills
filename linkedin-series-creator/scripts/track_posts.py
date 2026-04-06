#!/usr/bin/env python3
"""
LinkedIn Post Tracker
Tracks posting cadence and ensures minimum 3 posts per week.
"""

import sys
import json
import os
from datetime import datetime, timedelta
from pathlib import Path

def load_post_history(history_file):
    """Load post history from JSON file."""
    if not os.path.exists(history_file):
        return {"posts": []}
    
    try:
        with open(history_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading post history: {e}")
        return {"posts": []}

def save_post_history(history_file, history):
    """Save post history to JSON file."""
    try:
        os.makedirs(os.path.dirname(history_file), exist_ok=True)
        with open(history_file, 'w', encoding='utf-8') as f:
            json.dump(history, f, indent=2)
        return True
    except Exception as e:
        print(f"Error saving post history: {e}")
        return False

def get_current_week_posts(history):
    """Get posts from the current week (Monday to Sunday)."""
    today = datetime.now()
    week_start = today - timedelta(days=today.weekday())  # Monday
    week_start = week_start.replace(hour=0, minute=0, second=0, microsecond=0)
    
    current_week_posts = []
    for post in history.get("posts", []):
        post_date = datetime.fromisoformat(post["date"])
        if post_date >= week_start:
            current_week_posts.append(post)
    
    return current_week_posts

def check_posting_cadence(history_file):
    """Check if posting cadence meets minimum 3 posts per week."""
    history = load_post_history(history_file)
    current_week_posts = get_current_week_posts(history)
    
    posts_this_week = len(current_week_posts)
    min_posts = 3
    
    result = {
        "posts_this_week": posts_this_week,
        "min_required": min_posts,
        "meets_requirement": posts_this_week >= min_posts,
        "posts_needed": max(0, min_posts - posts_this_week),
        "current_week_posts": current_week_posts
    }
    
    return result

def log_post(history_file, post_content, post_date=None):
    """Log a new post to the history."""
    history = load_post_history(history_file)
    
    if post_date is None:
        post_date = datetime.now()
    
    new_post = {
        "date": post_date.isoformat(),
        "content_preview": post_content[:100] + "..." if len(post_content) > 100 else post_content,
        "status": "posted"
    }
    
    history["posts"].append(new_post)
    
    if save_post_history(history_file, history):
        print(f"Post logged successfully for {post_date.strftime('%Y-%m-%d')}")
        return True
    else:
        print("Failed to log post")
        return False

def get_recommendation(history_file):
    """Get posting recommendation based on current cadence."""
    cadence = check_posting_cadence(history_file)
    
    today = datetime.now()
    days_left_in_week = 7 - today.weekday()  # Days until Sunday
    
    recommendation = {
        "should_post_today": cadence["posts_needed"] > 0,
        "urgency": "high" if cadence["posts_needed"] >= 2 and days_left_in_week <= 2 else "normal",
        "message": ""
    }
    
    if cadence["meets_requirement"]:
        recommendation["message"] = f"Great! You've posted {cadence['posts_this_week']} times this week. Keep up the momentum!"
    elif cadence["posts_needed"] == 1:
        recommendation["message"] = f"You need 1 more post this week to meet your goal. {days_left_in_week} days left."
    else:
        recommendation["message"] = f"You need {cadence['posts_needed']} more posts this week. {days_left_in_week} days left. Let's catch up!"
    
    return recommendation

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python track_posts.py <command> [args]")
        print("Commands:")
        print("  check <history_file>                  - Check current posting cadence")
        print("  log <history_file> <post_content>     - Log a new post")
        print("  recommend <history_file>              - Get posting recommendation")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "check":
        if len(sys.argv) < 3:
            print("Usage: python track_posts.py check <history_file>")
            sys.exit(1)
        history_file = sys.argv[2]
        result = check_posting_cadence(history_file)
        print(json.dumps(result, indent=2))
    
    elif command == "log":
        if len(sys.argv) < 4:
            print("Usage: python track_posts.py log <history_file> <post_content>")
            sys.exit(1)
        history_file = sys.argv[2]
        post_content = sys.argv[3]
        log_post(history_file, post_content)
    
    elif command == "recommend":
        if len(sys.argv) < 3:
            print("Usage: python track_posts.py recommend <history_file>")
            sys.exit(1)
        history_file = sys.argv[2]
        result = get_recommendation(history_file)
        print(json.dumps(result, indent=2))
    
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)
