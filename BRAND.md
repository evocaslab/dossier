# Brand book: dossier

Status: name decided (maintainer, 2026-11-24, `evocaslab/hq#188`): `dossier`, package `evocaslab-dossier`, commands
`dossier` and `evocaslab-dossier`, domain `dossier.evocaslab.com`. Mark and colours decided 2026-11-26
(`evocaslab/hq#218`) and built with brandforge. Source of truth for colours, fonts and assets:
[brand/brand.yaml](brand/brand.yaml); the name lives in [brand/brand.config.json](brand/brand.config.json). The full
brand book (every asset on light and dark, crops, contrast, colour vision) is `brand/generated/brand-book.html`.

**Build and check.** Masters hold light colours only; brandforge writes the rest:

```bash
brandforge check . --strict   # 0 errors, 0 warnings
brandforge build .            # brand/generated/: dark variants, adaptive favicon, PNG and ICO icons, tokens, manifest
brandforge book .             # brand/generated/brand-book.html
```

| File | Use |
| --- | --- |
| `brand/logo-full-en.svg`, `brand/generated/lockup-en-dark.svg` | README and docs lockup (light, dark); `logo-full.svg` is the Ukrainian one |
| `brand/logo-mark.svg`, `brand/generated/mark-dark.svg` | The mark alone |
| `brand/generated/animated-mark.svg` | The check is drawn in; still under reduced motion |
| `brand/generated/favicon.svg`, `favicon.ico`, `png/favicon-{16,32,48}.png` | Favicon (the SVG follows the colour scheme) |
| `brand/generated/png/apple-touch-icon.png`, `icon-{192,512}.png`, `avatar-{400,1024}.png` | App icons and avatars (GitHub, chat) |
| `brand/logo-mark-mono.svg` | One colour, `currentColor` |
| `brand/images/social-{light,dark}.svg`, `social-*-1200.png` | Social card (GitHub preview, 1200x630) |
| `brand/images/{hero,banner}-{light,dark}.svg` | Project page hero and README banner |
| `brand/generated/tokens.css`, `tokens.json` | Colour tokens (CSS, W3C DTCG) |

**Licence.** The code is MIT; the name and the artwork are all rights reserved by EvoCASLab
([brand/legal/all-rights-reserved.txt](brand/legal/all-rights-reserved.txt)). A fork uses another name and mark.

- [English](#english)
- [Українською](#українською)

## English

**Audience.** Maintainers of repos that other people or agents read: people who want a check, not a reminder, that the
repo explains its purpose, reasons, design, contract and trust.

**Positioning.** dossier checks that a repo carries its dossier: the front door, working relative links, and the parts
its kind needs, declared in `dossier.yaml`. Deterministic: no LLM, no network; what it cannot tell is `unknown`, never
a pass. It does not judge whether the prose is good.

**Mission.** Every public repo explains itself, and a script checks it.

**Vision.** A repo with no purpose, reasons or design page is not called finished.

**Values.**

1. **Checked, not hand-kept.** A rule that matters is a check in CI.
2. **No LLM in the check.** The same tree gives the same result.
3. **Plain files.** Markdown and YAML beside the code, readable without the tool.
4. **Honest.** Unknown is reported as unknown.

**Tagline.** A repo that can explain itself.

**Voice.** Plain and exact. A finding names the check, the file and what is missing.

| Do | Do not |
| --- | --- |
| Write "links: docs/x.md: ../y.md does not exist" | Write "documentation issues found" |
| Say `unknown` with the reason | Count an unchecked part as passed |
| Keep the wordmark lower-case, bold | Stretch, outline, shadow or recolour the mark |

**It is not** a documentation generator and not a prose reviewer.

**Mark.** An open folder (the file a repo keeps on itself): a darker back with a tab, a sheet inside, and the amber
front with a white check mark on it. No tile. The small mark (`favicon.svg`) drops the sheet and has a heavier check, so
it reads at 16 px. Dark theme (`brand/generated/*-dark.svg`): the folder turns light amber, the sheet light and the
check dark. The mono version is the folder outline, the sheet edge and the check in `currentColor`.

**Colour.** One saturated primary (folder amber, `#8A5A00` light, `#F2B544` dark) with a contrast-tested pair in each
theme (every pair in `brand.yaml` meets its WCAG level), plus two roles used only inside the mark: `folder-back`
(`#6B4500` / `#C98A1C`) and `sheet` (`#FFFDF7` / `#ECEEF8`). Flat fills, no gradients. A different hue from folio (rust),
brandforge (indigo) and svgward (teal) so the tools are told apart; the neutrals are shared with them.

**Type.** Inter (OFL-1.1), Latin and Cyrillic, self-hosted in `brand/fonts/`; the same family as the sibling tools.

## Українською

**Аудиторія.** Мейнтейнери репозиторіїв, які читають інші люди чи агенти: ті, хто хоче перевірку, а не нагадування,
що репозиторій пояснює свою мету, причини, дизайн, контракт і довіру.

**Позиціювання.** dossier перевіряє, що репозиторій має своє досьє: головну сторінку, робочі відносні посилання і
частини, потрібні для його виду, оголошені в `dossier.yaml`. Детерміновано: без LLM і мережі; чого не може встановити,
те `unknown`, а не пройдено. Якість тексту не оцінює.

**Місія.** Кожен публічний репозиторій пояснює себе, і це перевіряє скрипт.

**Бачення.** Репозиторій без сторінки мети, причин чи дизайну не вважається завершеним.

**Цінності.**

1. **Перевірено, а не підтримано вручну.** Важливе правило — це перевірка в CI.
2. **Без LLM у перевірці.** Те саме дерево дає той самий результат.
3. **Прості файли.** Markdown і YAML поруч із кодом, читаються без інструмента.
4. **Чесно.** Невідоме звітується як невідоме.

**Гасло.** Репозиторій, що пояснює себе сам.

**Голос.** Просто й точно. Знахідка називає перевірку, файл і чого бракує.

**Знак.** Відкрита тека (файл, який репозиторій веде про себе): темніша задня стінка з вкладкою, аркуш усередині й
бурштинова передня стінка з білою галочкою. Без плитки. Малий знак (`favicon.svg`) без аркуша і з товщою галочкою, тож
читається на 16 px. У темній темі тека світло-бурштинова, аркуш світлий, галочка темна. Одноколірний варіант — контур
теки, край аркуша й галочка в `currentColor`.

**Колір.** Один насичений основний колір (бурштиновий, `#8A5A00` світлий, `#F2B544` темний) із перевіреною за
контрастом парою в кожній темі. Інший відтінок, ніж у folio (іржавий), brandforge (індиго) і svgward (бірюзовий).

**Шрифт.** Inter (OFL-1.1), латиниця й кирилиця, свій хостинг; та сама родина, що й у сусідніх інструментів.
