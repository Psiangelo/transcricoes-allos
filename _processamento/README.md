# _processamento

Material de trabalho usado para gerar o vault `Obsidian Allos/` a partir das transcrições. **Não copie esta pasta para o Obsidian.**

- `manifest.json` — as 136 fontes (id, caminho da transcrição, vídeo do YouTube, duração).
- `spec/extracao.md` — especificação seguida na leitura de cada transcrição (modelo da nota-fichamento + formato do JSON).
- `spec/sintese.md`, `spec/metodo_alan_comum.md` — especificações para notas de síntese escritas por modelo (uso futuro).
- `extract/<id>.json` — dados estruturados extraídos de cada vídeo já fichado (conceitos, dinâmicas, dicas, teses, citações, ideias de conteúdo, estrutura do encontro, movimentos de facilitação...).
- `tools/synth.py` — gera as notas de síntese do vault a partir de `extract/` (sem IA).
- `tools/ts_links.py` — converte `{{ts:ID@H:MM:SS}}` em links do YouTube no tempo exato.
- `tools/links.py` — relatório e normalização de wikilinks.
- `tools/aggregate.py` — agrega os JSONs em `agg/` (listas completas, útil para análises).

Passo a passo para continuar: ver `Obsidian Allos/LEIA-ME (para o Claude Code).md`.
