---
tipo: "moc"
tags: ["moc", "inicio"]
---

# Allos — vault clínico

> [!abstract] O que é
> Este vault é o acervo de vídeos da Allos (grupos de Aprimoramento Clínico, monitorias, cursos e vídeos do YouTube) transformado em notas de estudo, bancos de dinâmicas, dicas, teses e conteúdo. O foco é o **Método do Alan**: a estrutura e o conteúdo dos grupos de Aprimoramento Clínico.
> Toda afirmação aponta para a fonte, com link ▶ para o minuto exato do vídeo.

## Mapa
| Pasta | O que tem | Comece por |
|---|---|---|
| **01 · Método Alan** | Como o Alan conduz os grupos (forma) e o que ele ensina (apostilas) | [[MOC - Método Alan]] |
| **02 · Encontros do Alan** | Os 18 encontros fichados: estrutura, teoria, dinâmicas, condução, dicas e teses | [[Trilha curricular do Alan]] |
| **03 · Dinâmicas** | Cada exercício dos grupos, com consigna, passo a passo e critérios de feedback | [[MOC - Dinâmicas]] |
| **04 · Competências Clínicas** | As 18 competências que organizam tudo | [[MOC - Competências clínicas]] |
| **05 · Dicas Clínicas** | Dicas práticas por competência, sempre com o porquê | [[MOC - Dicas clínicas]] |
| **06 · Teses e Posicionamentos** | Pontos de vista justificados (argumento, contraponto, implicação) | [[MOC - Teses e posicionamentos]] |
| **07 · Conceitos** | Glossário teórico, com as definições como aparecem em cada fonte | [[MOC - Conceitos]] |
| **08 · Abordagens e Autores** | Onde cada abordagem e cada autor aparecem | [[MOC - Abordagens e Autores]] |
| **09 · Formatos de Grupo** | Aprimoramento, monitoria, duelo de abordagens, mesa de estudos, dinâmica de troca... | [[MOC - Formatos de grupo]] |
| **10 · Fichamentos** | Uma nota por vídeo (Acervo, Monitorias, Prática Deliberada, Prática Clínica, YouTube) | [[MOC - Fichamentos]] |
| **11 · Conteúdo e Vídeos** | Banco de ideias, cortes para reels, frases, pautas de vídeo longo e podcast | [[Estratégia de conteúdo]] |
| **99 · Templates** | Modelos para novas dinâmicas, planos de encontro, conceitos, teses e posts | pasta `99 - Templates` |

## Como as notas se conectam
- **Fichamento** (um vídeo) → cita **conceitos**, **dinâmicas**, **competências** e **abordagens**.
- **Competência** (hub) → reúne os encontros, as dinâmicas para treinar, as dicas e os conceitos daquela competência.
- **Apostila** → costura o conteúdo teórico dos encontros do Alan de um módulo, na ordem de estudo.
- **Links ▶ 0:12:34** → abrem o vídeo no YouTube no minuto exato.

## Convenções
- `tipo:` no frontmatter indica o tipo da nota: encontro, fichamento, dinamica, competencia, dicas, tese, conceito, abordagem, autor, formato, metodo, apostila, conteudo ou moc.
- Tags: `competencia/…`, `abordagem/…`, `allos/alan`, `allos/acervo`, `allos/monitoria`...
- Callouts `> [!note] Leitura do vault` ou "(?)" marcam inferências e trechos incertos da legenda automática.
- **Privacidade:** casos clínicos foram anonimizados. Não use material de caso em conteúdo público.

## Consultas úteis (plugin Dataview, opcional)
```dataview
TABLE origem, nivel, funciona_online FROM "03 - Dinâmicas" WHERE tipo = "dinamica" SORT origem ASC
```
```dataview
TABLE n_fontes AS "Fontes" FROM "07 - Conceitos" WHERE tipo = "conceito" SORT n_fontes DESC LIMIT 30
```
