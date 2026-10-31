"""
블로그 글 → 유튜브 영상 변환 모듈

흐름:
    post.html ─(Claude)→ 장면별 대본(JSON)
             ─(OpenAI TTS)→ 장면별 내레이션 mp3
             ─(Pillow)→ 큰 자막이 들어간 프레임 PNG
             ─(ffmpeg)→ video.mp4 + subtitles.srt

필요 시스템 패키지: ffmpeg, 한글 폰트(fonts-nanum 권장) — packages.txt 참고
"""

import json
import os
import re
import shutil
import subprocess
import tempfile
import textwrap
from dataclasses import dataclass, field
from html import unescape

from PIL import Image, ImageDraw, ImageFilter, ImageFont

# ============================================================
# 영상 포맷
# ============================================================
FORMATS = {
    # 일반 영상(16:9): 자막 80px — 휴대폰 세로 시청에서도 읽히는 크기
    "landscape": {"size": (1920, 1080), "sub_font": 80, "head_font": 64, "wrap": 20, "max_lines": 2},
    # 쇼츠(9:16): 자막 92px
    "shorts": {"size": (1080, 1920), "sub_font": 92, "head_font": 70, "wrap": 11, "max_lines": 3},
}

BRAND_NAVY = (18, 32, 58)
BRAND_GOLD = (212, 175, 55)
SUB_COLOR = (255, 255, 255)
SUB_HIGHLIGHT = (255, 221, 87)

FONT_CANDIDATES = [
    "/usr/share/fonts/truetype/nanum/NanumGothicExtraBold.ttf",
    "/usr/share/fonts/truetype/nanum/NanumSquareEB.ttf",
    "/usr/share/fonts/truetype/nanum/NanumGothicBold.ttf",
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Black.ttc",
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc",
    "/usr/share/fonts/noto-cjk/NotoSansCJK-Bold.ttc",
    "/System/Library/Fonts/AppleSDGothicNeo.ttc",
    "C:/Windows/Fonts/malgunbd.ttf",
    "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",
]


def find_korean_font() -> str:
    env = os.environ.get("VIDEO_FONT_PATH")
    if env and os.path.exists(env):
        return env
    for path in FONT_CANDIDATES:
        if os.path.exists(path):
            return path
    raise RuntimeError(
        "한글 폰트를 찾을 수 없습니다. 'apt install fonts-nanum' 설치 후 다시 시도하거나 "
        "VIDEO_FONT_PATH 환경변수로 폰트 경로를 지정하세요."
    )


def check_ffmpeg():
    if not shutil.which("ffmpeg") or not shutil.which("ffprobe"):
        raise RuntimeError("ffmpeg가 설치되어 있지 않습니다. (packages.txt의 ffmpeg 설치 필요)")


# ============================================================
# 1. 대본 생성 (Claude)
# ============================================================
@dataclass
class Scene:
    heading: str
    narration: str
    image_key: str = ""          # thumbnail.png / image_1.png ... (없으면 단색 배경)
    audio_path: str = ""
    duration: float = 0.0
    cues: list = field(default_factory=list)   # [(start, end, text)]


def html_to_text(html: str) -> str:
    html = re.sub(r"<(script|style)[^>]*>.*?</\1>", "", html, flags=re.DOTALL | re.IGNORECASE)
    html = re.sub(r"<h[1-6][^>]*>", "\n\n## ", html, flags=re.IGNORECASE)
    html = re.sub(r"<(br|/p|/li|/tr|/h[1-6])[^>]*>", "\n", html, flags=re.IGNORECASE)
    text = unescape(re.sub(r"<[^>]+>", " ", html))
    text = re.sub(r"[ \t]+", " ", text)
    return re.sub(r"\n\s*\n+", "\n\n", text).strip()


