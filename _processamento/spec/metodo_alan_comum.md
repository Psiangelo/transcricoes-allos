# Síntese do MÉTODO ALAN (pasta `01 - Método Alan/`)

Leia primeiro a especificação geral de síntese: SCRATCH/spec/sintese.md (regras de estilo, privacidade, tokens de
tempo, frontmatter). SCRATCH = _processamento

Fontes disponíveis:
- As 18 notas-fichamento dos encontros do Alan em `Obsidian Allos/02 - Encontros do Alan/`
  (cada uma com ~6 mil palavras; seções "Estrutura do encontro", "Dinâmica(s)", "Como o facilitador conduz",
  "Para replicar este encontro", "Teses e posicionamentos"...). Use `grep`/`sed -n` para ler seções específicas
  em vez de ler as 18 notas inteiras.
- Pacotes JSON com os dados estruturados em `SCRATCH/bundles/alan_*.json` (leia com python se for grande:
  `python3 -c "import json;d=json.load(open('...'));print(...)"`).
- Monitorias do Alan (supervisões): notas em `Obsidian Allos/10 - Fichamentos/Monitorias/Monitoria 0*.md`.

Fatos já verificados pelos agentes de leitura (use-os):
- O "Alan 04 - Cosmovisão e clínica 1" NÃO foi conduzido pelo Alan: quem conduziu foi Artur (núcleo junguiano), substituindo-o.
- O "Alan 18 - Terapia de casal" é o "especial de Dia dos Namorados" que o próprio Alan, na abertura do Alan 12,
  avalia como "excessivamente teórico" — por isso o 12 vira quase só prática. Na cronologia real, o 18 vem antes do 12.
- A numeração 01–18 não é cronológica (ex.: o 11 - Psicodiagnóstico, com a "dinâmica dos poemas", parece anterior ao 02 e ao 08;
  o 06 parece posterior ao 13; o 09 continua o exercício lacaniano iniciado no 08). O Alan fala em ciclos de 4 ou 8 semanas;
  o 16 e o 17 falam em "fim de ciclo".
- Títulos que enganam: "Alan 08 - Escuta em fenomenologia" tem pouca fenomenologia (muito Freud/Lacan/Kant-Hegel);
  "Alan 09 - Escuta em psicanálise" é majoritariamente análise do comportamento e TCC.

Regras de link para ESTAS notas:
- Linke livremente as 18 notas `[[Alan NN - ...]]` (use o nome exato do arquivo) e as monitorias existentes.
- Competências (hubs que existirão): Escuta clínica · Interpretação · Priorização clínica · Intervenção · Construção frasal ·
  Aprofundamento · Psicoeducação · Relação terapêutica · Formulação de caso · Psicodiagnóstico ·
  Primeira sessão e entrevistas iniciais · Abertura e encerramento de sessão · Direção do tratamento · Feedback clínico ·
  Acolhimento e validação · Articulação teoria-prática · Pessoa do terapeuta · Desenvolvimento profissional
- Dinâmicas: linke com o nome que aparece nas notas/JSON (`[[Dinâmica - ...]]`); a normalização final é feita depois.
- Conceitos: linke só os mais centrais (ex.: [[Prática deliberada]], [[Psicologia comparada]], [[Hermenêutica]],
  [[Aliança terapêutica]], [[Cosmovisão]], [[Máximas clínicas]], [[Esquemas de aprofundamento]]).
- Notas irmãs desta pasta (existirão) — "COMO o Alan ensina": [[Anatomia de um encontro de aprimoramento]] · [[Repertório de facilitação do Alan]] ·
  [[Situações difíceis no grupo]] · [[Princípios pedagógicos do Alan]] · [[Pensamento clínico do Alan]] ·
  [[Trilha curricular do Alan]] · [[Dinâmicas do Alan - visão geral]] · [[Como o Alan supervisiona]] · [[MOC - Método Alan]]
- Apostilas — "O QUE o Alan ensina" (existirão, subpasta `01 - Método Alan/Apostilas/`):
  [[Apostila - Relação terapêutica e cosmovisão]] · [[Apostila - Escuta nas abordagens]] · [[Apostila - Intervenção]] ·
  [[Apostila - Interpretação, diagnóstico e formulação de caso]] · [[Apostila - Priorização clínica]] ·
  [[Apostila - Aprofundamento e psicoeducação]] · [[Apostila - Terapia de casal]]

Frontmatter mínimo: `tipo: metodo`, `tags: [allos/alan, metodo]`, `fontes: [...]` (links das notas usadas), `aliases: [...]`.
Profundidade: estas são as notas mais importantes do vault — sejam densas, concretas, com exemplos reais e tempos
(`{{ts:alan-NN@H:MM:SS}}`), tabelas quando ajudar, e sempre com a pergunta "como eu uso isso para conduzir o MEU grupo?".

IMPORTANTE — CONTEÚDO É TÃO IMPORTANTE QUANTO FORMA: o dono do vault pediu explicitamente que o CONTEÚDO (a teoria, os
argumentos, os exemplos clínicos, as comparações entre abordagens, as dicas) tenha o mesmo peso que a estrutura e a forma
dos grupos. Mesmo nas notas sobre "como o Alan ensina", mostre O QUE está sendo ensinado em cada exemplo.
