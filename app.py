"""
LegalBlog Auto Publisher - Streamlit Web App
법무법인 강호 블로그 자동 발행 시스템

Usage:
    streamlit run app.py
"""

import streamlit as st
import anthropic
import openai
import base64
import json
import os
import re
import io
import zipfile
from datetime import datetime, date

# ============================================================
# Page Config
# ============================================================
st.set_page_config(
    page_title="LegalBlog Publisher",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# Sidebar - API Keys & Settings
# ============================================================
with st.sidebar:
    st.title("⚖️ LegalBlog Publisher")
    st.caption("법무법인 강호 블로그 자동 발행")
    st.divider()

    # API Keys (stored in session or secrets)
    st.subheader("🔑 API Keys")

    anthropic_key = st.text_input(
        "Anthropic API Key",
        value=st.session_state.get("anthropic_key", os.environ.get("ANTHROPIC_API_KEY", "")),
        type="password",
        help="Claude API key for content generation",
    )
    if anthropic_key:
        st.session_state["anthropic_key"] = anthropic_key

    openai_key = st.text_input(
        "OpenAI API Key",
        value=st.session_state.get("openai_key", os.environ.get("OPENAI_API_KEY", "")),
        type="password",
        help="OpenAI API key for image generation (gpt-image-2)",
    )
    if openai_key:
        st.session_state["openai_key"] = openai_key

    supabase_url = st.text_input(
        "Supabase URL",
        value=st.session_state.get("supabase_url", os.environ.get("SUPABASE_URL", "")),
        help="Supabase project URL",
    )
    if supabase_url:
        st.session_state["supabase_url"] = supabase_url

    supabase_key = st.text_input(
        "Supabase Anon Key",
        value=st.session_state.get("supabase_key", os.environ.get("SUPABASE_ANON_KEY", "")),
        type="password",
    )
    if supabase_key:
        st.session_state["supabase_key"] = supabase_key

    st.divider()

    # Settings
    st.subheader("⚙️ Settings")
    platform = st.selectbox("Blog Platform", ["Tistory", "Naver"])
    publish_date = st.date_input("Publish Date", value=date.today())
    date_str = publish_date.strftime("%Y-%m-%d")

    st.divider()
    st.caption("v1.0 | 법무법인 강호")


# ============================================================
# Helper Functions
# ============================================================
def get_claude_client():
    key = st.session_state.get("anthropic_key", "")
    if not key:
        st.error("Anthropic API Key를 입력하세요.")
        return None
    return anthropic.Anthropic(api_key=key)


def get_openai_client():
    key = st.session_state.get("openai_key", "")
    if not key:
        st.error("OpenAI API Key를 입력하세요.")
        return None
    return openai.OpenAI(api_key=key)


def generate_titles(client, topic: str, field: str) -> list:
    """Generate 5 SEO-optimized blog titles."""
    prompt = f"""당신은 대한민국 법률 블로그 SEO 전문가입니다.

[분야] {field}
[글감] {topic}

위 글감으로 티스토리 법률 블로그에 발행할 SEO 최적화 제목 5개를 추천해주세요.

규칙:
1. 각 제목은 | 기호로 부제목을 구분
2. 핵심 키워드를 앞부분에 배치
3. 의뢰인(일반인)이 실제로 검색할 만한 문구 포함
4. 30~50자 내외

JSON 형식으로만 응답하세요:
{{"titles": ["제목1", "제목2", "제목3", "제목4", "제목5"]}}"""

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1000,
        messages=[{"role": "user", "content": prompt}],
    )

    text = response.content[0].text
    # Extract JSON from response
    json_match = re.search(r'\{.*\}', text, re.DOTALL)
    if json_match:
        data = json.loads(json_match.group())
        return data.get("titles", [])
    return []


