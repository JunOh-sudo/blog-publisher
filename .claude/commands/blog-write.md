---
description: 주제 하나로 팩트시트 → 네이버/티스토리 원고 → 컴플라이언스 검수까지 진행한다
argument-hint: <주제 또는 topic_id> [naver|tistory|both]
---
주제: $ARGUMENTS

아래 순서로 진행하세요. 각 단계 산출물은 `marketing-team/work/<오늘날짜>-<slug>/`에 저장합니다.

1. **legal-researcher** 에이전트 → `factsheet.md`. `[확인필요]`가 남으면 목록을 저에게 보여주고 멈추세요.
2. 플랫폼 지정이 없으면 topic_backlog.csv의 platform을 따릅니다.
   - 네이버: **naver-writer** 에이전트
   - 티스토리: **tistory-writer** 에이전트
   - both: 두 에이전트를 병렬로 실행하되, 각도와 문장이 겹치지 않게 지시
3. **compliance-reviewer** 에이전트 → `review.md`. 반려면 작가에게 한 번 되돌려 수정 후 재검수.
4. 마지막에 저에게: 판정, 변호사 확인이 필요한 문장, 검수용 파일 경로를 요약해 주세요.
   제가 "승인"이라고 하면 `approval.md`를 만들고 **publisher** 에이전트로 발행 패키지를 준비하세요.
