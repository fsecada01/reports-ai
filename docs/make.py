"""
Build API documentation using pdoc, then enhance navigation/branding.

This script delegates API generation to run_pdoc.py (so django.setup() runs),
then ensures Markdown guides are present and styled consistently. Finally, it
adds a simple top bar and validates the output for CI.
"""

from __future__ import annotations

import os
import re
import subprocess
import sys
from pathlib import Path

try:
    import markdown as md
except Exception:  # pragma: no cover
    md = None  # type: ignore


ROOT = Path(__file__).resolve().parents[1]
BUILD_DIR = ROOT / "docs" / "api"


def run_pdoc_api() -> None:
    print("Generating documentation via run_pdoc.py ...")
    try:
        res = subprocess.run(
            [sys.executable, str(ROOT / "run_pdoc.py")],
            check=True,
            capture_output=True,
            text=True,
        )
        if res.stdout:
            print(res.stdout)
        print("Documentation generated successfully (see docs/api/).")
    except subprocess.CalledProcessError as e:  # pragma: no cover
        print(f"Error running run_pdoc.py: {e}")
        print("stdout:\n" + (e.stdout or ""))
        print("stderr:\n" + (e.stderr or ""))
        sys.exit(1)


def extract_pdoc_shell(api_html: Path) -> tuple[str, str, str]:
    head_html = nav_html = tail_js = ""
    if api_html.exists():
        txt = api_html.read_text(encoding="utf-8", errors="ignore")
        m_head = re.search(r"<head>([\s\S]*?)</head>", txt)
        if m_head:
            head_html = m_head.group(1)
        m_nav = re.search(r"(<nav class=\"pdoc\"[\s\S]*?</nav>)", txt)
        if m_nav:
            nav_html = m_nav.group(1)
        m_tail = re.search(r"(<script[\s\S]*?</script>)[\s\S]*?</body>", txt)
        if m_tail:
            tail_js = m_tail.group(1)
    return head_html, nav_html, tail_js


def render_markdown(
    src: Path,
    dst: Path,
    title: str,
    head: str,
    nav: str,
    tail: str,
    force: bool,
) -> None:
    if not src.exists():
        return
    if dst.exists() and not force:
        return
    if md is None:
        raise RuntimeError(
            "markdown package not available; run `uv sync --extra doc`."
        )
    body_html = md.markdown(
        src.read_text(encoding="utf-8"),
        extensions=["fenced_code", "tables", "toc"],
    )
    head = head or f'<meta charset="utf-8"><title>{title}</title>'
    doc = (
        f'<!doctype html>\n<html lang="en">\n<head>{head}</head>\n<body>\n'
        f'{nav}\n<main class="pdoc">\n{body_html}\n</main>\n{tail}\n'
        f"</body>\n</html>\n"
    )
    dst.write_text(doc, encoding="utf-8")


