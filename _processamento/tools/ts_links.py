#!/usr/bin/env python3
"""Converte tokens {{ts:ID@H:MM:SS}} em links do YouTube no minuto exato. Uso: ts_links.py <vault_dir> [--check]"""
import json, os, re, sys
SP = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
man = {m["id"]: m for m in json.load(open(os.path.join(SP, "manifest.json"), encoding="utf-8"))}
TOK = re.compile(r"\{\{\s*ts\s*:\s*([a-z]+-\d{1,2})\s*@\s*(\d{1,2}(?::\d{1,2}){1,2})\s*\}\}")
def conv(m):
    sid, t = m.group(1), m.group(2)
    pre, num = sid.split("-"); sid = f"{pre}-{int(num):02d}"
    if sid not in man: return m.group(0)
    parts = [int(x) for x in t.split(":")]
    while len(parts) < 3: parts.insert(0, 0)
    h, mi, s = parts; secs = h*3600 + mi*60 + s
    label = f"{h}:{mi:02d}:{s:02d}"
    return f"[▶ {label}](https://www.youtube.com/watch?v={man[sid]['video_id']}&t={secs}s)"
vault = sys.argv[1]; check = "--check" in sys.argv
tot = bad = files = 0
for root, _, fs in os.walk(vault):
    for f in fs:
        if not f.endswith(".md"): continue
        p = os.path.join(root, f); s = open(p, encoding="utf-8").read()
        n = len(TOK.findall(s)); tot += n
        leftovers = [x for x in re.findall(r"\{\{[^}]*\}\}", TOK.sub("", s)) if "ts" in x]
        if leftovers: bad += len(leftovers); print("MALFORMADO", p, leftovers[:3])
        if n and not check:
            new = TOK.sub(conv, s)
            if new != s: open(p, "w", encoding="utf-8").write(new); files += 1
print(f"tokens={tot} malformados={bad} arquivos_alterados={files}")
