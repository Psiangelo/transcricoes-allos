#!/usr/bin/env python3
"""Gera as notas de síntese do vault a partir dos JSONs extraídos (sem LLM).
Uso: synth.py <SP> <VAULT>
Escreve: 03 Dinâmicas, 04 Competências, 05 Dicas, 06 Teses, 07 Conceitos, 08 Abordagens e Autores,
09 Formatos, 11 Conteúdo (bancos e pautas), 01 Método Alan (partes geradas), MOCs; e SP/agg/aliases.json.
"""
import json, os, re, sys, glob, collections, unicodedata

SP, VAULT = sys.argv[1], sys.argv[2]
MAN = {m["id"]: m for m in json.load(open(os.path.join(SP, "manifest.json"), encoding="utf-8"))}
DOCS = {}
for p in sorted(glob.glob(os.path.join(SP, "extract", "*.json"))):
    d = json.load(open(p, encoding="utf-8")); DOCS[d.get("id") or os.path.basename(p)[:-5]] = d

SERIE_ORDEM = ["alan", "acervo", "mon", "pd", "pc", "dicas", "psigeral", "comparada", "pbe", "estudar", "formacao", "cumbuca", "avulsos"]
def ordem(sid): pre, n = sid.split("-"); return (SERIE_ORDEM.index(pre) if pre in SERIE_ORDEM else 99, int(n))
IDS = sorted(DOCS, key=ordem)

# ---------------------------------------------------------------- utilidades
def strip_acc(s): return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn")
def nkey(s):
    s = strip_acc((s or "").lower())
    s = re.sub(r"^din[aâ]mica\s*[-–—:]\s*", "", s)
    s = re.sub(r"\([^)]*\)", " ", s)
    s = re.sub(r"[^a-z0-9 ]", " ", s)
    s = " ".join(w for w in s.split() if w not in STOP)
    return MERGE.get(s, s)
STOP = {"de", "do", "da", "dos", "das", "e", "o", "a", "os", "as", "com", "em", "no", "na", "para", "por", "um", "uma"}
MERGE = {  # variantes conhecidas -> chave canônica
    "monitoria atendimento paciente ia": "leitura comentada atendimento simulado",
    "leitura comentada atendimento simulado ia": "leitura comentada atendimento simulado",
    "escutas": "escuta sistemica",
}
BAD = r'[#^\[\]|\\/:*?"<>]'
def fname(s):
    s = re.sub(r"\s*:\s*", " - ", s.strip()); s = re.sub(BAD, "", s)
    return re.sub(r"\s+", " ", s).strip().rstrip(".")
def link(n, alias=None): return f"[[{n}|{alias}]]" if alias and alias != n else f"[[{n}]]"
def ts(sid, t):
    t = (t or "").strip()
    return f"{{{{ts:{sid}@{t}}}}}" if re.fullmatch(r"\d{1,2}:\d{2}(:\d{2})?", t) else ""
def nota(sid): return DOCS[sid].get("nota") or sid
def src(sid, t=None):
    s = link(nota(sid)); x = ts(sid, t)
    return f"{s} {x}".strip()
def yq(v): return json.dumps(v, ensure_ascii=False)
def fm(**kw):
    out = ["---"]
    for k, v in kw.items():
        if v is None: continue
        out.append(f"{k}: {yq(v) if not isinstance(v, (int, float, bool)) else json.dumps(v)}")
    out.append("---"); return "\n".join(out) + "\n"
def clean(s): return re.sub(r"\s+", " ", str(s or "")).strip()
def write(folder, name, text):
    d = os.path.join(VAULT, folder); os.makedirs(d, exist_ok=True)
    p = os.path.join(d, fname(name) + ".md")
    open(p, "w", encoding="utf-8").write(text.rstrip() + "\n"); WRITTEN.append(p)
WRITTEN = []
ALAN_EXTRA = {"acervo-13"} | {s for s, d in DOCS.items() if any("alan" in strip_acc(str(f)).lower() for f in (d.get("facilitadores") or []))}
ALAN_EXTRA.discard("alan-04")
def is_alan(sid): return (sid.startswith("alan-") and sid != "alan-04") or sid in ALAN_EXTRA
def quem_de(sid): return ", ".join(DOCS[sid].get("facilitadores") or []) or "?"

# ---------------------------------------------------------------- vocabulários
COMPS = [
 ("Escuta clínica", "escuta", "Captar o que o paciente diz (e como diz) sem reduzir cedo demais: atenção, registro e abertura ao material."),
 ("Interpretação", "interpretacao", "Ler o caso: construir hipóteses de sentido sobre o que o paciente traz, com critérios para escolher entre leituras."),
 ("Priorização clínica", "priorizacao", "Escolher, entre muitos temas e sinais, aquilo em que intervir agora — e saber justificar a escolha."),
 ("Intervenção", "intervencao", "Transformar a leitura do caso em uma fala/ação com efeito: foco, forma, timing, intensidade e distância."),
 ("Construção frasal", "construcao-frasal", "O trabalho fino com a frase: como a mesma intervenção muda de efeito conforme palavras, ordem, tom e tamanho."),
 ("Aprofundamento", "aprofundamento", "Fazer o paciente falar mais e melhor sobre o que importa: encadear perguntas segundo um esquema."),
 ("Psicoeducação", "psicoeducacao", "Explicar ao paciente, de forma adequada a ele, como a terapia e o problema funcionam — sem aula nem jargão."),
 ("Relação terapêutica", "relacao-terapeutica", "Construir, sustentar, tensionar e reparar o vínculo; entender o lugar do terapeuta para o paciente."),
 ("Formulação de caso", "formulacao-de-caso", "Organizar as informações do caso num modelo explicativo que guie a direção do tratamento."),
 ("Psicodiagnóstico", "psicodiagnostico", "Tipos de diagnóstico (nosológico, estrutural, funcional, compreensivo...) e seu uso clínico."),
 ("Primeira sessão e entrevistas iniciais", "primeira-sessao", "Como receber, investigar e contratar nos primeiros encontros, em diferentes abordagens."),
 ("Abertura e encerramento de sessão", "abertura-encerramento", "Como começar e terminar sessões (e processos) de forma intencional."),
 ("Direção do tratamento", "direcao-do-tratamento", "Para onde o tratamento vai, quem define os objetivos e como revisá-los."),
 ("Feedback clínico", "feedback-clinico", "Devolutivas ao paciente e uso de feedback/medidas para ajustar o tratamento."),
 ("Acolhimento e validação", "acolhimento", "Receber o sofrimento de modo que o paciente se sinta compreendido — com concretude, não com fórmulas."),
 ("Articulação teoria-prática", "teoria-pratica", "Usar a teoria como ferramenta de leitura e decisão, e não como rótulo ou fórmula."),
 ("Pessoa do terapeuta", "pessoa-do-terapeuta", "Valores, cosmovisão, afetos e limites do terapeuta e como eles atravessam a clínica."),
 ("Desenvolvimento profissional", "desenvolvimento-profissional", "Como um clínico melhora: prática deliberada, feedback, supervisão, estudo."),
]
CNAMES = {c[0] for c in COMPS}; CKEY = {nkey(c[0]): c[0] for c in COMPS}; CSLUG = {c[0]: c[1] for c in COMPS}
def comp_ok(c):
    return CKEY.get(nkey(c))

