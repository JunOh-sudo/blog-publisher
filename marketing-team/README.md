# 오준성 변호사 블로그 콘텐츠 마케팅 에이전트 팀

| 문서 | 내용 |
|---|---|
| [01_blog_audit.md](01_blog_audit.md) | 기존 네이버·티스토리 블로그 진단 (2024 원고 약 140건 분석) |
| [02_content_strategy.md](02_content_strategy.md) | 포지셔닝, 4개 콘텐츠 기둥, 플랫폼 역할, 주제 채점, **12주 캘린더**, 리프레시 우선순위 |
| [03_agent_team.md](03_agent_team.md) | **에이전트 팀 구성**, 주간 워크플로우, 품질 게이트, 광고규정 체크리스트 |
| [04_kpi_and_aftercare.md](04_kpi_and_aftercare.md) | KPI 트리, 데이터 수집, 리포트 주기, 사후관리 규칙 |
| [topic_backlog.csv](topic_backlog.csv) | 채점된 주제 42개 (캘린더 36 + 백로그 6) |
| `data/` | 발행 로그·통계·순위·상담 CSV 템플릿 |
| `reports/` | 주간·월간 리포트 (performance-analyst 생성) |
| `work/` | 글별 작업 폴더 (팩트시트·원고·검수) |

## 에이전트 팀 (8명 + 변호사)

| 단계 | 에이전트 | 한 줄 역할 |
|---|---|---|
| 기획 | `topic-strategist` | 주제·키워드·주간 계획 |
| 제작 | `legal-researcher` | 출처 달린 법령·판례 팩트시트 |
| 제작 | `naver-writer` | 전환형 사례 Q&A 원고 |
| 제작 | `tistory-writer` | 구글 SEO 종합 가이드 원고 |
| 검수 | `compliance-reviewer` | 법리 정확성 + 변호사 광고규정 |
| 발행 | `publisher` | 패키징·비공개 발행·색인·로그 |
| 측정 | `performance-analyst` | 주간·월간 성과 리포트 |
| 사후관리 | `content-refresher` | 리프레시·통합·내부링크·법 개정 대응 |

## 첫 주 시작 순서
1. **기준선 측정**: 네이버 블로그 통계·티스토리 통계·Search Console에서 최근 3개월 데이터를 내보내 `data/`에 넣기
2. **추적 설정**: 상담 링크 UTM, 상담 접수 시 “어떻게 알고 오셨나요?” 질문 → `data/leads.csv`
3. `/blog-plan` → 주제 승인 → `/blog-write <주제> both`
4. 금요일 `/blog-report`, 월말 `/blog-refresh`
