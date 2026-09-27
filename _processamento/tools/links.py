#!/usr/bin/env python3
"""Checa e normaliza wikilinks do vault.
Uso:
  links.py report <vault> [transcricoes_root]         -> lista links não resolvidos (json em SP/links_report.json)
  links.py normalize <vault> <aliases.json>           -> reescreve [[alias]] -> [[Canônico|alias]] (corpo) e "[[alias]]" -> "[[Canônico]]" (frontmatter)
  links.py unlink <vault> <lista.json>                -> transforma links para alvos listados em texto simples
"""
import json, os, re, sys, unicodedata
SP = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LINK = re.compile(r"\[\[([^\]\|#\^]+)(#[^\]\|]*)?(\|[^\]]*)?\]\]")
def key(s): return unicodedata.normalize("NFC", s).strip().lower()
def notes(vault, extra=None):
    names = {}
    for base in [vault] + ([extra] if extra else []):
        for root, dirs, fs in os.walk(base):
            if ".git" in root: continue
            for f in fs:
                if f.endswith(".md"): names[key(f[:-3])] = f[:-3]
    return names
def iter_md(vault):
    for root, _, fs in os.walk(vault):
        for f in fs:
            if f.endswith(".md"): yield os.path.join(root, f)
cmd, vault = sys.argv[1], sys.argv[2]
if cmd == "report":
    extra = sys.argv[3] if len(sys.argv) > 3 else None
    have = notes(vault, extra); miss = {}
    total = 0
    for p in iter_md(vault):
        for m in LINK.finditer(open(p, encoding="utf-8").read()):
            t = m.group(1).split("/")[-1]; total += 1
            if key(t) not in have: miss.setdefault(t.strip(), []).append(os.path.relpath(p, vault))
    out = sorted(((k, len(v), sorted(set(v))[:5]) for k, v in miss.items()), key=lambda x: -x[1])
    json.dump(out, open(os.path.join(SP, "links_report.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"links={total} alvos_nao_resolvidos={len(out)} ocorrencias={sum(x[1] for x in out)}")
    for k, n, _ in out[:40]: print(f"{n:4d}  {k}")
elif cmd == "normalize":
    amap = {key(k): v for k, v in json.load(open(sys.argv[3], encoding="utf-8")).items()}
    changed = 0
    for p in iter_md(vault):
        s = open(p, encoding="utf-8").read(); orig = s
        fm_end = s.find("\n---", 3) if s.startswith("---") else -1
        def fix(m, in_fm):
            tgt, head, alias = m.group(1), m.group(2) or "", m.group(3) or ""
            k = key(tgt.split("/")[-1])
            if k not in amap or amap[k] == tgt.strip(): return m.group(0)
            can = amap[k]
            if in_fm or alias: return f"[[{can}{head}{alias}]]"
            return f"[[{can}{head}|{tgt.strip()}]]"
        if fm_end > 0:
            fm, body = s[:fm_end], s[fm_end:]
            s = LINK.sub(lambda m: fix(m, True), fm) + LINK.sub(lambda m: fix(m, False), body)
        else:
            s = LINK.sub(lambda m: fix(m, False), s)
        if s != orig: open(p, "w", encoding="utf-8").write(s); changed += 1
    print(f"arquivos_alterados={changed}")
elif cmd == "unlink":
    targets = {key(t) for t in json.load(open(sys.argv[3], encoding="utf-8"))}
    changed = 0
    for p in iter_md(vault):
        s = open(p, encoding="utf-8").read(); orig = s
        fm_end = s.find("\n---", 3) if s.startswith("---") else -1
        def rep_body(m):
            if key(m.group(1).split("/")[-1]) not in targets: return m.group(0)
            return (m.group(3) or "|" + m.group(1))[1:]
        def rep_fm(m):
            return m.group(0) if key(m.group(1).split("/")[-1]) not in targets else m.group(1)
        if fm_end > 0: s = LINK.sub(rep_fm, s[:fm_end]) + LINK.sub(rep_body, s[fm_end:])
        else: s = LINK.sub(rep_body, s)
        if s != orig: open(p, "w", encoding="utf-8").write(s); changed += 1
    print(f"arquivos_alterados={changed}")