ABORD = [
 ("Psicanálise freudiana", "psicanalise", r"freud|psican[aá]lise(?! lacan)"),
 ("Psicanálise lacaniana", "lacan", r"lacan"),
 ("Psicologia analítica junguiana", "junguiana", r"\bjung|jungian|anal[ií]tica junguiana"),
 ("Terapia cognitivo-comportamental", "tcc", r"\btcc\b|cognitivo|beck\b"),
 ("Análise do comportamento", "analise-do-comportamento", r"an[aá]lise do comportamento|behavior|skinner|an[aá]lise funcional|comportamental"),
 ("Terapias contextuais", "contextuais", r"\bact\b|\bfap\b|\bdbt\b|contextua|hayes"),
 ("Fenomenologia e existencialismo", "fenomenologia", r"fenomenol|existencial|husserl|heidegger"),
 ("Abordagem centrada na pessoa", "acp", r"centrada na pessoa|rogers|\bacp\b"),
 ("Gestalt-terapia", "gestalt", r"gestalt|perls"),
 ("Terapia sistêmica", "sistemica", r"sist[eê]mic|cibern|bateson"),
 ("Terapia do esquema", "esquema", r"terapia do esquema|young\b"),
 ("Psicodrama", "psicodrama", r"psicodrama|moreno"),
]
ANAMES = {a[0] for a in ABORD}

TEMAS = [
 ("Relação terapêutica e vínculo", r"rela[cç][aã]o terap|v[ií]nculo|alian[cç]a|ruptura|transfer[eê]ncia|confian[cç]a|rapport|antifr[aá]gil"),
 ("Escuta e interpretação", r"escut|interpret|hermen[eê]ut|sentido|significante|ato falho|leitura do caso|ler o caso|n[aã]o dito"),
 ("Intervenção e linguagem", r"interven|frase|pergunta|linguagem|palavra|comunica|confront|met[aá]fora|psicoeduca|explica[cç]"),
 ("Priorização e direção do tratamento", r"prioriz|dire[cç][aã]o do trat|objetivo|demanda|queixa|foco|cura|meta terap"),
 ("Diagnóstico e formulação de caso", r"diagn[oó]st|formula[cç][aã]o|hip[oó]tese|dsm|psicodiagn|constru[cç][aã]o de caso|prontu"),
 ("Abordagens, teoria e ciência", r"abordage|teoria|te[oó]ric|psican[aá]lise|\btcc\b|comportament|sist[eê]mic|fenomenol|lacan|freud|jung|evid[eê]ncia|ci[eê]ncia|pesquisa|protocolo|dod[oô]"),
 ("Formação, estudo e prática deliberada", r"forma[cç][aã]o|estud|pr[aá]tica deliberada|trein|aprend|supervis|faculdade|feedback|expertise|mem[oó]ria"),
 ("Pessoa do terapeuta e ética", r"[eé]tic|valores|cosmovis|moral|autocuidado|limite|pr[oó]pria terapia|terapeuta (?:tem|precisa|deve)|sinceridade|autenticidade"),
 ("Grupos, ensino e condução", r"grupo|aula|ensin|particip|din[aâ]mica|facilit|monitoria|roleplay"),
]
OUTRO_TEMA = "Outras reflexões"
def tema_de(text):
    t = strip_acc((text or "").lower()); best, bs = OUTRO_TEMA, 0
    for nome, rx in TEMAS:
        n = len(re.findall(strip_acc(rx), t))
        if n > bs: best, bs = nome, n
    return best

PILARES = [
 ("clinica-na-pratica", "Clínica na prática"), ("ciencia-e-mitos", "Ciência e mitos"),
 ("abordagens-em-dialogo", "Abordagens em diálogo"), ("formacao-do-psicologo", "Formação do psicólogo"),
 ("bastidores-dos-grupos", "Bastidores dos grupos"), ("maximas-e-reflexoes", "Máximas e reflexões"),
]
PNOME = dict(PILARES)

def all_items(field):
    for sid in IDS:
        for it in DOCS[sid].get(field) or []:
            if isinstance(it, dict): yield sid, it

# ================================================================ DINÂMICAS
dyn_groups = collections.OrderedDict()
for sid, it in all_items("dinamicas"):
    k = nkey(it.get("nome"))
    if not k: continue
    dyn_groups.setdefault(k, []).append((sid, it))
def dyn_canon(items):
    c = collections.Counter(fname(("Dinâmica - " + re.sub(r"^[Dd]in[aâ]mica\s*[-–—:]\s*", "", it.get("nome").strip()))) for _, it in items)
    return sorted(c.items(), key=lambda x: (-x[1], len(x[0])))[0][0]
ALIASES = {}
DYN = {}
for k, items in dyn_groups.items():
    can = dyn_canon(items); DYN[can] = items
    for _, it in items:
        raw = it.get("nome").strip()
        for v in {raw, "Dinâmica - " + re.sub(r"^[Dd]in[aâ]mica\s*[-–—:]\s*", "", raw), fname(raw)}:
            if v != can: ALIASES[v] = can

def dyn_note(can, items):
    comps = [];
    for _, it in items:
        for c in it.get("competencias") or []:
            c2 = comp_ok(c)
            if c2 and c2 not in comps: comps.append(c2)
    fontes = []
    for sid, _ in items:
        if nota(sid) not in fontes: fontes.append(nota(sid))
    facs = sorted({f for sid, _ in items for f in (DOCS[sid].get("facilitadores") or [])})
    niveis = sorted({clean(it.get("nivel")) for _, it in items if it.get("nivel")})
    online = any(it.get("funciona_online") is True for _, it in items)
    origem = "Alan" if any(is_alan(s) for s, _ in items) else ", ".join(facs) or "Allos"
    tags = ["dinamica"] + [f"competencia/{CSLUG[c]}" for c in comps] + (["allos/alan"] if origem == "Alan" else [])
    t = fm(tipo="dinamica", origem=origem, facilitadores=facs, competencias=[link(c) for c in comps],
           nivel=", ".join(niveis) or None, funciona_online=online, fontes=[link(f) for f in fontes], tags=tags)
    first = items[0][1]
    t += f"\n# {can}\n\n> [!summary] Objetivo\n> {clean(first.get('objetivo')) or '—'}\n\n"
    t += "| Competências | Nível | Online | Aparece em |\n|---|---|---|---|\n"
    t += f"| {', '.join(link(c) for c in comps) or '—'} | {', '.join(niveis) or '—'} | {'sim' if online else 'não informado'} | {len(fontes)} fonte(s) |\n\n"
    multi = len(items) > 1
    if multi:
        t += f"> [!info] Esta dinâmica aparece em {len(items)} versões (por fonte). Compare as versões abaixo para montar a sua.\n\n"
    for sid, it in items:
        h = "##" if not multi else "##"
        t += f"{h} {'Versão de ' if multi else 'Como funciona — '}{link(nota(sid))} {ts(sid, it.get('ts'))}\n"
        t += f"*Conduzida por {quem_de(sid)}.*\n\n"
        if multi and clean(it.get("objetivo")) and it is not first:
            t += f"- **Objetivo:** {clean(it.get('objetivo'))}\n"
        for lab, key in [("Configuração", "configuracao"), ("Tempo", "tempo"), ("Materiais", "materiais")]:
            if clean(it.get(key)): t += f"- **{lab}:** {clean(it.get(key))}\n"
        if clean(it.get("consigna")): t += f"\n**Consigna (o que o facilitador pede):**\n> {clean(it.get('consigna'))}\n"
        passos = [clean(p) for p in (it.get("passos") or []) if clean(p)]
        if passos: t += "\n**Passo a passo:**\n" + "\n".join(f"{i}. {p}" for i, p in enumerate(passos, 1)) + "\n"
        for lab, key in [("Feedback e critérios de qualidade", "feedback"), ("Como aconteceu na prática", "exemplos_praticos"),
                         ("Variações", "variacoes"), ("Armadilhas", "armadilhas")]:
            if clean(it.get(key)): t += f"\n**{lab}:** {clean(it.get(key))}\n"
        t += "\n"
    t += "## Relacionados\n" + "".join(f"- {link(c)}\n" for c in comps) + "- [[MOC - Dinâmicas]]\n"
    return t

