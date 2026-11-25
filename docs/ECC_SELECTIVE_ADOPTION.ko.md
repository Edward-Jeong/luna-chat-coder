# ECC 핵심 기능의 Luna 선택 흡수

원본: https://github.com/affaan-m/ECC (MIT License,
Copyright (c) 2026 Affaan Mustafa).

## 결정

기존 Luna Core Engineering Protocol v2, Agent Teams, Quality Engineering,
Security Ops, Cost-Aware Model Router의 역할과 설정을 유지한다.
ECC 자체를 추가 프레임워크로 설치하거나 Luna 모델/정책을 덮어쓰지 않는다.

| ECC 참고 영역 | Luna에 반영한 내용 | 활성화 조건 |
| --- | --- | --- |
| Change Impact | 변경 전후 영향 범위와 실제 diff를 비교하는 기존 품질 게이트 보강 | 고위험/교차 모듈 변경 |
| MCP Dependency Review | 읽기 전용 표준 라이브러리 기반 패키지 선택자 점검 CLI와 단위 테스트 | MCP 설정 또는 패키지 변경 |
| Eval Harness | 기존 라우터 테스트와 검증 결과를 활용하는 평가 설계 기준 | 라우터·스킬·모델 정책 변경 |

기술 계약과 비적용 범위:
.agents/skills/luna-quality-engineering/references/ecc-selective-adoption.md

## 검사 방법

~~~bash
python scripts/luna_mcp_audit.py --root .
python scripts/luna_mcp_audit.py --root . --config .mcp.json --fail-on-mutable
python -m unittest discover -s tests -p 'test_luna_mcp_audit.py' -v
~~~

스크립트는 외부 MCP를 실행하거나 설치하지 않고, 저장소 안의 지정된
설정 파일만 읽는다. Python 3.11 이상은 TOML을 파싱하며 Python 3.10에서는
TOML을 수동 검토 대상으로 보고한다. 직접 npm 선택자의 고정 여부만
판정하며 공급망 취약점 점검이나 Lockfile 분석을 대체하지 않는다.

## 반영하지 않는 기능

ECC 전역 설치·자동 동기화, 추가 모델 라우터, 중복 에이전트 팀,
강제 80% 커버리지, 전역 Git hooks, 별도 Memory Vault,
외부 MCP 자동 실행·설치, 기존 프로젝트 일괄 변경은 제외한다.

## 검증

단위 테스트/CI 결과와 실제 Codex 환경 동작 검증은 별개이다.
기존 프로젝트 반영은 별도 영향도 검토와 명시적인 갱신을 통해 수행한다.
