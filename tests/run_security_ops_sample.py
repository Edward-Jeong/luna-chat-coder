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
    parser.add_argument('--node', help='absolute native Node executable with REA .mjs')
    args = parser.parse_args()
    if bool(args.rea) != bool(args.version):
        parser.error('--rea and --version must be supplied together')
    if args.node and not args.rea:
        parser.error('--node requires --rea')
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
            result['rea'] = ops.rea(scope_file, sample, 'javascript', args.rea, args.version, True, args.node)
            # Exit zero alone does not establish that the static parser completed.
            output = json.loads(result['rea'].get('stdout', '{}'))
            observations = [observation for item in output.get('normalized_result', {}).get('graph', {}).get('nodes', [])
                            for observation in item.get('observations', [])]
            parsed = any(o.get('label') == 'portal.js'
                         and o.get('properties', {}).get('parse_status') == 'complete'
                         for o in observations)
            result['rea']['sample_parse_complete'] = parsed
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 1 if (failures or not before or not tamper_detected
                     or result['rea']['status'] == 'failed'
                     or (args.rea and not result['rea']['sample_parse_complete'])) else 0


if __name__ == '__main__':
    raise SystemExit(main())