def generate_content(client, topic: str, title: str, field: str, platform: str) -> dict:
    """Generate blog post HTML and meta.md."""

    if platform == "Tistory":
        consult_link = "https://m.expert.naver.com/mobile/expert/product/detail?storeId=100028074&productId=100149275"
        hashtag_instruction = "해시태그 미포함 (티스토리)"
    else:
        consult_link = "https://m.expert.naver.com/mobile/expert/product/detail?storeId=100028074&productId=100058152"
        hashtag_instruction = "해시태그 30개 포함 (네이버)"

    prompt = f"""당신은 법무법인 강호 오준성 변호사의 법률 블로그 작성 AI입니다.

[분야] {field}
[주제] {topic}
[제목] {title}
[플랫폼] {platform}

다음 두 파일을 생성해주세요.

=== post.html ===
규칙:
1. 도입부: "안녕하세요. 법무법인 강호 오준성 변호사입니다." 로 시작
2. 본문: h2 소제목 6~8개, 각 섹션에 상세한 법리 설명
3. 이미지: 4개의 플레이스홀더 {{{{IMAGE_1}}}}~{{{{IMAGE_4}}}} 를 적절한 섹션에 배치
4. 표: 비교표, 요약표 적극 활용
5. 상담 링크: {consult_link}
6. 면책 공고 포함
7. {hashtag_instruction}
8. 팝업 상담 유도창 포함 (30초 후 자동, F9 단축키, 드래그 가능)
9. 태그에 "상속전문변호사" 절대 미포함
10. 태그 10개 (항상 "오준성변호사", "법무법인강호" 포함)

=== meta.md ===
규칙:
1. 제목, 카테고리, 태그 10개
2. DALL-E 이미지 프롬프트 5개 (thumbnail + image_1~4)
3. 프롬프트: 영문, "No text" 필수, professional legal blog style

응답 형식 (반드시 이 구분자를 사용):
---POST_HTML_START---
(post.html 내용)
---POST_HTML_END---
---META_MD_START---
(meta.md 내용)
---META_MD_END---"""

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=8000,
        messages=[{"role": "user", "content": prompt}],
    )

    text = response.content[0].text

    # Parse response
    post_match = re.search(r'---POST_HTML_START---(.*?)---POST_HTML_END---', text, re.DOTALL)
    meta_match = re.search(r'---META_MD_START---(.*?)---META_MD_END---', text, re.DOTALL)

    result = {}
    if post_match:
        result["post_html"] = post_match.group(1).strip()
    if meta_match:
        result["meta_md"] = meta_match.group(1).strip()

    return result


MAX_IMAGE_SLOTS = 6


def parse_image_prompts(meta_md: str) -> dict:
    """Extract DALL-E prompts from meta.md content."""
    prompts = {}
    blocks = re.split(r"###\s+", meta_md)
    for block in blocks:
        block = block.strip()
        if not block:
            continue
        lines = block.split("\n", 1)
        header = lines[0].strip().lower()
        prompt_text = lines[1].strip() if len(lines) > 1 else ""
        if not prompt_text:
            continue

        # Slots handled by the local renderer (or not yet filled) carry notes, not prompts
        if any(note in prompt_text for note in ("로컬 렌더", "AI 생성 안 함", "visual-designer가 채움")):
            continue

        if "thumbnail" in header:
            prompts["thumbnail.png"] = prompt_text
            continue
        for i in range(1, MAX_IMAGE_SLOTS + 1):
            if f"image_{i}" in header or (str(i) in header and ("png" in header or "섹션" in header or "section" in header)):
                prompts[f"image_{i}.png"] = prompt_text
                break

    return prompts

def generate_single_image(client, prompt: str) -> bytes:
    """Generate a single image using gpt-image-2."""
    result = client.images.generate(
        model="gpt-image-1",
        prompt=prompt,
        size="1024x1024",
        quality="high",
        n=1,
    )

    image_data = result.data[0]
    if hasattr(image_data, "b64_json") and image_data.b64_json:
        return base64.b64decode(image_data.b64_json)
    elif hasattr(image_data, "url") and image_data.url:
        import urllib.request
        with urllib.request.urlopen(image_data.url) as resp:
            return resp.read()
    return None


