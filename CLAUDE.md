# LegalBlog Publisher — 오준성 변호사 블로그 마케팅 팀

이 저장소는 법무법인 강호 오준성 변호사의 네이버(blog.naver.com/ohjunsung_law)·티스토리(ohbhs.tistory.com) 블로그 콘텐츠를 기획·제작·발행·측정·사후관리한다.

- `app.py`: Streamlit 제작 엔진 (제목 → 본문 → 이미지 → Supabase 업로드). `streamlit run app.py`
- `marketing-team/`: 전략 문서, 주제 백로그, 성과 데이터, 리포트
- `.claude/agents/`: 에이전트 팀 9명, `.claude/commands/`: `/blog-plan`, `/blog-write`, `/blog-index`, `/blog-report`, `/blog-refresh`

## 팀 운영 원칙 (편집장 = 메인 세션)
1. 기획 → 팩트시트 → 원고 → 이미지(visual-designer) → 검수 → 변호사 승인 → 비공개 발행 → 공개(변호사) → 색인 등록(publisher) → 측정 → 사후관리.
2. 게이트: 팩트시트 `[확인필요]` 0건, 컴플라이언스 🔴 0건, 변호사 승인 없이는 공개 금지.
3. "전문/전문변호사", "최고/1위", 결과 보장 표현 금지. "상속전문변호사" 태그 금지.
4. Google Drive의 실제 사건 서류·의뢰인 자료는 원고에 사용하지 않는다. leads.csv에 개인정보 금지.
5. 네이버·티스토리 원고는 같은 주제라도 각도·문장을 다르게 쓴다.
6. 작업 산출물은 `marketing-team/work/`에, 발행 로그는 `marketing-team/data/published_posts.csv`에 남긴다.

7. 모든 글은 정보 이미지와 삽화를 번갈아 넣는다(삽화 2장 이상). 한글 글자가 들어가는 이미지는 AI 생성 대신 `marketing-team/design/render.py` 템플릿으로 만든다.

자세한 내용: `marketing-team/README.md`
