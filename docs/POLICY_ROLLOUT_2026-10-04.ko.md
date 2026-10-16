# Luna 정책 2.1 기존 프로젝트 적용 기록

2026-10-04 기준. 아래 변경은 별도 브랜치의 PR이며 아직 병합되지 않았습니다. 병합 후 로컬 체크아웃을 갱신하고 새 Codex 세션에서 적용합니다.

| 저장소 | PR | 기준 브랜치 |
| --- | --- | --- |
| Luna-RedLab | [업데이트 PR](https://github.com/Edward-Jeong/Luna-RedLab/pull/1) | `main` |
| TradingCodex | [업데이트 PR](https://github.com/Edward-Jeong/TradingCodex/pull/3) | `agent/kis-mock-milestone` |
| Notion_AX | [업데이트 PR](https://github.com/Edward-Jeong/Notion_AX/pull/2) | `main` |
| meetingnote | [업데이트 PR](https://github.com/Edward-Jeong/meetingnote/pull/1) | `main` |
| Luna-Knowledge-OS | [업데이트 PR](https://github.com/Edward-Jeong/Luna-Knowledge-OS/pull/16) | `main` |
| ai-project-template | [업데이트 PR](https://github.com/Edward-Jeong/ai-project-template/pull/1) | `main` |
| Luna-Log-Insight-API | [업데이트 PR](https://github.com/Edward-Jeong/Luna-Log-Insight-API/pull/2) | `main` |
| hanppyum | [업데이트 PR](https://github.com/Edward-Jeong/hanppyum/pull/1) | `main` |
| Transcriber | [업데이트 PR](https://github.com/Edward-Jeong/Transcriber/pull/5) | `main` |

각 PR은 기존 AGENTS.md 원문을 보존하고 관리 구간, 공통 정책 사본, SHA-256 잠금 파일만 추가합니다. 프로젝트별 보안 제한과 필수 검증을 유지합니다. 서로 다른 내용의 기존 정책 파일, symlink, 잘못된 관리 구간은 덮어쓰지 않고 오류로 처리합니다.

검증: updater 포함 unittest 10개 통과, 원문 보존 및 재적용 시 변경 없음 확인, 독립 리뷰 완료. 애플리케이션 코드 변경은 없으며 각 프로젝트의 애플리케이션 테스트는 실행하지 않았습니다. 원격 PR의 필수 CI와 저장소 승인 절차는 별도로 충족해야 합니다.

루트 Codex 지침이 확인된 9개 저장소를 대상으로 했습니다. 지침이 확인되지 않은 저장소와 다른 포크 전체에는 변경을 강제하지 않았습니다. 다른 로컬 프로젝트를 포함하는 Codex 전역 기본값 적용은 [업데이트 가이드](POLICY_UPDATES.ko.md)의 `--codex-home` 명령을 사용자 환경에서 실행해야 합니다. GitHub PR만으로 PC나 별도 클라우드의 설정은 변경되지 않습니다.

정책은 revision 2.1로 고정되어 있습니다. 이후 정책 개정은 검토한 최신 Luna 체크아웃에서 업데이트 도구를 재실행해야 반영됩니다.

