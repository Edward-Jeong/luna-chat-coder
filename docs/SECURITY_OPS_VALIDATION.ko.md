# Security Ops / REA 검증 기록

검증일: 2026-10-20. 기준 main: `f1b0e24f3808b3fe07ef257b2db1bb775650f67a`.

기존 `feature/luna-security-ops`의 개념·규격을 선별 복원하고 현재 Core 2.1, 팀 라우터, 검증·리뷰 규칙에 맞춰 보완했습니다. 기존 브랜치 전체나 최신 reverse-skill 전체를 병합하지 않았습니다. 고객 원문·실제 고객 바이너리는 사용하지 않았습니다.

## 결과

| 검증 | 결과 |
| --- | --- |
| Python 회귀 테스트 | 27개 중 24개 통과, 기존 PowerShell 테스트 3개는 런타임 부재로 건너뜀 |
| 업무 라우팅 예시 | 21/21 일치. 한국어 SecuMS 장애, API 권한, Black Duck, JAR 역공학, AI 보안 포함 |
| 가상 Detect 로그 증거 검사 | candidate 기록의 해시·참조 검사 성공, 변조 후 실패 확인 |
| 승인 범위 | 미승인·미허용 행위·변경된 샘플·문자열 대신 배열 오입력 거절 |
| 계획 전용 REA | 외부 프로세스 호출 없음; 버전 불일치와 공급자 실패를 성공으로 처리하지 않음 |
| 실제 REA 6.7.0 CLI | 버전 확인, ASAR 인식·해시/일부 목록 수집 확인; 전체 분석 실패 |
| TOML·diff 검사 | 기존 6개 TOML 파싱 및 git diff --check 통과 |
| 독립 리뷰 | 동작·보안 / 코드베이스 적합성 수행, 발견된 IMPORTANT 범위 자료형 결함 수정 후 재검증 |

최종 상태: **review-ready**. 지원 환경에서 실제 REA 분석 성공 검증이 남아 있으므로 초안 PR입니다. 병합 준비 완료로 표시하지 않습니다.

## 재현 방법

```bash
python -m unittest discover -s tests -v
python tests/run_security_ops_sample.py

# 이미 선택·검증한 설치가 있을 때만 실제 외부 도구 실행
python tests/run_security_ops_sample.py --rea /absolute/path/rea --version 6.7.0
```

샘플 러너는 저장소의 가상 `portal.asar.b64`를 임시 폴더에 복원하고 샘플 해시로 승인 범위를 고정합니다. 내부 `portal.js`는 함께 제공한 소스이며 실제 대상 애플리케이션으로 실행하지 않습니다. 로그도 가상 Detect 상태이며 실제 Black Duck/포세라 원인 검증을 주장하지 않습니다. 기본 실행은 REA를 호출하지 않습니다. `--rea` 실행은 실제 분석 실패를 종료코드 1로 전달합니다.

ASAR SHA-256: `f9ee7872ea5cff3f912de3140eaa4ad1434fd43cf2cfa7f88ba3c103a14dc3f9`.

## 실제 REA 실패와 제약

실행환경은 Linux, Node.js 24.19.0, Python 3, npm 패키지 `rea-agents@6.7.0`입니다. 패키지는 작업용 별도 디렉터리에 `--ignore-scripts --no-audit --no-fund`로 설치했고, 사용자 PC·Codex 설정을 변경하지 않았습니다.

첫 `.js` 입력은 `unsupported_target`으로 거절됐습니다. 실제 CLI가 앱 디렉터리 또는 ASAR만 받음을 확인해 어댑터를 **ASAR 파일 전용**으로 수정했습니다. 디렉터리는 단일 파일 해시로 범위를 보장할 수 없어 제외했습니다.

ASAR 입력은 인식됐지만 다음 REA 오류로 전체 분석이 종료됐습니다.

```text
code: capability_unavailable
provider_id: process-ownership
Linux process ownership inspection requires a procps-compatible ps
fatal library error, lookup self
returncode: 1
```

