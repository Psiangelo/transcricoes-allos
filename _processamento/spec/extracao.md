# ESPECIFICAÇÃO — Leitura e fichamento das transcrições da Allos (Fase 1)

Você faz parte de uma equipe de ~60 agentes que está transformando 136 transcrições de vídeos da Allos
(grupos de formação em psicologia clínica) num **vault de Obsidian** que servirá a um psicólogo para:
1. produzir conteúdo para Instagram;
2. criar e conduzir seus próprios grupos e dinâmicas de formação clínica (o foco principal é
   entender a fundo a **estrutura dos grupos de Aprimoramento Clínico do Alan**);
3. estudar a teoria, as dicas clínicas e os pontos de vista (posicionamentos justificados) que aparecem nos vídeos.

Tudo em **português do Brasil**. Você vai LER suas transcrições por inteiro e produzir, para cada uma:
- (A) uma **nota Markdown** (o "fichamento") dentro do vault;
- (B) um **arquivo JSON** com os dados estruturados (que outros agentes vão usar para montar as notas de síntese).

Caminhos:
- Repositório: `/home/user/transcricoes-allos`
- Vault: `Obsidian Allos/`
- Manifesto das fontes (id, caminho, vídeo, duração): `SCRATCH/manifest.json`
- JSONs de saída: `SCRATCH/extract/<id>.json`
  (SCRATCH = `_processamento`)

---------------------------------------------------------------------------------------------------
## 1. Como ler

- Leia a transcrição **inteira**, do começo ao fim (use Read com offset/limit se precisar ler em partes; não pule trechos
  — muitas vezes a dinâmica e o melhor conteúdo estão no meio ou no fim).
- São legendas automáticas do YouTube: há muito ruído ("eh", repetições, palavras erradas, nomes trocados:
  "apemoramento" = aprimoramento, "Dodô" = pássaro Dodô, "lacan" = Lacan etc.). Corrija o óbvio; se não tiver
  certeza de um termo/nome, escreva-o seguido de "(?)". **Nunca invente** conteúdo que não está na fala.
- Os parágrafos começam com o tempo do vídeo, ex.: `**[0:12:34]**`. Use esses tempos para ancorar tudo.
- Há falas de várias pessoas (marcadas às vezes com `>>`). Identifique quem é o **facilitador** (quem conduz) e
  distinga da fala de participantes.

## 2. Marcação de tempo (IMPORTANTE)

Sempre que citar um momento do vídeo, use EXATAMENTE este token (um script depois o transforma em link clicável
para o YouTube no minuto certo):

    {{ts:ID@H:MM:SS}}        exemplo: {{ts:alan-01@0:12:34}}

- ID é o id da fonte no manifesto (`alan-01`, `acervo-07`, `mon-12`, `pbe-03`...).
- Formato do tempo sempre H:MM:SS (ex.: 0:05:07, 1:02:44). Use o tempo do parágrafo onde a ideia aparece.
- NÃO use o token dentro do frontmatter YAML. No JSON, use só o campo `"ts": "0:12:34"`.

## 3. Privacidade e ética (obrigatório)

- Monitorias e exercícios podem envolver **casos clínicos**. Nunca registre dados que identifiquem pacientes
  (nome, cidade, trabalho, idade exata combinada com outros dados, detalhes muito específicos da história).
  Descreva de forma genérica ("paciente adulta, queixa de ansiedade no trabalho"). Não copie falas de pacientes.
  Se o caso for fictício/simulado (roleplay, paciente de IA, caso inventado), diga que é simulado.
- Participantes (alunos): cite pelo primeiro nome só quando for necessário para entender a cena; prefira
  "uma participante", "um aluno". Facilitadores (Alan, Diogo, João de Bragança etc.) podem ser citados pelo nome.
- **Ideias de conteúdo para Instagram nunca usam material de caso clínico** — só conceitos, técnicas e opiniões.

