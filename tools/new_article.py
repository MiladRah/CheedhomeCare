#!/usr/bin/env python3
"""Turn a Word article (.docx) into a post for cheedhomecare.com.

Usage (from the repo root):
    python3 tools/new_article.py path/to/Article.docx [--date YYYY-MM-DD]

Expects the Word file to have:
  * the article title as the first Heading 1 (or the first line),
  * optionally a paragraph starting "Description:" (used for Google and the article lists),
  * section headings as Heading 2.
A closing "Talk to CHEED Home Care" box is dropped, because every article page
already ends with that call-to-action automatically.

Writes _posts/<date>-<slug>.html, plus any images to images/articles/<slug>/.
Requires pandoc.
"""
import datetime, html, os, re, subprocess, sys, tempfile, unicodedata

def slugify(text):
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    text = re.sub(r"[^a-zA-Z0-9\s-]", "", text).strip().lower()
    return re.sub(r"[\s-]+", "-", text)[:70].strip("-")

def plain(fragment):
    return html.unescape(re.sub(r"<[^>]+>", "", fragment)).strip()

def main():
    args = sys.argv[1:]
    if not args:
        sys.exit(__doc__)
    src = args[0]
    date = None
    if "--date" in args:
        date = args[args.index("--date") + 1]
    if not date:
        try:
            from zoneinfo import ZoneInfo
            date = datetime.datetime.now(ZoneInfo("America/Edmonton")).date().isoformat()
        except Exception:
            date = datetime.date.today().isoformat()

    repo = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    media_tmp = tempfile.mkdtemp()
    body = subprocess.run(
        ["pandoc", src, "-t", "html5", "--wrap=none", f"--extract-media={media_tmp}"],
        check=True, capture_output=True, text=True).stdout

    # Title: first <h1>, else first paragraph.
    m = re.search(r"<h1[^>]*>(.*?)</h1>\s*", body, re.S) or re.search(r"<p>(.*?)</p>\s*", body, re.S)
    title = plain(m.group(1))
    body = body[:m.start()] + body[m.end():]

    # Description paragraph.
    description = ""
    d = re.search(r"<p>\s*(?:<strong>)?\s*Description:?\s*(?:</strong>)?\s*(.*?)</p>\s*", body, re.S)
    if d:
        description = plain(d.group(1))
        body = body[:d.start()] + body[d.end():]

    # Drop a closing "Talk to ... Home Care" box (Word table or paragraph).
    body = re.sub(r"<table.*?Talk to .*?</table>\s*", "", body, flags=re.S | re.I)
    body = re.sub(r"<p>\s*<strong>\s*Talk to [^<]*Home Care.*?</p>\s*$", "", body, flags=re.S | re.I)

    # Tidy: empty emphasis left by Word, spaced hyphens used as dashes, pandoc ids.
    body = re.sub(r"<(em|strong)>\s*([.,;:]?)\s*</\1>", r"\2", body)
    body = re.sub(r"(?<=\S) - (?=\S)", " – ", body)
    body = re.sub(r' id="[^"]*"', "", body)
    if not description:
        first_p = re.search(r"<p>(.*?)</p>", body, re.S)
        description = plain(first_p.group(1))[:200] if first_p else title
    description = re.sub(r"(?<=\S) - (?=\S)", " – ", description)

    slug = slugify(title)

    # Images: move into images/articles/<slug>/ and point the post at them.
    for root, _, files in os.walk(media_tmp):
        for f in files:
            dest_dir = os.path.join(repo, "images", "articles", slug)
            os.makedirs(dest_dir, exist_ok=True)
            os.replace(os.path.join(root, f), os.path.join(dest_dir, f))
            body = re.sub(r'src="[^"]*' + re.escape(f) + '"', f'src="/images/articles/{slug}/{f}"', body)
    body = re.sub(r'<img ', '<img loading="lazy" ', body)

    if "{{" in body or "{%" in body:
        body = "{% raw %}\n" + body + "\n{% endraw %}"

    def yq(s):
        return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'

    out = os.path.join(repo, "_posts", f"{date}-{slug}.html")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as fh:
        fh.write(f"---\ntitle: {yq(title)}\ndescription: {yq(description)}\n---\n{body.strip()}\n")
    print(out)
    print(f"URL: https://cheedhomecare.com/articles/{slug}/")

if __name__ == "__main__":
    main()