def upload_to_supabase(image_bytes: bytes, path: str) -> str:
    """Upload image to Supabase Storage and return public URL."""
    from supabase import create_client

    url = st.session_state.get("supabase_url", "")
    key = st.session_state.get("supabase_key", "")

    if not url or not key:
        return None

    client = create_client(url, key)
    bucket = "blog-images"

    try:
        client.storage.from_(bucket).upload(
            path,
            image_bytes,
            file_options={"content-type": "image/png", "upsert": "true"},
        )
    except Exception:
        # Try upsert on conflict
        client.storage.from_(bucket).update(
            path,
            image_bytes,
            file_options={"content-type": "image/png"},
        )

    public_url = f"{url}/storage/v1/object/public/{bucket}/{path}"
    return public_url


def replace_placeholders(html: str, image_urls: dict) -> str:
    """Replace {{IMAGE_N}} placeholders with actual URLs."""
    for i in range(1, MAX_IMAGE_SLOTS + 1):
        placeholder = f"{{{{IMAGE_{i}}}}}"
        key = f"image_{i}.png"
        if key in image_urls:
            html = html.replace(placeholder, image_urls[key])
    return html


def create_zip(post_html: str, meta_md: str, images: dict) -> bytes:
    """Create a ZIP file with all blog post files."""
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("post.html", post_html)
        zf.writestr("meta.md", meta_md)
        for name, data in images.items():
            zf.writestr(f"images/{name}", data)
    return buf.getvalue()


# ============================================================
# Main App - Step-by-Step Workflow
# ============================================================

# Initialize session state
for key in ["titles", "selected_title", "content", "images", "image_urls", "step"]:
    if key not in st.session_state:
        st.session_state[key] = None

if "step" not in st.session_state or st.session_state["step"] is None:
    st.session_state["step"] = 1

st.title("⚖️ 법률 블로그 자동 발행")

# Progress indicator
steps = ["글감 입력", "제목 선택", "콘텐츠 생성", "이미지 생성", "업로드 & 완료"]
current_step = st.session_state.get("step", 1)

cols = st.columns(len(steps))
for i, (col, step_name) in enumerate(zip(cols, steps), 1):
    if i < current_step:
        col.markdown(f"✅ **{step_name}**")
    elif i == current_step:
        col.markdown(f"🔵 **{step_name}**")
    else:
        col.markdown(f"⬜ {step_name}")

st.divider()

# ============================================================
# Step 1: Topic Input
# ============================================================
if st.session_state["step"] == 1:
    st.header("1️⃣ 글감 입력")

    field = st.selectbox(
        "법률 분야",
        ["상속", "가사(이혼)", "형사", "부동산", "민사", "기타"],
        index=0,
    )

    topic = st.text_area(
        "글감을 입력하세요",
        height=200,
        placeholder="예: 건물주가 사망한 후 유족이 상속포기를 하면 세입자 보증금은 어떻게 되나요?\n\n상담 질문, 판례, 뉴스 기사, 법률신문 칼럼 등을 붙여넣으시면 됩니다.",
    )

    if st.button("📝 제목 5개 생성", type="primary", disabled=not topic):
        client = get_claude_client()
        if client:
            with st.spinner("SEO 최적화 제목을 생성하고 있습니다..."):
                titles = generate_titles(client, topic, field)
                if titles:
                    st.session_state["titles"] = titles
                    st.session_state["topic"] = topic
                    st.session_state["field"] = field
                    st.session_state["step"] = 2
                    st.rerun()
                else:
                    st.error("제목 생성에 실패했습니다. 다시 시도해주세요.")

