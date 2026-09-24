#!/usr/bin/env python3
"""블로그 정보 이미지 렌더러 (한글 텍스트가 정확해야 하는 이미지용).

사용법:
    python3 marketing-team/design/render.py <spec.json> [출력폴더]

spec.json 예시:
    {"images": [
      {"template": "thumbnail", "file": "thumbnail.png",
       "data": {"pillar": "P3", "tag": "개인회생", "title": "첫 줄\\n둘째 줄", "subtitle": "...", "date": "2026.09"}}
    ]}

템플릿: thumbnail, checklist, compare, steps, illustration (templates/*.html). 결과는 1080x1080 PNG.
폰트(Noto Sans KR, Noto Serif KR)는 처음 실행 시 Google Fonts에서 받아 design/fonts/에 캐시한다.
Chromium 경로는 CHROME 환경변수 > /opt/pw-browsers(headless_shell 우선) > 시스템 chrome/chromium 순으로 찾는다.
일반 Chrome을 쓸 때 하단이 잘리면 chrome-headless-shell을 설치해 CHROME으로 지정한다.
"""
import json, os, re, shutil, subprocess, sys, tempfile, urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
FONT_DIR = HERE / "fonts"
FONT_CSS = "https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@500;800&family=Noto+Serif+KR:wght@700&display=swap"


def ensure_fonts() -> str:
    """Download TTFs once and return @font-face CSS pointing at local files."""
    FONT_DIR.mkdir(exist_ok=True)
    css_path = FONT_DIR / "fonts.css"
    if css_path.exists():
        return css_path.read_text(encoding="utf-8")
    css = urllib.request.urlopen(FONT_CSS, timeout=30).read().decode()
    for url in set(re.findall(r"url\((https://[^)]+\.ttf)\)", css)):
        local = FONT_DIR / url.rsplit("/", 1)[-1]
        if not local.exists():
            tmp = local.with_suffix(".part")
            tmp.write_bytes(urllib.request.urlopen(url, timeout=300).read())
            tmp.rename(local)
        css = css.replace(url, local.as_uri())
    css_path.write_text(css, encoding="utf-8")
    return css


def find_chrome() -> str:
    if os.environ.get("CHROME"):
        return os.environ["CHROME"]
    for pattern in ("chromium_headless_shell-*/chrome-linux/headless_shell", "chromium-*/chrome-linux/chrome"):
        for p in sorted(Path("/opt/pw-browsers").glob(pattern), reverse=True):
            return str(p)
    for name in ("google-chrome", "chromium", "chromium-browser", "chrome"):
        if shutil.which(name):
            return shutil.which(name)
    mac = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    if Path(mac).exists():
        return mac
    sys.exit("Chrome/Chromium을 찾지 못했습니다. CHROME 환경변수로 경로를 지정하세요.")


def render(template: str, data: dict, out: Path, fonts_css: str, chrome: str) -> None:
    base = (HERE / "templates" / "_base.css").read_text(encoding="utf-8")
    body = (HERE / "templates" / f"{template}.html").read_text(encoding="utf-8")
    payload = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    html = (f'<!doctype html><html lang="ko"><head><meta charset="utf-8"><style>{fonts_css}\n{base}</style>'
            f"<script>window.DATA={payload};</script></head><body>{body}</body></html>")
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf-8") as f:
        f.write(html)
        page = Path(f.name)
    try:
        # headless_shell은 창 UI가 없어 뷰포트가 정확히 1080x1080이다. 일반 chrome은 --headless=new 사용.
        mode = [] if "headless_shell" in chrome else ["--headless=new"]
        subprocess.run([chrome, *mode, "--no-sandbox", "--disable-gpu", "--hide-scrollbars",
                        "--allow-file-access-from-files", "--force-device-scale-factor=1",
                        "--window-size=1080,1080", "--virtual-time-budget=4000",
                        f"--screenshot={out}", page.as_uri()],
                       check=True, capture_output=True, timeout=60)
    finally:
        page.unlink(missing_ok=True)


def main() -> None:
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    spec_path = Path(sys.argv[1]).resolve()
    out_dir = Path(sys.argv[2]).resolve() if len(sys.argv) > 2 else spec_path.parent / "images"
    out_dir.mkdir(parents=True, exist_ok=True)
    spec = json.loads(spec_path.read_text(encoding="utf-8"))
    fonts_css, chrome = ensure_fonts(), find_chrome()
    for img in spec["images"]:
        out = out_dir / img["file"]
        render(img["template"], img.get("data", {}), out, fonts_css, chrome)
        print(f"rendered {out}")


if __name__ == "__main__":
    main()
