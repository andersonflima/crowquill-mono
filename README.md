# Crowquill Mono

[![release](https://img.shields.io/github/v/release/andersonflima/crowquill-mono?sort=semver)](https://github.com/andersonflima/crowquill-mono/releases)
[![Homebrew](https://img.shields.io/badge/brew-font--crowquill--mono-informational)](https://github.com/andersonflima/homebrew-fonts)
[![license: OFL 1.1](https://img.shields.io/badge/license-OFL--1.1-blue.svg)](OFL.txt)

Fonte de programação que **deixa as palavras reservadas em negrito automaticamente** —
a própria fonte diferencia keywords das linguagens, sem depender do tema do editor.

Base: um **build custom do Iosevka** (variante Curly + formas manuscritas + itálico cursivo +
largura folgada), com uma
feature OpenType `calt` que troca a sequência exata de uma keyword pelos glifos em negrito,
**só quando é a palavra inteira** — `const` bolda, `constante`/`myconst`/`const_val` não.

Acompanha o tema **Crowquill Ink** (VS Code + Neovim) — monocromático (preto & branco),
em duas variantes **dark** e **light**, onde a keyword é o único elemento em contraste
máximo (branco/preto puro) + negrito + sublinhado, e todo o resto fica em tons de cinza.

![Crowquill Ink dark](dist/specimen-dark.png)
![Crowquill Ink light](dist/specimen-light.png)

## Como funciona (o truque)

Uma fonte não entende a linguagem — ela casa **sequências de caracteres**. Então:

1. Copiamos os glifos das letras do peso **Heavy (900)** para dentro da Regular como
   variantes `a.kw`, `b.kw`, … (mesma largura mono, sem distorção) — keyword salta forte.
2. Geramos uma feature `calt` com **guarda de fronteira**: para cada keyword há regras
   `ignore` que cancelam a troca quando a palavra está colada a outro caractere de
   identificador (`[A-Za-z0-9_]`). Só quando é token isolado a troca `letra → letra.kw`
   acontece.
3. As **ligaduras nativas** do Iosevka são preservadas (fazemos *merge* no GSUB em vez de
   sobrescrever).

Cobertura atual: **338 keywords** de 14 linguagens (JS/TS, Python, Go, Rust, C#, Haskell,
Elixir, C/C++, Java, Ruby, SQL, Bash). O Python `True/False/None` (maiúsculo) e o `true/false`
(minúsculo) coexistem; SQL é tratado em minúsculo.

> Limite honesto: sem contexto semântico, a keyword bolda também dentro de string/comentário.
> O **tema** cobre esse caso (comentário/string têm cor própria e prioridade visual).

## Instalar

### Via Homebrew (recomendado)

```bash
brew tap andersonflima/fonts
brew install --cask font-crowquill-mono
```

> O Homebrew pode pedir para confiar no tap na primeira vez: `brew trust andersonflima/fonts`.

Isso instala **só a fonte**. Para o **tema** do editor, use o `install.sh` abaixo ou os arquivos em `editor/`.

### Fonte + tema (script do repo)

```bash
./scripts/install.sh          # fontes + tema VS Code + colorscheme Neovim
```

Depois:

- **VS Code** — cole `editor/vscode/settings-snippet.jsonc` no seu settings. É obrigatório
  `"editor.fontLigatures": true` (o negrito-de-keyword é `calt`). Selecione o tema
  *Crowquill Dark*.
- **Neovim** — veja `editor/nvim/README.md`. Terminal com suporte a ligaduras (kitty, WezTerm,
  Ghostty) mostra o negrito da fonte; o colorscheme já mantém `@keyword` em bold como fallback.

## Build a partir do código

```bash
python3 -m venv .venv && ./.venv/bin/pip install fonttools uharfbuzz pillow
./.venv/bin/python scripts/build.py      # gera dist/CrowquillMono-{Regular,Bold}.ttf
./.venv/bin/python scripts/verify.py     # shaping HarfBuzz: prova o comportamento
./.venv/bin/python scripts/specimen.py   # gera dist/specimen.png
```

As fontes-fonte ficam em `sources/` (baixadas dos releases oficiais); a lista de keywords em
`sources/keywords.json`.

## Roadmap

- **v0.1** — base JetBrains Mono + keyword-bold + tema.
- **v0.2** — tema Ink monocromático (dark/light) + faces itálicas.
- **v0.3 (atual)** — base trocada por um **build custom do Iosevka** (Curly + manuscrito +
  itálico cursivo + largura folgada), 4 faces, keyword-bold do Heavy 900. Plano em `iosevka/`.
- **próximo** — variante Nerd Font (ícones); afinar variantes caligráficas.

## Licenças / atribuição

- **Iosevka** — SIL Open Font License 1.1 (© Belleve Invis). Crowquill Mono é um derivado
  de um build custom do Iosevka; o plano de build fica em `iosevka/private-build-plans.toml`.

Este projeto é um derivado sob **OFL 1.1**. "Crowquill Mono" não usa os nomes reservados das
fontes originais.