for can, items in DYN.items():
    write("03 - Dinâmicas", can, dyn_note(can, items))

# MOC dinâmicas
t = fm(tipo="moc", tags=["moc", "dinamica"]) + "\n# MOC — Dinâmicas\n\n"
t += f"> [!abstract] {len(DYN)} dinâmicas extraídas dos grupos da Allos, agrupadas pela competência que treinam.\n> Cada nota traz consigna, passo a passo, critérios de feedback e o link para o minuto do vídeo em que ela acontece.\n\n"
bycomp = collections.defaultdict(list)
for can, items in DYN.items():
    cs = []
    for _, it in items:
        for c in it.get("competencias") or []:
            c2 = comp_ok(c)
            if c2 and c2 not in cs: cs.append(c2)
    for c in (cs[:1] or ["(sem competência definida)"]): bycomp[c].append((can, items))
for c in [x[0] for x in COMPS] + ["(sem competência definida)"]:
    if c not in bycomp: continue
    t += f"## {c if c.startswith('(') else link(c)}\n| Dinâmica | Origem | Nível | Objetivo |\n|---|---|---|---|\n"
    for can, items in sorted(bycomp[c]):
        o = "Alan" if any(is_alan(s) for s, _ in items) else quem_de(items[0][0])
        niv = clean(items[0][1].get("nivel")) or "—"
        obj = clean(items[0][1].get("objetivo"))[:160].replace("|", "/")
        t += f"| {link(can)} | {o} | {niv} | {obj} |\n"
    t += "\n"
write("03 - Dinâmicas", "MOC - Dinâmicas", t)

# ================================================================ CONCEITOS
RESERVED = {nkey(x): x for x in list(CNAMES) + list(ANAMES)}
for sid in IDS: RESERVED[nkey(nota(sid))] = nota(sid)
con_groups = collections.OrderedDict()
for sid, it in all_items("conceitos"):
    k = nkey(it.get("nome"))
    if k: con_groups.setdefault(k, []).append((sid, it))
CON = {}
for k, items in con_groups.items():
    if k in RESERVED or k in {nkey(x) for x in DYN}:
        tgt = RESERVED.get(k) or next(x for x in DYN if nkey(x) == k)
        for _, it in items:
            if it["nome"].strip() != tgt: ALIASES[it["nome"].strip()] = tgt
        continue
    c = collections.Counter(fname(it["nome"]) for _, it in items)
    can = sorted(c.items(), key=lambda x: (-x[1], "(" in x[0], len(x[0])))[0][0]
    CON[can] = items
    for _, it in items:
        for v in {it["nome"].strip(), fname(it["nome"])}:
            if v != can: ALIASES[v] = can

def con_note(can, items):
    fontes = []
    for sid, _ in items:
        if nota(sid) not in fontes: fontes.append(nota(sid))
    abds = []
    for _, it in items:
        a = clean(it.get("abordagem"))
        for nome, slug, rx in ABORD:
            if a and (nkey(a) == nkey(nome) or re.search(rx, strip_acc(a.lower()))) and nome not in abds: abds.append(nome)
    comps = collections.Counter(c2 for sid, _ in items for c in (DOCS[sid].get("competencias") or []) if (c2 := comp_ok(c)))
    aliases = sorted({it["nome"].strip() for _, it in items} - {can})
    best = sorted(items, key=lambda x: (not x[0].startswith("alan-"), -len(clean(x[1].get("definicao")))))[0]
    tags = ["conceito"] + [f"abordagem/{s}" for n, s, _ in ABORD if n in abds]
    t = fm(tipo="conceito", aliases=aliases or None, abordagens=[link(a) for a in abds], fontes=[link(f) for f in fontes], n_fontes=len(fontes), tags=tags)
    t += f"\n# {can}\n\n> [!abstract] Definição\n> {clean(best[1].get('definicao')) or '—'}\n> — {src(best[0], best[1].get('ts'))}\n\n"
    if len(items) > 1:
        t += f"## Como aparece nas fontes ({len(fontes)})\n"
        for sid, it in items:
            if it is best[1]: continue
            t += f"- **{link(nota(sid))}** {ts(sid, it.get('ts'))} — {clean(it.get('definicao'))}"
            if clean(it.get("exemplo")): t += f" *Exemplo:* {clean(it.get('exemplo'))}"
            t += "\n"
        t += "\n"
    elif clean(best[1].get("exemplo")):
        t += f"**Exemplo usado:** {clean(best[1].get('exemplo'))}\n\n"
    if abds: t += "## Abordagens\n" + "".join(f"- {link(a)}\n" for a in abds) + "\n"
    if comps: t += "## Competências relacionadas\n" + "".join(f"- {link(c)}\n" for c, _ in comps.most_common(4)) + "\n"
    t += "## Relacionados\n- [[MOC - Conceitos]]\n"
    return t
for can, items in CON.items():
    write("07 - Conceitos", can, con_note(can, items))
t = fm(tipo="moc", tags=["moc", "conceito"]) + "\n# MOC — Conceitos\n\n"
nf = {can: len({s for s, _ in items}) for can, items in CON.items()}
cent = sorted([c for c in CON if nf[c] >= 3], key=lambda c: (-nf[c], c))
t += f"> [!abstract] {len(CON)} conceitos. Os **centrais** aparecem em 3 ou mais fontes; o índice completo vem depois, em ordem alfabética.\n\n## Conceitos centrais\n"
t += "".join(f"- {link(c)} · {nf[c]} fontes\n" for c in cent) + "\n## Índice alfabético\n"
letra = None
for c in sorted(CON, key=lambda x: strip_acc(x.lower())):
    L = strip_acc(c[0].upper())
    if L != letra: t += f"\n### {L}\n"; letra = L
    t += f"- {link(c)}" + (f" · {nf[c]}" if nf[c] > 1 else "") + "\n"
write("07 - Conceitos", "MOC - Conceitos", t)

# ================================================================ AUTORES e ABORDAGENS
aut_groups = collections.OrderedDict()
for sid, it in all_items("autores"):
    k = nkey(it.get("nome"))
    if k: aut_groups.setdefault(k, []).append((sid, it))
AUT = {}
for k, items in aut_groups.items():
    c = collections.Counter(fname(it["nome"]) for _, it in items)
    can = sorted(c.items(), key=lambda x: (-x[1], "(" in x[0], -len(x[0])))[0][0]
    if nkey(can) in RESERVED or can in CON: continue
    AUT[can] = items
    for _, it in items:
        for v in {it["nome"].strip(), fname(it["nome"])}:
            if v != can: ALIASES[v] = can
for can, items in AUT.items():
    fontes = list(dict.fromkeys(nota(s) for s, _ in items))
    t = fm(tipo="autor", aliases=sorted({it["nome"].strip() for _, it in items} - {can}) or None, fontes=[link(f) for f in fontes], n_fontes=len(fontes), tags=["autor"])
    t += f"\n# {can}\n\n## Para que é citado nas fontes\n"
    for sid, it in items:
        t += f"- {link(nota(sid))} — {clean(it.get('contexto')) or '—'}\n"
    t += "\n## Relacionados\n- [[MOC - Abordagens e Autores]]\n"
    write("08 - Abordagens e Autores", can, t)

abd_src = collections.defaultdict(list)
for sid in IDS:
    for a in DOCS[sid].get("abordagens") or []:
        abd_src[fname(a)].append(sid)