# ============================================================
# Step 2: Title Selection
# ============================================================
elif st.session_state["step"] == 2:
    st.header("2️⃣ 제목 선택")

    titles = st.session_state.get("titles", [])

    for i, title in enumerate(titles, 1):
        if st.button(f"{i}. {title}", key=f"title_{i}", use_container_width=True):
            st.session_state["selected_title"] = title
            st.session_state["step"] = 3
            st.rerun()

    st.divider()
    if st.button("⬅️ 이전 단계"):
        st.session_state["step"] = 1
        st.rerun()

# ============================================================
# Step 3: Content Generation
# ============================================================
elif st.session_state["step"] == 3:
    st.header("3️⃣ 콘텐츠 생성")
    st.info(f"**선택된 제목:** {st.session_state['selected_title']}")

    if st.session_state.get("content") is None:
        client = get_claude_client()
        if client:
            with st.spinner("블로그 콘텐츠를 생성하고 있습니다... (약 30초)"):
                content = generate_content(
                    client,
                    st.session_state["topic"],
                    st.session_state["selected_title"],
                    st.session_state["field"],
                    platform,
                )
                if content.get("post_html") and content.get("meta_md"):
                    st.session_state["content"] = content
                    st.rerun()
                else:
                    st.error("콘텐츠 생성에 실패했습니다. 다시 시도해주세요.")
                    if st.button("🔄 재시도"):
                        st.rerun()
    else:
        content = st.session_state["content"]

        tab1, tab2 = st.tabs(["📄 post.html 미리보기", "📋 meta.md"])

        with tab1:
            st.components.v1.html(content["post_html"], height=600, scrolling=True)

        with tab2:
            st.code(content["meta_md"], language="markdown")

        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("⬅️ 이전 단계"):
                st.session_state["content"] = None
                st.session_state["step"] = 2
                st.rerun()
        with col2:
            if st.button("🔄 재생성"):
                st.session_state["content"] = None
                st.rerun()
        with col3:
            if st.button("🎨 이미지 생성으로", type="primary"):
                st.session_state["step"] = 4
                st.rerun()

# ============================================================
# Step 4: Image Generation
# ============================================================
elif st.session_state["step"] == 4:
    st.header("4️⃣ 이미지 생성 (gpt-image-2)")

    content = st.session_state.get("content", {})
    meta_md = content.get("meta_md", "")

    prompts = parse_image_prompts(meta_md)

    if not prompts:
        st.error("meta.md에서 이미지 프롬프트를 찾을 수 없습니다.")
    else:
        st.write(f"총 **{len(prompts)}개** 이미지를 생성합니다.")

        if st.session_state.get("images") is None:
            if st.button("🎨 이미지 생성 시작", type="primary"):
                oi_client = get_openai_client()
                if oi_client:
                    images = {}
                    image_names = ["thumbnail.png"] + [f"image_{i}.png" for i in range(1, MAX_IMAGE_SLOTS + 1)]

                    progress = st.progress(0)
                    status = st.empty()

                    todo = [name for name in image_names if name in prompts]
                    for idx, name in enumerate(todo):
                        status.text(f"Generating {name}... ({idx+1}/{len(todo)})")
                        try:
                            img_bytes = generate_single_image(oi_client, prompts[name])
                            if img_bytes:
                                images[name] = img_bytes
                        except Exception as e:
                            st.warning(f"{name} 생성 실패: {e}")

                        progress.progress((idx + 1) / len(todo))

                    status.text("Complete!")
                    st.session_state["images"] = images
                    st.rerun()
        else:
            images = st.session_state["images"]
            st.success(f"✅ {len(images)}개 이미지 생성 완료")

            # Display images in grid
            cols = st.columns(min(len(images), 3)) if len(images) > 0 else []
            for idx, (name, data) in enumerate(images.items()):
                with cols[idx % 3]:
                    st.image(data, caption=name, use_container_width=True)

            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("⬅️ 이전 단계"):
                    st.session_state["images"] = None
                    st.session_state["step"] = 3
                    st.rerun()
            with col2:
                if st.button("🔄 이미지 재생성"):
                    st.session_state["images"] = None
                    st.rerun()
            with col3:
                if st.button("☁️ 업로드 & 완료", type="primary"):
                    st.session_state["step"] = 5
                    st.rerun()

