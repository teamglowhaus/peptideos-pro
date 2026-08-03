# -*- coding: utf-8 -*-
"""
Ukrainian localization transformer for the 369 Portal journal.

Strategy: tokenize interior_v3.py, replace only STRING tokens whose literal
value is a known English UI string, and untokenize — so every layout
instruction stays byte-for-byte identical. Fonts are remapped to Cyrillic
faces (Lora / Arsenal / Jura) under the SAME reportlab names, so no drawing
code changes.

Glossary (consistent throughout):
  manifestation      -> маніфестація
  desire             -> бажання
  the universe       -> Всесвіт
  intention          -> намір
  abundance          -> достаток
  gratitude          -> вдячність
  affirmation        -> афірмація
  shadow work        -> робота з тінню
  subconscious       -> підсвідомість
  vibration          -> вібрація
  energy             -> енергія
  synchronicity      -> синхронічність
  limiting belief    -> обмежувальне переконання
  new moon           -> молодик
  full moon          -> повня
  portal             -> портал
"""

import io, tokenize

# ── English → native Ukrainian.  Keys MUST match source literals exactly. ──────
T = {
 # ── Cover ──
 "THE": "",
 "PORTAL": "ПОРТАЛ",
 "Manifestation Journal": "Щоденник маніфестації",
 "Write your reality into existence.": "Впиши свою реальність у життя.",
 "28 DAYS  ·  MORNING  ·  MIDDAY  ·  EVENING  ·  ALIGNMENT":
   "28 ДНІВ  ·  РАНОК  ·  ОПІВДНІ  ·  ВЕЧІР  ·  СУГОЛОССЯ",
 "THE PORTAL  ·  369 MANIFESTATION JOURNAL":
   "ПОРТАЛ  ·  ЩОДЕННИК МАНІФЕСТАЦІЇ 369",

 # ── Title page ──
 "THIS JOURNAL BELONGS TO": "ЦЕЙ ЩОДЕННИК НАЛЕЖИТЬ",
 "PORTAL ACTIVATION DATE": "ДАТА АКТИВАЦІЇ ПОРТАЛУ",
 "My Portal Intention": "Мій намір у порталі",
 "The single most important desire I am calling into form:":
   "Найважливіше бажання, яке я закликаю у своє життя:",
 "I AM WORTHY  ·  I AM READY  ·  I AM OPEN":
   "Я ГІДНА  ·  Я ГОТОВА  ·  Я ВІДКРИТА",

 # ── License / Terms ──
 "Terms of Use": "Умови використання",
 "PERSONAL USE ONLY": "ЛИШЕ ДЛЯ ОСОБИСТОГО ВИКОРИСТАННЯ",
 "This journal is licensed for your personal use only. One license per purchaser. ":
   "Цей щоденник призначений лише для вашого особистого користування. Одна ліцензія на одного покупця. ",
 "You may print this file for your own personal journaling practice as many times as you wish.":
   "Ви можете друкувати цей файл для власної практики ведення щоденника скільки завгодно разів.",
 "NO REDISTRIBUTION": "БЕЗ ПОШИРЕННЯ",
 "You may not share, email, upload, resell, or redistribute this file in any ":
   "Забороняється ділитися, надсилати, завантажувати, перепродавати чи поширювати цей файл у будь-якій ",
 "form — digital or printed — to any other person or platform.":
   "формі — цифровій чи друкованій — іншим особам або на будь-яких платформах.",
 "NO COMMERCIAL USE": "БЕЗ КОМЕРЦІЙНОГО ВИКОРИСТАННЯ",
 "You may not use this journal or its contents to create products for sale, ":
   "Забороняється використовувати цей щоденник або його вміст для створення товарів на продаж, ",
 "bundles, courses, coaching programs, or any commercial purpose.":
   "наборів, курсів, коучингових програм чи будь-якої комерційної мети.",
 "NO ALTERATIONS": "БЕЗ ЗМІН",
 "You may not modify, edit, rebrand, or claim this work as your own. ":
   "Забороняється змінювати, редагувати, ребрендувати чи видавати цю роботу за власну. ",
 "All text, design, layout, and content remain the intellectual property of GlowHausDigital.":
   "Увесь текст, дизайн, верстка та вміст залишаються інтелектуальною власністю GlowHausDigital.",
 "PRINTING": "ДРУК",
 "You are welcome to print this file at home or at a local print shop for your ":
   "Ви можете друкувати цей файл удома або в місцевій друкарні для власного ",
 "own personal use. Commercial printing and resale of printed copies is not permitted.":
   "особистого користування. Комерційний друк і перепродаж друкованих копій заборонені.",
 "© 2026 GlowHausDigital  ·  All Rights Reserved":
   "© 2026 GlowHausDigital  ·  Усі права захищено",
 "Questions? teamglowhaus@gmail.com": "Запитання? teamglowhaus@gmail.com",

 # ── Welcome ──
 "You Have Arrived.": "Ви прибули.",
 "The 369 Portal is more than a journal — it is a daily sacred practice,":
   "Портал 369 — це більше, ніж щоденник. Це щоденна священна практика,",
 "a living conversation between you and the infinite field of all possibility.":
   "жива розмова між вами та безмежним полем усіх можливостей.",
 "Nikola Tesla believed 3, 6, and 9 hold the key to the universe.":
   "Нікола Тесла вірив, що 3, 6 і 9 — це ключ до Всесвіту.",
 "This journal is built on that sacred code:":
   "Цей щоденник побудований на цьому священному коді:",
 "Write your desire 3 times in the morning to set the intention.":
   "Пиши своє бажання 3 рази вранці, щоб закласти намір.",
 "Write it 6 times at midday to anchor it in your energy field.":
   "Пиши його 6 разів опівдні, щоб закріпити його у своєму енергетичному полі.",
 "Write it 9 times in the evening to send it to the universe.":
   "Пиши його 9 разів увечері, щоб надіслати його Всесвіту.",
 "Each repetition is a signal. Each page is an act of faith.":
   "Кожне повторення — це сигнал. Кожна сторінка — це акт віри.",
 "Each completed day is proof that you showed up for your vision.":
   "Кожен завершений день — це доказ, що ти прийшла заради своєї мрії.",
 "This is not a wish list. This is a portal.":
   "Це не список бажань. Це портал.",
 "Step through it — daily, devotedly, powerfully.":
   "Пройди крізь нього — щодня, віддано, впевнено.",
 "3 · 6 · 9  ·  WRITE  ·  BELIEVE  ·  RECEIVE":
   "3 · 6 · 9  ·  ПИШИ  ·  ВІР  ·  ОТРИМУЙ",

 # ── Method ──
 "The 369 Method": "Метод 369",
 "MORNING TRANSMISSIONS": "РАНКОВІ ТРАНСМІСІЇ",
 "Write your desire 3 times upon waking. Morning is when the subconscious ":
   "Пиши своє бажання 3 рази одразу після пробудження. Вранці підсвідомість ",
 "mind is most receptive and the veil between worlds is thinnest. These ":
   "найбільш сприйнятлива, а завіса між світами найтонша. Ці ",
 "three repetitions plant the seed in the fertile soil of a new day.":
   "три повторення садять зерно у родючий ґрунт нового дня.",
 "MIDDAY ACTIVATION": "ОПІВДЕННА АКТИВАЦІЯ",
 "Write your desire 6 times at midday. This mid-point practice keeps your ":
   "Пиши своє бажання 6 разів опівдні. Ця практика посеред дня підтримує твій ",
 "intention alive through the distractions of the day. Six is the number ":
   "намір живим попри денну метушню. Шість — це число ",
 "of harmony — you are harmonizing your vibration with your desire.":
   "гармонії: ти гармонізуєш свою вібрацію зі своїм бажанням.",
 "EVENING INTEGRATION": "ВЕЧІРНЯ ІНТЕГРАЦІЯ",
 "Write your desire 9 times before sleep. Nine is the number of completion. ":
   "Пиши своє бажання 9 разів перед сном. Дев'ять — це число завершення. ",
 "Your evening writing sends a clear signal as your conscious mind releases ":
   "Вечірній запис надсилає чіткий сигнал, коли свідомість поринає ",
 "into the quantum field of dreams and deep creation.":
   "у квантове поле снів і глибокого творення.",
 "TIPS FOR MAXIMUM ACTIVATION": "ПОРАДИ ДЛЯ МАКСИМАЛЬНОЇ АКТИВАЦІЇ",
 "◆  Write by hand — the physical act encodes the intention in your body.":
   "◆  Пиши від руки — фізична дія закодовує намір у твоєму тілі.",
 '◆  Use present tense: "I am," "I have," "I experience."':
   "◆  Вживай теперішній час: «я є», «я маю», «я відчуваю».",
 "◆  Feel the emotion of already having it as you write each repetition.":
   "◆  Відчувай емоцію володіння цим уже зараз із кожним повторенням.",
 "◆  Stay consistent — 28 days of practice reshapes your beliefs and daily habits.":
   "◆  Будь послідовною — 28 днів практики змінюють твої переконання та щоденні звички.",
 "◆  Trust the process even when you cannot yet see the how.":
   "◆  Довіряй процесу, навіть коли ще не бачиш, яким чином це станеться.",

 # ── How to use ──
 "How to Use This Journal": "Як користуватися цим щоденником",
 "CHOOSE YOUR DESIRE": "ОБЕРИ СВОЄ БАЖАННЯ",
 "Select one specific, emotionally charged desire to focus on for 28 days. ":
   "Обери одне конкретне, емоційно наповнене бажання, на якому зосередишся 28 днів. ",
 "Write your exact desire statement on the next page before beginning.":
   "Запиши точне формулювання свого бажання на наступній сторінці перед початком.",
 "WRITE DAILY — MORNING, MIDDAY & EVENING":
   "ПИШИ ЩОДНЯ — ВРАНЦІ, ОПІВДНІ ТА ВВЕЧЕРІ",
 "Each day has two pages: morning/midday and evening. Complete both every ":
   "Кожен день має дві сторінки: ранок/опівдні та вечір. Заповнюй обидві ",
 "day. Consistency is the key that opens the portal.":
   "щодня. Послідовність — це ключ, що відчиняє портал.",
 "ENERGY CHECK-INS": "ПЕРЕВІРКА ЕНЕРГІЇ",
 "Shade the energy bar each morning and evening (1=low, 10=high). Tracking ":
   "Заштриховуй шкалу енергії щоранку та щовечора (1 — низька, 10 — висока). Відстеження ",
 "your vibrational state reveals patterns that predict breakthroughs.":
   "твого вібраційного стану виявляє закономірності, що передвіщають прориви.",
 "GRATITUDE & SYNCHRONICITIES": "ВДЯЧНІСТЬ І СИНХРОНІЧНОСТІ",
 "Log moments of alignment, unexpected signs, and things you are grateful ":
   "Занотовуй миті суголосся, несподівані знаки та все, за що ти ",
 "for. The more you notice, the more the universe sends.":
   "вдячна. Що більше ти помічаєш — то більше Всесвіт посилає.",
 "WEEKLY & MONTHLY REVIEWS": "ТИЖНЕВІ ТА МІСЯЧНІ ПІДСУМКИ",
 "Use the review pages every 7 days to track evidence of your manifestation, ":
   "Користуйся сторінками підсумків кожні 7 днів, щоб відстежувати докази своєї маніфестації, ",
 "shifts in belief, and what to amplify in the next cycle.":
   "зміни в переконаннях і те, що варто підсилити в наступному циклі.",
 "SHADOW WORK & SYNC LOG": "РОБОТА З ТІННЮ ТА ЖУРНАЛ ЗНАКІВ",
 "The shadow work section and synchronicity log at the back support deeper ":
   "Розділ роботи з тінню та журнал синхронічностей наприкінці підтримують глибшу ",
 "transformation and evidence collection throughout your practice.":
   "трансформацію та збір доказів упродовж усієї твоєї практики.",

 # ── Portal desire statement ──
 "My Portal Desire Statement": "Формулювання мого бажання",
 "Write the exact words you will use in your daily practice.":
   "Запиши точні слова, які використовуватимеш у щоденній практиці.",
 "Present tense, personal, positive, and emotionally alive.":
   "Теперішній час, особисто, стверджувально та емоційно живо.",
 "HOW THIS DESIRE WILL FEEL WHEN IT ARRIVES":
   "ЯК ВІДЧУВАТИМЕТЬСЯ ЦЕ БАЖАННЯ, КОЛИ ЗДІЙСНИТЬСЯ",
 "WHY I KNOW I AM WORTHY OF THIS": "ЧОМУ Я ЗНАЮ, ЩО ГІДНА ЦЬОГО",

 # ── Commitments ──
 "My Portal Commitments": "Мої обіцянки в порталі",
 "I enter this portal with full commitment to my vision.":
   "Я входжу в цей портал із повною відданістю своїй мрії.",
 "I sign my name below as a sacred contract with myself.":
   "Я підписуюся нижче як священна угода із самою собою.",
 "I commit to writing my desire 3–6–9 times every single day for 28 days.":
   "Я зобов'язуюся писати своє бажання 3–6–9 разів щодня протягом 28 днів.",
 "I commit to showing up even on days when I don’t believe it’s working.":
   "Я зобов'язуюся приходити навіть у дні, коли не вірю, що це працює.",
 "I commit to noticing and recording every sign of alignment, however small.":
   "Я зобов'язуюся помічати й записувати кожен знак суголосся, хай який маленький.",
 "I commit to treating this journal as a sacred ritual, not a chore.":
   "Я зобов'язуюся ставитися до цього щоденника як до священного ритуалу, а не обов'язку.",
 "I commit to trusting the timing of the universe and releasing outcomes.":
   "Я зобов'язуюся довіряти часу Всесвіту й відпускати результати.",
 "I commit to becoming the version of myself who already has this desire.":
   "Я зобов'язуюся стати тією версією себе, яка вже має це бажання.",
 "I commit to completing all 28 days without skipping or giving up.":
   "Я зобов'язуюся пройти всі 28 днів, не пропускаючи й не здаючись.",
 "SIGNED": "ПІДПИС",
 "DATE": "ДАТА",
 '"The moment you commit, the universe conspires in your favor."':
   "«Щойно ти наважуєшся — Всесвіт починає діяти на твою користь.»",
 "— GOETHE (ADAPTED)": "— ЙОГАНН ГЕТЕ (АДАПТОВАНО)",
 "MY PORTAL AFFIRMATION": "МОЯ АФІРМАЦІЯ ПОРТАЛУ",
 "Write the single affirmation that will anchor your belief throughout this portal:":
   "Запиши одну афірмацію, що закріплюватиме твою віру впродовж усього порталу:",
 "I carry this commitment into every page of this portal.":
   "Я несу цю відданість на кожну сторінку цього порталу.",

 # ── Moon overview ──
 "✶   THE MOON  ·  YOUR COSMIC PARTNER   ✶":
   "✶   МІСЯЦЬ  ·  ТВІЙ КОСМІЧНИЙ ПАРТНЕР   ✶",
 "Moon Phase Guide": "Путівник фазами Місяця",
 "NEW MOON": "МОЛОДИК",
 "Set intentions. Plant seeds. The ideal time to begin your portal.":
   "Закладай наміри. Сій зерна. Ідеальний час, щоб відкрити свій портал.",
 "WAXING CRESCENT": "МОЛОДИЙ СЕРП",
 "Take inspired action. Build momentum. Show the universe you’re serious.":
   "Дій натхненно. Набирай обертів. Покажи Всесвіту, що налаштована серйозно.",
 "FIRST QUARTER": "ПЕРША ЧВЕРТЬ",
 "Push through obstacles. Double your commitment. Keep writing.":
   "Долай перешкоди. Подвоюй відданість. Продовжуй писати.",
 "WAXING GIBBOUS": "ПРИБУВАЮЧИЙ МІСЯЦЬ",
 "Refine and align. Your manifestation is forming in the unseen.":
   "Уточнюй і вирівнюй. Твоя маніфестація формується в незримому.",
 "FULL MOON": "ПОВНЯ",
 "Celebrate evidence. Release blocks. Feel deep gratitude for what’s coming.":
   "Святкуй докази. Відпускай блоки. Відчувай глибоку вдячність за те, що йде.",
 "WANING GIBBOUS": "СПАДАЮЧИЙ МІСЯЦЬ",
 "Share your energy and gifts. Express thanks to the field of all creation.":
   "Ділися своєю енергією та дарами. Дякуй полю всього творіння.",
 "LAST QUARTER": "ОСТАННЯ ЧВЕРТЬ",
 "Let go of what no longer serves. Clear space for your desire to land.":
   "Відпусти те, що більше не служить. Звільни місце, щоб бажання втілилось.",
 "WANING CRESCENT": "СТАРИЙ СЕРП",
 "Rest and receive. Trust the silence. Prepare for the next new cycle.":
   "Відпочивай і приймай. Довіряй тиші. Готуйся до нового циклу.",
 "Work with the moon’s energy to amplify your 369 practice.":
   "Працюй з енергією Місяця, щоб підсилити свою практику 369.",
 "New moons are the most potent time to begin a new portal.":
   "Молодик — найпотужніший час, щоб відкрити новий портал.",
 "MY MOON NOTES FOR THIS PORTAL CYCLE":
   "МОЇ МІСЯЧНІ НОТАТКИ НА ЦЕЙ ЦИКЛ ПОРТАЛУ",

 # ── Evening prompts (rotating) ──
 "What evidence of my manifestation did I notice today, however small?":
   "Які докази моєї маніфестації я помітила сьогодні, хай які дрібні?",
 "How did I embody the feeling of already having my desire today?":
   "Як я сьогодні втілювала відчуття, що вже маю своє бажання?",
 "What belief about myself shifted or softened today?":
   "Яке переконання про себе змінилося чи пом'якшилося сьогодні?",
 "What am I choosing to release before I sleep tonight?":
   "Що я обираю відпустити перед сном сьогодні?",
 "How did the universe support me today in ways I might have missed?":
   "Як Всесвіт підтримав мене сьогодні так, що я могла й не помітити?",
 "What would the highest version of me say about today’s practice?":
   "Що сказала б найвища версія мене про сьогоднішню практику?",
 "What do I want to dream into being as I sleep tonight?":
   "Що я хочу вимріяти в реальність, поки спатиму цієї ночі?",

 # ── Daily morning page ──
 "MORNING  ·  MIDDAY": "РАНОК  ·  ОПІВДНІ",
 "DATE  ______ / ______ / ______": "ДАТА  ______ / ______ / ______",
 "WRITE YOUR DESIRE 3 TIMES": "НАПИШИ СВОЄ БАЖАННЯ 3 РАЗИ",
 "MORNING ENERGY — SHADE YOUR LEVEL  1 → 10":
   "РАНКОВА ЕНЕРГІЯ — ЗАШТРИХУЙ СВІЙ РІВЕНЬ  1 → 10",
 "WRITE YOUR DESIRE 6 TIMES": "НАПИШИ СВОЄ БАЖАННЯ 6 РАЗІВ",
 "INTENTION ALIGNMENT": "СУГОЛОССЯ З НАМІРОМ",
 "What aligned action can I take today that moves me toward this desire?":
   "Яку суголосну дію я можу зробити сьогодні, щоб наблизитися до бажання?",

 # ── Daily evening page ──
 "EVENING  ·  INTEGRATION": "ВЕЧІР  ·  ІНТЕГРАЦІЯ",
 "WRITE YOUR DESIRE 9 TIMES": "НАПИШИ СВОЄ БАЖАННЯ 9 РАЗІВ",
 "EVENING ENERGY — SHADE YOUR LEVEL  1 → 10":
   "ВЕЧІРНЯ ЕНЕРГІЯ — ЗАШТРИХУЙ СВІЙ РІВЕНЬ  1 → 10",
 "GRATITUDE SEED": "ЗЕРНО ВДЯЧНОСТІ",
 "One thing I’m grateful for that I noticed today:":
   "Одне, за що я вдячна й що помітила сьогодні:",
 "SYNCHRONICITIES  &  SIGNS": "СИНХРОНІЧНОСТІ ТА ЗНАКИ",
 "What aligned or unexpected moments did I notice today?":
   "Які суголосні чи несподівані миті я помітила сьогодні?",
 "EVENING REFLECTION": "ВЕЧІРНЯ РЕФЛЕКСІЯ",
 "I release this desire to the universe with full trust and gratitude.":
   "Я віддаю це бажання Всесвіту з повною довірою та вдячністю.",

 # ── Weekly review ──
 "EVIDENCE OF MANIFESTATION": "ДОКАЗИ МАНІФЕСТАЦІЇ",
 "What signs, synchronicities, or physical shifts did I notice this week?":
   "Які знаки, синхронічності чи відчутні зміни я помітила цього тижня?",
 "BELIEF SHIFTS": "ЗМІНИ В ПЕРЕКОНАННЯХ",
 "How has my belief in this desire strengthened or clarified?":
   "Як зміцніла чи прояснилася моя віра в це бажання?",
 "ENERGY PATTERNS": "ЕНЕРГЕТИЧНІ ЗАКОНОМІРНОСТІ",
 "Which days felt most aligned? What supported or drained my energy?":
   "Які дні відчувалися найсуголоснішими? Що живило, а що виснажувало мене?",
 "GRATITUDE HARVEST": "УРОЖАЙ ВДЯЧНОСТІ",
 "What am I most grateful for from this week’s practice?":
   "За що я найбільше вдячна з практики цього тижня?",
 "AMPLIFY NEXT WEEK": "ПІДСИЛИТИ НАСТУПНОГО ТИЖНЯ",
 "What will I do more of in the coming week to deepen my manifestation?":
   "Чого я робитиму більше наступного тижня, щоб поглибити маніфестацію?",
 "WEEKLY REVIEW": "ТИЖНЕВИЙ ПІДСУМОК",

 # ── Monthly review ──
 "Monthly Overview": "Місячний огляд",
 "Evidence & Alignment": "Докази та суголосся",
 "Shadow Integration": "Інтеграція тіні",
 "Portal Forward": "Портал уперед",
 "Reflecting on 28 days of sacred practice":
   "Роздуми про 28 днів священної практики",
 "What the universe has delivered": "Що подарував Всесвіт",
 "What I’ve released and transformed": "Що я відпустила й трансформувала",
 "Setting intentions for the next cycle": "Наміри на наступний цикл",
 "MONTHLY REVIEW": "МІСЯЧНИЙ ПІДСУМОК",
 "DAYS COMPLETED (out of 28)": "ЗАВЕРШЕНО ДНІВ (із 28)",
 "MOST POWERFUL SYNCHRONICITY": "НАЙПОТУЖНІША СИНХРОНІЧНІСТЬ",
 "BIGGEST BELIEF SHIFT": "НАЙБІЛЬША ЗМІНА В ПЕРЕКОНАННЯХ",
 "WHAT SURPRISED ME MOST": "ЩО НАЙБІЛЬШЕ МЕНЕ ЗДИВУВАЛО",
 "OVERALL ENERGY TREND": "ЗАГАЛЬНА ТЕНДЕНЦІЯ ЕНЕРГІЇ",
 "MANIFESTATION EVIDENCE — LIST EVERY SIGN":
   "ДОКАЗИ МАНІФЕСТАЦІЇ — ПЕРЕЛІЧИ КОЖЕН ЗНАК",
 "UNEXPECTED GIFTS THAT ARRIVED": "НЕСПОДІВАНІ ДАРИ, ЩО З'ЯВИЛИСЯ",
 "HOW MY LIFE HAS SHIFTED IN 28 DAYS":
   "ЯК ЗМІНИЛОСЯ МОЄ ЖИТТЯ ЗА 28 ДНІВ",
 "WHAT I RELEASED THIS MONTH": "ЩО Я ВІДПУСТИЛА ЦЬОГО МІСЯЦЯ",
 "SHADOW TREASURES I DISCOVERED": "СКАРБИ ТІНІ, ЯКІ Я ВІДКРИЛА",
 "HOW I INTEGRATED RESISTANCE INTO GROWTH":
   "ЯК Я ПЕРЕТВОРИЛА ОПІР НА ЗРОСТАННЯ",
 "MY NEXT DESIRE STATEMENT": "ФОРМУЛЮВАННЯ МОГО НАСТУПНОГО БАЖАННЯ",
 "HOW MY VIBRATION HAS PERMANENTLY SHIFTED":
   "ЯК МОЯ ВІБРАЦІЯ ЗМІНИЛАСЯ НАЗАВЖДИ",
 "MY MESSAGE OF GRATITUDE TO THE UNIVERSE":
   "МОЄ ПОСЛАННЯ ВДЯЧНОСТІ ВСЕСВІТУ",

 # ── Shadow work (titles + prompts) ──
 "Releasing the Fear of Being Seen": "Відпускаю страх бути поміченою",
 "What would happen if the world truly saw you — fully, powerfully, authentically?":
   "Що станеться, якщо світ побачить тебе справжньою — повністю, потужно, автентично?",
 "What am I afraid people will think if I actually achieve this desire?":
   "Чого я боюся, що подумають люди, якщо я справді здійсню це бажання?",
 "Where did I first learn that it wasn’t safe to be fully visible and powerful?":
   "Де я вперше засвоїла, що бути помітною й сильною — небезпечно?",
 "What would the most seen, most expressed version of me do differently today?":
   "Що б зробила інакше сьогодні найпомітніша, найвиразніша версія мене?",
 "What I’m Ready to Let Go Of": "Що я готова відпустити",
 "Completion is part of creation. What must end for your desire to begin?":
   "Завершення — частина творення. Що має скінчитися, щоб бажання почалося?",
 "What old story about myself is taking up space that my desire needs?":
   "Яка стара історія про мене займає місце, потрібне моєму бажанню?",
 "What habit, relationship, or belief is quietly blocking my portal?":
   "Яка звичка, стосунки чи переконання тихо блокують мій портал?",
 "If I knew letting this go was completely safe, what would I release right now?":
   "Якби я знала, що відпустити це цілком безпечно, що б я відпустила просто зараз?",
 "The Story I Tell About Myself": "Історія, яку я розповідаю про себе",
 "Your subconscious runs the programs it learned. Which ones need upgrading?":
   "Твоя підсвідомість виконує засвоєні програми. Які з них варто оновити?",
 "What is the core limiting belief I hold about whether I deserve this desire?":
   "Яке головне обмежувальне переконання я маю про те, чи заслуговую цього бажання?",
 "When was the first time I decided I wasn’t enough for something like this?":
   "Коли я вперше вирішила, що недостатньо гідна чогось такого?",
 "What is the upgraded belief I am choosing to install in its place?":
   "Яке оновлене переконання я обираю встановити натомість?",
 "My Relationship with Receiving": "Мої стосунки з отриманням",
 "Manifestation requires openness to receive. Are you truly open?":
   "Маніфестація потребує відкритості до отримання. Чи справді ти відкрита?",
 "When good things happen, do I deflect, minimize, or doubt? Why?":
   "Коли трапляється хороше, чи я відхиляю, знецінюю чи сумніваюся? Чому?",
 "What would I need to believe about myself to receive this desire gracefully?":
   "У що мені потрібно повірити про себе, щоб прийняти це бажання з легкістю?",
 "What’s one way I can practice receiving more fully this week?":
   "Як я можу практикувати повніше отримання цього тижня?",
 "Ancestral Patterns I’m Breaking": "Родові патерни, які я розриваю",
 "You are writing a new story not just for yourself, but for your entire lineage.":
   "Ти пишеш нову історію не лише для себе, а для всього свого роду.",
 "What patterns of lack, struggle, or unworthiness have I inherited?":
   "Які патерни нестачі, боротьби чи негідності я успадкувала?",
 "Which ancestors’ voices do I hear when I doubt my desire is possible?":
   "Чиї голоси предків я чую, коли сумніваюся, що бажання можливе?",
 "What new pattern am I consciously choosing to create for those who come after?":
   "Який новий патерн я свідомо обираю створити для тих, хто прийде після мене?",
 "My Shadow Desires": "Мої тіньові бажання",
 "Sometimes what we resist wanting is exactly what we most need to claim.":
   "Іноді те, чого ми боїмося хотіти, — саме те, що нам найбільше треба прийняти.",
 "What do I secretly want but have been afraid to admit, even to myself?":
   "Чого я потайки хочу, але боялася визнати навіть перед собою?",
 "What desire do I judge in others that I am actually longing for myself?":
   "Яке бажання я засуджую в інших, а насправді прагну його сама?",
 "What would I manifest if I were completely free of shame and judgment?":
   "Що б я проявила, якби була цілком вільна від сорому й осуду?",
 "Forgiveness as a Portal": "Прощення як портал",
 "Unforgiveness is a block in your energy field. Who do you need to release?":
   "Непрощення — це блок у твоєму енергетичному полі. Кого тобі треба відпустити?",
 "Who in my life am I holding grievances against that might be blocking my flow?":
   "На кого в житті я тримаю образу, що може блокувати мій потік?",
 "How has staying in unforgiveness served me, and what is it costing me?":
   "Чим непрощення служило мені й чого воно мені коштує?",
 "What would it feel like to forgive fully — not for them, but for my own freedom?":
   "Як це — простити повністю: не заради них, а заради власної свободи?",
 "Integration — Who Am I Becoming?": "Інтеграція — ким я стаю?",
 "Twenty-eight days of practice has changed you. Let’s witness that transformation.":
   "Двадцять вісім днів практики змінили тебе. Засвідчимо цю трансформацію.",
 "How am I fundamentally different from the person who opened this journal on day 1?":
   "Чим я докорінно відрізняюся від тієї, хто відкрила цей щоденник першого дня?",
 "What parts of my old identity am I finally ready to lay down permanently?":
   "Які частини старої себе я нарешті готова відкласти назавжди?",
 "Who is the person I am stepping into — what do they believe, feel, and do?":
   "Ким я стаю — у що ця людина вірить, що відчуває і як діє?",
 "SHADOW WORK": "РОБОТА З ТІННЮ",

 # ── Sync log ──
 "SYNCHRONICITY LOG": "ЖУРНАЛ СИНХРОНІЧНОСТЕЙ",
 "Signs & Alignments": "Знаки та суголосся",
 "ENTRY  #_____": "ЗАПИС  №_____",
 "DATE _____ / _____ / _____": "ДАТА _____ / _____ / _____",
 "WHAT HAPPENED": "ЩО СТАЛОСЯ",
 "MESSAGE OR MEANING": "ПОСЛАННЯ АБО ЗНАЧЕННЯ",
 "HOW I RESPONDED OR ACKNOWLEDGED IT": "ЯК Я ВІДРЕАГУВАЛА ЧИ ВІДЗНАЧИЛА ЦЕ",

 # ── Moon month names (visible) ──
 "First": "Перший",
 "Second": "Другий",
 "Third": "Третій",
 "Fourth": "Четвертий",

 # ── Moon calendar titles ──
 "New Moon Intentions": "Наміри на молодик",
 "Waxing Moon — Action": "Зростаючий Місяць — Дія",
 "Full Moon — Release": "Повня — Відпускання",
 "Waning Moon — Integrate": "Спадний Місяць — Інтеграція",

 # ── Moon calendar content ──
 "MY NEW MOON DESIRE FOR THIS CYCLE": "МОЄ БАЖАННЯ НА МОЛОДИК ЦЬОГО ЦИКЛУ",
 "What am I calling in during this lunar month?":
   "Що я закликаю у своє життя цього місячного циклу?",
 "RITUAL I WILL PERFORM AT NEW MOON": "РИТУАЛ, ЯКИЙ Я ПРОВЕДУ НА МОЛОДИК",
 "How will I mark this sacred threshold?":
   "Як я відзначу цей священний поріг?",
 "WHAT I AM PLANTING": "ЩО Я САДЖУ",
 "Seeds I am consciously sowing in this cycle:":
   "Зерна, які я свідомо сію цього циклу:",
 "INSPIRED ACTIONS I’M TAKING": "НАТХНЕННІ ДІЇ, ЯКІ Я РОБЛЮ",
 "Concrete steps I’m taking toward my desire this week:":
   "Конкретні кроки до мого бажання цього тижня:",
 "WHAT THE UNIVERSE IS SHOWING ME": "ЩО ПОКАЗУЄ МЕНІ ВСЕСВІТ",
 "Signs and signals appearing in my waxing energy:":
   "Знаки та сигнали, що з'являються в моїй зростаючій енергії:",
 "MOMENTUM NOTES": "НОТАТКИ ПРО ІМПУЛЬС",
 "How does my desire feel as it builds toward the full moon?":
   "Як відчувається моє бажання, наближаючись до повні?",
 "WHAT I AM RELEASING AT THE FULL MOON": "ЩО Я ВІДПУСКАЮ НА ПОВНЮ",
 "Beliefs, habits, or energy patterns I am consciously letting go:":
   "Переконання, звички чи патерни енергії, які я свідомо відпускаю:",
 "WHAT I AM CELEBRATING": "ЩО Я СВЯТКУЮ",
 "Evidence, growth, and wins from this lunar cycle:":
   "Докази, зростання та перемоги цього місячного циклу:",
 "MY FULL MOON GRATITUDE": "МОЯ ВДЯЧНІСТЬ НА ПОВНЮ",
 "What the full moon illuminates in my heart:":
   "Що повня освітлює в моєму серці:",
 "WHAT I AM INTEGRATING": "ЩО Я ІНТЕГРУЮ",
 "Lessons and gifts from this completed lunar cycle:":
   "Уроки та дари цього завершеного місячного циклу:",
 "HOW I HAVE GROWN": "ЯК Я ЗРОСЛА",
 "Who I am now that I wasn’t at the new moon:":
   "Ким я є тепер, якою не була на молодик:",
 "PREPARING FOR THE NEXT CYCLE": "ГОТУЮСЯ ДО НАСТУПНОГО ЦИКЛУ",
 "What I want to carry forward into the next new moon:":
   "Що я хочу понести далі, до наступного молодика:",

 # ── Bonus pages ──
 "Overflow — Extra Writing Space": "Простір — додаткове місце для письма",
 "Portal Notes": "Нотатки порталу",
 "Affirmation Playground": "Майданчик афірмацій",
 "Dream Journal": "Щоденник снів",
 "Letters to the Universe": "Листи до Всесвіту",
 "Quantum Leap Visualization": "Візуалізація квантового стрибка",
 "My Highest Self Speaks": "Промовляє моя найвища сутність",
 "Completion — Final Reflection": "Завершення — фінальна рефлексія",
 "Use this page for any writing that overflows from your daily practice.":
   "Використовуй цю сторінку для будь-яких записів, що не вмістилися в щоденну практику.",
 "Notes, insights, downloads, and ideas captured from your portal practice.":
   "Нотатки, осяяння, послання та ідеї, зібрані під час практики порталу.",
 "Write affirmations in every direction — fill the page with I AM statements.":
   "Пиши афірмації в усіх напрямках — заповни сторінку твердженнями «я є».",
 "Record your dreams, symbols, and nighttime downloads from the universe.":
   "Записуй свої сни, символи та нічні послання від Всесвіту.",
 "Write a letter to the universe, your future self, or your desire itself.":
   "Напиши лист Всесвіту, майбутній собі або самому своєму бажанню.",
 "Describe in vivid sensory detail the day your desire has fully manifested.":
   "Опиши в яскравих чуттєвих деталях день, коли твоє бажання повністю здійснилося.",
 "What does your highest self want you to know right now?":
   "Що твоя найвища сутність хоче, щоб ти знала просто зараз?",
 "You have completed 28 days. Who are you now? What has changed forever?":
   "Ти завершила 28 днів. Ким ти є тепер? Що змінилося назавжди?",
 "EXTRA SPACE": "ДОДАТКОВИЙ ПРОСТІР",

 # ── Closing ──
 "The Portal is Open.": "Портал відчинено.",
 "Twenty-eight days of sacred commitment.":
   "Двадцять вісім днів священної відданості.",
 "Five hundred and four repetitions of your desire.":
   "П'ятсот чотири повторення твого бажання.",
 "Each one a thread woven into the fabric of what is becoming real.":
   "Кожне — нитка, вплетена в тканину того, що стає реальним.",
 "You did not just write in a journal.":
   "Ти не просто писала в щоденнику.",
 "You reshaped your beliefs and raised your vibration,":
   "Ти змінила свої переконання й підняла свою вібрацію,",
 "and sent a signal so clear the universe could not ignore it.":
   "і надіслала сигнал такий чіткий, що Всесвіт не міг його оминути.",
 "The portal is not behind you. It is beneath your feet.":
   "Портал не позаду тебе. Він у тебе під ногами.",
 "Keep walking through it.": "Продовжуй іти крізь нього.",
 "3 · 6 · 9  ·  I WROTE IT  ·  I BELIEVED IT  ·  I RECEIVED IT":
   "3 · 6 · 9  ·  Я НАПИСАЛА  ·  Я ПОВІРИЛА  ·  Я ОТРИМАЛА",

 # ── Thank you ──
 "With Gratitude": "З вдячністю",
 "Thank you for choosing the 369 Portal Manifestation Journal.":
   "Дякую, що обрала Щоденник маніфестації «Портал 369».",
 "It was crafted with intention, love, and deep belief":
   "Його створено з наміром, любов'ю та глибокою вірою",
 "in the power of your desires.": "в силу твоїх бажань.",
 "Your purchase supports an independent creator who pours":
   "Твоя покупка підтримує незалежну авторку, яка вкладає",
 "everything into making tools that truly transform lives.":
   "усе, щоб створювати інструменти, які справді змінюють життя.",
 "If this journal moves you, please consider leaving a review":
   "Якщо цей щоденник зворушив тебе, будь ласка, залиш відгук",
 "on Etsy — it means the world and helps others find their portal.":
   "на Etsy — це безцінно й допомагає іншим знайти свій портал.",
 "You are worthy of everything you are calling in.":
   "Ти гідна всього, що закликаєш у своє життя.",
 "Trust the process. Keep writing. The universe is listening.":
   "Довіряй процесу. Продовжуй писати. Всесвіт слухає.",
 "GlowHausDigital  ·  teamglowhaus@gmail.com":
   "GlowHausDigital  ·  teamglowhaus@gmail.com",
}


def transform_source(src_text):
    """Return interior_v3 source with UI strings replaced by Ukrainian."""
    out = []
    toks = tokenize.generate_tokens(io.StringIO(src_text).readline)
    used = set()
    for tok in toks:
        if tok.type == tokenize.STRING:
            try:
                val = eval(tok.string)
            except Exception:
                val = None
            if isinstance(val, str) and val in T:
                used.add(val)
                # emit as a safe double-quoted literal
                new = T[val]
                lit = '"' + new.replace("\\", "\\\\").replace('"', '\\"') + '"'
                tok = tok._replace(string=lit)
        out.append(tok)
    result = tokenize.untokenize(out)
    missing = [k for k in T if k not in used]
    return result, used, missing


if __name__ == "__main__":
    src = open("interior_v3.py", encoding="utf-8").read()
    new_src, used, missing = transform_source(src)
    open("interior_uk_gen.py", "w", encoding="utf-8").write(new_src)
    print(f"translated {len(used)} strings; {len(missing)} dict keys unmatched")
    for m in missing:
        print("  UNMATCHED:", repr(m)[:80])