ALL_TESES = list(all_items("posicionamentos"))
for a in sorted(set(abd_src) | ANAMES):
    if a in CON or a in AUT: continue
    meta = next((x for x in ABORD if x[0] == a), None)
    slug = meta[1] if meta else re.sub(r"[^a-z0-9]+", "-", strip_acc(a.lower())).strip("-")
    rx = meta[2] if meta else re.escape(strip_acc(a.lower().split()[-1]))
    sids = list(dict.fromkeys(abd_src.get(a, [])))
    cons = [c for c, items in CON.items() if any(re.search(rx, strip_acc(clean(it.get("abordagem")).lower())) for _, it in items)]
    tes = [(s, it) for s, it in ALL_TESES if re.search(rx, strip_acc((clean(it.get("tese")) + " " + clean(it.get("argumento"))).lower()))]
    t = fm(tipo="abordagem", fontes=[link(nota(s)) for s in sids], tags=["abordagem", f"abordagem/{slug}"])
    t += f"\n# {a}\n\n> [!abstract] Onde esta abordagem aparece no acervo\n> {len(sids)} fontes a discutem diretamente; {len(cons)} conceitos e {len(tes)} teses a mencionam.\n\n"
    if sids:
        t += "## Fontes\n" + "".join(f"- {link(nota(s))} — {clean(DOCS[s].get('em_uma_frase'))}\n" for s in sids) + "\n"
    if cons: t += "## Conceitos ligados\n" + "".join(f"- {link(c)}\n" for c in sorted(cons)) + "\n"
    if tes:
        t += "## Teses e comparações que a mencionam\n"
        for s, it in tes[:40]:
            t += f"- **{clean(it.get('tese'))}** — {clean(it.get('argumento'))} *({clean(it.get('quem')) or quem_de(s)}, {src(s, it.get('ts'))})*\n"
        t += "\n"
    t += "## Relacionados\n- [[MOC - Abordagens e Autores]]\n"
    write("08 - Abordagens e Autores", a, t)
    ABD_WRITTEN = True
t = fm(tipo="moc", tags=["moc"]) + "\n# MOC — Abordagens e Autores\n\n## Abordagens\n"
for a in sorted(set(abd_src) | ANAMES):
    if a in CON or a in AUT: continue
    t += f"- {link(a)} · {len(set(abd_src.get(a, [])))} fontes\n"
t += "\n## Autores (por nº de fontes)\n"
for can, items in sorted(AUT.items(), key=lambda x: (-len({s for s, _ in x[1]}), x[0])):
    t += f"- {link(can)} · {len({s for s, _ in items})}\n"
write("08 - Abordagens e Autores", "MOC - Abordagens e Autores", t)

# ================================================================ DICAS por competência
dicas_by = collections.defaultdict(list)
for sid, it in all_items("dicas_clinicas"):
    c = comp_ok(it.get("competencia") or "") or "Intervenção"
    dicas_by[c].append((sid, it))
def fmt_dica(sid, it):
    s = f"- **{clean(it.get('dica'))}**"
    if clean(it.get("justificativa")): s += f" — *Por quê:* {clean(it.get('justificativa'))}"
    if clean(it.get("contexto")): s += f" *Quando:* {clean(it.get('contexto'))}"
    return s + f" — {src(sid, it.get('ts'))}\n"
for c, slug, desc in COMPS:
    items = dicas_by.get(c, [])
    t = fm(tipo="dicas", competencia=link(c), n_dicas=len(items), tags=["dicas", f"competencia/{slug}"])
    t += f"\n# Dicas — {c}\n\n> [!abstract] {len(items)} dicas clínicas sobre {link(c)}, cada uma com a justificativa dada na fonte e o link para o minuto do vídeo.\n> Primeiro as do Alan; depois as dos outros facilitadores e vídeos.\n\n"
    groups = collections.OrderedDict()
    for sid, it in items:
        g = "Alan" if is_alan(sid) else ("Monitorias" if sid.startswith("mon-") else ("Aprimoramento (Acervo)" if sid.startswith("acervo-") else ("Prática Deliberada" if sid.startswith("pd-") else ("Prática Clínica" if sid.startswith("pc-") else "Vídeos e podcasts"))))
        groups.setdefault(g, []).append((sid, it))
    for g in ["Alan", "Aprimoramento (Acervo)", "Monitorias", "Prática Clínica", "Prática Deliberada", "Vídeos e podcasts"]:
        if g not in groups: continue
        t += f"## {g}\n"
        cur = None
        for sid, it in groups[g]:
            if sid != cur: t += f"\n### {link(nota(sid))}\n"; cur = sid
            t += fmt_dica(sid, it)
        t += "\n"
    t += f"## Relacionados\n- {link(c)}\n- [[MOC - Dicas clínicas]]\n"
    write("05 - Dicas Clínicas", f"Dicas - {c}", t)
t = fm(tipo="moc", tags=["moc", "dicas"]) + "\n# MOC — Dicas clínicas\n\n| Competência | Nº de dicas |\n|---|---|\n"
for c, slug, _ in sorted(COMPS, key=lambda x: -len(dicas_by.get(x[0], []))):
    t += f"| {link('Dicas - ' + c, c)} | {len(dicas_by.get(c, []))} |\n"
write("05 - Dicas Clínicas", "MOC - Dicas clínicas", t)

# ================================================================ TESES por tema
teses_by = collections.defaultdict(list)
for sid, it in ALL_TESES:
    teses_by[tema_de(clean(it.get("tese")) + " " + clean(it.get("argumento")) + " " + clean(it.get("implicacao")))].append((sid, it))
def fmt_tese(sid, it, show_quem=True):
    s = f"- **{clean(it.get('tese'))}**\n"
    if clean(it.get("argumento")): s += f"  - *Argumento:* {clean(it.get('argumento'))}\n"
    if clean(it.get("contraponto")): s += f"  - *Contra quem / contraponto:* {clean(it.get('contraponto'))}\n"
    if clean(it.get("implicacao")): s += f"  - *Implicação prática:* {clean(it.get('implicacao'))}\n"
    s += f"  - {(clean(it.get('quem')) or quem_de(sid)) + ' · ' if show_quem else ''}{src(sid, it.get('ts'))}\n"
    return s
TEMA_NOMES = [x[0] for x in TEMAS] + [OUTRO_TEMA]
def quem_grupo(sid, it):
    q = clean(it.get("quem")) or quem_de(sid)
    if "alan" in q.lower() or (is_alan(sid) and not q): return "Alan"
    for n in ["Diogo", "João de Bragança", "Rodolfo", "Gabriel", "Artur"]:
        if strip_acc(n.split()[0].lower()) in strip_acc(q.lower()): return n
    return "Outros facilitadores e participantes"
for tema in TEMA_NOMES:
    items = teses_by.get(tema, [])
    if not items: continue
    t = fm(tipo="tese", tema=tema, n_teses=len(items), tags=["tese"])
    t += f"\n# Teses — {tema}\n\n> [!abstract] {len(items)} pontos de vista defendidos nos grupos e vídeos, cada um com o argumento, o contraponto e a implicação prática.\n> Ótimo ponto de partida para posts de opinião, debates em grupo e roteiros de vídeo.\n\n"
    g = collections.OrderedDict()
    for sid, it in items: g.setdefault(quem_grupo(sid, it), []).append((sid, it))
    for q in ["Alan", "Diogo", "João de Bragança", "Rodolfo", "Gabriel", "Artur", "Outros facilitadores e participantes"]:
        if q not in g: continue
        t += f"## {q}\n" + "".join(fmt_tese(s, it, q.startswith("Outros")) for s, it in g[q]) + "\n"
    t += "## Relacionados\n- [[MOC - Teses e posicionamentos]]\n"
    write("06 - Teses e Posicionamentos", f"Teses - {tema}", t)
t = fm(tipo="moc", tags=["moc", "tese"]) + "\n# MOC — Teses e posicionamentos\n\n> [!note] Como foi organizado\n> Cada tese foi classificada automaticamente por palavras-chave no tema mais provável. Uma tese pode tocar mais de um tema; use a busca do Obsidian para achar todas as ocorrências de um termo.\n\n| Tema | Nº de teses |\n|---|---|\n"
for tema in TEMA_NOMES:
    if teses_by.get(tema): t += f"| {link('Teses - ' + tema, tema)} | {len(teses_by[tema])} |\n"
