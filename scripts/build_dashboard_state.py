#!/usr/bin/env python3
"""Build read-only JSON state for the Commander dashboard.

No secrets, no writes outside COMMANDER/dashboard/state.json, no service changes.
"""
from __future__ import annotations

import csv
import json
import os
import re
import socket
import subprocess
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOV = Path('/home/josh/sovereignty_stack')
OUT = ROOT / 'dashboard' / 'state.json'


def read(path: Path, default: str = '') -> str:
    try:
        return path.read_text(errors='replace')
    except FileNotFoundError:
        return default


def run(cmd: list[str], timeout: int = 12) -> dict:
    try:
        p = subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True, timeout=timeout)
        return {'ok': p.returncode == 0, 'code': p.returncode, 'out': redact(p.stdout.strip()), 'err': redact(p.stderr.strip())}
    except Exception as e:
        return {'ok': False, 'code': None, 'out': '', 'err': str(e)}


def redact(text: str) -> str:
    text = re.sub(r'\b\d{8,10}:[A-Za-z0-9_-]{25,}\b', '[TELEGRAM_TOKEN_REDACTED]', text)
    text = re.sub(r'(?i)(api[_-]?key|secret|password|token)\s*[:=]\s*\S+', r'\1=[REDACTED]', text)
    return text


def section_after(text: str, heading: str, fallback: str = '') -> str:
    idx = text.find(heading)
    if idx < 0:
        return fallback
    part = text[idx + len(heading):].strip()
    # Stop at next emoji/all-caps style section or markdown heading.
    m = re.search(r'\n(?:[A-Z✅👀🚦➡️💰🌅][^\n]{0,70}\n|#{1,3}\s)', part)
    if m:
        part = part[:m.start()].strip()
    return part.strip() or fallback


def first_nonempty_lines(text: str, limit: int = 3) -> list[str]:
    lines = []
    for raw in text.splitlines():
        line = raw.strip().lstrip('-').strip()
        if line:
            lines.append(line)
        if len(lines) >= limit:
            break
    return lines


def first_section_lines(text: str, headings: list[str], limit: int = 3, fallback: str = '') -> list[str]:
    for heading in headings:
        lines = first_nonempty_lines(section_after(text, heading), limit)
        if lines:
            return lines
    return [fallback] if fallback else []


def parse_tasks(md: str) -> list[dict]:
    tasks = []
    for line in md.splitlines():
        if not line.startswith('|') or '|----' in line or '| ID ' in line:
            continue
        cells = [c.strip().strip('`') for c in line.strip('|').split('|')]
        if len(cells) < 7:
            continue
        task_id, project, pri, task, status, next_action, approval = cells[:7]
        if not re.match(r'^[A-Z]+-\d+', task_id):
            continue
        tasks.append({
            'id': task_id,
            'project': project,
            'priority': pri,
            'task': task,
            'status': status,
            'next_action': next_action,
            'approval': 'yes' if 'yes' in approval.lower() else 'no',
        })
    return tasks


def strip_md(text: str) -> str:
    return re.sub(r'[`*_]', '', text).strip()


def parse_project_cards() -> list[dict]:
    cards = []
    for file in sorted((ROOT / 'projects').glob('*.md')):
        text = read(file)
        if not text.strip():
            continue
        title_match = re.search(r'^#\s+Project:\s*(.+)$', text, re.M) or re.search(r'^#\s*(.+)$', text, re.M)
        title = strip_md(title_match.group(1)) if title_match else file.stem.replace('-', ' ').title()
        status_match = re.search(r'##\s*Status[^\n]*\n(.*?)(?=\n##\s|\Z)', text, re.S)
        if not status_match:
            continue
        block = status_match.group(1).strip()
        lines = []
        for raw in block.splitlines():
            line = raw.strip()
            if not line:
                continue
            if line.startswith('- '):
                line = line[2:].strip()
            lines.append(strip_md(line))
            if len(lines) >= 4:
                break
        if not lines:
            continue
        def pick(prefix: str) -> str:
            for line in lines:
                if line.lower().startswith(prefix):
                    return line[len(prefix):].strip(' :-')
            return ''
        cards.append({
            'id': file.stem,
            'title': title,
            'path': str(file.relative_to(ROOT)),
            'status_lines': lines[:4],
            'state': pick('state:'),
            'last_advanced': pick('last advanced:'),
            'next_action': pick('next action:'),
            'waiting_on': pick('waiting on:'),
        })
    return cards


def parse_goal_numbers(goals: str) -> dict:
    return {
        'sprint_target': '$6.9K in 69 days',
        'passive_income_target': '$6.9K/month in 1 year',
        'weekly_time_budget': '10–20 hrs/week',
        'weekly_cash_budget': '~$100/week',
    }


def local_ip() -> str:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 80))
        return s.getsockname()[0]
    except Exception:
        return 'unknown'
    finally:
        s.close()


def parse_hermes_status() -> dict:
    status = run(['/home/josh/.local/bin/hermes', '--profile', 'commander', 'status', '--all'], timeout=30)
    out = status['out']
    def find(pattern: str, default='unknown'):
        m = re.search(pattern, out, re.M)
        return m.group(1).strip() if m else default
    return {
        'raw_ok': status['ok'],
        'provider': find(r'Provider:\s+(.+)'),
        'model': find(r'Model:\s+(.+)'),
        'telegram': 'configured' if 'Telegram      ✓ configured' in out else 'unknown',
        'gateway': 'running' if 'Status:       ✓ running' in out or 'Gateway is running' in out else 'unknown',
        'scheduled_jobs': find(r'Jobs:\s+(.+)'),
        'active_sessions': find(r'Active:\s+(.+session\(s\))'),
    }


