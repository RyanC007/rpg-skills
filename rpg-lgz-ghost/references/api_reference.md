# Rpg Lgz Ghost — Content & Publishing API Reference

**Version:** 1.0
**Last Updated:** March 18, 2026

---

## 1. Overview

Ghost is responsible for content creation and publishing. While content generation is handled via LLM prompts, publishing is executed via the WordPress REST API.

---

## 2. WordPress REST API

Ghost uses the WordPress REST API to publish approved blog posts directly to the Logoclothz website.

### 2.1. Authentication
Authentication is handled via WordPress Application Passwords.
- **Header:** `Authorization: Basic {base64_encoded_username_and_password}`

### 2.2. Create a Post
- **Endpoint:** `POST /wp-json/wp/v2/posts`
- **Purpose:** Create a new blog post (defaults to draft status).
- **Example Payload:**
  ```json
  {
    "title": "Why Custom Uniforms Matter for Your Team",
    "content": "<!-- wp:paragraph --><p>Full HTML content here...</p><!-- /wp:paragraph -->",
    "status": "draft",
    "categories": [3, 5],
    "tags": [12, 15],
    "meta": {
        "_yoast_wpseo_title": "Why Custom Uniforms Matter | Logoclothz",
        "_yoast_wpseo_metadesc": "Learn why custom uniforms are essential for team unity. All our apparel is cut sewn and printed in the USA."
    }
  }
  ```
- **Example Request:**
  ```bash
  curl -X POST "https://logoclothz.com/wp-json/wp/v2/posts" \
    -H "Authorization: Basic YOUR_BASE64_CREDENTIALS" \
    -H "Content-Type: application/json" \
    -d '{"title":"Test Post","content":"Content here","status":"draft"}'
  ```

### 2.3. Upload Media (Images)
- **Endpoint:** `POST /wp-json/wp/v2/media`
- **Purpose:** Upload featured images or inline images for blog posts.
- **Headers:**
  - `Content-Disposition: attachment; filename="image.jpg"`
  - `Content-Type: image/jpeg`
