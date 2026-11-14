# Luna 전역 자연어 Codex 실행기

## 작동 범위

**한 번 설치한 `luna` 명령을 PC의 모든 개발 프로젝트에서 사용합니다.** 프로젝트별 `AGENTS.md`, `.agents/skills/`, `.codex/config.toml`, `hooks.json`은 수정하거나 복제하지 않습니다. 현재 디렉터리의 Git 저장소 루트를 확인한 다음 **그 디렉터리를 작업 폴더로 Codex CLI를 실행**하므로 기존 프로젝트 정책과 샌드박스·승인 설정은 Codex가 그대로 적용합니다.

`luna`는 사용자 요청을 받아 **각 실행 전에** 기존 Luna Model Router로 `gpt-6-luna`, `gpt-6.1-terra`, `gpt-6.1-sol`, `gpt-6-astra` 중 하나와 reasoning 수준을 선택합니다. 실행 중 모델을 임의로 교체하지 않습니다. `codex exec --json`의 `thread.started` 식별자를 프로젝트별로 보존하며, 후속 자연어 입력은 `codex exec resume SESSION_ID`로 이어갑니다. 서로 다른 프로젝트 간 대화는 공유하지 않습니다.

**주의: 기존 Codex 데스크톱 앱/IDE 입력창을 직접 사용하는 경우 자동 모델 선택이 적용되지 않습니다.** Codex의 `PreModelRequest`·`UserPromptSubmit` 훅은 메인 모델을 직접 변경할 수 없습니다. 이 기능은 별도로 실행하는 `luna` 터미널 대화/명령에만 적용됩니다. 공식 문서: <https://learn.chatgpt.com/docs/hooks>, <https://learn.chatgpt.com/docs/cli/reference>.

## Windows PC에 한 번 설치

Python 3.10 이상과 로그인된 Codex CLI가 필요합니다. **관리자 권한이나 별도 API 키는 필요하지 않습니다.** Codex CLI의 기존 로그인 및 사용 한도를 사용합니다.

```powershell
# Luna 소스가 저장된 폴더에서 실행
cd C:\path\to\luna-chat-coder
git pull --ff-only origin main

# 설치가 바꿀 파일만 미리 확인
python .\scripts\install_luna_global.py --dry-run

# 사용자 경로에만 설치, 현재 프로젝트 설정은 변경하지 않음
python .\scripts\install_luna_global.py --add-to-user-path
```

`--add-to-user-path`는 Windows 계정의 **사용자 PATH(HKCU)** 에 `~\.codex\luna\bin`을 추가합니다. 관리자 권한은 필요하지 않습니다. 적용 후 새 PowerShell 창을 열어 `luna doctor`를 확인하십시오. 회사 정책으로 PATH 수정이 제한된 경우 옵션 없이 설치하고 `& "$env:USERPROFILE\.codex\luna\bin\luna.cmd"`으로 사용할 수 있습니다. `CODEX_HOME`을 사용 중이라면 설치·실행 과정에서 동일한 환경 변수를 유지하십시오.

## 모든 프로젝트에서 자연어 대화

```powershell
cd C:\Projects\MyProduct
luna
```

이후 다음처럼 **자연어만 입력**합니다.

```text
Luna> 로그인 오류 원인을 분석해 줘
Luna> 방금 분석을 바탕으로 수정하고 테스트해 줘
Luna> 변경 파일을 보안 관점에서 검토해 줘
```

매 입력마다 모델을 재판단하며, 동일 프로젝트의 Codex 대화 식별자를 이어 사용합니다. 위험도가 명시적으로 높았던 대화에서는 자동으로 낮추지 않으므로 과도한 비용이 발생한다면 `:new`로 새 세션을 시작하십시오.

다른 프로젝트는 그 프로젝트로 이동한 후 `luna`를 실행하면 됩니다. `--project`로 직접 지정할 수도 있습니다.