## 4. Vocabulários controlados (use os nomes EXATOS — eles viram links do Obsidian)

### 4.1 Competências clínicas (notas-hub na pasta `04 - Competências Clínicas`)
Escuta clínica · Interpretação · Priorização clínica · Intervenção · Construção frasal · Aprofundamento ·
Psicoeducação · Relação terapêutica · Formulação de caso · Psicodiagnóstico · Primeira sessão e entrevistas iniciais ·
Abertura e encerramento de sessão · Direção do tratamento · Feedback clínico · Acolhimento e validação ·
Articulação teoria-prática · Pessoa do terapeuta · Desenvolvimento profissional

Slugs para tags (`competencia/<slug>`): escuta, interpretacao, priorizacao, intervencao, construcao-frasal,
aprofundamento, psicoeducacao, relacao-terapeutica, formulacao-de-caso, psicodiagnostico, primeira-sessao,
abertura-encerramento, direcao-do-tratamento, feedback-clinico, acolhimento, teoria-pratica, pessoa-do-terapeuta,
desenvolvimento-profissional

### 4.2 Abordagens (pasta `08 - Abordagens e Autores`)
Psicanálise freudiana · Psicanálise lacaniana · Psicologia analítica junguiana · Terapia cognitivo-comportamental ·
Análise do comportamento · Terapias contextuais · Fenomenologia e existencialismo · Abordagem centrada na pessoa ·
Gestalt-terapia · Terapia sistêmica · Terapia do esquema · Psicodrama
(Se aparecer outra abordagem relevante, crie um nome no mesmo estilo.)
Slugs para tags (`abordagem/<slug>`): psicanalise, lacan, junguiana, tcc, analise-do-comportamento, contextuais,
fenomenologia, acp, gestalt, sistemica, esquema, psicodrama

### 4.3 Autores
Nome completo usual: "Sigmund Freud", "Jacques Lacan", "Carl Jung", "Carl Rogers", "Aaron Beck", "B. F. Skinner",
"Anders Ericsson", "Bruce Wampold", "James Prochaska", "Gregory Bateson", "Edmund Husserl", "Martin Heidegger",
"Hans-Georg Gadamer", "Paul Ricoeur", "Immanuel Kant", "G. W. F. Hegel", "Steven Hayes", "Stefan Hofmann",
"Scott D. Miller", "Tony Rousmaniere", "Donald Winnicott", "William James"... (mesmo padrão para outros).

### 4.4 Conceitos (pasta `07 - Conceitos`) — nomes-semente preferenciais
Use estes nomes quando o conceito for o mesmo; para conceitos novos, crie nome curto, no singular, com só a
primeira letra maiúscula (exceto nomes próprios), sem sigla solta (escreva por extenso):
Aliança terapêutica · Transferência · Contratransferência · Ruptura e reparo da aliança · Equação pessoal ·
Cosmovisão · Pragmatismo · Hermenêutica · Antihermenêutica · Significante · Significante mestre ·
Quatro discursos de Lacan · Associação livre · Atenção flutuante · Corte da sessão · Redução fenomenológica ·
Empatia · Congruência · Aceitação positiva incondicional · Cibernética · Causalidade circular · Pergunta circular ·
Homeostase familiar · Prática deliberada · Expertise clínica · Psicologia baseada em evidências ·
Melhor evidência disponível · Preferências do paciente · Veredito do pássaro Dodô · Fatores comuns ·
Psicologia baseada em processos · Psicologia baseada em medidas · Diagnóstico diferencial · DSM ·
Estágios de mudança · Entrevista motivacional · Máximas clínicas · Curva do esquecimento · Palácio mental ·
Prontuário · Psicologia comparada · Psicologia transteórica · Protocolos clínicos · Ensaio clínico randomizado ·
Hierarquia de evidências · Objetivos da terapia · Esquemas de aprofundamento · Parâmetros da intervenção
(distância, intensidade, forma e conteúdo)

