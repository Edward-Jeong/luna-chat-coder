# Luna Cost-Aware Model Router (선택형)

## 목적 및 경계

Luna의 **기존 Coding/Security/Incident 라우팅과 검증 정책은 그대로 유지**합니다. 이 도구는 일반 Codex CLI 실행 **전에** 작업을 분류해 메인 실행 모델을 선택하고, `codex exec --json` 실행에서 보고된 토큰 사용량을 로컬에 기록합니다. `AGENTS.md`만으로 이미 진행 중인 Codex 세션의 메인 모델을 변경할 수는 없습니다. 따라서 자연어 요청만으로 자동 선택하고 싶다면 아래 `run` 진입점으로 작업을 시작해야 합니다. Codex CLI가 설치 및 로그인되어 있어야 하고 선택한 모델을 실제 계정/제품에서 사용할 수 있어야 합니다.

Luna는 에이전트 정책의 이름이기도 하며, `gpt-6-luna`는 별도의 저비용 **모델 ID**입니다. 두 용어를 혼동하지 마십시오.

## 사용법

Python 3.10+ 표준 라이브러리만 사용합니다. Windows에서는 `python`, macOS/Linux에서는 `python3`로 실행합니다. 명령은 리포지토리 루트에서 실행합니다.

```bash
# API 호출·모델 사용 없이 판단만 확인
python3 scripts/luna_model_router.py plan "USAM 패키지 업데이트 장애 원인을 분석해 줘"

# 실제 Codex 실행; 토큰 사용량을 로컬에 기록
python3 scripts/luna_model_router.py run "USAM 패키지 업데이트 장애 원인을 분석해 줘"

# 코드 변경 규모 및 보안 위험을 명시적으로 전달
python3 scripts/luna_model_router.py run "인증 모듈 재설계 및 테스트" --risk critical --files 20

# 명령 검증만 수행(과금·토큰 소비 없음)
python3 scripts/luna_model_router.py run "이 문서 요약해 줘" --dry-run

# 모델별 총 토큰, 검증 성공률, API 상당액 추정치
python3 scripts/luna_model_router.py report
```

Codex 실행 종료 시 `run_id`가 stderr에 표시됩니다. 자동 실행 성공(종료 코드 0)만으로 테스트 통과를 주장할 수 없으므로 검증 결과는 별도로 입력합니다.

```bash
# 테스트/검토가 실제 통과했을 때만 등록
python3 scripts/luna_model_router.py record <run_id> --verification passed

# 테스트 실패 원인을 확인한 뒤 등록
python3 scripts/luna_model_router.py record <run_id> --verification failed --failure-reason reasoning
# 기타 실패 원인: environment, external, unknown
```

`plan`의 `--kind routine|coding|incident|security|architecture|reverse`, `--risk auto|low|medium|high|critical`, `--files N`, `--failed-runs N`, `--failure-reason reasoning|environment|external|unknown|none` 값은 판단에 반영됩니다. 매개변수 없이도 작업 문구로 1차 분류하지만 키워드 분류는 완전한 위험 분석이 아닙니다. 위험 작업에서는 `--risk`를 명시하십시오. 모델/추론 수준이 지원되지 않으면 Codex CLI 오류를 그대로 반환합니다. 별도 인증 우회나 자동 과금 수단은 없습니다.

## 결정 규칙

- 짧은 단순 요약: `gpt-6-luna`, 저위험 단일 파일 수정: `gpt-6.1-terra`
- 일반 개발: `gpt-6.1-sol` medium, 보안·장애 분석: Sol high
- 복잡한 설계·역공학/critical 작업: `gpt-6-astra` high
- 최근 동일 작업의 추론 한계가 **검증된** 실패가 2회 이상인 경우 상위 모델 승격
- 동일 업무 범주·모델에서 **검증 결과가 8건 이상** 누적되고 실패율이 25% 이상이며 추론 실패가 3건 이상이면 다음 작업을 한 단계 상향(고위험 요청은 동적 재분류 배제)
- 단순 종료 실패·환경 설정·외부 시스템 오류만으로 고가 모델에 승격하지 않음

현 단계는 재현 가능한 규칙 기반 라우팅이며 모델별 실측 품질 학습은 **증거가 충분히 수집된 경우에만** 작동합니다. 모델 가용성 점검, Codex 계정의 남은 할당량 조회, 실시간 API 가격 조회 및 프롬프트 품질의 자동 평가 기능은 포함되지 않습니다. 서로 다른 난도의 작업을 무작위 배정한 A/B 성능 평가를 수행하는 기능도 아닙니다.

## 사용량, 비용 및 개인정보

- 기본 기록: `~/.codex/luna/usage.jsonl`. 다른 위치는 전역 옵션 `--metrics-file`로 지정합니다.
- `codex exec --json`의 `turn.completed.usage` 중 input/output/cached input 토큰만 누적합니다. 해당 이벤트가 누락되면 사용량은 `null`(미확인)로 표시합니다.
- 원문 요청, 코드, Codex JSONL 추적, 대화, 파일 내용, API 키는 기록하지 않습니다. 콘솔에는 Codex의 최종 답변이 표시되므로 출력 공개 범위는 사용자의 터미널 환경에 따릅니다.
- 성공률 분모는 별도로 `record --verification`된 건만 사용합니다. 실행 성공과 검증 성공을 구분합니다.
- 비용은 **2026-11-14 기준 표준 API 단가를 적용한 참고용 USD 상당액**입니다. 실제 Codex 구독 크레딧/추가 결제액/긴 컨텍스트 가격/지역 가산액이 아니며 모델 가격이나 과금 정책은 변할 수 있습니다. 근거: https://developers.openai.com/api/docs/pricing
- 실행 전 예상 토큰은 임의 추정하지 않습니다. 토큰 수는 실제 Codex 이벤트에서 확인합니다. 입력 파일, 이미지 등에는 단순 글자 수 환산을 사용하지 않습니다.
- 지표는 사용자 컴퓨터에만 저장하고 Git에는 커밋하지 마십시오. 삭제 시 라우팅 학습 이력이 초기화됩니다.

## 검증

```bash
python3 -m unittest discover -s tests -v
python3 -m py_compile scripts/luna_model_router.py
```

로컬/CI 테스트는 모의 Codex CLI로 옵션 전달과 이벤트 파싱을 검증합니다. 실제 Codex 계정 연동·요금 청구를 발생시키는 E2E 테스트는 수행하지 않으며 별도의 사용자 환경 점검이 필요합니다. 독립 코드 리뷰 없이 PR은 `review-ready`로 유지합니다.

## 출처

- Codex CLI의 `exec --json` 및 사용량 이벤트: https://developers.openai.com/blog/eval-skills
- 모델 ID와 추론 수준: https://developers.openai.com/api/docs/models
- API 표준 과금: https://developers.openai.com/api/docs/pricing
