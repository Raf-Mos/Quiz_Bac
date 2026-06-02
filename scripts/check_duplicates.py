import json
from pathlib import Path

p = Path('data') / 'questions.json'
if not p.exists():
    print('no file')
    raise SystemExit(1)

with p.open(encoding='utf-8') as f:
    d = json.load(f)

texts = []
keys = []
for subj, qs in d.items():
    for q in qs:
        qtext = q.get('question','').strip()
        opts = q.get('options', [])
        key = (subj, qtext, tuple(opts))
        keys.append(key)
        texts.append(qtext)

# find duplicate question texts across whole payload
from collections import Counter
c = Counter(texts)
dups = [t for t, cnt in c.items() if cnt > 1]
print('total_questions:', len(texts))
print('duplicate_question_texts_count:', len(dups))
if dups:
    print('examples:')
    for t in dups[:10]:
        print('-', t)

# check exact question+options duplicates
key_counter = Counter(keys)
dup_keys = [k for k, cnt in key_counter.items() if cnt > 1]
print('duplicate_question+options_count:', len(dup_keys))
if dup_keys:
    print('examples:')
    for k in dup_keys[:5]:
        print('-', k)