ATENÇÃO: um conceito NÃO pode ter o mesmo nome de uma competência (4.1) nem de uma abordagem (4.2). Se o conceito
for a própria competência (ex.: psicoeducação), link para a competência.

### 4.5 Dinâmicas (pasta `03 - Dinâmicas`)
Nome da nota: `Dinâmica - <Nome curto>` (ex.: `Dinâmica - Construção frasal`, `Dinâmica - Poemas`,
`Dinâmica - Variação de intervenção`). Se o facilitador der nome à dinâmica, use o nome dele.

### 4.6 Pilares de conteúdo (Instagram)
clinica-na-pratica (técnica, "como fazer") · ciencia-e-mitos (evidências, PBE, mitos) ·
abordagens-em-dialogo (comparação entre abordagens) · formacao-do-psicologo (estudo, carreira, prática deliberada) ·
bastidores-dos-grupos (dinâmicas e grupos — atrair participantes) · maximas-e-reflexoes (frases e posicionamentos)

### 4.7 Tipos de bloco (estrutura do encontro)
Abertura · Retomada · Combinados · Teoria · Comparação de abordagens · Demonstração · Dinâmica · Rodada de respostas ·
Feedback · Discussão · Dúvidas · Fechamento · Tarefa · Bate-papo/Outro

### 4.8 Caracteres proibidos em nomes de arquivo/nota
`# ^ [ ] | \ / : * ? " < >` — troque ":" por " -" e remova "?".

---------------------------------------------------------------------------------------------------
## 5. Onde salvar e como nomear a nota (A)

| Série (prefixo do id) | Pasta dentro do vault | Nome da nota |
|---|---|---|
| alan | `02 - Encontros do Alan/` | nome FIXO, ver lista abaixo |
| acervo | `10 - Fichamentos/Aprimoramento (Acervo)/` | `Acervo NN - <tema do encontro>` |
| mon | `10 - Fichamentos/Monitorias/` | `Monitoria NN - <Supervisor> - <tema>` |
| pd | `10 - Fichamentos/Prática Deliberada/` | `PD NN - <tema>` |
| pc | `10 - Fichamentos/Prática Clínica/` | `Prática Clínica NN - <tema>` |
| dicas | `10 - Fichamentos/YouTube/` | `YT Avaliação Clínica NN - <título em português>` |
| psigeral | `10 - Fichamentos/YouTube/` | `YT Psicologia Geral NN - <título em português>` |
| comparada | `10 - Fichamentos/YouTube/` | `YT Psicologia Comparada NN - <título em português>` |
| pbe | `10 - Fichamentos/YouTube/` | `YT PBE NN - <título em português>` |
| estudar | `10 - Fichamentos/YouTube/` | `YT Como Estudar NN - <título em português>` |
| formacao | `10 - Fichamentos/YouTube/` | `YT Formação NN - <título em português>` |
| cumbuca | `10 - Fichamentos/Podcasts/` | `Podcast CumbucaCast NN - <título em português>` |
| avulsos | `10 - Fichamentos/Podcasts/` | `Podcast Comunicallos NN - <título>` (avulsos-03 é duplicata de psigeral-04: ver prompt) |

NN = número do arquivo original com 2 dígitos. <tema> = título curto e descritivo (3 a 8 palavras) do que realmente
é trabalhado — os títulos originais do Acervo ("Encontro 1 e Encontro 2") não dizem nada, então dê um título temático.
Títulos em inglês (tradução automática do YouTube) devem virar português.

