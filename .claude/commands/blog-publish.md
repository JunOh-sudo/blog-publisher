---
description: 발행 패키지를 브라우저(Claude in Chrome)로 티스토리·네이버 에디터에 올려 비공개 저장한다. 변호사 PC의 Claude Code에서 실행
argument-hint: <패키지 폴더, 예: posts_tistory/2026-09-24-limited-acceptance-guide>
---
publisher 에이전트의 규칙에 따라 `$ARGUMENTS` 패키지를 에디터에 올려 주세요. 브라우저 조작은 Claude in Chrome(사람이 로그인한 Chrome)을 사용합니다.

## 원칙
- **비공개 저장까지만** 합니다. 공개 전환은 제가(변호사) 합니다.
- 카카오·네이버 로그인, 2단계 인증은 제가 직접 합니다. 계정 정보를 묻거나 입력하지 마세요.
- 각 단계를 마치면 무엇을 했는지 한 줄로 보고하고, 다음 단계로 넘어가기 전에 확인받으세요.
- 새 탭에서 작업하고, 이미 열려 있는 제 탭은 건드리지 마세요.

## 티스토리 (posts_tistory/...)
1. `https://ohbhs.tistory.com/manage/newpost` 열기 → 로그인 화면이면 멈추고 제게 로그인 요청
2. 제목: 패키지 `meta.md`의 1순위 제목
3. 에디터 모드를 **HTML**로 전환 → `post.html` 내용 전체를 붙여넣기
4. 이미지: 기본 모드로 돌아가 `images/`의 파일을 업로드하고, 본문의 `{{IMAGE_N}}` 자리(또는 `[이미지 N 삽입]` 표시)를 해당 이미지로 교체. 이미지마다 대체텍스트 입력(meta.md 표). 삽화 캡션이 있으면 입력
   - Supabase URL이 이미 치환된 post.html이면 이 단계는 확인만
5. 카테고리, 태그 10개(meta.md), 대표 이미지 = `*-thumbnail.png`
6. 공개 설정 **비공개** → 저장. 미리보기 URL을 알려 주세요
7. `marketing-team/data/published_posts.csv`에 status=private, URL 기록

## 네이버 (posts_naver/...)
1. `https://blog.naver.com/ohjunsung_law/postwrite` 열기 → 로그인 필요 시 멈추고 요청
2. 제목 입력 → `body_paste.html`을 새 탭에서 열어 본문을 복사해 에디터에 붙여넣기
3. `[이미지 N 삽입: 파일명]` 줄마다 [사진]으로 해당 파일 업로드 후 그 줄 삭제, 대체텍스트·캡션 입력
4. 대표 사진 = `*-thumbnail.png`, 카테고리, 해시태그(meta.md)
5. 공개 설정 **비공개** → 발행. URL을 알려 주세요
6. `published_posts.csv` 기록

## 마지막 보고
- 비공개 글 URL, 넣은 이미지 수, 대체텍스트 입력 여부
- 패키지 `README.md`의 "에디터에서 꼭 확인할 문장" 목록 다시 보여주기
- 제가 공개 전환 후 URL을 알려 주면 `/blog-index` 진행
