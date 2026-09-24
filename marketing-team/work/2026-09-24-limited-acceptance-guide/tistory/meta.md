# meta.md — T005 한정승인 가이드 (티스토리 ohbhs.tistory.com)

- 작성일: 2026-09-24 / 최종 업데이트 표기: 2026.09.24
- 기둥: P1 상속 채무
- 상태: **원고 초안 (verification.md 판정 전, 공개 금지)** — 법적 문장마다 `<!-- V# -->` 주석으로 확인표 행 번호 연결

## 제목

한정승인 절차·비용·기간 완벽 가이드 | 재산목록 작성법

### 제목 후보 (변호사 선택)
1. (기본) 한정승인 절차·비용·기간 완벽 가이드 | 재산목록 작성법
2. ('비용' 제외) 한정승인 절차·기간 총정리 | 재산목록 작성법과 주의할 행동
3. ('비용' 제외) 한정승인 신청 방법과 기간 | 안심상속으로 재산목록 만들기
4. ('비용' 제외, '완벽' 제외) 한정승인 절차·기간 가이드 | 재산목록 작성법

> 참고: 본문의 비용 내용은 "인지대·송달료가 있고 상속인 수에 따라 달라진다"(verification.md 2절 허용 문구)와 세금 검토 필요(V17)뿐입니다. 금액이 없어 제목의 '비용'이 기대보다 약할 수 있으므로 2~4번 안을 권합니다. '완벽'은 금지어는 아니지만 과장으로 읽힐 수 있어 4번 안도 함께 둡니다.

## 카테고리

상속

## 태그 (10개)

오준성변호사, 법무법인강호, 한정승인, 한정승인절차, 한정승인기간, 상속재산목록, 특별한정승인, 안심상속원스톱서비스, 상속포기, 상속채무

(해시태그 없음 / '전문'·'상속전문변호사' 미사용)

## 발행 설정

- 공개 설정: 비공개 (변호사 승인 후 공개)
- 저작물사용허가: 표시 / 상업적 이용: 아니요 / 콘텐츠변경: 아니요
- 상담 링크: https://m.expert.naver.com/mobile/expert/product/detail?storeId=100028074&productId=100149275
- 광고책임변호사: 오준성 (법무법인 강호) — 본문 하단 표기 완료

## 내부링크 (자리만 표시)

티스토리 발행 URL이 아직 없어 본문에 주석으로만 자리를 두었습니다. URL 확정 후 교체.
- 허브 후보: 상속포기 기간 (2절 끝)
- 관련: 특별한정승인 (3절 끝), 상속재산파산 (7절 중간)
- 하단 "함께 읽으면 좋은 글" 자리 (마무리 문단 아래)

## 이미지 배치 (이미지 프롬프트·제작은 visual-designer가 채움)

| 자리 | 위치 | 종류 | 의도 |
|---|---|---|---|
| thumbnail | 본문 미포함(에디터 첨부 후 "대표" 지정) | thumbnail 템플릿 | 제목 2~3줄 + 부제 1줄 |
| {{IMAGE_1}} | 도입부 직후 | 삽화 | 장례 후 쌓인 우편물을 차분히 분류하는 손 |
| {{IMAGE_2}} | 2절 비교표 바로 아래 | 정보(compare) | 한정승인 vs 상속포기 표 4행 그대로 |
| {{IMAGE_3}} | 4절 끝 | 삽화 | 정돈된 집 현관의 열쇠, 아침 햇살(손대지 않고 그대로 두기) |
| {{IMAGE_4}} | 6절 절차표 아래 | 정보(steps) | 절차표 6단계를 5단계로 압축(기간 연장은 선택 단계) |
| {{IMAGE_5}} | 7절 끝, FAQ 앞 | 삽화 (h2 8개라 추가) | 달력에 표시한 날짜, 차 한 잔, 정리된 서류철 |

> (갱신 2026.09.24 visual-designer) 현재 app.py `MAX_IMAGE_SLOTS = 6`이라 `replace_placeholders()`가 {{IMAGE_5}}까지 치환합니다. post.html 311행 주석의 'IMAGE_1~4만 치환' 문구는 옛 내용입니다.
> 주의: app.py `parse_image_prompts()`는 아래 `###` 블록 본문을 프롬프트로 읽습니다. 아래 '이미지 프롬프트' 절이 채워져 image_1·3·5 세 개만 프롬프트로 인식됩니다(파서로 확인).