Nomes FIXOS dos encontros do Alan:
Alan 01 - Relação terapêutica tensionada · Alan 02 - Construção frasal · Alan 03 - Distância, intensidade, forma e conteúdo ·
Alan 04 - Cosmovisão e clínica 1 · Alan 05 - Cosmovisão e clínica 2 · Alan 06 - Esquemas de aprofundamento ·
Alan 07 - Psicoeducação · Alan 08 - Escuta em fenomenologia · Alan 09 - Escuta em psicanálise ·
Alan 10 - Escuta em sistêmica · Alan 11 - Psicodiagnóstico · Alan 12 - Formulação de caso 1 ·
Alan 13 - Formulação de caso 2 · Alan 14 - Priorização clínica 1 · Alan 15 - Priorização clínica 2 ·
Alan 16 - Intervenção · Alan 17 - Qualidade da intervenção · Alan 18 - Terapia de casal
(Pode e deve linkar os encontros vizinhos do Alan por esses nomes quando houver retomada/continuação.)

---------------------------------------------------------------------------------------------------
## 6. Modelo da nota (A)

Frontmatter (YAML) — todos os campos, mesmo que alguma lista fique vazia `[]`:

```yaml
---
tipo: encontro            # "encontro" para alan; "fichamento" para todas as outras séries
serie: "Aprimoramento Clínico — Alan"   # nome legível da série
fonte_id: alan-01
numero: 1
titulo_original: "Relação Terapêutica tensionada"
facilitadores: ["Alan"]
formato: "Aprimoramento clínico"   # Aprimoramento clínico | Monitoria | Mesa de estudos | Duelo de abordagens | Aula | Podcast | Vídeo curto | Prática clínica | Curso de PD | outro (diga qual)
video: "https://www.youtube.com/watch?v=..."
duracao: "1:49:12"
transcricao: "[[01 - Relação Terapêutica tensionada]]"   # nome do arquivo da transcrição sem .md (campo `transcricao` do manifesto)
competencias: ["[[Relação terapêutica]]", "[[Intervenção]]"]
abordagens: ["[[Psicanálise lacaniana]]"]
dinamicas: ["[[Dinâmica - Nome]]"]
conceitos: ["[[Transferência]]", "[[Aliança terapêutica]]"]
autores: ["[[Sigmund Freud]]"]
tags: [allos/alan, competencia/relacao-terapeutica, abordagem/lacan]
aliases: ["Relação Terapêutica tensionada"]
---
```
Tags de série: `allos/alan`, `allos/acervo`, `allos/monitoria`, `allos/pratica-deliberada`, `allos/pratica-clinica`,
`allos/youtube`, `allos/podcast`.

Corpo da nota (seções nesta ordem; omita uma seção só se realmente não houver nada para ela):

```markdown
# Alan 01 — Relação terapêutica tensionada

> [!abstract] Em uma frase
> <a ideia central do encontro/vídeo em 1–2 frases>

> [!info] Ficha
> **Facilitador:** ... · **Duração:** ... · **Formato:** ... · **Competências:** [[...]], [[...]]
> **Vídeo:** [assistir no YouTube](URL) · **Transcrição:** [[nome da transcrição]]

## Resumo
2 a 5 parágrafos: o que foi feito, qual o argumento central, como terminou.

## Estrutura do encontro
| Início | Bloco | O que acontece | Função pedagógica |
|---|---|---|---|
| {{ts:ID@0:00:02}} | Abertura | ... | por que isso está ali / o que prepara |
(uma linha por bloco — cubra o encontro inteiro; para vídeos curtos, faça "Roteiro do vídeo" com 3–6 linhas)

## Conteúdo teórico
Reconstrua o raciocínio de forma LIMPA, organizada e fiel (sem o ruído da fala), em subseções `### <Tema> {{ts:...}}`.
Explique como o facilitador explica: exemplos, metáforas, comparações entre abordagens, esquemas e listas que ele monta.
Esta é a parte que transforma a transcrição em material de estudo — seja generoso e preciso.

