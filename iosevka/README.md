# Base Iosevka custom

A Crowquill Mono e construida a partir de um build custom do Iosevka.

## Regenerar a base

```bash
git clone --depth 1 https://github.com/be5invis/Iosevka ~/.ghq/github.com/be5invis/Iosevka
cp iosevka/private-build-plans.toml ~/.ghq/github.com/be5invis/Iosevka/
cd ~/.ghq/github.com/be5invis/Iosevka && npm install
npm run build -- ttf::Crowquill        # gera dist/Crowquill/TTF/*.ttf
```

Copie os 6 `.ttf` (Regular/Bold/Heavy x reta/italico) para `sources/iosevka/` e rode
`scripts/build.py` (adiciona o keyword-bold `calt` e renomeia p/ "Crowquill Mono").

Plano: Curly (ss20) + `g` andar unico + italico cursivo (i/l tailed) + largura 560.
