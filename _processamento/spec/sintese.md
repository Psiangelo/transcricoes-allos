# ESPECIFICAÇÃO — Síntese do vault (Fase 3)

Contexto: 136 transcrições de vídeos da Allos (grupos de formação em psicologia clínica) já foram lidas por
agentes que produziram (a) uma nota-fichamento por vídeo, dentro do vault, e (b) dados estruturados em JSON,
agregados em `SCRATCH/agg/`. Agora você escreve NOTAS DE SÍNTESE que cruzam as fontes.

O dono do vault é um psicólogo que quer: (1) produzir conteúdo para Instagram; (2) criar e conduzir seus próprios
grupos e dinâmicas de formação clínica — com foco no modelo dos grupos de **Aprimoramento Clínico do Alan**;
(3) estudar teoria, dicas clínicas e pontos de vista justificados.
**O vault também será passado a NOVAS PESSOAS que querem começar a conduzir grupos**, e usado para desenvolver roteiros
de grupos, de vídeos (YouTube/aulas) e de posts. Escreva para um leitor inteligente que NÃO viu os vídeos e talvez
nunca tenha conduzido um grupo: explique o necessário, dê exemplos concretos, e deixe tudo "pronto para usar".

SCRATCH = `_processamento`
VAULT   = `Obsidian Allos`

## Prioridade de conteúdo
O dono do vault pediu explicitamente: o CONTEÚDO (teoria, argumentos, exemplos, comparações entre abordagens, dicas
clínicas, pontos de vista justificados) é tão importante quanto a estrutura/forma dos grupos. Toda nota de síntese deve
ENSINAR — reconstruir as explicações, com os exemplos e metáforas dos facilitadores — e não apenas listar ou linkar.

## Regras gerais (valem para todas as notas)

1. **Português do Brasil**, texto claro, direto, sem floreio de IA ("é importante ressaltar", "em suma", "no cenário
   atual", "mergulhar", "jornada" etc.). Tom de caderno de estudo de um clínico experiente: preciso, com exemplos.
2. **Fidelidade**: tudo que atribuir ao Alan, Diogo, João de Bragança etc. precisa vir das fontes (JSON/notas).
   Quando você acrescentar algo seu (síntese, proposta, comparação que ninguém fez), deixe explícito com um callout
   `> [!tip] Proposta do vault` ou `> [!note] Leitura do vault`. Nunca invente citações, pesquisas ou números.
3. **Links (wikilinks)**: só linke para notas que EXISTEM ou que estão na lista oficial de notas planejadas
   `SCRATCH/agg/notas_planejadas.txt` (um nome por linha — use o nome EXATO; para mostrar outro texto use
   `[[Nome exato|texto]]`). Qualquer outro termo fica em texto simples. Para conferir se uma nota existe, rode
   `ls` ou `find` no VAULT.
4. **Fontes e tempos**: ao citar uma fonte, linke a nota-fichamento (campo `nota` do JSON, ex.:
   `[[Alan 03 - Distância, intensidade, forma e conteúdo]]`) e, quando houver `ts`, acrescente o token
   `{{ts:ID@H:MM:SS}}` (ID = `fonte_id`, ex. `{{ts:alan-03@0:12:34}}`). Um script converte o token em link do
   YouTube no minuto exato. Não use o token no frontmatter.
5. **Privacidade**: nunca inclua dados de pacientes/casos clínicos; nomes de alunos não aparecem nas notas de
   síntese (use "um participante"). Facilitadores podem ser citados pelo nome.
6. **Frontmatter YAML** válido em toda nota, com `tipo`, `tags` e os campos pedidos. Listas de links no frontmatter
   entre aspas: `["[[Escuta clínica]]"]`.
7. **Formatação Obsidian**: títulos `#`/`##`/`###`, callouts (`> [!abstract]`, `> [!tip]`, `> [!warning]`,
   `> [!quote]`, `> [!example]`, `> [!question]`), tabelas quando comparar, listas curtas. Nada de HTML.
8. **Nomes de arquivo**: sem `# ^ [ ] | \ / : * ? " < >`. Use exatamente os nomes que o seu prompt determinar.
9. Edite SOMENTE os arquivos que o seu prompt manda criar. Não rode sed/regravação em massa. Não faça git.
10. Resposta final ao coordenador: CURTA (lista de arquivos criados + problemas). Não cole o conteúdo.

## Tags (use estas famílias)
- tipo de nota via campo `tipo:` (encontro, fichamento, dinamica, competencia, dicas, tese, conceito, abordagem,
  autor, formato, metodo, conteudo, plano, kit, moc)
- `competencia/<slug>` — slugs: escuta, interpretacao, priorizacao, intervencao, construcao-frasal, aprofundamento,
  psicoeducacao, relacao-terapeutica, formulacao-de-caso, psicodiagnostico, primeira-sessao, abertura-encerramento,
  direcao-do-tratamento, feedback-clinico, acolhimento, teoria-pratica, pessoa-do-terapeuta, desenvolvimento-profissional
- `abordagem/<slug>` — psicanalise, lacan, junguiana, tcc, analise-do-comportamento, contextuais, fenomenologia, acp,
  gestalt, sistemica, esquema, psicodrama, adleriana (e outras no mesmo padrão)
- `conteudo/<pilar>` — clinica-na-pratica, ciencia-e-mitos, abordagens-em-dialogo, formacao-do-psicologo,
  bastidores-dos-grupos, maximas-e-reflexoes
- `allos/alan` quando a nota for majoritariamente sobre o Alan