# ============================================================
# Step 5: Upload & Finalize
# ============================================================
elif st.session_state["step"] == 5:
    st.header("5️⃣ 업로드 & 완료")

    content = st.session_state.get("content", {})
    images = st.session_state.get("images", {})

    # Upload to Supabase
    supabase_ok = st.session_state.get("supabase_url") and st.session_state.get("supabase_key")

    if supabase_ok:
        if st.session_state.get("image_urls") is None:
            with st.spinner("Supabase에 이미지를 업로드하고 있습니다..."):
                image_urls = {}
                for name, data in images.items():
                    path = f"{date_str}/{name}"
                    try:
                        url = upload_to_supabase(data, path)
                        if url:
                            image_urls[name] = url
                    except Exception as e:
                        st.warning(f"{name} 업로드 실패: {e}")

                st.session_state["image_urls"] = image_urls

        image_urls = st.session_state.get("image_urls", {})

        if image_urls:
            st.success(f"✅ Supabase 업로드 완료 ({len(image_urls)}개)")

            # Replace placeholders
            final_html = replace_placeholders(content["post_html"], image_urls)
        else:
            final_html = content["post_html"]
    else:
        st.warning("Supabase 설정이 없어 업로드를 건너뜁니다. 파일을 다운로드하여 수동으로 처리하세요.")
        final_html = content["post_html"]
        image_urls = {}

    st.divider()

    # Preview final HTML
    with st.expander("📄 최종 post.html 미리보기", expanded=False):
        st.components.v1.html(final_html, height=400, scrolling=True)

    st.divider()

    # Download options
    st.subheader("📥 다운로드")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.download_button(
            label="📄 post.html",
            data=final_html,
            file_name=f"{date_str}-post.html",
            mime="text/html",
        )

    with col2:
        st.download_button(
            label="📋 meta.md",
            data=content.get("meta_md", ""),
            file_name=f"{date_str}-meta.md",
            mime="text/markdown",
        )

    with col3:
        zip_data = create_zip(final_html, content.get("meta_md", ""), images)
        st.download_button(
            label="📦 전체 ZIP",
            data=zip_data,
            file_name=f"{date_str}-blog-package.zip",
            mime="application/zip",
        )

    st.divider()

    # Claude Code command
    st.subheader("🚀 Claude Code 발행 명령어")

    folder_prefix = "posts_tistory" if platform == "Tistory" else "posts_naver"
    claude_cmd = f"""{folder_prefix}/{date_str}/ 폴더의 글을 {'티스토리' if platform == 'Tistory' else '네이버'}에 비공개 발행해줘.
각 단계마다 나에게 확인받고 진행해.

폴더에는 post.html과 meta.md 두 파일이 있어.
- meta.md에서 제목, 카테고리, 태그를 읽어서 적용
- post.html을 본문으로 삽입 (setContent + save 필수)
- images/thumbnail.png를 대표 이미지로 지정

Supabase 업로드 경로는 blog-images/{date_str}/ 로 사용해줘."""

    st.code(claude_cmd, language=None)
    st.caption("위 명령어를 Claude Code에 붙여넣으세요. 카카오 로그인만 직접 수행합니다.")

    st.divider()

    # Post-publish checklist
    st.subheader("✅ 발행 후 체크리스트")
    st.checkbox("비공개 글 미리보기 검수")
    st.checkbox("법리·판례 정확성 확인")
    st.checkbox("이미지 4장 정상 표시 확인")
    st.checkbox("공개 전환")
    st.checkbox("index_queue.md에 URL 추가")

    st.divider()

    # Reset
    if st.button("🔄 새 글 작성", type="primary"):
        for key in ["titles", "selected_title", "content", "images", "image_urls", "step"]:
            st.session_state[key] = None
        st.session_state["step"] = 1
        st.rerun()
