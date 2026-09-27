---
tipo: "moc"
tags: ["sistema"]
---

# LEIA-ME — instruções para o Claude Code (computador local)

Este arquivo é para o **Claude Code** que vai levar este material para o Obsidian. As notas para leitura humana começam em [[00 - Início]].

## 1. Estrutura do repositório
```
transcricoes-allos/
├── Obsidian Allos/          ← O VAULT (notas de síntese, fichamentos, templates)
├── _processamento/          ← spec, scripts e dados estruturados (NÃO vai para o vault)
├── 00 - Índice.md           ← índice das transcrições brutas
└── <13 pastas de transcrições>  (Aprimoramento clínico - Alan/, Monitorias/, Playlist - .../ ...)
```

## 2. Como importar para o Obsidian
1. Copie a pasta `Obsidian Allos/` inteira para dentro do vault do usuário, ou abra-a diretamente como vault.
2. Copie as **13 pastas de transcrições** e o `00 - Índice.md` para dentro de `Obsidian Allos/90 - Transcrições/`.
   - Motivo: cada fichamento linka a transcrição original pelo nome do arquivo (ex.: `[[01 - Relação Terapêutica tensionada]]`). O Obsidian resolve o link pelo nome, em qualquer pasta do vault.
3. **Não renomeie notas.** Os links dependem dos nomes exatos. Se precisar renomear, faça isso pelo próprio Obsidian, que atualiza os links.
4. Plugins: nenhum é obrigatório.
   - Opcional: **Dataview**, para as consultas em [[00 - Início]] (os campos `tipo`, `origem`, `nivel`, `n_fontes` etc. estão no frontmatter).
   - Recomendado: plugin nativo **Templates** apontando para `99 - Templates`.
5. Os links "▶ 0:12:34" são links do YouTube com o tempo exato e funcionam direto no Obsidian.

## 3. O que foi feito e o que falta
- **Fichados (nota + JSON estruturado):** 18 encontros do Alan, 22 monitorias, 25 encontros do Acervo, 9 de Prática Deliberada, 7 de Prática Clínica e 14 vídeos da playlist "Dicas para a Avaliação Clínica". O [[MOC - Fichamentos]] mostra o estado exato.
- **Pendentes (49 vídeos, só com transcrição bruta):** Psicologia Geral (7), Psicologia Geral - Allos Formação (11), PBE (8), Psicologia Comparada (4), Como Estudar (6), CumbucaCast (2), Vídeos avulsos (3; o `avulsos-03` é idêntico ao `psigeral-04`).
- **Notas de síntese** (dinâmicas, competências, dicas, teses, conceitos, abordagens, autores, formatos, bancos de conteúdo, apostilas e trilha do Alan): **geradas por script** a partir dos JSONs. Se novos vídeos forem fichados, basta rodar o script de novo (passo 4).

## 4. Como continuar o processamento (vídeos pendentes)
Todos os caminhos abaixo são relativos à raiz do repositório.
1. Leia `_processamento/spec/extracao.md`: é a especificação que cada agente seguiu (modelo de nota, vocabulários controlados, privacidade, formato do JSON e o token de tempo `{{ts:ID@H:MM:SS}}`).
2. Os IDs, caminhos e vídeos das fontes estão em `_processamento/manifest.json`. Os pendentes são os IDs sem arquivo em `_processamento/extract/`.
3. Para cada vídeo pendente: leia a transcrição inteira, escreva a nota em `Obsidian Allos/10 - Fichamentos/...` e o JSON em `_processamento/extract/<id>.json`, seguindo a spec.
4. Depois, regenere a síntese e os links:
   ```bash
   python3 _processamento/tools/synth.py _processamento "Obsidian Allos"      # notas de síntese
   python3 _processamento/tools/ts_links.py "Obsidian Allos"                   # tokens {{ts}} → links do YouTube
   python3 _processamento/tools/links.py normalize "Obsidian Allos" _processamento/agg/aliases.json
   python3 _processamento/tools/links.py report "Obsidian Allos" .             # confere links quebrados
   ```
   O `synth.py` sobrescreve só as notas que ele gera. Notas escritas à mão ([[Anatomia de um encontro de aprimoramento]], [[MOC - Método Alan]], [[Estratégia de conteúdo]], [[00 - Início]]) e os fichamentos não são tocados.

## 5. Melhorias possíveis (quando houver cota)
- Reescrever as apostilas (hoje montadas por transclusão das seções "Conteúdo teórico") como texto corrido e didático.
- Consolidar conceitos duplicados com nomes diferentes (há ~670 conceitos; os centrais estão no topo de [[MOC - Conceitos]]).
- Criar um kit de formação de novos facilitadores (trilha de preparação, roteiros de encontro prontos, rubrica de feedback) e uma porta de entrada por perfil na [[00 - Início]]. O usuário pediu para deixar isso para depois.

## 6. Regras que valem sempre
- **Privacidade:** nenhum dado de paciente ou de caso clínico em nota pública ou em conteúdo; participantes aparecem anonimizados.
- **Fidelidade:** o que se atribui a um facilitador precisa estar na fonte; inferências vão marcadas como "Leitura do vault" ou com "(?)".