## Dinâmica(s)
Para cada exercício/dinâmica feito ou proposto:
### [[Dinâmica - Nome]]
- **Objetivo:** ...
- **Competência treinada:** [[...]]
- **Configuração:** (individual / duplas / trios / grupo todo; online/presencial; nº de pessoas)
- **Tempo aproximado:** ...
- **Consigna (o que o facilitador pede):** "..." (adaptada da fala)
- **Passo a passo:** 1. ... 2. ...
- **Como o facilitador dá feedback / critérios de qualidade:** ...
- **O que aconteceu na prática:** exemplos de respostas dos participantes e das correções (anonimizado) {{ts:...}}
- **Variações e armadilhas:** ...

## Dicas clínicas
Dicas práticas e acionáveis que aparecem (explícitas ou implícitas), SEMPRE com a justificativa:
- **<Dica no imperativo, concreta>** — *Por quê:* <justificativa dada/implícita>. *Quando:* <contexto>. {{ts:...}}

## Teses e posicionamentos
Pontos de vista defendidos (opiniões fortes, críticas, "eu penso que..."), com o argumento:
- **Tese:** <afirmação clara>
  - *Argumento:* <como é justificada>
  - *Contra quem / contraponto:* <a posição criticada ou objeção considerada, se houver>
  - *Implicação prática:* <o que muda na clínica ou na formação>
  - {{ts:...}}

## Como o facilitador conduz
(ESSENCIAL nas notas do Alan e de grupos; em vídeos-aula, curto ou omitido)
Movimentos de facilitação observados: como abre, como convoca participação, como corrige sem expor, como usa
exemplos, como lida com resistência/discordância/silêncio, como administra tempo, como fecha, meta-comentários
sobre a própria condução. Cada item com exemplo e {{ts:...}}.

## Conceitos-chave
- [[Conceito]] — definição tal como usada aqui (1–2 frases).

## Frases para guardar
> "<frase limpa, fiel ao sentido, pronta para citar>" {{ts:...}}
(5 a 15 frases fortes; limpe os vícios de fala sem mudar o sentido)

## Ideias de conteúdo
- **[Carrossel | Reels | Post | Stories] · pilar:** <gancho em 1 linha> → <mensagem central>. Corte sugerido: {{ts:...}}–{{ts:...}}

## Para replicar este encontro
(para Alan, Acervo, Prática Clínica, PD — roteiro enxuto com tempos para outra pessoa conduzir este mesmo encontro
com um novo grupo: preparação, abertura, bloco teórico mínimo, dinâmica, feedback, fechamento)

## Perguntas para aprofundar
- perguntas abertas, lacunas, pontos polêmicos para estudar depois

## Relacionados
- [[...]] (competências, conceitos, encontros vizinhos do Alan)
```

Para **monitorias**, acrescente depois do Resumo:
`## Caso em discussão (anonimizado)` (3–6 linhas, só o necessário) e `## Lições de supervisão` (o que o supervisor
ensina, erros apontados, raciocínio clínico demonstrado) — as lições são o coração dessas notas.

Profundidade esperada: encontros do Alan 3.000–6.000 palavras (são o foco do projeto — capriche na estrutura,
na dinâmica e no "como o Alan conduz"); Acervo, Monitorias, Prática Clínica, PD e podcasts 1.500–3.500 palavras;
vídeos curtos do YouTube 400–1.500 palavras (proporcional ao conteúdo).

---------------------------------------------------------------------------------------------------
## 7. Arquivo JSON (B) — `SCRATCH/extract/<id>.json`

Um JSON por fonte, UTF-8, válido (valide com `python3 -c "import json,sys;json.load(open(sys.argv[1]))" arquivo`).
Todos os campos presentes (listas podem ser vazias). Textos em português, limpos.