write("06 - Teses e Posicionamentos", "MOC - Teses e posicionamentos", t)

# ================================================================ COMPETÊNCIAS (hubs)
def src_comps(sid): return [c2 for c in (DOCS[sid].get("competencias") or []) if (c2 := comp_ok(c))]
for c, slug, desc in COMPS:
    alan = [s for s in IDS if s.startswith("alan-") and c in src_comps(s)]
    outros = [s for s in IDS if not s.startswith("alan-") and c in src_comps(s)]
    dyns = [can for can, items in DYN.items() if any(comp_ok(x) == c for _, it in items for x in (it.get("competencias") or []))]
    cons = collections.Counter()
    for s in alan + outros:
        for it in DOCS[s].get("conceitos") or []:
            k = nkey(it.get("nome")); can = next((x for x in CON if nkey(x) == k), None) or ALIASES.get(fname(it.get("nome", "")))
            if can in CON: cons[can] += 1
    dk = dicas_by.get(c, [])
    top = sorted(dk, key=lambda x: (not is_alan(x[0]), -len(clean(x[1].get("justificativa")))))[:12]
    t = fm(tipo="competencia", tags=["competencia", f"competencia/{slug}"], n_fontes=len(alan) + len(outros))
    t += f"\n# {c}\n\n> [!abstract] O que é\n> {desc}\n\n"
    if alan:
        t += "## Nos encontros do Alan\n| Encontro | Em uma frase |\n|---|---|\n"
        for s in alan: t += f"| {link(nota(s))} | {clean(DOCS[s].get('em_uma_frase')).replace('|', '/')} |\n"
        t += "\n"
    if outros:
        t += "## Em outros grupos e vídeos\n" + "".join(f"- {link(nota(s))} — {clean(DOCS[s].get('em_uma_frase'))}\n" for s in outros) + "\n"
    if dyns: t += "## Dinâmicas para treinar\n" + "".join(f"- {link(d)}\n" for d in sorted(dyns)) + "\n"
    if top:
        t += f"## Dicas essenciais\n*Seleção; todas as {len(dk)} dicas estão em {link('Dicas - ' + c)}.*\n\n" + "".join(fmt_dica(s, it) for s, it in top) + "\n"
    if cons: t += "## Conceitos mais ligados\n" + "".join(f"- {link(x)} · {n}\n" for x, n in cons.most_common(15)) + "\n"
    t += f"## Relacionados\n- {link('Dicas - ' + c)}\n- [[MOC - Competências clínicas]]\n"
    write("04 - Competências Clínicas", c, t)
t = fm(tipo="moc", tags=["moc", "competencia"]) + "\n# MOC — Competências clínicas\n\n> [!abstract] As 18 competências que organizam o vault. A lógica vem do Aprimoramento Clínico: pegar uma competência geral (\"interpretar\", \"acolher\") e quebrá-la em pedaços treináveis.\n\n| Competência | O que é | Fontes | Dinâmicas | Dicas |\n|---|---|---|---|---|\n"
for c, slug, desc in COMPS:
    nfo = sum(1 for s in IDS if c in src_comps(s))
    nd = sum(1 for can, items in DYN.items() if any(comp_ok(x) == c for _, it in items for x in (it.get("competencias") or [])))
    t += f"| {link(c)} | {desc} | {nfo} | {nd} | {len(dicas_by.get(c, []))} |\n"
write("04 - Competências Clínicas", "MOC - Competências clínicas", t)

# ================================================================ FORMATOS DE GRUPO
FORMATOS = [
 ("Aprimoramento clínico (modelo Alan)", lambda s, f: s.startswith("alan-") or s == "acervo-13"),
 ("Curso de introdução à prática deliberada", lambda s, f: s.startswith("pd-")),
 ("Prática clínica (série de encontros)", lambda s, f: s.startswith("pc-")),
 ("Monitoria (supervisão em grupo)", lambda s, f: s.startswith("mon-") or "monitoria" in f or "monitoring" in f),
 ("Duelo de abordagens", lambda s, f: "duelo" in f),
 ("Mesa de estudos", lambda s, f: "mesa de estudo" in f),
 ("Dinâmica de troca (roleplay em revezamento)", lambda s, f: "dinamica de troca" in f or "revezamento" in f),
 ("Roleplay com plateia observadora", lambda s, f: "aquario" in f or "plateia" in f or "observador" in f or "roleplay unico" in f or "interrompido" in f),
 ("Roda de discussão com análise de vídeo", lambda s, f: "analise de video" in f),
 ("Roda reflexiva", lambda s, f: "reflexiv" in f or "vivencial" in f or "roda de discuss" in f or "roda de conversa" in f or "dialogic" in f),
 ("Aprimoramento clínico (outras variações)", lambda s, f: True),
]
fmt_src = collections.defaultdict(list)
for sid in IDS:
    fg = DOCS[sid].get("formato_grupo")
    if not isinstance(fg, dict): continue
    txt = strip_acc((clean(DOCS[sid].get("formato")) + " " + clean(fg.get("nome")) + " " + clean(fg.get("estrutura_padrao"))[:200]).lower())
    for nome, fn in FORMATOS:
        if fn(sid, txt): fmt_src[nome].append(sid); break
for nome, _ in FORMATOS:
    sids = fmt_src.get(nome, [])
    if not sids: continue
    facs = sorted({f for s in sids for f in (DOCS[s].get("facilitadores") or [])})
    t = fm(tipo="formato", facilitadores=facs, fontes=[link(nota(s)) for s in sids], n_exemplos=len(sids), tags=["formato-de-grupo"])
    t += f"\n# {nome}\n\n> [!abstract] {len(sids)} encontro(s) do acervo usam este formato · facilitadores: {', '.join(facs) or '—'}\n\n"
    t += "## Como cada fonte descreve o formato\n"
    for s in sids:
        fg = DOCS[s]["formato_grupo"]
        t += f"\n### {link(nota(s))}\n*{clean(fg.get('nome'))}* — conduzido por {quem_de(s)}.\n\n"
        for lab, k in [("Objetivo", "objetivo"), ("Público", "publico"), ("Tamanho", "tamanho"), ("Duração", "duracao"),
                       ("Estrutura padrão", "estrutura_padrao"), ("Papel do facilitador", "papel_facilitador"), ("Regras e combinados", "regras_combinados"),
                       ("Comparação com o modelo do Alan", "comparacao_com_alan")]:
            if clean(fg.get(k)): t += f"- **{lab}:** {clean(fg.get(k))}\n"
    t += "\n## Relacionados\n- [[MOC - Formatos de grupo]]\n- [[Anatomia de um encontro de aprimoramento]]\n"
    write("09 - Formatos de Grupo", nome, t)
t = fm(tipo="moc", tags=["moc", "formato-de-grupo"]) + "\n# MOC — Formatos de grupo\n\n> [!abstract] Os formatos de encontro que aparecem no acervo da Allos. Use a tabela para escolher o formato pelo objetivo; abra a nota do formato para ver roteiros e exemplos reais.\n\n| Formato | Exemplos | Objetivo (1ª fonte) | Estrutura padrão (1ª fonte) |\n|---|---|---|---|\n"
for nome, _ in FORMATOS:
    sids = fmt_src.get(nome, [])
    if not sids: continue
    fg = DOCS[sids[0]]["formato_grupo"]
    t += f"| {link(nome)} | {len(sids)} | {clean(fg.get('objetivo'))[:180].replace('|', '/')} | {clean(fg.get('estrutura_padrao'))[:220].replace('|', '/')} |\n"
write("09 - Formatos de Grupo", "MOC - Formatos de grupo", t)