def parse_cron() -> dict:
    res = run(['/home/josh/.local/bin/hermes', '--profile', 'commander', 'cron', 'list'], timeout=25)
    out = res['out']
    return {
        'ok': res['ok'],
        'daily_loop_active': 'daily-money-loop' in out and '[active]' in out,
        'next_run': (re.search(r'Next run:\s+(.+)', out) or ['','unknown'])[1].strip(),
        'deliver': (re.search(r'Deliver:\s+(.+)', out) or ['','unknown'])[1].strip(),
        'last_run': (re.search(r'Last run:\s+(.+)', out) or ['','unknown'])[1].strip(),
    }


def service_inventory() -> list[dict]:
    overview = read(SOV / 'STACK_OVERVIEW.md')
    names = ['CasaOS', 'Immich', 'Grafana', 'Uptime Kuma', 'Tailscale', 'ticker-service', 'wallet-service', 'resource-service']
    files = {
        'ticker-service': SOV / 'ticker-service' / 'server.py',
        'wallet-service': SOV / 'wallet-service' / 'server.py',
        'resource-service': SOV / 'resource-service' / 'server.py',
    }
    services = []
    for name in names:
        present = name.lower() in overview.lower() or (name in files and files[name].exists())
        status = 'known' if present else 'unknown'
        if name in files and files[name].exists():
            status = 'code present'
        services.append({'name': name, 'status': status, 'present': present})
    return services


def docker_snapshot() -> dict:
    if not run(['bash', '-lc', 'command -v docker'], timeout=5)['ok']:
        return {'available': False, 'containers': []}
    res = run(['docker', 'ps', '--format', '{{.Names}}|{{.Status}}|{{.Ports}}'], timeout=10)
    containers = []
    if res['ok']:
        for line in res['out'].splitlines():
            parts = line.split('|', 2)
            if len(parts) == 3:
                containers.append({'name': parts[0], 'status': parts[1], 'ports': parts[2]})
    return {'available': True, 'containers': containers[:12], 'ok': res['ok'], 'error': res['err'][:160]}


def git_snapshot() -> dict:
    status = run(['git', 'status', '--short'], timeout=8)['out'].splitlines()
    branch = run(['git', 'branch', '--show-current'], timeout=8)['out'] or 'unknown'
    head = run(['git', 'rev-parse', '--short', 'HEAD'], timeout=8)['out'] or 'unknown'
    return {'branch': branch, 'head': head, 'dirty_count': len(status), 'changes': status[:12]}


def main() -> None:
    now_md = read(ROOT / 'NOW.md')
    goals_md = read(ROOT / 'GOALS.md')
    tasks = parse_tasks(read(ROOT / 'TASK_QUEUE.md'))
    projects = parse_project_cards()
    morning = read(ROOT / 'MORNING_REPORT.md')
    doing = [t for t in tasks if t['status'] == 'doing']
    blocked = [t for t in tasks if t['status'] == 'blocked']
    todo = [t for t in tasks if t['status'] == 'todo']
    approval = [t for t in tasks if t['approval'] == 'yes' and t['status'] not in ('done',)]

    money_lines = first_section_lines(
        morning,
        ["💰 TODAY'S MONEY MOVE", "💰 TODAY'S REAL MONEY MOVE"],
        1,
        'Clean the operating loop before adding more features.',
    )
    review_lines = first_section_lines(
        morning,
        ['👀 YOUR 60-SECOND REVIEW'],
        4,
        'Open: NOW.md',
    )

    state = {
        'generated_at': datetime.now(timezone.utc).isoformat(),
        'host': {'name': socket.gethostname(), 'lan_ip': local_ip(), 'cwd': str(ROOT)},
        'goals': parse_goal_numbers(goals_md),
        'focus': {
            'active': (re.search(r'\*\*Active focus:\*\*\s*(.+)', now_md) or ['','unknown'])[1],
            'next3': re.findall(r'^\d+\.\s+(.+)', now_md, flags=re.M)[:3],
            'money_move': money_lines[0],
            'review': review_lines,
        },
        'tasks': {'all': tasks, 'doing': doing, 'blocked': blocked, 'todo': todo[:8], 'approval': approval[:8], 'counts': {s: sum(1 for t in tasks if t['status'] == s) for s in ['doing','blocked','todo','done']}},
        'projects': projects,
        'lanes': projects,
        'hermes': parse_hermes_status(),
        'cron': parse_cron(),
        'git': git_snapshot(),
        'sovereignty': {'path': str(SOV), 'services': service_inventory(), 'docker': docker_snapshot()},
        'learning': {
            'today': 'Dashboards are decision systems: surface the next action, hide the noise.',
            'qol': 'Telegram for quick steering; dashboard for cockpit review; PuTTY only for maintenance.',
            'system_rule': 'Private/Tailscale first. Read-only before action buttons.',
        },
        'safety': ['no public ports', 'no secrets displayed', 'no spending', 'no outbound posting/sending without approval'],
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(state, indent=2, ensure_ascii=False) + '\n')
    print(f'wrote {OUT} ({OUT.stat().st_size} bytes)')


if __name__ == '__main__':
    main()
