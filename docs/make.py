"""
Build API documentation using pdoc.

This script mirrors the structure used in SQLModel-CRUD-Utilities but delegates to
the repo's run_pdoc.py to ensure Django is correctly configured during import.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]

print("Generating documentation via run_pdoc.py ...")

try:
    result = subprocess.run(
        [sys.executable, str(ROOT / "run_pdoc.py")],
        check=True,
        capture_output=True,
        text=True,
    )
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print("pdoc stderr:")
        print(result.stderr)
    print("Documentation generated successfully (see docs/api/).")
except subprocess.CalledProcessError as e:
    print(f"Error running run_pdoc.py: {e}")
    print("stdout:")
    print(e.stdout)
    print("stderr:")
    print(e.stderr)
    sys.exit(1)

# Post-process HTML: inject top navigation, favicon, and footer across pages.
build_dir = ROOT / "docs" / "api"
if build_dir.exists():
    print("Enhancing generated pages with nav/footer ...")

    head_inject = """
    <!-- custom-head start -->
    <link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Ccircle cx='32' cy='32' r='30' fill='%230a58ca'/%3E%3Ctext x='32' y='38' font-size='28' text-anchor='middle' fill='white' font-family='Arial, sans-serif'%3EA%3C/text%3E%3C/svg%3E" type="image/svg+xml"/>
    <style>
      /* layout + typography */
      nav.pdoc, main.pdoc { max-width: 1100px; margin: 0 auto; padding: 0 16px; }
      main.pdoc { padding-top: 16px; }
      main.pdoc h1 { margin-top: 0.6em; }
      main.pdoc h2, main.pdoc h3 { margin-top: 1.4em; }
      .pdoc-code { border-radius: 6px; }
      pre { padding: 12px 14px; border-radius: 6px; }

      /* custom topbar */
      .topbar { position: sticky; top: 0; z-index: 1000; background:#0a58ca; color:#fff; padding: 8px 12px; box-shadow: 0 2px 4px rgba(0,0,0,.1);}
      .topbar .brand { font-weight: 600; margin-right: 16px; }
      .topbar a { color:#fff; text-decoration:none; margin-right:12px; }
      .topbar a:hover { text-decoration:underline; }
      .topbar .spacer { flex: 1; }
      .topbar .wrap { display:flex; align-items:center; max-width: 1100px; margin: 0 auto; }

      /* search input tweak */
      nav.pdoc input[type="search"] { border-radius: 6px; padding: 6px 10px; border: 1px solid #d0d7de; }

      /* light theme polish */
      @media (prefers-color-scheme: light) {
        body { background: #fafafa; }
        .pdoc-code { background: #f6f8fa; }
      }

      /* dark theme */
      @media (prefers-color-scheme: dark) {
        html, body { background: #0b0d12; color: #e2e6ee; }
        a { color: #8ab4ff; }
        a:hover { color: #a6c8ff; }
        .topbar { background:#0b5ed7; box-shadow: 0 2px 6px rgba(0,0,0,.5); }
        nav.pdoc, main.pdoc { color: #e2e6ee; }
        .pdoc-code, pre { background: #111521; color: #e2e6ee; }
        code { color: #ffd6a5; }
        nav.pdoc input[type="search"] { background: #0f1320; border-color: #263042; color: #e2e6ee; }
      }
    </style>
    <!-- custom-head end -->
    """

    header_html = """
    <!-- custom-nav start -->
    <div class="topbar">
      <div class="wrap">
        <div class="brand">🧠 Reports AI</div>
        <a href="./index.html">Home</a>
        <a href="./usage.html">Guides</a>
        <a href="./configuration.html">Configuration</a>
        <a href="./reports_ai.html">API</a>
        <div class="spacer"></div>
        <a href="https://github.com/fsecada01/reports_ai" target="_blank" rel="noopener">GitHub ↗</a>
      </div>
    </div>
    <!-- custom-nav end -->
    """

    footer_html = """
    <!-- custom-footer start -->
    <footer style="margin-top:32px;padding:16px 12px;border-top:1px solid #eee;">
      <div style="max-width:1100px;margin:0 auto;color:#666;font-size:0.9em;">
        © {year} Reports AI · Built with pdoc · <a href="https://github.com/fsecada01/reports_ai" target="_blank" rel="noopener">GitHub</a>
      </div>
    </footer>
    <!-- custom-footer end -->
    """.format(year=__import__("datetime").datetime.now().year)

    for html_path in build_dir.rglob("*.html"):
        text = html_path.read_text(encoding="utf-8")

        if "<!-- custom-head start -->" not in text:
            text = re.sub(r"(<head[^>]*>)", r"\1\n" + head_inject, text, count=1)

        if "<!-- custom-nav start -->" not in text:
            text = re.sub(r"(<body[^>]*>)", r"\1\n" + header_html, text, count=1)

        if "<!-- custom-footer start -->" not in text:
            text = re.sub(r"(</body>)", footer_html + r"\n\1", text, count=1)

        html_path.write_text(text, encoding="utf-8")
    print("Enhancements applied.")
