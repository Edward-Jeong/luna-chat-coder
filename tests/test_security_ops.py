"""Workflow checks for routing, scope, evidence integrity, and optional REA."""
import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
import subprocess

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'scripts/security-ops.py'
spec = importlib.util.spec_from_file_location('security_ops', SCRIPT)
ops = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ops)


class SecurityOpsTests(unittest.TestCase):
    def test_business_routing_corpus(self):
        cases = ops.read_json(ROOT / '.agents/skills/luna-security-ops/tests/routing-cases.json')
        for case in cases['cases']:
            with self.subTest(case=case['input']):
                result = ops.route(case['input'])
                self.assertEqual(result['primary'], case['expected'])
                self.assertTrue(result['advisory'])

    def test_tied_and_negated_routes_do_not_grant_authority(self):
        result = ops.route('malware graphql')
        self.assertEqual(result['confidence'], 'low')
        self.assertEqual(result['action'], 'semantic_review')
        self.assertTrue(ops.route('do not decompile')['advisory'])

    def sample_scope(self, target):
        return {'authorization': {'status': 'granted', 'evidence': 'synthetic owned fixture'},
                'network_profile': {'mode': 'offline_sample'},
                'scope': {'samples': [{'path': str(target), 'sha256': ops.sha256(target)}],
                          'allowed_actions': ['static_analysis']}}

    def test_scope_rejects_pending_changed_sample_and_unlisted_action(self):
        with tempfile.TemporaryDirectory() as temp:
            target = Path(temp) / 'app.asar'
            target.write_text('exports.test = true;')
            scope = self.sample_scope(target)
            self.assertTrue(ops.check_scope(scope, 'static_analysis', str(target))['allowed'])
            with self.assertRaises(ValueError):
                ops.check_scope(scope, 'launch', str(target))
            target.write_text('changed')
            with self.assertRaises(ValueError):
                ops.check_scope(scope, 'static_analysis', str(target))
            scope['authorization']['status'] = 'pending'
            with self.assertRaises(ValueError):
                ops.check_scope(scope, 'static_analysis', str(target))

    def test_live_scope_is_exact_and_prohibitions_win(self):
        scope = {'authorization': {'status': 'granted', 'evidence': 'lab ticket'},
                 'network_profile': {'mode': 'lab_only'},
                 'scope': {'assets': ['https://lab.invalid'], 'allowed_actions': ['http_get']}}
        self.assertTrue(ops.check_scope(scope, 'http_get', 'https://lab.invalid')['allowed'])
        with self.assertRaises(ValueError):
            ops.check_scope(scope, 'http_get', 'https://lab.invalid.evil')
        scope['scope']['prohibited_actions'] = ['http_get']
        with self.assertRaises(ValueError):
            ops.check_scope(scope, 'http_get', 'https://lab.invalid')

    def test_malformed_scope_cannot_turn_exact_membership_into_substrings(self):
        base = {'authorization': {'status': 'granted', 'evidence': 'ticket'},
                'network_profile': {'mode': 'lab_only'},
                'scope': {'assets': ['https://lab.invalid.evil'], 'allowed_actions': ['http_get_private']}}
        for field, bad in [('assets', 'https://lab.invalid.evil'),
                           ('allowed_actions', 'http_get_private'), ('prohibited_actions', 'http_get'),
                           ('assets', [123])]:
            with self.subTest(field=field, bad=bad):
                value = json.loads(json.dumps(base))
                value['scope'][field] = bad
                with self.assertRaises(ValueError):
                    ops.check_scope(value, 'http_get', 'https://lab.invalid')
        for value in [[], {'authorization': []}, {'authorization': {'status': 'granted'},
                                                 'network_profile': None}]:
            with self.assertRaises(ValueError):
                ops.check_scope(value, 'http_get', 'https://lab.invalid')

    def test_malformed_case_is_blocked_json_not_traceback(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / 'case.json'
            for value in [[], {'evidence': [None]}, {'findings': 'bad'},
                          {'findings': [{'id': [], 'evidence_ids': 'E1'}]}]:
                path.write_text(json.dumps(value))
                result = subprocess.run([sys.executable, str(SCRIPT), 'verify-case', str(path)],
                                        capture_output=True, text=True)
                self.assertEqual(result.returncode, 1)
                self.assertEqual(json.loads(result.stdout)['status'], 'blocked')
                self.assertNotIn('Traceback', result.stderr)

    def test_evidence_tamper_missing_links_and_escape_are_detected(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            artifact = root / 'scan.log'
            artifact.write_text('Synthetic Detect exit=11; no confirmed root cause')
            case = {'evidence': [{'id': 'E1', 'artifact': 'scan.log', 'sha256': ops.sha256(artifact)}],
                    'findings': [{'id': 'F1', 'evidence_ids': ['E1'], 'status': 'candidate',
                                  'confidence': 'medium'}]}
            path = root / 'case.json'
            path.write_text(json.dumps(case))
            self.assertTrue(ops.verify_case(path)['valid'])
            artifact.write_text('tampered')
            self.assertFalse(ops.verify_case(path)['valid'])
            case['evidence'][0]['artifact'] = '../outside'
            case['findings'][0]['evidence_ids'] = ['E404']
            case['findings'][0]['status'] = 'validated'
            path.write_text(json.dumps(case))
            errors = ops.verify_case(path)['errors']
            self.assertTrue(any('relative' in e for e in errors))
            self.assertTrue(any('reference' in e for e in errors))
            self.assertTrue(any('validation' in e for e in errors))

    def test_plan_never_executes_and_jar_is_not_claimed_supported(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            target = root / 'app.asar'
            target.write_text('module.exports = 1;')
            path = root / 'scope.json'
            path.write_text(json.dumps(self.sample_scope(target)))
            with patch.object(ops.subprocess, 'run', side_effect=AssertionError('unexpected execution')):
                result = ops.rea(path, target, 'javascript', sys.executable, '6.7.0')
                self.assertEqual(result['status'], 'planned')
            jar = root / 'app.jar'
            jar.write_bytes(b'PK')
            path.write_text(json.dumps(self.sample_scope(jar)))
            with self.assertRaisesRegex(ValueError, 'JAR/WAR'):
                ops.rea(path, jar, 'javascript', sys.executable, '6.7.0')

    def test_wrong_version_and_provider_failure_are_not_success(self):
        with tempfile.TemporaryDirectory() as temp:
            target = Path(temp) / 'sample.asar'
            target.write_text('module.exports = 1;')
            scope = Path(temp) / 'scope.json'
            scope.write_text(json.dumps(self.sample_scope(target)))
            with patch.object(ops.subprocess, 'run', return_value=subprocess.CompletedProcess([], 0, '6.6.0\n', '')) as run:
                with self.assertRaisesRegex(ValueError, 'version differs'):
                    ops.rea(scope, target, 'native', sys.executable, '6.7.0', True)
                self.assertEqual(run.call_count, 1)
            outcomes = [subprocess.CompletedProcess([], 0, '6.7.0\n', ''),
                        subprocess.CompletedProcess([], 1, '', 'provider unavailable')]
            with patch.object(ops.subprocess, 'run', side_effect=outcomes):
                self.assertEqual(ops.rea(scope, target, 'native', sys.executable, '6.7.0', True)['status'], 'failed')

    def test_cli_failures_are_machine_readable(self):
        result = subprocess.run([sys.executable, str(SCRIPT), 'verify-case', '/nonexistent/luna-case'],
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 1)
        self.assertEqual(json.loads(result.stdout)['status'], 'blocked')


if __name__ == '__main__':
    unittest.main()