def inject_branding() -> (  # noqa: C901 - keep logic centralized; template override planned
    None
):
    head_inject = (
        """
    <!-- custom-head start -->
    <link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Ccircle cx='32' cy='32' r='30' fill='%230a58ca'/%3E%3Ctext x='32' y='38' font-size='28' text-anchor='middle' fill='white' font-family='Arial, sans-serif'%3EA%3C/text%3E%3C/svg%3E" type="image/svg+xml"/>
    <style>
      /* custom topbar */
      .topbar { position: sticky; top: 0; z-index: 1000; background:#0a58ca; color:#fff; padding: 8px 12px; box-shadow: 0 2px 4px rgba(0,0,0,.1);}
      .topbar .brand { font-weight: 600; margin-right: 16px; }
      .topbar a { color:#fff; text-decoration:none; margin-right:12px; }
      .topbar a:hover { text-decoration:underline; }
      .topbar .spacer { flex: 1; }
      .topbar .wrap { display:flex; align-items:center; max-width: 1100px; margin: 0 auto; }
      main.pdoc { padding-top: 8px; }
    </style>
    <!-- custom-head end -->
    """
    ).strip()

    def header(prefix: str) -> str:
        return f"""<!-- custom-nav start -->
    <div class=\"topbar\">
      <div class=\"wrap\">
        <div class=\"brand\">🧠 Reports AI</div>
        <a href=\"{prefix}index.html\">Home</a>
        <a href=\"{prefix}usage.html\">Guides</a>
        <a href=\"{prefix}configuration.html\">Configuration</a>
        <a href=\"{prefix}reports_ai.html\">API</a>
        <div class=\"spacer\"></div>
        <a href=\"https://github.com/fsecada01/reports_ai\" target=\"_blank\" rel=\"noopener\">GitHub ↗</a>
      </div>
    </div>
    <!-- custom-nav end -->"""

    footer_html = (
        """
    <!-- custom-footer start -->
    <footer style="margin-top:32px;padding:16px 12px;border-top:1px solid #eee;">
      <div style="max-width:1100px;margin:0 auto;color:#666;font-size:0.9em;">
        © {year} Reports AI · Built with pdoc · <a href="https://github.com/fsecada01/reports_ai" target="_blank" rel="noopener">GitHub</a>
      </div>
    </footer>
    <!-- custom-footer end -->
    """
    ).format(year=__import__("datetime").datetime.now().year)

    # Build a nested API tree for sidebar augmentation
    def build_api_tree() -> dict:
        root: dict = {}
        for p in sorted(BUILD_DIR.rglob("reports_ai/**/*.html")):
            rel = p.relative_to(BUILD_DIR).as_posix()
            if rel == "reports_ai.html":
                continue
            parts = rel.split(
                "/"
            )  # e.g., [reports_ai, services, git_service.html]
            # drop the top-level package name
            parts = parts[1:]
            node = root
            for i, part in enumerate(parts):
                if i == len(parts) - 1:
                    node.setdefault("__files__", []).append((rel, part))
                else:
                    node = node.setdefault(part, {})
        return root

    def render_tree(node: dict, prefix: str) -> str:
        html = ["<ul>"]
        # render subfolders first
        for key in sorted(k for k in node.keys() if k != "__files__"):
            html.append(f"<li>{key}{render_tree(node[key], prefix)}</li>")
        # render files
        for href, name in sorted(node.get("__files__", []), key=lambda x: x[0]):
            label = name.replace(".html", "")
            html.append(f'<li><a href="{prefix}{href}">{label}</a></li>')
        html.append("</ul>")
        return "".join(html)

    api_tree = build_api_tree()

    for html_path in BUILD_DIR.rglob("*.html"):
        text = html_path.read_text(encoding="utf-8")

        if "<!-- custom-head start -->" not in text:
            text = re.sub(r"</head>", head_inject + "\n</head>", text, count=1)

        # Compute prefix back to site root
        rel = os.path.relpath(BUILD_DIR, html_path.parent).replace("\\", "/")
        prefix = "" if rel == "." else rel.rstrip("/") + "/"

        # Add sidebar links to docs
        if "custom-sidenav start" not in text and '<nav class="pdoc"' in text:
            api_modules_section = (
                '<div class="pdoc-topic"><h3>API Modules</h3>'
                + render_tree(api_tree, prefix)
                + "</div>"
                if api_tree
                else ""
            )
            sidenav = f"""
            <!-- custom-sidenav start -->
            <div class=\"pdoc-topic\">
              <h3>Docs</h3>
              <ul>
                <li><a href=\"{prefix}index.html\">Home</a></li>
                <li><a href=\"{prefix}usage.html\">Guides</a></li>
                <li><a href=\"{prefix}configuration.html\">Configuration</a></li>
                <li><a href=\"{prefix}reports_ai.html\">API</a></li>
              </ul>
            </div>
            {api_modules_section}
            <!-- custom-sidenav end -->
            """
            text = re.sub(r"</nav>", sidenav + "\n</nav>", text, count=1)

        if "<!-- custom-nav start -->" not in text:
            text = re.sub(
                r"(<body[^>]*>)", r"\1\n" + header(prefix), text, count=1
            )

        if "<!-- custom-footer start -->" not in text:
            text = re.sub(r"(</body>)", footer_html + r"\n\1", text, count=1)

        html_path.write_text(text, encoding="utf-8")


def validate_site() -> None:
    print("Validating generated site contents ...")
    required = [
        (BUILD_DIR / "index.html", "Homepage (index.html)"),
        (BUILD_DIR / "reports_ai.html", "API page"),
        (BUILD_DIR / "usage.html", "Usage guide"),
        (BUILD_DIR / "configuration.html", "Configuration guide"),
    ]
    missing = [(str(p), label) for p, label in required if not p.exists()]

    def looks_like_html(p: Path) -> bool:
        try:
            t = p.read_text(encoding="utf-8", errors="ignore").lower()
            return "<html" in t and "</html>" in t
        except Exception:
            return False

    invalid = [
        (str(p), label)
        for p, label in required
        if p.exists() and not looks_like_html(p)
    ]

    print("\nGenerated files under docs/api:")
    for p in sorted(BUILD_DIR.rglob("*")):
        if p.is_file():
            print(
                f" - {p.relative_to(BUILD_DIR).as_posix()} ({p.stat().st_size} bytes)"
            )

    if missing or invalid:
        if missing:
            print("\nERROR: Missing required pages:")
            for path, label in missing:
                print(f" - {label}: {path}")
        if invalid:
            print("\nERROR: Invalid HTML detected in:")
            for path, label in invalid:
                print(f" - {label}: {path}")
        sys.exit(1)
    print("Validation passed: required pages present.")


def main() -> None:
    run_pdoc_api()

    BUILD_DIR.mkdir(parents=True, exist_ok=True)
    head, nav, tail = extract_pdoc_shell(BUILD_DIR / "reports_ai.html")

    # Always re-generate homepage from README to make it the landing page.
    render_markdown(
        ROOT / "README.md",
        BUILD_DIR / "index.html",
        "Reports AI",
        head,
        nav,
        tail,
        True,
    )

    # Ensure Guides and Configuration exist (generate if missing).
    render_markdown(
        ROOT / "docs" / "usage.md",
        BUILD_DIR / "usage.html",
        "Usage",
        head,
        nav,
        tail,
        False,
    )
    render_markdown(
        ROOT / "docs" / "configuration.md",
        BUILD_DIR / "configuration.html",
        "Configuration",
        head,
        nav,
        tail,
        False,
    )

    print("Enhancing generated pages with nav/footer ...")
    inject_branding()
    print("Enhancements applied.")
    validate_site()


if __name__ == "__main__":
    main()
