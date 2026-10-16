# 기존 프로젝트와 Codex 공통 정책 업데이트

Luna 정책 revision 2.1은 필수 검증 통과, 독립 리뷰, 준비 상태를 하나의 Core 계약으로 정리합니다. 기존 템플릿 복사본은 원본 수정만으로 갱신되지 않습니다.

## 기존 프로젝트

최신 Luna 체크아웃에서 먼저 미리보기를 실행합니다. 아래 경로는 실제 대상 경로로 바꾸십시오.

```powershell
python scripts/apply-luna-policy.py --project C:\Codex\Luna-RedLab --project C:\Codex\Luna-Knowledge-OS
```

확인한 변경을 적용하려면 같은 명령에 `--apply`를 추가합니다. 프로젝트마다 별도 feature branch에서 적용하고 diff를 검토한 뒤 commit/PR로 반영합니다.

프로젝트 업데이트는 `docs/luna/CORE_ENGINEERING_PROTOCOL_V2.md`, `docs/luna/policy-lock.json`, 루트 지침의 Luna 관리 구간만 다룹니다. 기존 지침은 보존하고, 루트의 비어 있지 않은 `AGENTS.override.md`가 있으면 그 파일에 포인터를 넣습니다. 프로젝트 기술 스택, 보안 제한, 필수 검증과 더 엄격한 리뷰·승인 규칙은 유지됩니다. 기존 Luna 공통 정책 요약보다 새 Core 계약을 우선합니다.

## 모든 로컬 Codex 프로젝트의 기본값

Windows 기본 프로필의 예입니다. `CODEX_HOME`을 별도로 사용한다면 그 실제 경로를 지정하십시오.

```powershell
python scripts/apply-luna-policy.py --codex-home "$env:USERPROFILE\.codex"
python scripts/apply-luna-policy.py --codex-home "$env:USERPROFILE\.codex" --apply
```

macOS/Linux:

```bash
python3 scripts/apply-luna-policy.py --codex-home "${CODEX_HOME:-$HOME/.codex}"
python3 scripts/apply-luna-policy.py --codex-home "${CODEX_HOME:-$HOME/.codex}" --apply
```

정책은 Codex 홈의 `luna/`에 저장되고 활성 전역 지침에 절대 경로 포인터가 추가됩니다. 프로젝트/하위 디렉터리 지침이 더 구체적이면 그 규칙을 존중합니다. 활성 세션의 이미 로드된 지침이 자동 교체된다고 보장하지 않습니다. 다음 새 작업 세션에서 로드한 지침 출처를 확인하십시오. 다른 PC, 다른 CODEX_HOME, 별도 클라우드 실행 환경에는 따로 적용해야 합니다.

이 작업은 사용자 PC에서 명령을 실행해야 전역 적용됩니다. GitHub PR 생성은 사용자 PC의 설정 변경을 의미하지 않습니다.

기존에 선택 설치한 Luna named agent TOML은 이 도구가 덮어쓰지 않습니다. 개별 수정 사항을 보존하고 최신 `integrations/codex/agents/` 정의와 diff를 검토해 갱신하십시오. 새 정의는 활성 지침의 정책 포인터를 따릅니다. 설치하지 않은 경우에는 기본 Codex 지침으로 진행할 수 있습니다.

## 보존·충돌·업데이트

- 기본은 미리보기이고 `--apply`만 쓰기를 수행합니다. 현재 체크아웃의 정책만 사용하며 원격 최신 파일을 자동 다운로드하거나 실행하지 않습니다.
- 기존 파일을 바꾸면 `.luna-backup` 사본을 남깁니다. 원래 지침은 관리 구간 밖에서 그대로 유지됩니다.
- 정책 잠금 파일의 SHA-256과 현재 정책이 다르면 로컬 편집 충돌로 멈춥니다. 수동 변경을 보존하고 차이를 검토한 뒤 다시 적용합니다.
- 다른 내용의 백업이 이미 있으면 덮어쓰지 않습니다. 이전 백업을 안전하게 별도 보관한 후 다시 실행하십시오.
- symlink 경로와 잘못된 관리 마커를 거부합니다. 파일별 쓰기는 atomic replace이며, 디스크/권한 오류 시 여러 파일 전체가 하나의 트랜잭션으로 롤백된다고 보장하지 않습니다. 오류 후 diff와 백업을 확인하십시오.
- 향후 정책을 적용하려면 검토한 최신 Luna 체크아웃에서 같은 업데이트 명령을 다시 실행합니다. 템플릿이나 GitHub main을 실시간 자동 추적하지 않습니다.

검증 기준: `python -m unittest discover -s tests -v`와 `python .agents/skills/doctor/scripts/health.py --root . --deep`.

공식 지침: [OpenAI의 AGENTS.md 검색·우선순위 설명](https://learn.chatgpt.com/docs/agent-configuration/agents-md).
