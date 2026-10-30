#!/usr/bin/env python3
"""Offline structural checks; this does not evaluate an LLM or render video."""
import argparse
import json
import re
from pathlib import Path
from urllib.parse import unquote, urlsplit


def validate(root):
    errors = []
    skills = sorted(root.glob('*/educational-video/SKILL.md'))
    if len(skills) != 1:
        errors.append('Expected exactly one educational-video skill entry')
    for entry in skills:
        folder = entry.parent
        for path in (entry, folder / 'SKILL.zh.md'):
            if not path.is_file():
                errors.append(f'Missing translation: {path.relative_to(root)}')
                continue
            text = path.read_text(encoding='utf-8')
            if not re.match(r'\A---\nname: educational-video\ndescription: .+\n---\n', text):
                errors.append(f'Invalid expected skill frontmatter: {path.relative_to(root)}')
        for path in folder.rglob('*.md'):
            for target in local_targets(path):
                if not target.is_relative_to(folder.resolve()):
                    errors.append(f'Skill is not self-contained: {path.relative_to(root)} -> {target}')

    for path in root.rglob('*.md'):
        if '.git' in path.parts:
            continue
        name = path.name
        counterpart = None
        if name.endswith('.en.md'):
            counterpart = path.with_name(name.replace('.en.md', '.zh.md'))
        elif name.endswith('.zh.md'):
            english = path.with_name(name.replace('.zh.md', '.en.md'))
            counterpart = english if english.exists() else path.with_name(name.replace('.zh.md', '.md'))
        elif name in ('README.md', 'SKILL.md'):
            counterpart = path.with_name(name.replace('.md', '.zh.md'))
        if counterpart is not None and not counterpart.is_file():
            errors.append(f'Missing language pair: {path.relative_to(root)}')
        for target in local_targets(path):
            if not target.exists():
                errors.append(f'Broken local link: {path.relative_to(root)} -> {target}')

    if skills:
        reference = skills[0].parent / 'references'
        schedules = []
        for lang in ('en', 'zh'):
            path = reference / f'aws-cases.{lang}.md'
            if not path.is_file():
                errors.append(f'Missing case library: {path.relative_to(root)}')
                continue
            sections = re.split(r'^## \d+\. ', path.read_text(encoding='utf-8'), flags=re.M)[1:]
            if len(sections) != 8:
                errors.append(f'Expected eight historical variants: {path.relative_to(root)}')
            timelines = []
            expected_ends = [30, 120, 120, 120, 120, 120, 210, 180]
            for index, section in enumerate(sections):
                intervals = [(int(a), int(b)) for a, b in re.findall(r'^\| (\d+)–(\d+) \|', section, flags=re.M)]
                cursor = 0
                for start, end in intervals:
                    if start != cursor or end <= start:
                        errors.append(f'Invalid scene interval in {lang} case {index + 1}: {start}–{end}')
                    cursor = end
                if index >= len(expected_ends) or cursor != expected_ends[index]:
                    errors.append(f'Unexpected total duration in {lang} case {index + 1}: {cursor}')
                timelines.append(intervals)
            schedules.append(timelines)
        if len(schedules) == 2 and schedules[0] != schedules[1]:
            errors.append('English and Chinese case timelines differ')

    try:
        cases = json.loads((root / 'evals/cases.json').read_text(encoding='utf-8'))
        ids = [case['id'] for case in cases]
        if len(ids) != len(set(ids)):
            errors.append('Duplicate behavioral case ID')
        modes = {case['expect']['mode'] for case in cases}
        if not {'preview', 'full', 'extend', 'prompt-only'}.issubset(modes):
            errors.append('Behavioral scenarios do not cover all production modes')
        languages = {case['expect'].get('language') for case in cases}
        if not {'en', 'zh'}.issubset(languages):
            errors.append('Behavioral scenarios do not cover both languages')
        for case in cases:
            if not case.get('prompt') or not case.get('checks'):
                errors.append(f'Empty behavioral scenario: {case.get("id")}')
    except (OSError, ValueError, KeyError, TypeError) as exc:
        errors.append(f'Cannot read behavioral scenarios: {exc}')
    return errors


def local_targets(path):
    text = path.read_text(encoding='utf-8')
    # Repository Markdown uses ordinary inline links without parentheses in paths.
    for raw in re.findall(r'\[[^\]]*\]\(([^)]+)\)', text):
        target = raw.strip().strip('<>')
        parsed = urlsplit(target)
        if parsed.scheme or parsed.netloc or not parsed.path:
            continue
        yield (path.parent / unquote(parsed.path)).resolve()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    root = parser.parse_args().root.resolve()
    errors = validate(root)
    if errors:
        for error in errors:
            print(f'FAIL: {error}')
        return 1
    print('PASS: skill packaging, local links, translation pairs, eight bilingual timelines, and evaluation coverage')
    print('NOT RUN: Opus behavioral evaluation, rendering, video playback, or audio review')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
