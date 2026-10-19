#!/usr/bin/env python3
"""Optional, standard-library Security Ops helpers. No installs or global writes."""
import argparse
import hashlib
import json
import re
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / '.agents/skills/luna-security-ops/config/routing.json'


def read_json(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def object_value(value, label):
    if not isinstance(value, dict):
        raise ValueError(f'{label} must be an object')
    return value


def string_array(value, label):
    if not isinstance(value, list) or any(not isinstance(item, str) or not item for item in value):
        raise ValueError(f'{label} must be an array of nonempty strings')
    return value


def sha256(path):
    digest = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for block in iter(lambda: stream.read(65536), b''):
            digest.update(block)
    return digest.hexdigest()


def route(hint):
    """Advisory lexical triage; the agent's semantic team decision stays canonical."""
    config = read_json(CONFIG)
    text = hint.casefold()
    matches = []
    for rule in config['routes']:
        hits = [word for word in rule['keywords'] if word.casefold() in text]
        if hits:
            matches.append((len(hits), rule, hits))
    matches.sort(key=lambda row: -row[0])  # stable configuration order breaks ties
    if not matches:
        return {'primary': 'unmatched', 'confidence': 'low', 'matches': [],
                'advisory': True, 'action': 'semantic_review'}
    score, rule, hits = matches[0]
    tied = len(matches) > 1 and matches[1][0] == score
    return {'primary': rule['capability'], 'confidence': 'low' if tied else 'medium',
            'matches': hits, 'alternatives': [r['capability'] for _, r, _ in matches[1:]],
            'advisory': True, 'action': 'semantic_review' if tied else 'confirm_intent'}


def check_scope(scope, action, asset):
    """Exact asset/action admission; scope declarations are not OS isolation."""
    scope = object_value(scope, 'scope document')
    authorization = object_value(scope.get('authorization'), 'authorization')
    profile = object_value(scope.get('network_profile'), 'network_profile')
    boundary = object_value(scope.get('scope'), 'scope')
    allowed = string_array(boundary.get('allowed_actions'), 'allowed_actions')
    prohibited = string_array(boundary.get('prohibited_actions', []), 'prohibited_actions')
    assets = string_array(boundary.get('assets', []), 'assets')
    if authorization.get('status') != 'granted':
        raise ValueError('authorization must be granted')
    if not isinstance(authorization.get('evidence'), str) or not authorization['evidence'].strip():
        raise ValueError('authorization evidence is required')
    mode = profile.get('mode')
    if mode not in {'offline_sample', 'authorized_target_only', 'lab_only'}:
        raise ValueError('unsupported execution network profile')
    if action in prohibited:
        raise ValueError('action is prohibited')
    if action not in allowed:
        raise ValueError('action is outside scope')
    if mode == 'offline_sample':
        if action != 'static_analysis':
            raise ValueError('offline sample permits static_analysis only')
        selected = Path(asset).resolve(strict=True)
        if not selected.is_file():
            raise ValueError('sample must be a regular file')
        samples = boundary.get('samples', [])
        if not isinstance(samples, list):
            raise ValueError('samples must be an array')
        for item in samples:
            object_value(item, 'sample')
            if (not isinstance(item.get('path'), str) or not Path(item['path']).is_absolute()
                    or not isinstance(item.get('sha256'), str)
                    or not re.fullmatch(r'[0-9a-f]{64}', item['sha256'])):
                raise ValueError('sample needs an absolute path and lowercase SHA-256')
        admitted = any(Path(item['path']).resolve(strict=True) == selected
                       and item['sha256'] == sha256(selected) for item in samples)
        if not admitted:
            raise ValueError('sample path/digest is outside scope')
    elif asset not in assets:
        raise ValueError('asset is outside scope (exact match required)')
    return {'allowed': True, 'action': action, 'asset': asset, 'network_profile': mode,
            'limitation': 'declaration check only; no sandbox or network enforcement'}


def verify_case(case_path):
    """Check JSON evidence links and case-local artifact hashes without mutations."""
    source = Path(case_path).resolve(strict=True)
    case = object_value(read_json(source), 'case')
    root = source.parent
    errors, ids = [], set()
    evidence = case.get('evidence', [])
    if not isinstance(evidence, list):
        raise ValueError('evidence must be an array')
    for item in evidence:
        object_value(item, 'evidence record')
        identity = item.get('id')
        if not isinstance(identity, str) or not identity or identity in ids:
            errors.append('missing or duplicate evidence ID')
        else:
            ids.add(identity)
        raw = item.get('artifact')
        if not isinstance(raw, str) or not raw or Path(raw).is_absolute() or '..' in Path(raw).parts:
            errors.append(f'{identity}: artifact must be a case-relative path')
            continue
        artifact = (root / raw).resolve()
        if not artifact.is_relative_to(root) or not artifact.is_file():
            errors.append(f'{identity}: artifact missing or escapes case root')
        elif item.get('sha256') != sha256(artifact):
            errors.append(f'{identity}: digest mismatch')
    finding_ids = set()
    findings = case.get('findings', [])
    if not isinstance(findings, list):
        raise ValueError('findings must be an array')
    for finding in findings:
        object_value(finding, 'finding')
        identity = finding.get('id')
        if not isinstance(identity, str) or not identity or identity in finding_ids:
            errors.append('missing or duplicate finding ID')
        else:
            finding_ids.add(identity)
        refs = string_array(finding.get('evidence_ids', []), 'evidence_ids')
        if not refs or any(ref not in ids for ref in refs):
            errors.append(f'{identity}: missing evidence reference')
        if finding.get('status') not in {'candidate', 'validated', 'false_positive', 'accepted_risk'}:
            errors.append(f'{identity}: invalid finding status')
        if finding.get('confidence') not in {'high', 'medium', 'low'}:
            errors.append(f'{identity}: invalid confidence')
        if finding.get('status') == 'validated' and (
                not isinstance(finding.get('validation'), str) or not finding['validation'].strip()):
            errors.append(f'{identity}: validated finding needs a validation explanation')
    return {'valid': not errors, 'errors': errors, 'evidence_count': len(evidence),
            'limitation': 'checks structure and fixity, not truth or independent validation'}


def doctor():
    # Discovery only. Even --version is code execution, so do not probe found tools here.
    return {'tools': {name: {'status': 'found' if (path := shutil.which(name)) else 'missing',
                             'path': str(Path(path).absolute()) if path else None,
                             'version': None, 'verification': 'not executed'}
                      for name in ('rea', 'java', 'tshark', 'semgrep', 'trivy')},
            'mcp': 'not observed; CLI presence does not establish an MCP connection'}


def rea(scope_path, target, kind, executable, version, execute=False):
    """Plan/run only two static CLI operations using an explicitly selected install."""
    scope = read_json(scope_path)
    object_value(scope, 'scope document')
    if object_value(scope.get('network_profile'), 'network_profile').get('mode') != 'offline_sample':
        raise ValueError('REA adapter requires offline_sample scope')
    target_path = Path(target).resolve(strict=True)
    gate = check_scope(scope, 'static_analysis', str(target_path))
    if not re.fullmatch(r'\d+\.\d+\.\d+', version):
        raise ValueError('expected version must be an exact stable semver')
    if kind not in {'javascript', 'native'}:
        raise ValueError('REA adapter supports javascript or native only; JAR/WAR needs a Java workflow')
    if target_path.suffix.lower() in {'.jar', '.war'}:
        raise ValueError('JAR/WAR is not admitted by the REA adapter')
    if kind == 'javascript' and target_path.suffix.lower() != '.asar':
        raise ValueError('JavaScript application analysis requires an ASAR file; directory scope is not supported')
    command_path = Path(executable)
    if not command_path.is_absolute() or not command_path.is_file():
        raise ValueError('choose an existing absolute REA executable path; no automatic install')
    command = ([str(command_path), 'analyze-javascript-application', str(target_path), '--json']
               if kind == 'javascript' else
               [str(command_path), 'inspect', str(target_path), '--provider', 'ghidra', '--format', 'json'])
    result = {'status': 'planned', 'command': command, 'expected_version': version,
              'target_sha256': sha256(target_path), 'scope': gate,
              'limitation': 'static provider execution is not a sandbox; results may contain sensitive content'}
    if not execute:
        return result
    observed = subprocess.run([str(command_path), '--version'], capture_output=True,
                              text=True, timeout=30, check=True)
    # Accept the plain CLI version or a labelled `rea[-agents] X.Y.Z` line only.
    if not re.fullmatch(r'(?:rea(?:-agents)?\s+)?' + re.escape(version), observed.stdout.strip()):
        raise ValueError('installed REA version differs from the selected version')
    check_scope(scope, 'static_analysis', str(target_path))
    completed = subprocess.run(command, capture_output=True, text=True, timeout=360, check=False)
    result.update(status='succeeded' if completed.returncode == 0 else 'failed',
                  returncode=completed.returncode, stdout=completed.stdout, stderr=completed.stderr,
                  tool_version=version)
    if sha256(target_path) != result['target_sha256']:
        raise ValueError('target changed during analysis')
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='command', required=True)
    routing = commands.add_parser('route')
    routing.add_argument('hint')
    commands.add_parser('doctor')
    verify = commands.add_parser('verify-case')
    verify.add_argument('case')
    gate = commands.add_parser('check-scope')
    gate.add_argument('--scope', required=True)
    gate.add_argument('--action', required=True)
    gate.add_argument('--asset', required=True)
    adapter = commands.add_parser('rea')
    adapter.add_argument('--scope', required=True)
    adapter.add_argument('--target', required=True)
    adapter.add_argument('--kind', choices=['javascript', 'native'], required=True)
    adapter.add_argument('--executable', required=True)
    adapter.add_argument('--version', required=True)
    adapter.add_argument('--execute', action='store_true')
    args = parser.parse_args()
    try:
        if args.command == 'route':
            result = route(args.hint)
        elif args.command == 'doctor':
            result = doctor()
        elif args.command == 'verify-case':
            result = verify_case(args.case)
        elif args.command == 'check-scope':
            result = check_scope(read_json(args.scope), args.action, args.asset)
        else:
            result = rea(args.scope, args.target, args.kind, args.executable, args.version, args.execute)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 1 if result.get('valid') is False or result.get('status') == 'failed' else 0
    except (OSError, ValueError, KeyError, TypeError, subprocess.SubprocessError) as error:
        print(json.dumps({'status': 'blocked', 'error': str(error)}, ensure_ascii=False))
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