부분 ASAR 목록과 루트 해시는 반환됐으나 JavaScript 파싱 완료는 확인하지 못했습니다. 반환된 오류는 관측 사실이며 정확한 호스트 내부 원인은 확정하지 않았습니다. REA 보안 검사나 실행환경 격리를 우회하지 않았습니다. 지원 Linux 환경에서 위 명령을 다시 실행하고, 공급자 결과의 파싱 범위·근거를 확인해야 합니다. CLI 종료코드 0만으로 분석 내용의 정확성까지 보장할 수는 없습니다.

Windows npm `.cmd` 실행, Windows/Ghidra 실제 네이티브 분석, 실제 고객 JAR/WAR 디컴파일, 네트워크 대상 능동 검증, MCP 연결은 검증하지 않았습니다. 이 어댑터는 JAR/WAR를 명시적으로 거절합니다. PowerShell 건너뜀은 기존 설치 도구 테스트이며 새 기능의 Windows 지원 검증으로 대체할 수 없습니다.

## 리뷰·정책 확인

독립 리뷰에서 잘못된 `assets`/`allowed_actions` JSON 문자열이 부분 문자열 비교로 허용되는 결함을 재현했습니다. 객체·배열·문자열 자료형 검사와 부정 회귀 테스트로 수정했고 독립 재검증을 받았습니다. 동일 세션의 자기검토를 독립 리뷰로 계산하지 않았습니다.

Doctor의 기존 겹침/대형 스킬 경고 및 `docs/luna/CORE_ENGINEERING_PROTOCOL_V2.md` 조건부 이관 경로 경고는 기존 main에도 있는 상태이며 이번 기능의 실행 의존성이 아닙니다. 자동 삭제·전역 업데이트는 하지 않았습니다. 신규 기능은 조건부 진입점으로만 추가했습니다.

## 출처

- 기존 초안: https://github.com/Edward-Jeong/luna-chat-coder/tree/feature/luna-security-ops
- 비교한 라우팅·규격: https://github.com/Edward-Jeong/reverse-skill
- REA CLI·설치·보안 경계: https://github.com/morluto/rea

reverse-skill의 동작 규칙 전체, GPLv3 CTF 모듈 및 외부 공격 도구 코드는 포함하지 않았습니다. REA 런타임도 저장소에 포함하지 않습니다.

## 2026-10-21 재검증 및 Codex 연결

PR #11 병합 main `523cc3eac5f825964e087e56c9a52eac3101afbf`에서 재개했습니다. 위 2026-10-20 실패 기록은 당시 환경의 관측 사실로 유지하며, 아래 재검증 결과와 구분합니다.

- 동일 샌드박스에서는 REA process-ownership 오류가 다시 발생했습니다. 보안 검사나 격리 설정을 우회하지 않고 GitHub Actions의 실제 OS 러너로 검증을 옮겼습니다.
- 최초 원격 실행: https://github.com/Edward-Jeong/luna-chat-coder/actions/runs/39518820185 (분석 대상 소스 `07df5094e83506db6662b9aa414d97675f77d828`). Ubuntu 24.04에서 REA 6.7.0 분석 성공과 `portal.js`의 `parse_status=complete`를 확인했습니다. 샘플을 실행하지 않았습니다.
- 같은 실행의 Windows 2022는 기존 정책 업데이트 테스트가 Windows 경로 구분자를 그대로 비교해 실패했습니다. 실제 정책은 POSIX 형식 경로를 의도적으로 기록하므로 기대값을 `Path.as_posix()`로 수정했습니다. 정책 업데이트 런타임이나 검증 기준을 완화하지 않았습니다. Windows REA는 해당 실행에서 수행되지 않았습니다.
- Windows/POSIX 공용으로 `--node ABSOLUTE_NODE --executable ABSOLUTE_REA_MJS`를 추가했습니다. shell 없이 인수 배열을 전달하고 `.cmd`/`.bat`를 거절합니다. 계획 호출에는 버전 조회를 포함한 프로세스 실행이 없습니다.
- `Luna Reverse Engineer` 선택형 에이전트를 추가했습니다. 임시 Codex 홈에서 설치 도구가 새 정의를 설치하는 것과 TOML 7개 파싱을 확인했습니다. 사용자 PC에 설치했거나 실제 Codex 모델 세션에서 실행했다고 주장하지 않습니다.
- Windows 최종 재검증과 독립 리뷰 결과는 후속 기록에 추가합니다. 네이티브/Ghidra·MCP 등록·JAR/WAR·macOS는 이번 검증 범위에 포함하지 않습니다.

