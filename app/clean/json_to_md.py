import os
import json
from bs4 import BeautifulSoup


def extract_markdown_from_discourse_json(
    json_dir="app/data/raw/discourse", output_dir="app/data/raw/discourse_md"
):
    os.makedirs(output_dir, exist_ok=True)

    for filename in os.listdir(json_dir):
        if not filename.endswith(".json"):
            continue

        filepath = os.path.join(json_dir, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)

        topic_title = data.get("title", data.get("slug", "Untitled Topic"))
        topic_slug = data.get("slug", "unknown-slug")
        topic_id = data.get("id", "unknown-id")

        base_url = f"https://discourse.onlinedegree.iitm.ac.in/t/{topic_slug}/{topic_id}"
        posts = data.get("post_stream", {}).get("posts", [])

        md_lines = [f"# {topic_title}\n"]

        for post in posts:
            author = post.get("username", "unknown")
            created = post.get("created_at", "")[:10]
            html = post.get("cooked", "")
            text = BeautifulSoup(html, "html.parser").get_text()
            post_number = post.get("post_number", 1)
            post_url = f"{base_url}/{post_number}"

            md_lines.append(
                f"**{author}** on {created}:\n\n{text}\n\n[Source]({post_url})"
            )

        md_filename = filename.replace(".json", ".md")
        output_path = os.path.join(output_dir, md_filename)
        with open(output_path, "w", encoding="utf-8") as out:
            out.write("\n\n---\n\n".join(md_lines))

    print(
        f"✅ Discourse JSON → Markdown with source links saved to: {output_dir}")
