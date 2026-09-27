#!/usr/bin/env python3
"""Agrega SP/extract/*.json em SP/agg/ (listas completas anotadas + versões compactas para os agentes de registro)."""
import json, os, glob, collections, unicodedata, re
SP = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
A = os.path.join(SP, "agg"); os.makedirs(A, exist_ok=True)
def key(s): return re.sub(r"\s+", " ", unicodedata.normalize("NFC", s or "").strip().lower())
man = {m["id"]: m for m in json.load(open(os.path.join(SP, "manifest.json"), encoding="utf-8"))}
fontes, lists = {}, collections.defaultdict(list)
FIELDS = ["conceitos","dinamicas","movimentos_facilitacao","dicas_clinicas","posicionamentos","citacoes","ideias_conteudo","autores"]
errs = []
for p in sorted(glob.glob(os.path.join(SP, "extract", "*.json"))):
    try: d = json.load(open(p, encoding="utf-8"))
    except Exception as e: errs.append((p, str(e))); continue
    sid = d.get("id") or os.path.basename(p)[:-5]
    m = man.get(sid, {})
    fontes[sid] = {k: d.get(k) for k in ["id","nota","pasta","titulo","serie","formato","facilitadores","resumo","em_uma_frase","competencias","abordagens"]}
    fontes[sid].update(video=m.get("video"), duracao=m.get("duracao"), transcricao=m.get("transcricao"))
    for f in FIELDS:
        for i, it in enumerate(d.get(f) or []):
            if isinstance(it, dict): it = dict(it)
            else: it = {"texto": it}
            it["fonte_id"] = sid; it["nota"] = d.get("nota")
            lists[f].append(it)
    if d.get("formato_grupo"): lists["formatos"].append(dict(d["formato_grupo"], fonte_id=sid, nota=d.get("nota")))
    for r in d.get("reflexoes_do_facilitador") or []: lists["reflexoes"].append({"texto": r, "fonte_id": sid, "nota": d.get("nota")})
    for r in d.get("referencias_a_outros_encontros") or []: lists["referencias"].append({"texto": r, "fonte_id": sid, "nota": d.get("nota")})
    for s in d.get("estrutura") or []: lists["estrutura"].append(dict(s, fonte_id=sid, nota=d.get("nota")))
json.dump(fontes, open(os.path.join(A, "fontes.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
for f, L in lists.items():
    for i, it in enumerate(L): it["_i"] = i
    json.dump(L, open(os.path.join(A, f + ".json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
# compactos
cc = collections.OrderedDict()
for it in lists["conceitos"]:
    k = key(it.get("nome"))
    e = cc.setdefault(k, {"nome": it.get("nome"), "n": 0, "fontes": set(), "def": (it.get("definicao") or "")[:140]})
    e["n"] += 1; e["fontes"].add(it["fonte_id"])
with open(os.path.join(A, "conceitos_compacto.txt"), "w", encoding="utf-8") as o:
    for k, e in sorted(cc.items(), key=lambda x: (-len(x[1]["fontes"]), x[0])):
        o.write(f'{e["nome"]} | n={e["n"]} | fontes={",".join(sorted(e["fontes"]))} | {e["def"]}\n')
ac = collections.OrderedDict()
for it in lists["autores"]:
    k = key(it.get("nome")); e = ac.setdefault(k, {"nome": it.get("nome"), "fontes": set()}); e["fontes"].add(it["fonte_id"])
with open(os.path.join(A, "autores_compacto.txt"), "w", encoding="utf-8") as o:
    for k, e in sorted(ac.items(), key=lambda x: (-len(x[1]["fontes"]), x[0])): o.write(f'{e["nome"]} | fontes={",".join(sorted(e["fontes"]))}\n')
with open(os.path.join(A, "dinamicas_compacto.txt"), "w", encoding="utf-8") as o:
    for it in lists["dinamicas"]:
        o.write(f'D{it["_i"]:03d} | {it.get("nome")} | {it["fonte_id"]} | {(it.get("objetivo") or "")[:160]}\n')
with open(os.path.join(A, "teses_compacto.txt"), "w", encoding="utf-8") as o:
    for it in lists["posicionamentos"]:
        o.write(f'T{it["_i"]:04d} | {it.get("tese")} | {it.get("quem")} | {it["fonte_id"]}\n')
abc = collections.Counter(a for f in fontes.values() for a in (f.get("abordagens") or []))
cpc = collections.Counter(a for f in fontes.values() for a in (f.get("competencias") or []))
print("fontes:", len(fontes), "| erros:", errs)
print({f: len(L) for f, L in lists.items()})
print("conceitos unicos:", len(cc), "| autores unicos:", len(ac))
print("abordagens:", dict(abc)); print("competencias:", dict(cpc))