```json
{
  "id": "alan-01",
  "nota": "Alan 01 - Relação terapêutica tensionada",
  "pasta": "02 - Encontros do Alan",
  "titulo": "Relação terapêutica tensionada",
  "serie": "Aprimoramento clínico - Alan",
  "formato": "Aprimoramento clínico",
  "facilitadores": ["Alan"],
  "resumo": "3 a 6 frases",
  "em_uma_frase": "…",
  "competencias": ["Relação terapêutica"],
  "abordagens": ["Psicanálise lacaniana"],
  "estrutura": [
    {"ts": "0:00:02", "bloco": "Abertura", "descricao": "…", "funcao": "…", "duracao_min": 5}
  ],
  "conceitos": [
    {"nome": "Transferência", "definicao": "como é definido/explicado aqui (2–4 frases)", "exemplo": "exemplo/metáfora usado, se houver", "abordagem": "Psicanálise freudiana", "ts": "0:01:16"}
  ],
  "dinamicas": [
    {"nome": "Dinâmica - Construção frasal", "objetivo": "…", "competencias": ["Construção frasal"],
     "configuracao": "…", "tempo": "…", "materiais": "…", "consigna": "…",
     "passos": ["…", "…"], "feedback": "como o facilitador avalia/corrige, critérios",
     "exemplos_praticos": "o que aconteceu (anonimizado)", "variacoes": "…", "armadilhas": "…",
     "nivel": "iniciante|intermediário|avançado", "funciona_online": true, "ts": "0:10:00"}
  ],
  "movimentos_facilitacao": [
    {"movimento": "nome curto do movimento", "descricao": "o que ele faz e por quê", "exemplo": "…", "ts": "…"}
  ],
  "dicas_clinicas": [
    {"dica": "…", "justificativa": "…", "contexto": "…", "competencia": "Intervenção", "ts": "…"}
  ],
  "posicionamentos": [
    {"tese": "…", "argumento": "…", "contraponto": "…", "implicacao": "…", "quem": "Alan", "ts": "…"}
  ],
  "citacoes": [ {"texto": "…", "tema": "…", "ts": "…"} ],
  "ideias_conteudo": [
    {"formato": "carrossel|reels|post|stories", "pilar": "clinica-na-pratica", "gancho": "…", "mensagem": "…",
     "roteiro": ["slide/cena 1", "…"], "corte_inicio": "0:12:00", "corte_fim": "0:13:30"}
  ],
  "autores": [ {"nome": "Sigmund Freud", "contexto": "para que é citado"} ],
  "formato_grupo": {"nome": "…", "objetivo": "…", "publico": "…", "tamanho": "…", "duracao": "…",
                    "estrutura_padrao": "…", "papel_facilitador": "…", "regras_combinados": "…"},
  "reflexoes_do_facilitador": ["comentários do facilitador sobre a própria condução, erros, ajustes, críticas recebidas"],
  "referencias_a_outros_encontros": ["menções a encontros anteriores/próximos, cronograma, ciclos"],
  "observacoes": "qualquer coisa importante que não coube acima (qualidade da transcrição, trechos confusos etc.)"
}
```
Metas de quantidade (quando o conteúdo permitir — não invente para bater número):
- conceitos: 6–25 · dicas_clinicas: 8–30 · posicionamentos: 4–15 · citacoes: 6–15 · ideias_conteudo: 3–8
- movimentos_facilitacao: 5–15 nas notas do Alan/grupos; pode ser vazio em vídeo-aula
- `formato_grupo`: preencha para qualquer fonte que seja um GRUPO (Alan, Acervo, Monitoria, PC, PD); `null` para vídeos/podcasts.

---------------------------------------------------------------------------------------------------
## 8. Ao terminar

1. Confira: a nota existe no caminho certo, o frontmatter é YAML válido, os tokens `{{ts:ID@H:MM:SS}}` estão no
   formato exato, o JSON valida.
2. NÃO faça git add/commit/push (o coordenador faz isso).
3. Sua resposta final para o coordenador deve ser CURTA (máx. 6 linhas): caminhos dos arquivos criados + qualquer
   problema (ex.: trecho inaudível, dúvida de identificação do facilitador). Nada de colar o conteúdo.