# ================================================================ CONTEÚDO
ideias = list(all_items("ideias_conteudo"))
t = fm(tipo="conteudo", n_ideias=len(ideias), tags=["conteudo"]) + f"\n# Banco de ideias de conteúdo\n\n> [!abstract] {len(ideias)} ideias extraídas das fontes, por pilar e formato. Cada uma aponta para o trecho do vídeo de onde saiu.\n> Regra de ouro: nenhuma ideia usa material de caso clínico. Confira o [[Estratégia de conteúdo|checklist ético]] antes de publicar.\n\n"
for p, pn in PILARES + [("outros", "Outros")]:
    its = [(s, it) for s, it in ideias if (it.get("pilar") or "outros") == p or (p == "outros" and it.get("pilar") not in PNOME)]
    if not its: continue
    t += f"## {pn} · {len(its)}\n"
    for f in ["carrossel", "reels", "post", "stories"] + sorted({clean(it.get('formato')) for _, it in its} - {"carrossel", "reels", "post", "stories"}):
        fi = [(s, it) for s, it in its if clean(it.get("formato")) == f]
        if not fi: continue
        t += f"\n### {f.capitalize()}\n"
        for s, it in fi:
            t += f"- **{clean(it.get('gancho'))}** → {clean(it.get('mensagem'))} — {link(nota(s))}"
            if ts(s, it.get("corte_inicio")): t += f" · corte {ts(s, it.get('corte_inicio'))}–{clean(it.get('corte_fim'))}"
            t += "\n"
            rot = [clean(r) for r in (it.get("roteiro") or []) if clean(r)]
            if rot: t += "".join(f"    {i}. {r}\n" for i, r in enumerate(rot, 1))
    t += "\n"
write("11 - Conteúdo e Vídeos", "Banco de ideias de conteúdo", t)

def secs(x):
    try:
        p = [int(v) for v in x.split(":")]
        while len(p) < 3: p.insert(0, 0)
        return p[0] * 3600 + p[1] * 60 + p[2]
    except Exception: return None
cortes = [(s, it) for s, it in ideias if ts(s, it.get("corte_inicio")) and secs(clean(it.get("corte_fim")) or "") ]
t = fm(tipo="conteudo", tags=["conteudo", "conteudo/cortes"]) + f"\n# Cortes para Reels e vídeos\n\n> [!abstract] {len(cortes)} trechos que funcionam sozinhos, com início e fim. Clique no tempo para abrir o vídeo no ponto exato.\n> Antes de usar um corte de vídeo da Allos, confirme a autorização de uso da imagem e da fala de quem aparece.\n\n| Início | Fim | Duração | Gancho | Pilar | Fonte |\n|---|---|---|---|---|---|\n"
for s, it in cortes:
    a, b = secs(clean(it.get("corte_inicio"))), secs(clean(it.get("corte_fim")))
    dur = f"{(b - a)} s" if a is not None and b and b > a else "—"
    t += f"| {ts(s, it.get('corte_inicio'))} | {clean(it.get('corte_fim'))} | {dur} | {clean(it.get('gancho')).replace('|', '/')} | {PNOME.get(it.get('pilar'), '—')} | {link(nota(s))} |\n"
write("11 - Conteúdo e Vídeos", "Cortes para Reels e vídeos", t)

cit = list(all_items("citacoes"))
cit_by = collections.defaultdict(list)
for s, it in cit: cit_by[tema_de(clean(it.get("texto")) + " " + clean(it.get("tema")))].append((s, it))
t = fm(tipo="conteudo", n_frases=len(cit), tags=["conteudo", "conteudo/frases"]) + f"\n# Frases para citar\n\n> [!abstract] {len(cit)} frases limpas das falas (vícios de fala removidos, sentido preservado), por tema. Ao publicar, credite quem disse e a Allos.\n\n"
for tema in TEMA_NOMES:
    its = cit_by.get(tema, [])
    if not its: continue
    t += f"## {tema} · {len(its)}\n"
    for s, it in its:
        t += f"> \"{clean(it.get('texto'))}\"\n> — {quem_de(s)}, {src(s, it.get('ts'))}\n\n"
write("11 - Conteúdo e Vídeos", "Frases para citar", t)

# Pautas de vídeo por tema
for tema in TEMA_NOMES:
    tes = teses_by.get(tema, [])
    if len(tes) < 5: continue
    tes_s = sorted(tes, key=lambda x: (not is_alan(x[0]), -len(clean(x[1].get("argumento")))))[:8]
    ids_t = [(s, it) for s, it in ideias if tema_de(clean(it.get("gancho")) + " " + clean(it.get("mensagem"))) == tema][:10]
    cits = cit_by.get(tema, [])[:8]
    dic = [(s, it) for s, it in all_items("dicas_clinicas") if tema_de(clean(it.get("dica")) + " " + clean(it.get("justificativa"))) == tema]
    dic = sorted(dic, key=lambda x: (not is_alan(x[0]), -len(clean(x[1].get("justificativa")))))[:8]
    fontes = list(dict.fromkeys([nota(s) for s, _ in tes_s + dic]))[:12]
    t = fm(tipo="conteudo", formato="video-longo", tema=tema, status="pauta", tags=["conteudo", "conteudo/video"])
    t += f"\n# Pauta de vídeo — {tema}\n\n> [!abstract] Pauta montada automaticamente a partir do acervo, para um vídeo de 8–15 min, aula ou episódio de podcast/live.\n> Escolha 1 gancho, 3 teses como blocos, 1–2 dicas práticas por bloco e feche com uma frase. Revise a linguagem antes de gravar.\n\n"
    t += "## Estrutura sugerida\n1. **Gancho (0–30 s):** uma pergunta ou afirmação forte (opções abaixo).\n2. **O problema (1–2 min):** por que isso importa na clínica.\n3. **Três blocos (2–3 min cada):** tese → argumento → exemplo → o que fazer na prática.\n4. **Contraponto (1 min):** a posição que a tese critica, apresentada com honestidade.\n5. **Fechamento (30 s):** uma frase para lembrar + chamada (comentário, grupo, próximo vídeo).\n\n"
    if ids_t: t += "## Opções de gancho\n" + "".join(f"- {clean(it.get('gancho'))} — {link(nota(s))}\n" for s, it in ids_t) + "\n"
    t += "## Teses para os blocos\n" + "".join(fmt_tese(s, it) for s, it in tes_s) + "\n"
    if dic: t += "## Dicas práticas para ilustrar\n" + "".join(fmt_dica(s, it) for s, it in dic) + "\n"
    if cits: t += "## Frases para fechar\n" + "".join(f"> \"{clean(it.get('texto'))}\" — {quem_de(s)}, {src(s, it.get('ts'))}\n\n" for s, it in cits)
    t += "## Para aprofundar antes de gravar\n" + "".join(f"- {link(f)}\n" for f in fontes) + f"- {link('Teses - ' + tema)}\n"
    write("11 - Conteúdo e Vídeos/Pautas de vídeo", f"Pauta - {tema}", t)

