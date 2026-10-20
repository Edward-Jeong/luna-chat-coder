#!/usr/bin/env python3
"""Reproduce synthetic business cases; optional REA acceptance, no target execution."""
import argparse
import base64
import importlib.util
import json
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('security_ops', ROOT / 'scripts/security-ops.py')
ops = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ops)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--rea', help='absolute trusted REA executable; executes static analysis when supplied')
    parser.add_argument('--version', help='exact installed version, required with --rea')
    args = parser.parse_args()
    if bool(args.rea) != bool(args.version):
        parser.error('--rea and --version must be supplied together')
    cases = ops.read_json(ROOT / '.agents/skills/luna-security-ops/tests/routing-cases.json')['cases']
    failures = [c for c in cases if ops.route(c['input'])['primary'] != c['expected']]
    with tempfile.TemporaryDirectory(prefix='luna-security-sample-') as temp:
        root = Path(temp)
        sample = root / 'portal.asar'
        sample.write_bytes(base64.b64decode((ROOT / 'tests/fixtures/security-ops/portal.asar.b64').read_text(), validate=False))
        scope = {'authorization': {'status': 'granted', 'evidence': 'owned synthetic sample runner'},
                 'network_profile': {'mode': 'offline_sample'},
                 'scope': {'allowed_actions': ['static_analysis'],
                           'samples': [{'path': str(sample), 'sha256': ops.sha256(sample)}]}}
        scope_file = root / 'scope.json'
        scope_file.write_text(json.dumps(scope))
        log = root / 'detect.log'
        log.write_text('SYNTHETIC: Detect exit=11, components=0; root cause unverified.\n')
        case = {'evidence': [{'id': 'E1', 'artifact': 'detect.log', 'sha256': ops.sha256(log)}],
                'findings': [{'id': 'F1', 'evidence_ids': ['E1'], 'status': 'candidate', 'confidence': 'medium'}]}
        case_file = root / 'case.json'
        case_file.write_text(json.dumps(case))
        before = ops.verify_case(case_file)['valid']
        log.write_text('changed')
        tamper_detected = not ops.verify_case(case_file)['valid']
        result = {'synthetic_data': True, 'routing_cases': len(cases), 'routing_failures': failures,
                  'evidence_valid_before': before, 'evidence_tamper_detected': tamper_detected,
                  'sample_sha256': ops.sha256(sample), 'rea': {'status': 'not_run'}}
        if args.rea:
            result['rea'] = ops.rea(scope_file, sample, 'javascript', args.rea, args.version, True)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 1 if failures or not before or not tamper_detected or result['rea']['status'] == 'failed' else 0


if __name__ == '__main__':
    raise SystemExit(main())
