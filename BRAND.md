# Brand book: dossier

Status: name decided (maintainer, 2026-11-24, `evocaslab/hq#188`): `dossier`, package `evocaslab-dossier`, commands
`dossier` and `evocaslab-dossier`, domain `dossier.evocaslab.com`. The colours and the mark below are a **draft default**
(2026-11-26) until the maintainer answers the brand question in HQ; changing them is a recolour of `brand/` only. Source of
truth for colours, fonts and assets: [brand/brand.yaml](brand/brand.yaml); the name lives in
[brand/brand.config.json](brand/brand.config.json).

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

**Mark.** A folder with a tab (the file a repo keeps on itself) and a white check mark on it. Amber folder, no tile. It
reads at 16 px (`favicon.svg` has a heavier stroke). Dark theme: the folder turns light amber and the check dark
(`prefers-color-scheme`). The mono version is the folder outline and the check in `currentColor`.

**Colour.** One saturated primary (folder amber, `#8A5A00` light, `#F2B544` dark) with a contrast-tested pair in each
theme (every pair in `brand.yaml` meets its WCAG level). Flat fills, no gradients. A different hue from folio (rust),
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

**Знак.** Тека з вкладкою (файл, який репозиторій веде про себе) і біла галочка на ній. Бурштинова тека без плитки.
Читається на 16 px (`favicon.svg` має товщий штрих). У темній темі тека світло-бурштинова, галочка темна. Одноколірний
варіант — контур теки й галочка в `currentColor`.

**Колір.** Один насичений основний колір (бурштиновий, `#8A5A00` світлий, `#F2B544` темний) із перевіреною за
контрастом парою в кожній темі. Інший відтінок, ніж у folio (іржавий), brandforge (індиго) і svgward (бірюзовий).

**Шрифт.** Inter (OFL-1.1), латиниця й кирилиця, свій хостинг; та сама родина, що й у сусідніх інструментів.