# ================================================================ MÉTODO ALAN (partes geradas)
ALAN = [s for s in IDS if s.startswith("alan-")]
MODULOS = [
 ("Relação terapêutica e cosmovisão", ["alan-01", "alan-04", "alan-05"]),
 ("Escuta nas abordagens", ["alan-08", "alan-09", "alan-10"]),
 ("Intervenção", ["alan-02", "alan-03", "alan-16", "alan-17"]),
 ("Interpretação, diagnóstico e formulação de caso", ["alan-11", "alan-12", "alan-13"]),
 ("Priorização clínica", ["alan-14", "alan-15"]),
 ("Aprofundamento e psicoeducação", ["alan-06", "acervo-13", "alan-07"]),
 ("Terapia de casal", ["alan-18"]),
]
for mod, sids in MODULOS:
    sids = [s for s in sids if s in DOCS]
    t = fm(tipo="apostila", modulo=mod, fontes=[link(nota(s)) for s in sids], tags=["allos/alan", "apostila"])
    t += f"\n# Apostila — {mod}\n\n> [!abstract] Como usar\n> Esta apostila reúne, na ordem de estudo, o **conteúdo** dos encontros do Alan sobre {mod.lower()}.\n> Os blocos abaixo são trechos embutidos (transclusão) das notas dos encontros: o texto fica na nota original e aparece aqui já organizado para leitura.\n\n"
    t += "## Roteiro de estudo\n" + "".join(f"{i}. {link(nota(s))} — {clean(DOCS[s].get('em_uma_frase'))}\n" for i, s in enumerate(sids, 1)) + "\n"
    for i, s in enumerate(sids, 1):
        n = nota(s)
        t += f"---\n## {i}. {n}\n> {clean(DOCS[s].get('em_uma_frase'))}\n\n![[{n}#Conteúdo teórico]]\n\n### Dicas clínicas deste encontro\n![[{n}#Dicas clínicas]]\n\n### Teses deste encontro\n![[{n}#Teses e posicionamentos]]\n\n"
    dy = list(dict.fromkeys(can for can, items in DYN.items() if any(x in sids for x, _ in items)))
    if dy: t += "---\n## Dinâmicas para praticar este módulo\n" + "".join(f"- {link(d)}\n" for d in dy) + "\n"
    cc = collections.Counter()
    for s in sids:
        for it in DOCS[s].get("conceitos") or []:
            k = nkey(it.get("nome")); can = next((x for x in CON if nkey(x) == k), None)
            if can: cc[can] += 1
    if cc: t += "## Glossário do módulo\n" + "".join(f"- {link(c)}\n" for c, _ in cc.most_common(30)) + "\n"
    t += "## Perguntas para aprofundar\n" + "".join(f"![[{nota(s)}#Perguntas para aprofundar]]\n\n" for s in sids)
    t += "## Relacionados\n- [[Trilha curricular do Alan]]\n- [[MOC - Método Alan]]\n"
    write("01 - Método Alan/Apostilas", f"Apostila - {mod}", t)

# Trilha curricular
t = fm(tipo="metodo", tags=["allos/alan", "metodo"]) + "\n# Trilha curricular do Alan\n\n"
t += "> [!abstract] Os 18 encontros de Aprimoramento Clínico do Alan organizados em módulos de estudo, com o que cada um ensina, quem conduziu e quais dinâmicas usa.\n\n"
t += "## Módulos\n"
for mod, sids in MODULOS:
    t += f"\n### {link('Apostila - ' + mod, mod)}\n| Encontro | Conduzido por | Em uma frase | Dinâmicas |\n|---|---|---|---|\n"
    for s in sids:
        if s not in DOCS: continue
        dy = ", ".join(link(can) for can, items in DYN.items() if any(x == s for x, _ in items)) or "—"
        t += f"| {link(nota(s))} | {quem_de(s)} | {clean(DOCS[s].get('em_uma_frase')).replace('|', '/')} | {dy} |\n"
t += """
## Cronologia e ressalvas (o que os fichamentos descobriram)
- A numeração 01–18 **não é cronológica**. O Alan trabalha em ciclos de 4 ou 8 semanas; o 16 e o 17 falam em "fim de ciclo".
- O **Alan 18 (Terapia de casal)** é o "especial de Dia dos Namorados" que o próprio Alan, na abertura do **Alan 12**, avalia como "excessivamente teórico". Por isso o 12 é quase só prática. Na cronologia real, o 18 vem antes do 12.
- O **Alan 11 (Psicodiagnóstico)**, com a "dinâmica dos poemas", parece anterior ao 02 e ao 08, que citam essa dinâmica como já feita.
- O **Alan 04** não foi conduzido pelo Alan: quem conduziu foi Artur (núcleo junguiano), substituindo-o. O Alan comenta isso no início do 05.
- O **Alan 09** continua o exercício lacaniano começado no **Alan 08**. Os títulos enganam: o 08 tem pouca fenomenologia, e o 09 é majoritariamente análise do comportamento e TCC.
- O **Acervo 13** (gincana de esquemas de aprofundamento) tudo indica que foi conduzido pelo próprio Alan e repete o conteúdo do 06.

## Relacionados
- [[MOC - Método Alan]] · [[Anatomia de um encontro de aprimoramento]] · [[Dinâmicas do Alan - visão geral]]
"""
write("01 - Método Alan", "Trilha curricular do Alan", t)

# Dinâmicas do Alan
t = fm(tipo="metodo", tags=["allos/alan", "metodo", "dinamica"]) + "\n# Dinâmicas do Alan — visão geral\n\n| Dinâmica | Encontro | Competências | Nível | Online | Objetivo |\n|---|---|---|---|---|---|\n"
for s in [x for x in IDS if is_alan(x)]:
    for it in DOCS[s].get("dinamicas") or []:
        can = ALIASES.get(it["nome"].strip(), fname(it["nome"].strip()))
        if not can.startswith("Dinâmica - "): can = ALIASES.get("Dinâmica - " + can, "Dinâmica - " + can)
        cs = ", ".join(link(c2) for c in (it.get("competencias") or []) if (c2 := comp_ok(c)))
        t += f"| {link(can)} | {link(nota(s))} {ts(s, it.get('ts'))} | {cs} | {clean(it.get('nivel'))} | {'sim' if it.get('funciona_online') else '—'} | {clean(it.get('objetivo'))[:200].replace('|', '/')} |\n"
t += "\n## Relacionados\n- [[MOC - Dinâmicas]] · [[MOC - Método Alan]]\n"
write("01 - Método Alan", "Dinâmicas do Alan - visão geral", t)

# Repertório de facilitação
CATS = [
 ("Abrir, contextualizar e combinar", r"abr|contextualiz|retom|cronograma|combinad|introdu|enquadr|contrato|objetivo do encontro"),
 ("Convocar participação", r"convoc|chama|particip|chat|volunt|rodada|levant|pelo nome|engaj|inclui"),
 ("Perguntar e fazer o grupo pensar", r"pergunt|socr|desafi|provoc|problematiz|faz o grupo|devolve a pergunta|enigma|adivinh"),
 ("Demonstrar e encenar", r"demonstr|encen|roleplay|faz o paciente|faz de paciente|modela|ao vivo|caricat|interpreta o paciente"),
 ("Dar feedback e corrigir", r"feedback|corrig|valid|elogi|reformul|parafras|nomeia|critério|avalia|aponta"),
 ("Teorizar e comparar abordagens", r"teori|compar|abordage|esquema|taxonom|conceit|explica|lousa|quadro|diagrama|desenh"),
 ("Lidar com discordância, silêncio e imprevistos", r"discord|resist|sil[eê]ncio|conflit|imprevist|atras|pouca gente|grupo pequeno|question|contest|obje[cç]"),
 ("Gerir tempo e ritmo", r"tempo|ritmo|encurt|adia|cronometr|acelera|corta"),
 ("Humor, clima e vínculo com o grupo", r"humor|piada|brinc|leve|descontra|clima|acolh|autoironia|ironia"),
 ("Metacomentário e autocrítica", r"meta|autocr|pr[oó]pria condu|admite|transpar|explicita a inten|explica por que"),
 ("Fechar e encaminhar", r"fech|encerr|tarefa|s[ií]ntese|resum|pr[oó]ximo encontro|casa"),
]
mov = [(s, it) for s in IDS if is_alan(s) for it in (DOCS[s].get("movimentos_facilitacao") or [])]
by = collections.defaultdict(list)
for s, it in mov:
    txt = strip_acc((clean(it.get("movimento")) + " " + clean(it.get("descricao"))).lower()); best, bs = "Outros movimentos", 0
    for nome, rx in CATS:
        n = len(re.findall(strip_acc(rx), txt))
        if n > bs: best, bs = nome, n
    by[best].append((s, it))
