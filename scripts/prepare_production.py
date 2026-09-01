#!/usr/bin/env python3
"""Build a production-ready static package without mutating the staging source tree."""
from __future__ import annotations
from pathlib import Path
import json, shutil, sys, os

ROOT=Path(__file__).resolve().parents[1]
DEST=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else (ROOT/"dist-production")
KEEP_NOINDEX={"404.html","enquiry-received.html"}
STAGING_ROBOTS='<meta name="robots" content="noindex,nofollow">'
PROD_ROBOTS='<meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1,max-video-preview:-1">'

if DEST.exists(): shutil.rmtree(DEST)
DEST.mkdir(parents=True)

for page in ROOT.glob("*.html"):
    text=page.read_text(encoding="utf-8")
    if page.name not in KEEP_NOINDEX:
        if STAGING_ROBOTS not in text:
            raise SystemExit(f"{page.name}: staging robots marker missing")
        text=text.replace(STAGING_ROBOTS,PROD_ROBOTS,1)
    (DEST/page.name).write_text(text,encoding="utf-8")

for name in ("sitemap.xml",".nojekyll"):
    src=ROOT/name
    if src.exists(): shutil.copy2(src,DEST/name)
shutil.copytree(ROOT/"assets",DEST/"assets")

(DEST/"robots.txt").write_text(
"""User-agent: *
Allow: /

Sitemap: https://zeptologic.com/sitemap.xml
""",encoding="utf-8")

(DEST/".htaccess").write_text(r"""DirectoryIndex index.html
ErrorDocument 404 /404.html

<IfModule mod_rewrite.c>
RewriteEngine On

# Canonicalise direct .html requests while retaining static .html files internally.
RewriteCond %{THE_REQUEST} \s/+index\.html(?:[\s?]) [NC]
RewriteRule ^index\.html$ / [R=301,L]

RewriteCond %{THE_REQUEST} \s/+([^?\s]+)\.html(?:[\s?]) [NC]
RewriteCond %1 !^404$ [NC]
RewriteCond %1 !^enquiry-received$ [NC]
RewriteRule ^(.+)\.html$ /$1/ [R=301,L,NE]

# Resolve canonical extensionless routes to the static HTML file.
RewriteCond %{REQUEST_FILENAME} !-f
RewriteCond %{REQUEST_FILENAME} !-d
RewriteCond %{DOCUMENT_ROOT}/$1.html -f
RewriteRule ^([^/.]+)/?$ $1.html [L]
</IfModule>

<IfModule mod_headers.c>
Header always set X-Content-Type-Options "nosniff"
Header always set Referrer-Policy "strict-origin-when-cross-origin"
Header always set Permissions-Policy "camera=(), microphone=(), geolocation=()"
Header always set X-Frame-Options "SAMEORIGIN"

<FilesMatch "\.(?:png|jpg|jpeg|webp|gif|ico|mp4|webm)$">
Header set Cache-Control "public, max-age=604800"
</FilesMatch>
<FilesMatch "\.(?:css|js)$">
Header set Cache-Control "public, max-age=3600"
</FilesMatch>
</IfModule>
""",encoding="utf-8")

manifest={
  "source_commit":os.environ.get("GITHUB_SHA","local"),
  "canonical_origin":"https://zeptologic.com",
  "indexable_pages":sorted(p.name for p in DEST.glob("*.html") if p.name not in KEEP_NOINDEX),
  "non_indexable_pages":sorted(KEEP_NOINDEX),
  "staging_source_unchanged":True
}
(DEST/"release-manifest.json").write_text(json.dumps(manifest,indent=2)+"\n",encoding="utf-8")
print(f"Production package prepared at {DEST}")
