---
description: 공개된 글의 색인 등록 요청 목록을 만들고, 발행 3일·7일 경과 글의 색인 여부를 확인·기록한다
argument-hint: [URL 또는 비워두면 published_posts.csv 기준]
---
publisher 에이전트로 색인 작업을 진행해 주세요. 대상: $ARGUMENTS (비어 있으면 `marketing-team/data/published_posts.csv`에서 status=public이고 index_requested_at이 비어 있는 글)

1. 요청할 URL 표를 만들어 주세요: 플랫폼 · URL · 대상 검색엔진 · 제출 경로(Search Console URL 검사 / 서치어드바이저 웹 페이지 수집 / 다음 웹마스터도구). 네이버 블로그 글은 요청 대신 확인 대상으로 분류합니다.
2. 제가 콘솔에서 제출을 마쳤다고 하면 `index_requested_at`을 기록해 주세요.
3. 발행 3일·7일이 지난 글은 검색 노출 여부를 확인해 `indexed_google/naver/daum`을 기록하고, 7일 미색인 글은 content-refresher에게 넘길 목록으로 정리해 주세요.