t = fm(tipo="metodo", tags=["allos/alan", "metodo"]) + f"\n# Repertório de facilitação do Alan\n\n> [!abstract] {len(mov)} movimentos de condução observados nos encontros e monitorias do Alan (inclui encontros, monitorias e Prática Clínica conduzidos por ele; o Alan 04, conduzido por Artur, fica de fora), agrupados por função.\n> Use como cardápio: escolha 2 ou 3 movimentos para treinar de propósito no seu próximo grupo.\n\n"
for nome in [c[0] for c in CATS] + ["Outros movimentos"]:
    its = by.get(nome, [])
    if not its: continue
    t += f"## {nome} · {len(its)}\n"
    for s, it in its:
        t += f"- **{clean(it.get('movimento'))}** — {clean(it.get('descricao'))}"
        if clean(it.get("exemplo")): t += f" *Ex.:* {clean(it.get('exemplo'))}"
        t += f" — {src(s, it.get('ts'))}\n"
    t += "\n"
t += "## Relacionados\n- [[Anatomia de um encontro de aprimoramento]] · [[Reflexões do Alan sobre a condução]] · [[MOC - Método Alan]]\n"
write("01 - Método Alan", "Repertório de facilitação do Alan", t)

# Reflexões
t = fm(tipo="metodo", tags=["allos/alan", "metodo"]) + "\n# Reflexões do Alan sobre a condução\n\n> [!abstract] O que o Alan diz sobre o próprio jeito de conduzir: erros que admite, ajustes que faz, críticas que recebeu, o que funciona online e o que não funciona. Esse é o material mais direto para quem vai conduzir grupos.\n\n"
for s in [x for x in IDS if is_alan(x)]:
    rs = [clean(r) for r in (DOCS[s].get("reflexoes_do_facilitador") or []) if clean(r)]
    if not rs: continue
    t += f"## {link(nota(s))}\n" + "".join(f"- {r}\n" for r in rs) + "\n"
t += "## Relacionados\n- [[Repertório de facilitação do Alan]] · [[MOC - Método Alan]]\n"
write("01 - Método Alan", "Reflexões do Alan sobre a condução", t)

# Pensamento clínico (teses do Alan por tema)
t = fm(tipo="metodo", tags=["allos/alan", "metodo", "tese"]) + "\n# Pensamento clínico do Alan\n\n> [!abstract] As teses defendidas pelo Alan nos encontros e monitorias, organizadas por tema, com o argumento de cada uma. É o \"o que o Alan pensa\" em forma de índice; as versões completas estão nas notas [[MOC - Teses e posicionamentos|Teses]].\n\n"
for tema in TEMA_NOMES:
    its = [(s, it) for s, it in teses_by.get(tema, []) if quem_grupo(s, it) == "Alan"]
    if not its: continue
    t += f"## {tema} · {len(its)}\n" + "".join(f"- **{clean(it.get('tese'))}** — {clean(it.get('argumento'))} ({src(s, it.get('ts'))})\n" for s, it in its) + "\n"
t += "## Relacionados\n- [[MOC - Método Alan]]\n"
write("01 - Método Alan", "Pensamento clínico do Alan", t)

# Anatomia — dados
est = [(s, b) for s in ALAN if s != "alan-04" for b in (DOCS[s].get("estrutura") or []) if isinstance(b, dict)]
def bnorm(b):
    x = strip_acc(clean(b).lower())
    for k, v in [("abert", "Abertura"), ("retom", "Retomada"), ("combin", "Combinados"), ("compar", "Comparação de abordagens"), ("teor", "Teoria"),
                 ("demonstr", "Demonstração"), ("dinam", "Dinâmica"), ("rodada", "Rodada de respostas"), ("feedback", "Feedback"), ("discuss", "Discussão"),
                 ("duvid", "Dúvidas"), ("fech", "Fechamento"), ("taref", "Tarefa")]:
        if k in x: return v
    return "Bate-papo/Outro"
cnt = collections.Counter(); mins = collections.defaultdict(list)
for s, b in est:
    k = bnorm(b.get("bloco")); cnt[k] += 1
    try: mins[k].append(float(b.get("duracao_min")))
    except Exception: pass
t = fm(tipo="metodo", tags=["allos/alan", "metodo"]) + "\n# Anatomia de um encontro de aprimoramento — dados\n\n> [!abstract] Levantamento automático dos blocos de todos os encontros do Alan (exceto o 04). Serve de base empírica para a [[Anatomia de um encontro de aprimoramento]].\n\n## Frequência e duração dos blocos\n| Bloco | Ocorrências | Duração média (min) |\n|---|---|---|\n"
for k, n in cnt.most_common():
    m = mins.get(k) or []; t += f"| {k} | {n} | {round(sum(m) / len(m)) if m else '—'} |\n"
t += "\n## Sequência de blocos em cada encontro\n| Encontro | Sequência |\n|---|---|\n"
for s in ALAN:
    if s == "alan-04": continue
    seq = []
    for b in DOCS[s].get("estrutura") or []:
        k = bnorm(b.get("bloco"))
        if not seq or seq[-1] != k: seq.append(k)
    t += f"| {link(nota(s))} | {' → '.join(seq)} |\n"
write("01 - Método Alan", "Anatomia de um encontro - dados", t)

# ================================================================ MOC FICHAMENTOS
SER = [("alan", "Aprimoramento clínico — Alan"), ("acervo", "Aprimoramento clínico — Acervo (outros facilitadores)"), ("mon", "Monitorias"),
       ("pd", "Introdução à Prática Deliberada"), ("pc", "Prática Clínica"), ("dicas", "YouTube — Dicas para a Avaliação Clínica"),
       ("psigeral", "YouTube — Psicologia Geral"), ("comparada", "YouTube — Psicologia Comparada"), ("pbe", "YouTube — PBE"),
       ("estudar", "YouTube — Como Estudar"), ("formacao", "YouTube — Allos Formação"), ("cumbuca", "Podcast — CumbucaCast"), ("avulsos", "Vídeos avulsos")]
t = fm(tipo="moc", tags=["moc"]) + f"\n# MOC — Fichamentos\n\n> [!abstract] {len(DOCS)} de {len(MAN)} vídeos já têm fichamento. Os pendentes estão listados no fim, com o link da transcrição.\n\n"
for pre, nome in SER:
    sids = [s for s in IDS if s.startswith(pre + "-")]
    pend = [m for k, m in MAN.items() if k.startswith(pre + "-") and k not in DOCS]
    if not sids and not pend: continue
    t += f"## {nome} · {len(sids)}/{len(sids) + len(pend)}\n"
    if sids:
        t += "| Nota | Facilitador(es) | Em uma frase |\n|---|---|---|\n"
        for s in sids: t += f"| {link(nota(s))} | {quem_de(s)} | {clean(DOCS[s].get('em_uma_frase')).replace('|', '/')} |\n"
    if pend:
        t += "\n**Ainda sem fichamento:** " + " · ".join(link(m["transcricao"]) for m in sorted(pend, key=lambda m: m["id"])) + "\n"
    t += "\n"
write("10 - Fichamentos", "MOC - Fichamentos", t)

json.dump(ALIASES, open(os.path.join(SP, "agg", "aliases.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"fontes={len(DOCS)} dinamicas={len(DYN)} conceitos={len(CON)} autores={len(AUT)} aliases={len(ALIASES)} arquivos={len(WRITTEN)}")
print({k: len(v) for k, v in fmt_src.items()})
print({k: len(v) for k, v in teses_by.items()})