```powershell
luna --project C:\Projects\OtherProject
luna --project C:\Projects\OtherProject "설정 오류 분석해 줘"
luna --plan "전체 인증 모듈 재설계"
luna --risk critical "인증 우회 취약점을 수정해 줘"
```

모델 선택만 확인하는 `--plan`은 Codex를 실행하지 않아 토큰을 사용하지 않습니다. `luna doctor`는 Codex CLI 경로, 프로젝트, 세션 보유 여부를 보여줍니다. `luna new` 또는 대화 중 `:new`는 **Luna의 후속 대화 포인터만 초기화**하며 Codex 원본 대화 기록은 지우지 않습니다. `:exit`로 종료합니다.

## 통합 사용량과 결과 기록

어느 프로젝트에서 실행하더라도 동일한 사용자별 데이터에 기록됩니다.

- 사용량: `$CODEX_HOME/luna/usage.jsonl` 또는 기본 `~/.codex/luna/usage.jsonl`
- 세션: `$CODEX_HOME/luna/sessions/<프로젝트 경로 해시>.json`
- 기록 항목: 선택 모델, reasoning, 실제 `turn.completed.usage` 토큰, 실행 상태, 명시된 검증 결과, 프로젝트 경로 해시
- **저장하지 않는 항목:** 사용자 자연어 원문, 코드, 실제 프로젝트 경로, API 키, Codex 원시 실행 로그

```powershell
luna stats
luna verify <RUN_ID> passed
luna verify <RUN_ID> failed reasoning
```

`RUN_ID`는 실행 마지막에 표시됩니다. **Codex 종료코드 0은 자동으로 검증 통과로 해석하지 않습니다.** 테스트·리뷰 근거가 있을 때만 `verify`로 확인합니다. 검증된 실패 이력에 한해 다음 작업의 모델 선택을 보정합니다. `stats`의 USD 금액은 API **상당액 추정치**이며 Plus/Codex 구독 결제액이나 크레딧 잔량이 아닙니다.

동일 프로젝트에서 두 개의 Luna 프로세스가 동시에 동일 대화 포인터를 수정하지 않도록 잠금 파일을 사용합니다. 비정상 종료 후 잠금이 남으면 다른 실행이 없는지 확인한 뒤 해당 `<해시>.lock` 파일만 정리하십시오.

## 유지보수 및 제거

템플릿이 업데이트되더라도 PC의 설치본은 자동 갱신되지 않습니다. 해당 소스에서 `git pull` 후 설치 명령을 다시 실행하면, **이전 설치 관리 파일이 사용자에 의해 수정되지 않은 경우에만** 갱신합니다. 수정된 파일이나 동일 이름의 다른 파일을 발견하면 덮어쓰지 않고 오류를 출력합니다.

```powershell
python .\scripts\install_luna_global.py --uninstall
```

제거해도 사용량, 대화 포인터, Codex 원본 세션, 프로젝트별 정책은 보존합니다. Windows 사용자 PATH의 항목은 필요한 경우 사용자 환경변수 설정에서 직접 제거할 수 있습니다.

## 검증 및 제한

```powershell
python -m unittest discover -s tests -v
python -m py_compile scripts\luna_workspace.py scripts\install_luna_global.py
```

각 환경에서 선택 모델의 사용 가능 여부가 달라 Codex 자체가 특정 모델을 거부할 수 있습니다. 이 경우 **과금이나 품질에 영향을 줄 수 있는 임의 대체 모델로 자동 재시도하지 않으며** 원래 오류를 전달합니다. 현재 배포본은 Codex CLI의 비대화형 실행 경로이므로 기본 Codex 데스크톱 앱의 대화 UI와 기능적으로 동일하지 않고, 실시간 TUI의 승인 요청 UX도 그대로 제공하지 않습니다. 이 점은 각 프로젝트의 Codex 보안 설정을 변경하지 않기 위한 제약입니다.