def generate_video_script(client, post_html: str, title: str, fmt: str = "landscape",
                          style_notes: str = "", model: str = "claude-sonnet-4-20250514") -> dict:
    """블로그 본문으로 장면별 내레이션 대본과 유튜브 메타데이터를 만든다."""
    body = html_to_text(post_html)[:15000]
    if fmt == "shorts":
        length_rule = "전체 내레이션 50~55초 분량(약 300~330자), 장면 4~5개. 첫 장면은 3초 안에 시청자를 붙잡는 질문형 훅."
    else:
        length_rule = "전체 내레이션 4~6분 분량(약 1,300~1,800자), 장면 7~10개."

    prompt = f"""당신은 법무법인 강호 오준성 변호사의 유튜브 영상 대본 작가입니다.
아래 블로그 글을 유튜브 영상용 내레이션 대본으로 바꿔주세요.

[제목] {title}
[채널 스타일 메모] {style_notes or "차분하고 신뢰감 있는 변호사 해설 톤, 쉬운 말로 핵심부터"}

규칙:
1. {length_rule}
2. 첫 장면 내레이션은 "안녕하세요. 법무법인 강호 오준성 변호사입니다."로 시작 (쇼츠는 훅 다음 문장에 짧게)
3. 귀로 듣는 글: 문장은 짧게(한 문장 40자 이내), 표·괄호·기호·영문약어 대신 말로 풀어쓰기, 조문은 "민법 제1019조"처럼 읽기 쉽게
4. 법리는 블로그 내용을 벗어나 새로 지어내지 말 것, 단정적 승소 보장 표현 금지
5. 마지막 장면: 핵심 요약 + "구체적인 사안은 상담을 통해 확인하시기 바랍니다." + 구독·좋아요 요청
6. heading: 화면 상단에 띄울 장면 제목(15자 이내)
7. image: 해당 장면에 어울리는 블로그 이미지 키 — "thumbnail.png", "image_1.png"~"image_4.png" 중 하나
8. 유튜브 제목(60자 이내), 설명(상담 안내·면책 문구 포함), 태그 15개도 작성

JSON으로만 응답:
{{"scenes": [{{"heading": "...", "narration": "...", "image": "image_1.png"}}],
  "youtube": {{"title": "...", "description": "...", "tags": ["..."]}}}}

[블로그 본문]
{body}"""

    resp = client.messages.create(
        model=model,
        max_tokens=8000,
        messages=[{"role": "user", "content": prompt}],
    )
    text = resp.content[0].text
    m = re.search(r"\{.*\}", text, re.DOTALL)
    if not m:
        raise ValueError("대본 JSON을 파싱하지 못했습니다.")
    data = json.loads(m.group())
    if not data.get("scenes"):
        raise ValueError("대본에 장면이 없습니다.")
    return data


# ============================================================
# 2. 내레이션 (OpenAI TTS)
# ============================================================
TTS_VOICES = ["onyx", "echo", "ash", "alloy", "sage", "nova", "shimmer", "coral"]

TTS_INSTRUCTIONS = (
    "한국어 법률 해설 유튜브 내레이션. 신뢰감 있는 30~40대 변호사 목소리로, "
    "또박또박 차분하게, 중요한 법률 용어는 살짝 힘주어 읽으세요."
)


def synthesize_narration(client, text: str, out_path: str, voice: str = "onyx", speed: float = 1.05):
    """gpt-4o-mini-tts 로 음성 생성, 실패하면 tts-1-hd 로 대체."""
    try:
        resp = client.audio.speech.create(
            model="gpt-4o-mini-tts",
            voice=voice,
            input=text,
            instructions=TTS_INSTRUCTIONS,
            response_format="mp3",
        )
    except Exception:
        resp = client.audio.speech.create(
            model="tts-1-hd",
            voice=voice if voice in ("alloy", "echo", "fable", "onyx", "nova", "shimmer") else "onyx",
            input=text,
            speed=speed,
            response_format="mp3",
        )
    with open(out_path, "wb") as f:
        f.write(resp.content)


def audio_duration(path: str) -> float:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path],
        capture_output=True, text=True, check=True,
    )
    return float(out.stdout.strip())


# ============================================================
# 3. 자막 분할 / 타이밍
# ============================================================
def split_subtitles(narration: str, wrap: int, max_lines: int) -> list:
    """내레이션을 화면 한 장에 들어갈 자막 단위로 나눈다 (줄당 wrap 글자, 최대 max_lines 줄)."""
    sentences = [s.strip() for s in re.split(r"(?<=[.?!。])\s+", narration.strip()) if s.strip()]
    chunks = []
    for sent in sentences:
        lines = textwrap.wrap(sent, width=wrap, break_long_words=True, break_on_hyphens=False)
        for i in range(0, len(lines), max_lines):
            chunks.append("\n".join(lines[i:i + max_lines]))
    return chunks


def time_cues(chunks: list, duration: float) -> list:
    """글자 수 비례로 각 자막의 표시 시간을 배분."""
    weights = [max(len(c.replace("\n", "").replace(" ", "")), 1) + 2 for c in chunks]
    total = sum(weights)
    cues, t = [], 0.0
    for c, w in zip(chunks, weights):
        d = duration * w / total
        cues.append((t, t + d, c))
        t += d
    return cues