Codex 사용·1회 설치 명령은 `integrations/codex/README.md`의 REA 절을 참고하십시오. 동일 에이전트 파일의 사용자 수정은 기존 설치 도구의 보존 정책을 따릅니다.

### 최종 재검증 결과 (2026-10-21)

[최종 실제 실행 39519035740](https://github.com/Edward-Jeong/luna-chat-coder/actions/runs/39519035740)의 두 작업이 모두 성공했습니다. 검증한 소스 커밋은 `8b070b66343d9eedeb505167c3a8eadd68f25bf3`, Git tree는 `cb867bb03cffaaac8b6b0d42355238e4f51ebe06`입니다. 이 절을 추가하는 후속 변경은 검증 기록·참조 문구만 수정하며 실행 코드와 검증 입력은 같습니다.

| 환경 | 회귀 테스트 | 실제 REA 6.7.0 ASAR 분석 |
| --- | --- | --- |
| Ubuntu 24.04 / Node 24.19.0 / Python 3.11 | 28/28 통과, 건너뜀 없음 | 종료코드 0, `portal.js` 파싱 complete |
| Windows Server 2022 / Node 24.19.0 / Python 3.11 | 28/28 통과, 건너뜀 없음 | 종료코드 0, `portal.js` 파싱 complete |

원격 로그의 성공 표식은 각각 `REA_ACCEPTANCE_OK Linux 6.7.0`과 `REA_ACCEPTANCE_OK Windows 6.7.0`이며 동일 샘플 SHA-256과 일치합니다. 단순 패키지 시작이나 종료코드만 확인한 것이 아니라 결과 그래프의 대상 파일 파싱 완료를 검사했습니다. 결과에는 동적 호출 등의 미해결 의미 관계도 남아 있으므로 런타임 동작이나 의미 관계 전체의 복원을 보장하지 않습니다.

Windows 러너에서 PowerShell 에이전트 설치 테스트도 실제 실행됐습니다. 7개 TOML 정의의 검사와 새 reverse 에이전트 설치·기존 사용자 정의 보존은 해당 설치 계약 테스트 범위입니다. 실제 사용자 PC 설치나 Codex 모델 세션 내 실행, 모든 Codex 제품 표면의 named-agent 지원까지 검증한 것은 아닙니다.

독립 리뷰는 동작·보안과 코드베이스 적합성을 구분해 수행했고, 리뷰어도 최종 원격 로그·정확한 소스 SHA·28개 테스트와 실제 파싱 성공을 확인했습니다. 범위 내 남은 BLOCKER/IMPORTANT는 발견되지 않았습니다. 현재 변경은 **ASAR 정적 분석 및 Codex 진입점 범위에서 merge-ready**입니다. 위 2026-10-20의 review-ready 판정은 당시 실패 상태에 대한 역사 기록이며 이 최종 결과가 현재 ASAR 범위의 준비 상태를 대체합니다. PR #12는 자동 병합하지 않습니다.

샌드박스 자체의 process-ownership 오류는 그대로이며 우회하지 않았습니다. 전체 분석 성공 근거는 실제 GitHub Actions OS 러너입니다. 네이티브/Ghidra, MCP 연결, JAR/WAR, 실제 고객 앱, macOS는 여전히 별도 검증 대상입니다.
