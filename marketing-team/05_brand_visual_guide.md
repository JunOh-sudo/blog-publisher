# 05. 브랜드 비주얼 가이드

담당: `visual-designer` · 렌더러: `marketing-team/design/render.py` · 템플릿: `marketing-team/design/templates/`

## 1. 톤
차분하고 신뢰감 있게. 겁주는 이미지(수갑, 빨간 경고, 우는 사람)보다 **정리된 정보와 해결 방향**을 보여준다.

## 2. 이미지 구성 규칙 (모든 글 공통)

정보 이미지만 이어지면 독자가 쉴 곳이 없습니다. **정보 이미지와 삽화를 번갈아** 배치합니다.

| 자리 | 종류 | 역할 |
|---|---|---|
| 대표 이미지 | `thumbnail` | 목록·검색에서 클릭 유도 (본문 자리와 별도) |
| `{{IMAGE_1}}` 도입부 직후 | **삽화** | 독자 상황에 공감하는 장면. 글의 첫인상을 부드럽게 |
| `{{IMAGE_2}}` 본문 핵심 | 정보 이미지 | 체크리스트·비교·절차 중 하나 |
| `{{IMAGE_3}}` 본문 중반 | **삽화** | 긴 설명 뒤 숨 고르기. 해결·안도 방향의 장면 |
| `{{IMAGE_4}}` 마무리 | 정보 이미지 | 요약·다음 행동 |

- 한 글에 삽화 최소 2장, 정보 이미지 최소 1장.
- 정보 이미지 두 장이 연달아 오지 않게 한다. 글이 길면(티스토리 h2 7개 이상) 삽화를 1장 더 넣는다.
- 삽화 바로 아래에 한 줄 캡션(선택)을 달아 다음 내용으로 자연스럽게 넘긴다. 예: "서두르기 전에, 지금 할 일부터 정리해 볼까요?"

### 삽화 만드는 법
1. **기본: AI 삽화** (app.py 4단계, gpt-image). 아래 6절 스타일 접미어를 반드시 붙여 블로그 전체의 그림체를 통일한다.
2. **대체: 삽화 템플릿** (`illustration`, API 없이 로컬 렌더링). 장면 4종: `desk`(서류 정리·준비), `home`(집·열쇠·보증금·상속 부동산), `path`(갈림길·선택), `calm`(창가의 차 한 잔·안도). AI 이미지를 쓸 수 없거나 급할 때 쓴다.

### 삽화 장면 라이브러리 (기둥별)

| 기둥 | 장면 예시 |
|---|---|
| P1 상속 채무 | 식탁 위 봉투 더미를 차분히 분류하는 손 · 오래된 집 현관의 열쇠 · 달력에 표시한 날짜와 따뜻한 차 |
| P2 상속 분쟁 | 가족 식탁의 빈 의자들과 햇살 · 오래된 사진첩 · 두 갈래 길 위의 벤치 |
| P3 회생·파산 | 정리된 가계부와 화분 · 새벽 창가에서 기지개 켜는 뒷모습 · 계단을 한 칸씩 오르는 발 |
| P4 교차·시의성 | 이삿짐 상자와 새 열쇠 · 비 갠 뒤 골목 · 두 문서철 사이의 저울 대신 나란히 놓인 두 컵 |

인물은 **뒷모습·손·실루엣**으로만 표현한다(실존 인물 닮음 방지). 불안을 과장하지 않고, 장면 안에 해결 방향(정리, 햇살, 열린 문)을 하나 둔다.

## 3. 색상

| 토큰 | HEX | 용도 |
|---|---|---|
| navy | `#1F3A5F` | 하단 바, 비교표 기준열, 브랜드 |
| ink | `#18212D` | 제목 |
| ink-2 | `#48525F` | 본문·설명 |
| paper | `#F5F6F8` | 배경 |
| line | `#D9DEE5` | 테두리 |
| P1 상속 채무 | `#23507C` / 배경 `#E1EAF4` | 기둥 태그·강조 |
| P2 상속 분쟁 | `#7A4A86` / `#F0E7F2` | |
| P3 회생·파산 | `#2F6B52` / `#E2EFE8` | |
| P4 교차·시의성 | `#8A5A14` / `#F5ECDC` | |

기둥 색은 글의 기둥(P1~P4)에 맞춰 자동 적용된다. 한 이미지에 기둥 색은 하나만 쓴다.

## 4. 글꼴
- 제목: Noto Serif KR 700
- 본문·라벨: Noto Sans KR 500 / 800
- 둘 다 무료 상업 이용 가능(SIL OFL). 다른 폰트는 라이선스 확인 전 사용 금지.

## 5. 이미지 종류와 규격

| 종류 | 템플릿 | 규격 | 언제 |
|---|---|---|---|
| 대표 이미지 | `thumbnail` | 1080×1080 PNG | 모든 글 1장. 제목 2~3줄, 부제 1줄 |
| 체크리스트 | `checklist` | 1080×1080 | "○가지", 준비물, 주의사항 (최대 5개) |
| 비교표 | `compare` | 1080×1080 | A vs B (최대 5행) |
| 절차 | `steps` | 1080×1080 | 실제 순서가 있는 절차 (최대 5단계) |
| 삽화 (기본) | AI 생성 | 1024×1024 | `IMAGE_1`, `IMAGE_3`. 글자 없음 |
| 삽화 (대체) | `illustration` | 1080×1080 | AI 삽화를 쓸 수 없을 때. 장면 desk/home/path/calm |

모든 정보 이미지 하단에 "법무법인 강호 오준성 변호사" 바가 들어간다(비교·체크리스트·절차에는 "일반 정보이며 개별 사안은 상담이 필요합니다" 문구 포함).

## 6. AI 삽화 프롬프트 스타일 접미어
```
, warm flat editorial illustration, soft grain texture, muted navy (#1F3A5F) and slate palette
with one gentle accent color, soft paper background, rounded simple shapes, generous negative space,
soft morning light, calm and hopeful mood, people shown only from behind or as hands or silhouettes,
No text, no letters, no numbers, no logos, no flags, no recognizable faces
```
프롬프트 구조: `[장면 한 문장] + [해결 방향 소품 하나] + [기둥 강조색] + 스타일 접미어`
예: "Hands calmly sorting a stack of envelopes on a kitchen table, a small plant and a cup of tea nearby, accent color deep green (#2F6B52)" + 접미어
주제 대상 예: 서류 정리하는 손, 계산기와 가계부, 열쇠와 집 모형, 갈림길. 판사봉·법원 건물·수갑 같은 상투적 소재는 피한다.

## 7. 대체텍스트·파일명
- 대체텍스트: "개인회생 신청 전 멈춰야 할 행동 5가지 체크리스트: 특정 채권자 우선 변제, 재산 명의 이전…" 처럼 이미지 내용을 문장으로.
- 파일명: `rehab-before-filing-checklist.png` (영문 소문자·하이픈)

## 8. 사용 예
```bash
python3 marketing-team/design/render.py marketing-team/design/examples/sample.json marketing-team/design/examples
```
처음 실행하면 폰트를 내려받아 `design/fonts/`에 캐시합니다(약 26MB, git 제외).