def to_srt(scenes: list) -> str:
    def ts(sec):
        ms = int(round(sec * 1000))
        h, ms = divmod(ms, 3600000)
        m, ms = divmod(ms, 60000)
        s, ms = divmod(ms, 1000)
        return f"{h:02}:{m:02}:{s:02},{ms:03}"

    out, idx, offset = [], 1, 0.0
    for sc in scenes:
        for start, end, text in sc.cues:
            out.append(f"{idx}\n{ts(offset + start)} --> {ts(offset + end)}\n{text}\n")
            idx += 1
        offset += sc.duration
    return "\n".join(out)


# ============================================================
# 4. 프레임 렌더링 (Pillow)
# ============================================================
def _cover(img: Image.Image, size) -> Image.Image:
    w, h = size
    scale = max(w / img.width, h / img.height)
    img = img.resize((int(img.width * scale) + 1, int(img.height * scale) + 1), Image.LANCZOS)
    left, top = (img.width - w) // 2, (img.height - h) // 2
    return img.crop((left, top, left + w, top + h))


def make_background(size, image_bytes: bytes = None) -> Image.Image:
    w, h = size
    if image_bytes:
        import io
        src = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        if w > h:
            # 가로 영상: 흐린 배경 + 오른쪽 원본
            bg = _cover(src, size).filter(ImageFilter.GaussianBlur(28))
            bg = Image.blend(bg, Image.new("RGB", size, BRAND_NAVY), 0.55)
            side = int(h * 0.62)
            fg = _cover(src, (side, side))
            bg.paste(fg, ((w - side) // 2, int(h * 0.13)))
        else:
            # 쇼츠: 가운데 정사각 이미지
            bg = Image.new("RGB", size, BRAND_NAVY)
            blur = _cover(src, size).filter(ImageFilter.GaussianBlur(30))
            bg = Image.blend(blur, bg, 0.6)
            fg = _cover(src, (w, w))
            bg.paste(fg, (0, int(h * 0.22)))
        return bg
    # 이미지 없을 때: 네이비 그라데이션
    bg = Image.new("RGB", size, BRAND_NAVY)
    d = ImageDraw.Draw(bg)
    for y in range(h):
        k = y / h
        d.line([(0, y), (w, y)], fill=(int(18 + 20 * k), int(32 + 25 * k), int(58 + 40 * k)))
    return bg


def render_frame(bg: Image.Image, heading: str, subtitle: str, fmt: str, font_path: str,
                 channel_label: str = "법무법인 강호 · 오준성 변호사") -> Image.Image:
    cfg = FORMATS[fmt]
    w, h = cfg["size"]
    img = bg.copy().convert("RGBA")
    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)

    head_font = ImageFont.truetype(font_path, cfg["head_font"])
    sub_font = ImageFont.truetype(font_path, cfg["sub_font"])
    label_font = ImageFont.truetype(font_path, int(cfg["head_font"] * 0.5))

    # 상단 제목 바
    pad = int(w * 0.035)
    if heading:
        tb = d.textbbox((0, 0), heading, font=head_font)
        bar_h = (tb[3] - tb[1]) + pad
        top = int(h * 0.055) if fmt == "landscape" else int(h * 0.08)
        d.rectangle([0, top, w, top + bar_h], fill=(*BRAND_NAVY, 230))
        d.rectangle([0, top + bar_h - 8, w, top + bar_h], fill=(*BRAND_GOLD, 255))
        d.text((w // 2, top + bar_h // 2 - 4), heading, font=head_font, fill=BRAND_GOLD, anchor="mm")

    # 채널 라벨 (우상단/하단)
    lb_y = int(h * 0.012) if fmt == "landscape" else int(h * 0.035)
    d.text((w - pad, lb_y), channel_label, font=label_font, fill=(255, 255, 255, 200), anchor="ra")

    # 하단 큰 자막: 반투명 박스 + 외곽선
    if subtitle:
        spacing = int(cfg["sub_font"] * 0.3)
        sb = d.multiline_textbbox((0, 0), subtitle, font=sub_font, spacing=spacing, align="center")
        tw, th = sb[2] - sb[0], sb[3] - sb[1]
        bottom = int(h * 0.92) if fmt == "landscape" else int(h * 0.86)
        box = [(w - tw) // 2 - pad, bottom - th - pad, (w + tw) // 2 + pad, bottom + pad // 2]
        d.rounded_rectangle(box, radius=24, fill=(0, 0, 0, 175))
        d.multiline_text(
            (w // 2, bottom - th // 2 - pad // 4), subtitle, font=sub_font, fill=SUB_COLOR,
            anchor="mm", align="center", spacing=spacing,
            stroke_width=max(4, cfg["sub_font"] // 16), stroke_fill=(0, 0, 0),
        )

    return Image.alpha_composite(img, overlay).convert("RGB")


# ============================================================
# 5. 전체 파이프라인
# ============================================================
def build_video(script: dict, openai_client, images: dict = None, fmt: str = "landscape",
                voice: str = "onyx", out_dir: str = None, progress=None) -> dict:
    """
    script: generate_video_script() 결과
    images: {"image_1.png": bytes, ...} (블로그 이미지, 선택)
    반환: {"video": mp4 경로, "srt": srt 경로, "duration": 초}
    """
    check_ffmpeg()
    font_path = find_korean_font()
    images = images or {}
    cfg = FORMATS[fmt]
    work = out_dir or tempfile.mkdtemp(prefix="blogvideo_")
    os.makedirs(work, exist_ok=True)

    def report(frac, msg):
        if progress:
            progress(frac, msg)

    scenes = [Scene(s.get("heading", ""), s["narration"], s.get("image", "")) for s in script["scenes"]]
    n = len(scenes)

    # 내레이션
    for i, sc in enumerate(scenes):
        report(0.6 * i / n, f"내레이션 생성 중... ({i + 1}/{n})")
        sc.audio_path = os.path.join(work, f"scene_{i:02}.mp3")
        synthesize_narration(openai_client, sc.narration, sc.audio_path, voice=voice)
        sc.duration = audio_duration(sc.audio_path) + 0.35   # 장면 사이 짧은 숨
        chunks = split_subtitles(sc.narration, cfg["wrap"], cfg["max_lines"])
        sc.cues = time_cues(chunks, sc.duration - 0.35)

    # 프레임 렌더링 + concat 목록
    report(0.65, "자막 프레임 렌더링 중...")
    concat_lines, frame_idx, last_frame = [], 0, None
    for i, sc in enumerate(scenes):
        bg = make_background(cfg["size"], images.get(sc.image_key))
        elapsed = 0.0
        for start, end, text in sc.cues:
            frame = os.path.join(work, f"f_{frame_idx:04}.png")
            render_frame(bg, sc.heading, text, fmt, font_path).save(frame)
            concat_lines += [f"file '{frame}'", f"duration {end - start:.3f}"]
            elapsed = end
            frame_idx += 1
            last_frame = frame
        # 장면 끝 숨 고르기 구간 (자막 없이)
        gap = sc.duration - elapsed
        if gap > 0.01:
            frame = os.path.join(work, f"f_{frame_idx:04}.png")
            render_frame(bg, sc.heading, "", fmt, font_path).save(frame)
            concat_lines += [f"file '{frame}'", f"duration {gap:.3f}"]
            frame_idx += 1
            last_frame = frame
    concat_lines.append(f"file '{last_frame}'")   # concat demuxer: 마지막 duration 적용용
    frames_txt = os.path.join(work, "frames.txt")
    with open(frames_txt, "w") as f:
        f.write("\n".join(concat_lines))

    # 오디오 합치기 (장면 사이 0.35초 무음 포함)
    report(0.8, "오디오 합치는 중...")
    silence = os.path.join(work, "silence.mp3")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "lavfi", "-i",
                    "anullsrc=r=24000:cl=mono", "-t", "0.35", "-q:a", "4", silence], check=True)
    audio_txt = os.path.join(work, "audio.txt")
    with open(audio_txt, "w") as f:
        for sc in scenes:
            f.write(f"file '{sc.audio_path}'\nfile '{silence}'\n")
    narration = os.path.join(work, "narration.m4a")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", audio_txt,
                    "-c:a", "aac", "-b:a", "192k", narration], check=True)

    # 영상 인코딩
    report(0.85, "영상 인코딩 중...")
    video = os.path.join(work, "video.mp4")
    subprocess.run([
        "ffmpeg", "-y", "-loglevel", "error",
        "-f", "concat", "-safe", "0", "-i", frames_txt,
        "-i", narration,
        "-vf", "fps=30,format=yuv420p",
        "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-tune", "stillimage",
        "-c:a", "copy", "-shortest", "-movflags", "+faststart", video,
    ], check=True)

    srt = os.path.join(work, "subtitles.srt")
    with open(srt, "w", encoding="utf-8") as f:
        f.write(to_srt(scenes))

    report(1.0, "완료!")
    return {"video": video, "srt": srt, "duration": sum(s.duration for s in scenes), "dir": work}


def youtube_meta_text(script: dict) -> str:
    yt = script.get("youtube", {})
    return (
        f"[제목]\n{yt.get('title', '')}\n\n"
        f"[설명]\n{yt.get('description', '')}\n\n"
        f"[태그]\n{', '.join(yt.get('tags', []))}\n"
    )
