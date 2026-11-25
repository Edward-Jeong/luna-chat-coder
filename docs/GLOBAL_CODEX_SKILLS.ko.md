# 모든 Codex 프로젝트에서 prune-tests 공통 사용

## 범위와 우선순위

공식 Codex 사용자 범위 스킬 디렉터리는 ~/.agents/skills/ 입니다. Windows 기본 경로는 %USERPROFILE%\.agents\skills\prune-tests\SKILL.md 입니다.

이 위치에 설치하면 같은 사용자 계정의 Codex CLI와 지원 환경이 여러 프로젝트에서 스킬을 발견할 수 있습니다. 프로젝트별 AGENTS.md, .agents/skills/, .codex/config.toml, 테스트 설정과 보안 지침은 변경하지 않습니다. 기존 프로젝트 지침과 필수 검증이 이 선택형 스킬보다 우선합니다.

**전역 발견은 매 작업에서 자동 실행한다는 의미가 아닙니다.** 테스트 정리·중복 제거·테스트 품질 개선 요청에서 Codex가 스킬을 선택하도록 설명을 구성했습니다. 반드시 사용하려면 자연어 요청에 $prune-tests를 명시하십시오. 테스트나 보안 회귀를 임의로 제거하지 않습니다.

기존 Luna 실행기 설치 경로인 ~/.codex/luna 와 다릅니다. 이 스킬 설치 대상인 ~/.agents 는 CODEX_HOME 설정과 무관합니다.

## Windows PowerShell 1회 설치

PR 병합 후 최신 Luna 소스에서 실행합니다. Python 3.10 이상이 필요하며 관리자 권한은 불필요합니다.

    cd C:\path\to\luna-chat-coder
    git pull --ff-only origin main
    python .\scripts\install_codex_shared_skills.py --dry-run
    python .\scripts\install_codex_shared_skills.py
    Test-Path "$env:USERPROFILE\.agents\skills\prune-tests\SKILL.md"

새 Codex 세션을 열고 다음과 같이 사용합니다.

    $prune-tests 현재 테스트 중 중복·무효 테스트를 분석해줘.
    프로젝트별 필수 검증과 보안 회귀 테스트는 유지하고 변경 전후 결과를 확인해줘.

## macOS / Linux

    cd /path/to/luna-chat-coder
    git pull --ff-only origin main
    python3 scripts/install_codex_shared_skills.py --dry-run
    python3 scripts/install_codex_shared_skills.py
    test -f "$HOME/.agents/skills/prune-tests/SKILL.md"

## 업데이트와 안전한 제거

최신 소스를 받은 후 같은 설치 명령을 다시 실행하면 관리 파일을 갱신합니다. 이미 동일한 스킬 이름의 비관리 디렉터리가 있거나 관리 파일이 수정되면 **덮어쓰지 않고 중단**합니다. 기존 파일은 먼저 백업하여 수동으로 차이를 검토하십시오. 원격의 변경 가능한 스킬을 실행할 때마다 다운로드하지 않습니다.

    python .\scripts\install_codex_shared_skills.py --uninstall --dry-run
    python .\scripts\install_codex_shared_skills.py --uninstall

제거는 관리 대상인 두 파일과 기록만 삭제하며, 같은 폴더에 사용자가 추가한 다른 파일은 유지합니다. 다중 파일 업데이트 도중 디스크 오류가 발생하면 완전한 트랜잭션 롤백은 보장되지 않습니다.

## 검증과 제약

    python -m py_compile scripts/install_codex_shared_skills.py
    python -m unittest discover -s tests -p test_codex_shared_skills.py -v

GitHub PR 생성·병합만으로 PC에 설치되지는 않습니다. 다른 PC, 다른 OS 계정, 별도 클라우드 실행 환경에는 각각 설치해야 합니다. Codex에서 자동 선택할지 여부는 요청과 실행 환경에 따라 달라집니다.

출처: https://developers.openai.com/api/reference/cli
원본 스킬: https://github.com/caldoai/skills/blob/main/skills/prune-tests/SKILL.md
