#!/usr/bin/env python3
"""Local, idempotent experience journal. Does not change skill instructions or run UI."""
import argparse
from contextlib import contextmanager
from datetime import datetime, timezone
import fcntl
import json
import os
from pathlib import Path
import tempfile

DEFAULT_STORE = Path(__file__).resolve().parents[1] / 'learning' / 'experience.json'


def now():
    return datetime.now(timezone.utc).isoformat(timespec='seconds')


@contextmanager
def locked_store(path):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.with_suffix('.lock').open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        data = json.loads(path.read_text()) if path.exists() else {'schemaVersion': 1, 'uses': {}}
        if data.get('schemaVersion') != 1 or not isinstance(data.get('uses'), dict):
            raise ValueError('Unsupported or damaged experience store; preserve it for diagnosis')
        yield data
        fcntl.flock(lock, fcntl.LOCK_UN)


def save(path, data):
    tmp = None
    try:
        with tempfile.NamedTemporaryFile('w', dir=path.parent, delete=False) as handle:
            tmp = Path(handle.name)
            json.dump(data, handle, ensure_ascii=False, indent=2, allow_nan=False)
            handle.write('\n')
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(tmp, path)
    finally:
        if tmp is not None:
            tmp.unlink(missing_ok=True)


def checked_report(path):
    report = json.loads(path.read_text())
    if not isinstance(report, dict):
        raise ValueError('Report must be an object')
    allowed = {'outcome', 'summary', 'checks', 'observations', 'feedback'}
    if set(report) - allowed:
        raise ValueError('Unknown report fields')
    if report.get('outcome') not in ('completed', 'partial', 'failed'):
        raise ValueError('outcome must be completed, partial or failed')
    if not isinstance(report.get('summary'), str) or not report['summary'].strip():
        raise ValueError('A nonempty summary is required')
    checks = report.get('checks', [])
    if not isinstance(checks, list) or not all(isinstance(c, str) for c in checks):
        raise ValueError('checks must be a list of descriptions of checks actually run')
    observations = report.get('observations', [])
    if not isinstance(observations, list):
        raise ValueError('observations must be a list')
    for item in observations:
        if not isinstance(item, dict) or set(item) != {'kind', 'text', 'evidence'}:
            raise ValueError('Observation fields: kind, text, evidence')
        if item['kind'] not in ('verified_fact', 'user_preference', 'hypothesis'):
            raise ValueError('Invalid observation kind')
        if not isinstance(item['text'], str) or not item['text'].strip():
            raise ValueError('Observation text is required')
        refs = item['evidence']
        if not isinstance(refs, list) or not all(isinstance(r, str) and r.strip() for r in refs):
            raise ValueError('evidence must be a list of references')
        if item['kind'] != 'hypothesis' and not refs:
            raise ValueError('Facts and preferences require evidence references')
    feedback = report.get('feedback', {'state': 'pending', 'note': ''})
    if not isinstance(feedback, dict) or set(feedback) != {'state', 'note'}:
        raise ValueError('feedback fields: state, note')
    if feedback['state'] not in ('pending', 'approved', 'changes_requested', 'not_requested'):
        raise ValueError('Invalid feedback state')
    if not isinstance(feedback['note'], str):
        raise ValueError('feedback.note must be text')
    report['checks'], report['observations'], report['feedback'] = checks, observations, feedback
    return report


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--store', type=Path, default=DEFAULT_STORE, help='Override for isolated tests')
    sub = p.add_subparsers(dest='command', required=True)
    show = sub.add_parser('show')
    show.add_argument('--limit', type=int, default=5)
    start = sub.add_parser('start')
    start.add_argument('--id', required=True, help='Stable ID for one video task, reused across its revisions')
    start.add_argument('--scope', required=True, help='Project/scenario label, not a global preference')
    start.add_argument('--task', required=True)
    finish = sub.add_parser('finish')
    finish.add_argument('--id', required=True)
    finish.add_argument('--report', type=Path, required=True)
    args = p.parse_args()
    report = checked_report(args.report) if args.command == 'finish' else None
    with locked_store(args.store) as data:
        uses = data['uses']
        if args.command == 'start':
            if not all(v.strip() for v in (args.id, args.scope, args.task)):
                p.error('id, scope and task must be nonempty')
            if args.id not in uses:
                uses[args.id] = {'scope': args.scope, 'task': args.task, 'startedAt': now(),
                                 'status': 'started', 'reports': []}
                save(args.store, data)
            elif (uses[args.id]['scope'], uses[args.id]['task']) != (args.scope, args.task):
                p.error('Existing ID belongs to another scope/task; choose a distinct ID')
            print(json.dumps({'id': args.id, 'status': uses[args.id]['status'],
                              'trackedUses': len(uses)}, ensure_ascii=False))
        elif args.command == 'finish':
            if args.id not in uses:
                p.error('Unknown use ID; start it first')
            use = uses[args.id]
            # Retain later corrections/feedback without inflating the use count.
            if not use['reports'] or use['reports'][-1]['report'] != report:
                use['reports'].append({'recordedAt': now(), 'report': report})
                use['status'] = report['outcome']
                save(args.store, data)
            print(json.dumps({'id': args.id, 'status': use['status'],
                              'trackedUses': len(uses), 'reportVersions': len(use['reports'])}, ensure_ascii=False))
        else:
            if not 1 <= args.limit <= 20:
                p.error('limit must be between 1 and 20')
            recent = sorted(uses.items(), key=lambda kv: kv[1]['reports'][-1]['recordedAt']
                            if kv[1]['reports'] else kv[1]['startedAt'], reverse=True)[:args.limit]
            print(json.dumps({'trackedUses': len(uses),
                              'outcomes': {s: sum(u['status'] == s for u in uses.values())
                                           for s in ('started', 'completed', 'partial', 'failed')},
                              'recent': [dict(id=k, scope=v['scope'], task=v['task'], status=v['status'],
                                              latest=v['reports'][-1]['report'] if v['reports'] else None)
                                         for k, v in recent]}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