## 이미지 제작 안내 (visual-designer, 2026.09.24)

상세: `../visual_plan.md` · 렌더 파일: `../images/` · 원본 spec: `../images.json`

| 자리 | 파일 | 방식 |
|---|---|---|
| 대표 | limited-acceptance-thumbnail.png | 로컬 렌더 사용 (thumbnail 템플릿) |
| {{IMAGE_1}} | AI(image_1.png) / 대체 limited-acceptance-illust-1.png | AI 삽화 기본, 대체는 illustration desk |
| {{IMAGE_2}} | limited-acceptance-compare.png | 정보 이미지 로컬 렌더 사용 — AI 생성 안 함 |
| {{IMAGE_3}} | AI(image_3.png) / 대체 limited-acceptance-illust-2.png | AI 삽화 기본, 대체는 illustration path |
| {{IMAGE_4}} | limited-acceptance-steps.png | 정보 이미지 로컬 렌더 사용 — AI 생성 안 함 |
| {{IMAGE_5}} | AI(image_5.png) / 대체 limited-acceptance-illust-3.png | AI 삽화 기본, 대체는 illustration calm |

> image_2, image_4는 app.py가 프롬프트로 읽지 않도록 아래에 `###` 헤더를 두지 않았습니다. 4단계에서 AI로 만들지 말고 위 렌더 파일을 업로드하세요.
> 아래 `###` 블록 본문은 app.py `parse_image_prompts()`가 다음 `###` 전까지 통째로 읽으므로 프롬프트 외 문장을 넣지 마세요(발행 절차 섹션을 이 위로 옮긴 이유).
> 참고: 현재 app.py는 `MAX_IMAGE_SLOTS = 6`이라 {{IMAGE_5}}도 `replace_placeholders()`로 치환됩니다.

## 발행 절차 (수동)
1. ohbhs.tistory.com/manage/newpost/ 접속
2. 카테고리 "상속" 선택, 제목 입력
3. 에디터 "HTML" 모드로 전환 → post.html 붙여넣기(이미지 자리 URL 교체 후)
4. "기본모드"로 복귀
5. 썸네일: "첨부" → "사진" → 업로드 → 이미지 클릭 → "대표"
6. 태그 10개 입력(하나씩 Enter)
7. "완료" → "비공개" → "비공개 저장"
8. 검수 시 `<!-- V# -->` 주석과 V3 문단(삭제 여부) 확인

## 이미지 프롬프트

### thumbnail.png
로컬 렌더 사용 (limited-acceptance-thumbnail.png)

### image_1.png
Hands calmly sorting a pile of plain mail envelopes into neat small stacks on a wooden kitchen table, a warm cup of tea and a small potted plant nearby with soft sunlight falling across the table, accent color deep blue (#23507C), warm flat editorial illustration, soft grain texture, muted navy (#1F3A5F) and slate palette with one gentle accent color, soft paper background, rounded simple shapes, generous negative space, soft morning light, calm and hopeful mood, people shown only from behind or as hands or silhouettes, No text, no letters, no numbers, no logos, no flags, no recognizable faces

### image_3.png
A quiet, tidy entryway of an old family home seen from inside, a set of house keys resting untouched in a small dish on a wooden shelf, morning sunlight streaming in through a half-open front door, accent color deep blue (#23507C), warm flat editorial illustration, soft grain texture, muted navy (#1F3A5F) and slate palette with one gentle accent color, soft paper background, rounded simple shapes, generous negative space, soft morning light, calm and hopeful mood, people shown only from behind or as hands or silhouettes, No text, no letters, no numbers, no logos, no flags, no recognizable faces

### image_5.png
Seen from behind, a person sits relaxed by a sunny window holding a warm cup of tea, a neatly closed document folder on the table and a blank wall calendar with one square softly circled, accent color deep blue (#23507C), warm flat editorial illustration, soft grain texture, muted navy (#1F3A5F) and slate palette with one gentle accent color, soft paper background, rounded simple shapes, generous negative space, soft morning light, calm and hopeful mood, people shown only from behind or as hands or silhouettes, No text, no letters, no numbers, no logos, no flags, no recognizable faces
