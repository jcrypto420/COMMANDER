#!/usr/bin/env python3
"""THE DAILY MOG — shared layout + curated content banks.

Single source of truth for rendering, used by both the sample-data mockup
(mockup_daily_mog_v2.py) and the live generator (generate_daily_mog.py), so
the two can never visually diverge — same lesson as v1's shared data-parse
for MORNING_REPORT.md/.pdf.

render(ctx, out_path) takes a fully-populated context dict (see the two
callers for the exact shape) and builds the one-page PDF. This module has
no knowledge of where the data came from — sample or live.
"""
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer,
                                HRFlowable, Table, TableStyle)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_RIGHT, TA_CENTER
from reportlab.graphics.shapes import Drawing, Circle, PolyLine, Path, Group
import math

# --- content banks: small, curated, auditable — rotates daily via pick(),
# never freshly improvised at generation time (same pattern for every bank).
# FACT_BANK and ON_THIS_DAY_BANK were retired 2026-07-10 (Josh's call: "no
# rotation of facts thats so lame") in favor of live sources — Field Notes
# is now a second independent live-fact fetch, On This Day pulls from
# Wikipedia's own daily feed. See generate_daily_mog.py. ---
BABY_TIP_BANK = [
    "The Moro reflex makes newborns startle and fling their arms — often "
    "enough to wake themselves up. Swaddling with arms in, not just legs, "
    "blocks the flail. It fades on its own by 2-4 months.",
    "A newborn's stomach holds about a marble's worth at birth, a cherry's "
    "worth by day 3. Frequent small feeds aren't a feeding problem — that's "
    "just the actual size of the tank.",
    "Newborn vision favors sharp black-and-white contrast over soft colors "
    "for the first few months — their eyes can't resolve subtle color "
    "differences yet, so bold patterns are what actually gets noticed.",
    "White noise works on babies because the womb was loud — closer to a "
    "running vacuum than a lullaby. Quiet isn't naturally soothing to a "
    "newborn; it's a preference they learn later.",
    "Newborns are born with roughly 300 bones — many fuse together as they "
    "grow, leaving adults with 206. The soft spots on a baby's skull are "
    "the most visible version of this still-fusing process.",
    "Newborns often can't produce tears when they cry for the first few "
    "weeks — the tear ducts aren't fully functional yet. The cry is real "
    "even when the tears aren't.",
    "A newborn's grasp reflex is strong enough that they can briefly "
    "support their own weight gripping a finger. It's involuntary, not "
    "strength, and fades by around 5-6 months.",
    "Babies are obligate nose-breathers for the first few months — they "
    "haven't learned to mouth-breathe on cue yet, which is why a stuffy "
    "nose hits an infant much harder than it hits an adult.",
    "A newborn's sense of smell is remarkably developed at birth — babies "
    "can recognize their own mother's scent within days, well before their "
    "vision is sharp enough to recognize a face.",
    "Newborns can't yet make enough vitamin K on their own — the gut "
    "bacteria that helps synthesize it hasn't established itself yet. "
    "That's the reason for the standard vitamin K shot after birth.",
    "A newborn's kidneys can't concentrate urine as efficiently as an "
    "adult's — part of why frequent small feeds work better than fewer "
    "large ones; their systems are built for small volumes early on.",
    "The soft spots on a baby's skull (fontanelles) aren't fused on "
    "purpose — they let the head compress slightly during birth and leave "
    "room for the rapid brain growth that follows.",
    "Newborns are born nearsighted, with their sharpest focus around 8-12 "
    "inches away — almost exactly the distance from a nursing baby's face "
    "to its mother's.",
    "Stroke a newborn's cheek and they'll turn toward it, mouth open — the "
    "rooting reflex, an instinct that helps them find a nipple or bottle "
    "without ever being taught.",
    "Newborns cycle through shorter, more REM-heavy sleep than adults — "
    "about 50-60 minutes per cycle, with roughly half spent in REM versus "
    "about a fifth for adults.",
    "A newborn's resting heart rate runs roughly 120-160 beats per minute "
    "— more than double a typical adult's — which is normal, not "
    "something to be alarmed by.",
    "Newborns can recognize their mother's voice at birth, having learned "
    "to distinguish it during the third trimester in the womb.",
    "Babies are born with an innate preference for sweet tastes over "
    "bitter or sour ones — it's there from day one, not learned.",
    "A newborn's skin is significantly thinner than an adult's, which is "
    "part of why they lose body heat faster and need extra warmth.",
    "A baby's kneecap starts out as cartilage at birth and doesn't fully "
    "harden into bone until somewhere around age 3 to 5.",
    "Newborns rely partly on a special heat-generating tissue called "
    "brown fat to help maintain body temperature, since they can't "
    "shiver effectively yet.",
    "Babies typically double their birth weight by about 5 months old "
    "and triple it by their first birthday.",
    "A newborn's head makes up roughly a quarter of their total body "
    "length — closer to an eighth by adulthood.",
    "It's normal for a newborn to lose 5-10% of their birth weight in "
    "the first few days before regaining it by around two weeks old.",
    "Newborns blink far less than adults — only about once or twice a "
    "minute, versus roughly 15-20 times a minute for an adult.",
    "By around 8 months old, babies can already recognize patterns in "
    "speech sounds well enough to start picking individual words out of "
    "a stream of talking.",
    "The valve at the top of a baby's stomach is still immature at "
    "birth, which is a big part of why spit-up is so common in the "
    "first months.",
    "Newborns have a reflex that makes them briefly hold their breath "
    "and paddle if submerged in water — real, but not a substitute for "
    "supervision or swim lessons.",
    "A newborn's brain is about a quarter of its eventual adult weight "
    "at birth, and reaches roughly three-quarters of adult brain weight "
    "by age 2.",
    "Newborns sleep 14 to 17 hours a day in total, but rarely more than "
    "3 to 4 hours in a single stretch — their body clock hasn't caught "
    "up yet.",
    "A baby's circadian rhythm doesn't really start developing until 6 "
    "to 8 weeks old, and isn't well established until 3 to 4 months.",
    "Newborns can't produce much saliva until around 3 months old, "
    "which is why early drooling usually isn't a sign of teething yet.",
    "Studies show newborns just days old can pick out their own "
    "mother's breast milk scent from another woman's.",
    "Even minutes-old newborns will track a face-like pattern of shapes "
    "more than a scrambled version of the same features.",
    "A newborn's first smiles are usually reflexive, sometimes even "
    "happening in sleep — the first true \"social smile\" typically "
    "shows up around 6 to 8 weeks.",
    "A baby is only medically classified as a \"newborn\" for the first "
    "28 days of life — after that, the term is \"infant.\"",
    "A baby's eye color can keep changing for up to a year after birth, "
    "as the pigment in the iris keeps developing.",
    "A baby typically grows about 10 inches in their first year — more "
    "than in any other 12-month stretch of their life.",
    "A newborn's hearing works fine at birth, but the ability to tell "
    "where a sound is coming from takes months of practice for the "
    "brain to learn.",
    "Newborns don't sweat efficiently for the first few weeks, since "
    "their sweat glands aren't fully working yet.",
    "Mild jaundice is common in the first week of life because a "
    "newborn's liver is still learning to process bilirubin efficiently.",
    "Some newborns can imitate simple facial expressions, like sticking "
    "out a tongue, within hours of being born.",
    "Not every baby crawls — some go straight from sitting to walking, "
    "and pediatricians consider both patterns completely normal.",
    "The fine, soft hair sometimes present on a newborn's back and "
    "shoulders, called lanugo, usually sheds before birth or within the "
    "first few weeks after.",
    "A baby's first tooth usually appears around 6 months old, but "
    "anywhere from 3 months to a year is considered within normal range.",
    "A newborn's fingernails are already fully formed and can be "
    "surprisingly sharp — one reason mittens or gentle trims are common "
    "in the first weeks.",
    "A baby's sense of hearing is actually more developed than their "
    "eyesight at birth — hearing has been \"in training\" since the "
    "womb, while vision needs weeks to sharpen.",
    "Newborns often develop a small red or pink patch on their eyelids "
    "or the back of the neck — sometimes called a \"stork bite\" — that's "
    "just a cluster of blood vessels and usually fades on its own.",
    "A baby's soft spot on top of the head usually doesn't fully close "
    "until somewhere between 9 and 18 months old.",
    "It's normal for a newborn's hands and feet to look slightly "
    "bluish in the first day or two after birth, as their circulation "
    "adjusts to life outside the womb.",
    "Newborns often have puffy eyelids for the first few days after "
    "birth — a normal, temporary effect of the birth process, not a "
    "sign of a problem.",
    "A baby's different cries — hungry, tired, in pain — start out "
    "sounding similar and become easier for caregivers to tell apart "
    "with practice over time.",
    "A baby's brain roughly triples the number of neural connections it "
    "has within the first year — wiring that later gets pruned based on "
    "which connections actually get used.",
    "A baby can often recognize a face they've seen repeatedly within "
    "just a few days, even though their overall vision is still blurry "
    "at that stage.",
    "Infants are born with more taste buds than adults have, including "
    "some on the sides and back of the tongue that fade away with age.",
    "A baby's umbilical cord stump typically dries up and falls off on "
    "its own within one to three weeks after birth.",
    "Newborns often develop mild acne-like bumps on the face in the "
    "first few weeks — usually from residual maternal hormones, and it "
    "typically clears up on its own.",
    "A baby's swallowing reflex is present well before birth — by "
    "around 12 weeks of pregnancy, a fetus is already swallowing "
    "amniotic fluid.",
    "Hiccups are extremely common before birth, and many babies keep "
    "hiccuping frequently in the first months after birth too.",
    "A baby's sense of balance, via the inner ear, is functional well "
    "before birth — part of why gentle rocking is such an effective way "
    "to soothe a newborn.",
    "Newborns can only focus on one object at a time at first, and "
    "don't develop the ability to smoothly track a moving object until "
    "around 2 to 3 months old.",
    "A baby is born able to notice basic musical rhythm — studies show "
    "newborns can detect a steady beat and register when it's disrupted.",
    "It's common for a newborn to sneeze often in the first weeks — "
    "usually not from being sick, but from tiny nasal passages clearing "
    "out fluid and mucus.",
    "A newborn's very first stool, called meconium, is a thick, dark, "
    "tar-like substance made up of everything swallowed in the womb — "
    "not digested milk.",
    "Newborns typically need to eat every 2 to 3 hours around the "
    "clock for the first few weeks, since their small stomachs empty "
    "quickly.",
    "A baby's ear canal is short and straight at birth, which is part "
    "of why ear infections become more common later once the canal's "
    "angle changes with growth.",
    "Infant motor development generally follows a head-to-toe pattern "
    "— babies gain control of their head and neck before their trunk, "
    "and their trunk before their legs.",
    "A baby's two bottom front teeth are almost always the first to "
    "come in, typically followed by the top two.",
    "A newborn's voice box sits higher in the throat than an adult's, "
    "which is part of why babies can breathe and swallow at almost the "
    "same time — a setup that changes as they grow.",
]

# masthead epigraph — the paper's own voice, a daily creed. Short, confident,
# builder-coded; no attribution (this is identity, not a quote). Includes
# imperative-voice "Daily Directive" lines folded straight into this bank
# rather than given a separate section (Josh's call, 2026-07-07) — same
# creed-not-quote register, just phrased as a command instead of a maxim.
EPIGRAPH_BANK = [
    "Small edges, stacked daily.",
    "Make something today that outlives the day.",
    "The quiet work compounds.",
    "Build in the morning; the world argues after lunch.",
    "Fortune favors the finished.",
    "Ideas are cheap. Mornings are not.",
    "Print it, ship it, prove it.",
    "Ship the small thing before you chase the big one.",
    "Finish one loop before you open another.",
    "Do the boring rep nobody's watching.",
    "Close the tab. Open the file.",
    "Decide today's one thing before you check anything else.",
]

# word of the day — real, checkable; a mix of useful and delightful-rare
WORD_OF_DAY_BANK = [
    ("Sisu", "Finnish noun", "Extraordinary grit that shows up after the "
     "normal kind runs out — resolve in the face of odds that should have "
     "ended the effort already."),
    ("Apricity", "archaic noun", "The warmth of the sun in winter."),
    ("Sonder", "noun", "The dawning awareness that every stranger is living "
     "a life as vivid and tangled as your own."),
    ("Eucatastrophe", "noun", "A sudden turn toward good that rescues a story "
     "from ruin — coined by J.R.R. Tolkien for the moment hope breaks "
     "through."),
    ("Petrichor", "noun", "The earthy scent produced when rain falls on dry "
     "soil."),
    ("Hiraeth", "Welsh noun", "A homesickness for a home you can't return "
     "to, or that never quite existed."),
    ("Ineffable", "adjective", "Too great or extreme to be expressed or "
     "described in words."),
    ("Serendipity", "noun", "The occurrence of finding valuable or pleasant "
     "things by chance."),
    ("Gloaming", "noun", "Twilight; the soft, dim light just after sunset."),
    ("Ephemeral", "adjective", "Lasting for a very short time."),
    ("Limerence", "noun", "The state of being infatuated with someone, "
     "often involving intrusive, obsessive thoughts about them."),
    ("Ubuntu", "Nguni Bantu noun", "A philosophy roughly meaning \"I am "
     "because we are\" — humanity expressed toward others."),
    ("Wanderlust", "noun", "A strong, innate desire to travel and explore "
     "the world."),
    ("Halcyon", "adjective", "Denoting a past period regarded as idyllically "
     "happy and peaceful."),
    ("Verisimilitude", "noun", "The appearance of being true or real."),
    ("Mellifluous", "adjective", "A sound that is sweet and smooth to "
     "hear — literally \"flowing like honey.\""),
    ("Hygge", "Danish noun", "A quality of coziness and comfortable "
     "conviviality that engenders a feeling of contentment."),
    ("Wabi-sabi", "Japanese noun", "A worldview centered on accepting "
     "beauty in imperfection and impermanence."),
    ("Saudade", "Portuguese noun", "A deep emotional state of nostalgic "
     "longing for a person or thing that is absent."),
    ("Tsundoku", "Japanese noun", "Acquiring reading materials and letting "
     "them pile up unread."),
    ("Fernweh", "German noun", "An ache for distant places; a craving to "
     "travel."),
    ("Komorebi", "Japanese noun", "Sunlight filtering through the leaves "
     "of trees."),
    ("Schadenfreude", "German noun", "Pleasure derived from another "
     "person's misfortune."),
    ("Gezellig", "Dutch adjective", "Cozy, convivial, and warmly sociable."),
    ("Meraki", "Greek noun", "Doing something with soul, creativity, or "
     "love — putting a piece of yourself into your work."),
    ("Duende", "Spanish noun", "A heightened state of emotion and "
     "authenticity, especially in art or performance."),
    ("Forelsket", "Norwegian noun", "The euphoria of falling in love for "
     "the first time."),
    ("Ikigai", "Japanese noun", "A reason for being — the intersection of "
     "what you love, what you're good at, and what sustains you."),
    ("Waldeinsamkeit", "German noun", "The feeling of being alone in the "
     "woods, at peace with nature."),
    ("Sobremesa", "Spanish noun", "The time spent lingering at the table "
     "after a meal, talking with the company you shared it with."),
    ("Gigil", "Filipino noun", "The overwhelming urge to squeeze or pinch "
     "something unbearably cute."),
    ("Mångata", "Swedish noun", "The road-like reflection of moonlight on "
     "water."),
    ("Kalsarikänni", "Finnish noun", "Drinking alone at home in your "
     "underwear, with no intention of going out."),
    ("Pochemuchka", "Russian noun", "A person, often a child, who asks "
     "too many questions."),
    ("Utepils", "Norwegian noun", "A beer enjoyed outdoors, especially on "
     "the first warm day of the year."),
    ("Tarab", "Arabic noun", "A state of musically induced ecstasy or "
     "enchantment."),
    ("Jayus", "Indonesian noun", "A joke told so badly, and so unfunny, "
     "that you can't help but laugh."),
    ("Iktsuarpok", "Inuit noun", "The anticipation of waiting for someone, "
     "checking again and again to see if they're coming."),
    ("Torschlusspanik", "German noun", "Literally \"gate-closing panic\" — "
     "the fear that time is running out to act."),
    ("L'appel du vide", "French phrase", "Literally \"the call of the "
     "void\" — the fleeting, intrusive urge to jump from a high place."),
    ("Age-otori", "Japanese adjective", "To look worse after a haircut."),
    ("Sturmfrei", "German adjective", "The freedom of having the place "
     "entirely to yourself, with no one watching."),
    ("Cafuné", "Brazilian Portuguese noun", "The act of tenderly running "
     "your fingers through someone's hair."),
    ("Sprezzatura", "Italian noun", "A practiced carelessness that makes "
     "a difficult accomplishment look effortless."),
    ("Kummerspeck", "German noun", "Literally \"grief bacon\" — excess "
     "weight gained from emotional overeating."),
    ("Shemomedjamo", "Georgian verb", "To keep eating past the point of "
     "fullness because the food tastes too good to stop."),
    ("Toska", "Russian noun", "A spiritual anguish, a longing with "
     "nothing specific to long for."),
    ("Abbiocco", "Italian noun", "The drowsiness that follows a big meal."),
    ("Culaccino", "Italian noun", "The ring or mark left on a table by a "
     "cold glass."),
    ("Uitwaaien", "Dutch verb", "To take a walk in the wind, for the "
     "simple pleasure of it."),
    ("Resfeber", "Swedish noun", "The restless race of anxiety and "
     "anticipation before a journey begins."),
    ("Selcouth", "archaic English adjective", "Unfamiliar, rare, and "
     "strange, yet marvelous."),
    ("Susurrus", "noun", "A whispering or rustling sound."),
    ("Peregrination", "noun", "A journey, especially a long or meandering "
     "one."),
    ("Crepuscular", "adjective", "Relating to twilight; active primarily "
     "at dusk and dawn."),
    ("Nyctophilia", "noun", "A strong preference for darkness or night."),
    ("Eunoia", "Greek noun", "Beautiful thinking — a well mind; goodwill "
     "toward others."),
    ("Aeonian", "adjective", "Lasting for an immeasurably or indefinitely "
     "long period of time; eternal."),
    ("Vesper", "noun", "The evening star; also, evening prayer."),
    ("Lucent", "adjective", "Glowing softly with light; luminous."),
    ("Numinous", "adjective", "Having a strong religious or spiritual "
     "quality; suggesting the presence of a divinity."),
    ("Zephyr", "noun", "A soft, gentle breeze."),
    ("Empyrean", "adjective/noun", "Relating to heaven or the sky; the "
     "highest, purest part of heaven."),
    ("Diaphanous", "adjective", "Light, delicate, and translucent."),
    ("Effulgent", "adjective", "Shining brightly; radiant."),
    ("Threnody", "noun", "A lament for the dead; a song of mourning."),
    ("Somnolent", "adjective", "Sleepy and drowsy; also, tending to induce "
     "sleep."),
    ("Ethereal", "adjective", "Extremely delicate and light in a way that "
     "seems too perfect for this world."),
    ("Opalescent", "adjective", "Showing shifting colors as light catches "
     "it at different angles, like an opal."),
]

# sub rosa — the arcane/philosophical inscription. Real, attributed lines from
# the old esoteric + wisdom traditions (hermetic, alchemical, Stoic, Taoist,
# Heraclitus, Rumi, Delphic). Deliberately a MIX of short deadpan hits and
# longer, weightier passages so the closing seal reads differently each morning.
ARCANA_BANK = [
    ("Nature loves to hide.", "Heraclitus, c. 500 BC"),
    ("What you seek is seeking you.", "Rumi"),
    ("As above, so below.", "The Emerald Tablet"),
    ("Sell your cleverness and buy bewilderment.", "Rumi"),
    ("The soul becomes dyed with the color of its thoughts.",
     "Marcus Aurelius, Meditations"),
    ("No man ever steps in the same river twice — for it is not the same "
     "river, and he is not the same man.", "Heraclitus"),
    ("Know thyself — and nothing in excess.",
     "inscribed at the Temple of Apollo, Delphi"),
    ("We suffer more often in imagination than in reality.",
     "Seneca, Letters to Lucilius"),
    ("The impediment to action advances action. What stands in the way "
     "becomes the way.", "Marcus Aurelius, Meditations"),
    ("Knowing others is intelligence; knowing yourself is true wisdom.",
     "Lao Tzu, Tao Te Ching"),
    ("Visit the interior of the earth, and by rectification thou shalt find "
     "the hidden stone.", "the alchemists' VITRIOL formula"),
    ("All things are poison, and nothing is without poison — only the dose "
     "makes a thing not a poison.", "Paracelsus, 1538"),
    ("Yesterday I was clever, so I wanted to change the world. Today I am "
     "wise, so I am changing myself.", "Rumi"),
    ("Character is fate.", "Heraclitus"),
    ("The Tao that can be told is not the eternal Tao.",
     "Lao Tzu, Tao Te Ching"),
    ("Out beyond ideas of wrongdoing and rightdoing, there is a field. "
     "I'll meet you there.", "Rumi"),
    ("The wound is the place where the Light enters you.", "Rumi"),
    ("You have power over your mind — not outside events. Realize this, "
     "and you will find strength.", "Marcus Aurelius, Meditations"),
    ("If it is not right, do not do it; if it is not true, do not say it.",
     "Marcus Aurelius, Meditations"),
    ("It is not that we have a short time to live, but that we waste a "
     "lot of it.", "Seneca, On the Shortness of Life"),
    ("As is a tale, so is life: not how long it is, but how good it is, "
     "is what matters.", "Seneca, Letters to Lucilius"),
    ("Nothing is enough for the man to whom enough is too little.",
     "Epicurus"),
    ("It is impossible for a man to learn what he thinks he already "
     "knows.", "Epictetus, Discourses"),
    ("Man is disturbed not by things, but by the views he takes of them.",
     "Epictetus, Enchiridion"),
    ("The journey of a thousand miles begins with a single step.",
     "Lao Tzu, Tao Te Ching"),
    ("Water is the softest thing, yet it can penetrate mountains and "
     "earth.", "Lao Tzu, Tao Te Ching"),
    ("Control your temper.", "one of the 147 Delphic maxims, Temple of "
     "Apollo"),
    ("The All is Mind; the Universe is Mental.",
     "The Kybalion, 1908 — the Hermetic Principle of Mentalism"),
    ("Follow God.", "one of the 147 Delphic maxims, Temple of Apollo"),
    ("Obey the law.", "one of the 147 Delphic maxims, Temple of Apollo"),
    ("Worship the gods.", "one of the 147 Delphic maxims, Temple of Apollo"),
    ("Respect your parents.", "one of the 147 Delphic maxims, Temple of "
     "Apollo"),
    ("Be gracious.", "one of the 147 Delphic maxims, Temple of Apollo"),
    ("Use time sparingly.", "one of the 147 Delphic maxims, Temple of "
     "Apollo"),
    ("Foresee the future.", "one of the 147 Delphic maxims, Temple of "
     "Apollo"),
    ("Despise insolence.", "one of the 147 Delphic maxims, Temple of "
     "Apollo"),
    ("Be discreet.", "one of the 147 Delphic maxims, Temple of Apollo"),
    ("Guard what is yours.", "one of the 147 Delphic maxims, Temple of "
     "Apollo"),
    ("Shun what belongs to others.", "one of the 147 Delphic maxims, "
     "Temple of Apollo"),
    ("Listen, and understand.", "one of the 147 Delphic maxims, Temple of "
     "Apollo"),
    ("Do not tire of learning.", "one of the 147 Delphic maxims, Temple "
     "of Apollo"),
    ("The best revenge is to be unlike him who performed the injury.",
     "Marcus Aurelius, Meditations"),
    ("Confine yourself to the present.", "Marcus Aurelius, Meditations"),
    ("How much more grievous are the consequences of anger than the "
     "causes of it.", "Marcus Aurelius, Meditations"),
    ("Everything we hear is an opinion, not a fact. Everything we see is "
     "a perspective, not the truth.", "Marcus Aurelius, Meditations"),
    ("Very little is needed to make a happy life; it is all within "
     "yourself, in your way of thinking.", "Marcus Aurelius, Meditations"),
    ("The universe is change; our life is what our thoughts make it.",
     "Marcus Aurelius, Meditations"),
    ("Accept the things to which fate binds you, and love the people "
     "with whom fate brings you together.", "Marcus Aurelius, Meditations"),
    ("He who is brave is free.", "Seneca, Letters to Lucilius"),
    ("Every new beginning comes from some other beginning's end.",
     "Seneca, Letters to Lucilius"),
    ("While we wait for life, life passes.", "Seneca, Letters to Lucilius"),
    ("Difficulties strengthen the mind, as labor does the body.",
     "Seneca, Letters to Lucilius"),
    ("He suffers more than necessary who suffers before it is necessary.",
     "Seneca, Letters to Lucilius"),
    ("It is the power of the mind to be unconquerable.",
     "Seneca, Letters to Lucilius"),
    ("When I let go of what I am, I become what I might be.",
     "Lao Tzu, Tao Te Ching"),
    ("A good traveler has no fixed plans and is not intent on arriving.",
     "Lao Tzu, Tao Te Ching"),
    ("Silence is a source of great strength.", "Lao Tzu, Tao Te Ching"),
    ("Nature does not hurry, yet everything is accomplished.",
     "Lao Tzu, Tao Te Ching"),
    ("He who knows he has enough is rich.", "Lao Tzu, Tao Te Ching"),
    ("New beginnings are often disguised as painful endings.",
     "Lao Tzu, Tao Te Ching"),
    ("Let yourself be silently drawn by the strange pull of what you "
     "really love.", "Rumi"),
    ("Raise your words, not your voice. It is rain that grows flowers, "
     "not thunder.", "Rumi"),
    ("You were born with wings, why prefer to crawl through life?",
     "Rumi"),
    ("The quieter you become, the more you are able to hear.", "Rumi"),
    ("Respond to every call that excites your spirit.", "Rumi"),
    ("Much learning does not teach understanding.", "Heraclitus"),
    ("The soul that is dry is wisest and best.", "Heraclitus"),
    ("Big results require big ambitions.", "Heraclitus"),
    ("Waste no more time arguing about what a good man should be. Be one.",
     "Marcus Aurelius, Meditations"),
]

# closing quote — real, verifiably-attributed lines from actual historically
# important people (Josh's call, 2026-07-07: distinct from FORBIDDEN WISDOM's
# esoteric bent — "an actual quote from historically important ppl")
HISTORY_QUOTE_BANK = [
    ("That's one small step for a man, one giant leap for mankind.",
     "Neil Armstrong, 1969"),
    ("Injustice anywhere is a threat to justice everywhere.",
     "Martin Luther King Jr., Letter from Birmingham Jail, 1963"),
    ("Ask not what your country can do for you — ask what you can do for "
     "your country.", "John F. Kennedy, Inaugural Address, 1961"),
    ("The only thing we have to fear is fear itself.",
     "Franklin D. Roosevelt, Inaugural Address, 1933"),
    ("I think, therefore I am.", "René Descartes, 1637"),
    ("The unexamined life is not worth living.", "Socrates, c. 399 BC"),
    ("Imagination is more important than knowledge.",
     "Albert Einstein, 1929"),
    ("Give me liberty, or give me death!", "Patrick Henry, 1775"),
    ("Four score and seven years ago our fathers brought forth on this "
     "continent a new nation.",
     "Abraham Lincoln, Gettysburg Address, 1863"),
    ("Free at last! Free at last! Thank God Almighty, we are free at last!",
     "Martin Luther King Jr., 'I Have a Dream,' 1963"),
    ("That which does not kill us makes us stronger.",
     "Friedrich Nietzsche, Twilight of the Idols, 1888"),
    ("Genius is one percent inspiration and ninety-nine percent "
     "perspiration.", "Thomas Edison, Harper's Monthly, 1932"),
    ("Never give in, never give in, never, never, never, never.",
     "Winston Churchill, Harrow School address, 1941"),
    ("The best way to predict the future is to invent it.", "Alan Kay, 1971"),
    ("Nothing in life is to be feared, it is only to be understood.",
     "Marie Curie"),
    ("It always seems impossible until it's done.",
     "Nelson Mandela, Long Walk to Freedom, 1994"),
    ("It is not the critic who counts, but the man who is actually in "
     "the arena.", "Theodore Roosevelt, 'Citizenship in a Republic,' 1910"),
    ("Failure is impossible.",
     "Susan B. Anthony, final public address, 1906"),
    ("If there is no struggle, there is no progress.",
     "Frederick Douglass, 1857"),
    ("The most difficult thing is the decision to act; the rest is "
     "merely tenacity.", "Amelia Earhart"),
    ("We hold these truths to be self-evident, that all men are created "
     "equal.", "The Declaration of Independence, 1776"),
    ("We the People of the United States, in Order to form a more "
     "perfect Union.", "The U.S. Constitution, preamble, 1787"),
    ("With malice toward none, with charity for all.",
     "Abraham Lincoln, Second Inaugural Address, 1865"),
    ("A house divided against itself cannot stand.",
     "Abraham Lincoln, 'House Divided' speech, 1858"),
    ("Yesterday, December 7th, 1941 — a date which will live in infamy.",
     "Franklin D. Roosevelt, address to Congress, 1941"),
    ("We shall fight on the beaches, we shall fight on the landing "
     "grounds, we shall never surrender.",
     "Winston Churchill, House of Commons, 1940"),
    ("Never was so much owed by so many to so few.",
     "Winston Churchill, House of Commons, 1940"),
    ("It is our true policy to steer clear of permanent alliances with "
     "any portion of the foreign world.",
     "George Washington, Farewell Address, 1796"),
    ("I cannot live without books.",
     "Thomas Jefferson, letter to John Adams, 1815"),
    ("Early to bed and early to rise, makes a man healthy, wealthy, and "
     "wise.", "Benjamin Franklin, Poor Richard's Almanack, 1758"),
    ("We hold these truths to be self-evident: that all men and women "
     "are created equal.",
     "Elizabeth Cady Stanton, Declaration of Sentiments, 1848"),
    ("If I have seen further, it is by standing on the shoulders of "
     "giants.", "Isaac Newton, letter to Robert Hooke, 1675"),
    ("Try not to become a man of success, but rather try to become a "
     "man of value.", "Albert Einstein"),
    ("In spite of everything, I still believe that people are truly "
     "good at heart.", "Anne Frank, The Diary of a Young Girl, 1947"),
    ("Although the world is full of suffering, it is also full of the "
     "overcoming of it.", "Helen Keller, 'Optimism,' 1903"),
    ("I have learned over the years that when one's mind is made up, "
     "this diminishes fear.", "Rosa Parks, Rosa Parks: My Story, 1992"),
    ("There is as much dignity in tilling a field as in writing a poem.",
     "Booker T. Washington, Up From Slavery, 1901"),
    ("The function of education is to teach one to think intensively "
     "and to think critically.", "W.E.B. Du Bois, 'The Talented Tenth,' 1903"),
    ("An eye for an eye only ends up making the whole world blind.",
     "Mahatma Gandhi, Non-Violence in Peace and War, 1948"),
    ("Power concedes nothing without a demand. It never did and it "
     "never will.", "Frederick Douglass, 'West India Emancipation,' 1857"),
    ("Speak softly and carry a big stick; you will go far.",
     "Theodore Roosevelt, State of the Union, 1901"),
    ("The world must be made safe for democracy.",
     "Woodrow Wilson, war message to Congress, 1917"),
    ("We must guard against unwarranted influence by the "
     "military-industrial complex.", "Dwight D. Eisenhower, Farewell "
     "Address, 1961"),
    ("We choose to go to the Moon in this decade, not because it is "
     "easy, but because it is hard.",
     "John F. Kennedy, Rice University, 1962"),
    ("Mr. Gorbachev, tear down this wall!",
     "Ronald Reagan, Brandenburg Gate, 1987"),
    ("Education is the most powerful weapon which you can use to "
     "change the world.", "Nelson Mandela"),
    ("A man who dares to waste one hour of time has not discovered the "
     "value of life.", "Charles Darwin, autobiography"),
    ("Learning never exhausts the mind.", "Leonardo da Vinci, notebooks"),
    ("It does not matter how slowly you go as long as you do not stop.",
     "Confucius, Analects"),
    ("The supreme art of war is to subdue the enemy without fighting.",
     "Sun Tzu, The Art of War"),
    ("The heaviest penalty for declining to rule is to be ruled by "
     "someone inferior to yourself.", "Plato, The Republic"),
    ("Knowing yourself is the beginning of all wisdom.",
     "Aristotle, Nicomachean Ethics"),
    ("Veni, vidi, vici.", "Julius Caesar, report to the Roman Senate, "
     "47 BC"),
    ("I know I have the body of a weak and feeble woman, but I have the "
     "heart and stomach of a king.",
     "Elizabeth I, Tilbury speech, 1588"),
    ("Facts are stubborn things.",
     "John Adams, letter to Abigail Adams, 1776"),
    ("A nation which can prefer disgrace to danger is prepared for a "
     "master, and deserves one.", "Alexander Hamilton, Federalist No. 1, "
     "1787"),
    ("If men were angels, no government would be necessary.",
     "James Madison, Federalist No. 51, 1788"),
    ("Not to know what happened before you were born is to remain "
     "forever a child.", "Cicero, De Officiis"),
    ("We must cultivate our garden.", "Voltaire, Candide, 1759"),
    ("I do not wish women to have power over men, but over themselves.",
     "Mary Wollstonecraft, A Vindication of the Rights of Woman, 1792"),
    ("The only freedom which deserves the name is that of pursuing our "
     "own good in our own way.", "John Stuart Mill, On Liberty, 1859"),
    ("The philosophers have only interpreted the world in various ways; "
     "the point is to change it.", "Karl Marx, Theses on Feuerbach, 1845"),
    ("It is not from the benevolence of the butcher, the brewer, or the "
     "baker that we expect our dinner.", "Adam Smith, The Wealth of "
     "Nations, 1776"),
    ("It was the best of times, it was the worst of times.",
     "Charles Dickens, A Tale of Two Cities, 1859"),
    ("Real knowledge is to know the extent of one's ignorance.",
     "Confucius, Analects"),
    ("Call me Ishmael.", "Herman Melville, Moby-Dick, 1851"),
    ("A woman must have money and a room of her own if she is to write "
     "fiction.", "Virginia Woolf, A Room of One's Own, 1929"),
    ("War is peace. Freedom is slavery. Ignorance is strength.",
     "George Orwell, 1984, 1949"),
    ("What, to the American slave, is your 4th of July?",
     "Frederick Douglass, 'What to the Slave is the Fourth of July?,' "
     "1852"),
]

# curated seasonal gardening notes, folded into the Primoscapes line as
# "this week in the garden" — rotates by month, distinct from the real
# weather-conditioned flavor text in primoscapes_note() (Josh's call,
# 2026-07-07: "this week in the garden" as its own idea, merged in rather
# than given a whole new section to protect the one-page budget)
PRIMOSCAPES_SEASONAL_BANK = {
    1: "Bare-root planting season — roots establish with no top growth "
       "competing for energy.",
    2: "Cut back last year's ornamental grasses before new blades come in.",
    3: "Crabgrass preventer goes down when redbuds bloom, not by the "
       "calendar.",
    4: "Frost risk is fading, but OKC has burned people on early transplants "
       "before.",
    5: "Mow high this month — longer blades shade and root deeper.",
    6: "Native prairie plantings hit their stride — the payoff month for "
       "going native.",
    7: "Water deep and infrequent, not daily — trains roots down where it "
       "stays cool.",
    8: "Hold fall fertilizer until temps break — feeding it now just "
       "stresses the lawn.",
    9: "Best month of the year to seed or sod in OKC.",
    10: "Plant trees and shrubs now — roots keep growing until the ground "
        "freezes.",
    11: "Leave the leaves where practical — free soil-building a bagged "
        "cleanup throws away.",
    12: "Slowest month by design — plan next year's beds instead of "
        "fighting dormant ground.",
}


def pick(bank, day_ordinal, salt=0):
    """Deterministic daily rotation, not per-run randomness: the same
    calendar day always yields the same pick, so regenerating twice in one
    morning (e.g. two Pi boots) shows the same content, and it's auditable
    (you can predict tomorrow's index)."""
    return bank[(day_ordinal + salt) % len(bank)]


# --- palette: warm almanac base, 4 purposeful accents, nothing decorative ---
PAPER = HexColor("#FBF6EC")
INK = HexColor("#241F16")
MUTED = HexColor("#6B6255")
LINE = HexColor("#DDD3BF")
RULE = HexColor("#C4B89F")    # slightly darker hairline for header underlines
BRAND = HexColor("#4B3F8F")   # masthead / identity only
GREEN = HexColor("#1B7A4D")   # price up / index reading "greed" side
RED = HexColor("#A3402F")     # price down / index reading "fear" side

# golden-ratio (phi = 1.618) two-column split, replacing the earlier
# near-even 3.55/3.35 divide — same 6.9in interior width convention already
# used by the ticker strip and folio row
PHI = 1.6180339887
_CONTENT_WIDTH = 6.9 * inch
COL_MAJOR = _CONTENT_WIDTH * PHI / (1 + PHI)
COL_MINOR = _CONTENT_WIDTH - COL_MAJOR

FEAR_GREED_COLOR = {
    "EXTREME FEAR": "#A3402F", "FEAR": "#A3402F",
    "NEUTRAL": "#6B6255",
    "GREED": "#1B7A4D", "EXTREME GREED": "#1B7A4D",
}

# Typographic system: serif (Times) for everything that reads as editorial —
# nameplate, body, headlines, pull-quote — for authentic newspaper/almanac
# feel. Sans (Helvetica) reserved for kickers, data strips, and fine print,
# so the two roles stay visually distinct.
## Type scale: consolidated to a small set of harmonious sizes rather than a
## new size per element (~20 near-duplicate sizes before this pass) — the
## "modular scale" principle from classic editorial/Swiss-style typography:
## hierarchy comes from a few deliberate, reused steps, not fine-grained
## +0.2pt drift between elements that end up visually indistinguishable
## anyway. KICKER (7.5) is every small bold-caps section label; ATTR (7.5)
## is every quote-attribution line; both previously had 3-4 near-duplicate
## sizes (7, 7.7, 7.5, 8) doing the same job.
KICKER = 7.5
ATTR = 7.5

S = {
    "masthead": ParagraphStyle("mh", fontName="Times-Bold", fontSize=42,
                                textColor=BRAND, leading=44, alignment=TA_CENTER),
    "epigraph": ParagraphStyle("ep", fontName="Times-Italic", fontSize=11.5,
                               textColor=INK, leading=14, alignment=TA_CENTER),
    "wod_term": ParagraphStyle("wt", fontName="Times-Bold", fontSize=12,
                               textColor=INK, leading=14),
    "folio_side": ParagraphStyle("fs", fontName="Helvetica-Bold", fontSize=KICKER,
                                  textColor=MUTED, leading=10),
    "folio_center": ParagraphStyle("fc", fontName="Times-Bold", fontSize=9.5,
                                    textColor=INK, alignment=TA_CENTER, leading=11),
    "folio_timestamp": ParagraphStyle("ft", fontName="Helvetica", fontSize=7,
                                       textColor=MUTED, alignment=TA_CENTER, leading=8),
    "almanac_line": ParagraphStyle("al", fontName="Times-Roman", fontSize=8.7,
                                    textColor=MUTED, alignment=TA_CENTER, leading=12.5),
    "ticker": ParagraphStyle("tk", fontName="Helvetica", fontSize=8,
                              textColor=INK, alignment=TA_CENTER, leading=10.5),
    "signal": ParagraphStyle("sig", fontName="Helvetica", fontSize=8,
                              textColor=INK, leading=10.5),
    "section_h": ParagraphStyle("sh", fontName="Helvetica-Bold", fontSize=9.5,
                                 textColor=BRAND, spaceBefore=11, spaceAfter=3),
    "body": ParagraphStyle("b", fontName="Times-Roman", fontSize=10.5,
                            textColor=INK, leading=15),
    "muted_sm": ParagraphStyle("ms", fontName="Times-Italic", fontSize=9,
                                textColor=MUTED, leading=12.5),
    "news_headline": ParagraphStyle("nh", fontName="Times-Bold", fontSize=11,
                                     textColor=INK, leading=13.5),
    "news_tag": ParagraphStyle("nt", fontName="Helvetica-Bold", fontSize=KICKER,
                                textColor=BRAND, leading=9.5),
    "decide_inline": ParagraphStyle("di", fontName="Times-Roman", fontSize=9,
                                     textColor=INK, leading=13.5),
    "index_line": ParagraphStyle("il", fontName="Helvetica", fontSize=8.7,
                                  textColor=INK, alignment=TA_CENTER, leading=11),
    "otd_line": ParagraphStyle("otd", fontName="Times-Italic", fontSize=8.7,
                                textColor=MUTED, alignment=TA_CENTER, leading=11.5),
    "arcana_kicker": ParagraphStyle("ak", fontName="Helvetica-Bold", fontSize=KICKER,
                                     textColor=BRAND, alignment=TA_CENTER, leading=12),
    "arcana_quote": ParagraphStyle("aq", fontName="Times-Italic", fontSize=13,
                                    textColor=INK, alignment=TA_CENTER, leading=17),
    "arcana_attr": ParagraphStyle("aa", fontName="Helvetica", fontSize=ATTR,
                                   textColor=MUTED, alignment=TA_CENTER, leading=10),
    "seal_kicker": ParagraphStyle("sk", fontName="Helvetica-Bold", fontSize=KICKER,
                                   textColor=BRAND, alignment=TA_CENTER, leading=12),
    "random_fact": ParagraphStyle("rf", fontName="Times-Italic", fontSize=8.7,
                                   textColor=MUTED, alignment=TA_CENTER, leading=12),
    "history_quote": ParagraphStyle("hq", fontName="Times-Italic", fontSize=10.5,
                                     textColor=INK, alignment=TA_CENTER, leading=14),
    "history_attr": ParagraphStyle("ha", fontName="Helvetica", fontSize=ATTR,
                                    textColor=MUTED, alignment=TA_CENTER, leading=9.5),
}


def sec(title):
    """Section header (sans kicker) + hairline rule beneath — the newspaper
    section-divider look. Returns a list to extend a column's flowables."""
    return [Paragraph(title, S["section_h"]),
            HRFlowable(width="100%", thickness=0.5, color=RULE,
                       spaceBefore=1, spaceAfter=6)]


def ticker_strip(items):
    """items: list of (symbol, price_str, is_up) tuples, exactly 7 for the
    layout to balance. Every item stacks symbol atop price+arrow — uniform,
    so nothing wraps differently just because one string is longer."""
    cells = []
    for sym, price, up in items:
        arrow = "▲" if up else "▼"
        color = "#1B7A4D" if up else "#A3402F"
        cells.append(Paragraph(
            f'<font face="Helvetica-Bold" size="8">{sym}</font><br/>'
            f'<font face="Courier" size="8">{price} '
            f'<font color="{color}">{arrow}</font></font>', S["ticker"]))
    t = Table([cells], colWidths=[0.98 * inch] * 7)
    t.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LINEAFTER", (0, 0), (-2, -1), 0.5, LINE),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 3),
        ("RIGHTPADDING", (0, 0), (-1, -1), 3),
    ]))
    return t


def signals_strip(items):
    """items: list of (label, value, color_hex_or_None) tuples — compact
    non-price stats (sats/$, halving countdown, gas gwei). Label and value
    share ONE line (unlike ticker_strip's stacked symbol/price), and cells
    use a fixed width rather than stretching to fill 6.9in — with only a
    few items this reads as a tidy left-anchored strip instead of getting
    stretched sparse across the full page width."""
    cells = []
    for label, value, color in items:
        open_tag = f'<font color="{color}">' if color else ""
        close_tag = "</font>" if color else ""
        cells.append(Paragraph(
            f'<font face="Helvetica-Bold" size="7.2">{label}</font> '
            f'<font face="Courier" size="7.8">{open_tag}{value}{close_tag}'
            f'</font>', S["signal"]))
    t = Table([cells], colWidths=[1.5 * inch] * len(cells))
    t.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("LINEAFTER", (0, 0), (-2, -1), 0.5, LINE),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 3),
        ("RIGHTPADDING", (0, 0), (-1, -1), 3),
    ]))
    return t


# --- small vector graphics: hand-drawn shapes, not images/matplotlib —
# stays print-crisp at any size and adds no new dependency. Kept neutral
# (INK/MUTED/LINE only, no accent colors) since these are informational
# marks, not meaning-encoded like the price/index colors. ---

def sparkline(values, width=50, height=14, color=None):
    """Minimal line chart, no axes/labels — just the trend shape and an
    end-point dot. `values` oldest-to-newest."""
    color = color or INK
    d = Drawing(width, height)
    if len(values) < 2:
        return d
    lo, hi = min(values), max(values)
    span = (hi - lo) or 1
    n = len(values)
    pad = 2
    pts = []
    for i, v in enumerate(values):
        x = i / (n - 1) * width
        y = pad + (v - lo) / span * (height - 2 * pad)
        pts += [x, y]
    d.add(PolyLine(pts, strokeColor=color, strokeWidth=1.1,
                    strokeLineJoin=1, strokeLineCap=1))
    d.add(Circle(pts[-2], pts[-1], 1.5, fillColor=color, strokeColor=None))
    return d


def _circle_clip_path(cx, cy, r):
    """4-bezier circle approximation (the standard 0.5522847498 magic-number
    constant), marked as a clip path so a Group's later children only
    render within this circular silhouette — a rectangular Drawing bound
    is NOT equivalent to this and clips the wrong region at most offsets."""
    k = 0.5522847498 * r
    p = Path()
    p.moveTo(cx + r, cy)
    p.curveTo(cx + r, cy + k, cx + k, cy + r, cx, cy + r)
    p.curveTo(cx - k, cy + r, cx - r, cy + k, cx - r, cy)
    p.curveTo(cx - r, cy - k, cx - k, cy - r, cx, cy - r)
    p.curveTo(cx + k, cy - r, cx + r, cy - k, cx + r, cy)
    p.closePath()
    p.isClipPath = 1
    return p


def moon_icon(phase_frac, r=6):
    """Small moon-phase disk. phase_frac: 0=new, 0.5=full, 1=new (next
    cycle). Technique: two same-radius circles, one dark (INK, the 'new
    moon' base) and one light (PAPER) offset horizontally, clipped to the
    base circle's silhouette — where they overlap, light covers dark;
    where they don't, dark shows through as a crescent/gibbous.
    offset = 2r*cos(pi*phase_frac): 2r at phase 0 (no overlap, fully dark),
    0 at phase 0.5 (full overlap, fully lit), back to 2r at phase 1.
    Positive offset (phase 0-0.5, waxing) shifts the light circle right,
    exposing dark on the left — lit crescent grows on the right."""
    size = 2 * r + 2
    d = Drawing(size, size)
    cx = cy = size / 2.0
    d.add(Circle(cx, cy, r, fillColor=INK, strokeColor=None))
    offset = 2 * r * math.cos(math.pi * phase_frac)
    lit = Group()
    lit.add(_circle_clip_path(cx, cy, r))
    lit.add(Circle(cx + offset, cy, r, fillColor=PAPER, strokeColor=None))
    d.add(lit)
    d.add(Circle(cx, cy, r, fillColor=None, strokeColor=MUTED, strokeWidth=0.5))
    return d


def sun_arc(progress_frac, width=52, height=18):
    """Small sky-dome arc with a dot marking how far through the daylight
    window 'now' is. progress_frac: 0=sunrise (left), 1=sunset (right).
    Clamped so a pre-dawn/post-dusk generation run doesn't place the dot
    off the arc."""
    progress_frac = max(0.0, min(1.0, progress_frac))
    d = Drawing(width, height)
    cx = width / 2.0
    baseline_y = 2.5
    r = width / 2.0 - 3
    # arc traced as short line segments — simplest reliable way to get a
    # smooth curve out of reportlab's shape primitives without relying on
    # exact Path/arc-command behavior across reportlab versions
    steps = 24
    pts = []
    for i in range(steps + 1):
        theta = math.pi * (1 - i / steps)  # pi (left) -> 0 (right)
        pts += [cx + r * math.cos(theta), baseline_y + r * math.sin(theta)]
    d.add(PolyLine(pts, strokeColor=LINE, strokeWidth=0.8))
    theta = math.pi * (1 - progress_frac)
    mx = cx + r * math.cos(theta)
    my = baseline_y + r * math.sin(theta)
    d.add(Circle(mx, my, 2, fillColor=INK, strokeColor=None))
    return d


def render(ctx, out_path, pdf_title="THE DAILY MOG"):
    """ctx keys (all required):
    date_str, generated_at (precise HH:MM:SS-style string, printed right
    after the date as freshness proof), vol_no, epigraph, sun_text,
    sun_progress_frac, moon_text, moon_phase_frac, ticker_items,
    fear_greed_value, fear_greed_label, otd_year, otd_rest,
    weather_headline, uv_aqi_line, primoscapes_note, fact, baby_tip,
    word_of_day (term, pos, definition), news (list of (tag, headline)),
    decide_title, feature_title, feature_body, tvl_line,
    tvl_history (list of floats, oldest-first, empty list to omit the
    sparkline), arcana (quote, source), market_cap (formatted string, e.g.
    "$2.28T"), btc_dominance (formatted string, e.g. "56.1%"), random_fact
    (fresh live fact, not a curated bank), history_quote (quote, source —
    a real attributed line from a historically important person), signals_items
    (list of (label, value, color_or_None) tuples for the compact stat strip,
    empty list to omit it)

    sun_text/moon_text should use &nbsp; WITHIN each clause (e.g.
    "Sunrise&nbsp;6:22&nbsp;AM") and a normal breakable space only around the
    " · " separators — this guarantees that if the line ever needs to wrap,
    it breaks at a clause boundary instead of leaving a lone orphan word
    dangling on its own line (a real bug found 2026-07-08: "Fall Eq. in 76d"
    wrapped to "...Fall Eq. in" / "76d").
    """
    # Bottom margin deliberately exceeds the top (0.36in vs 0.3in) —
    # classical page-construction canons (Van de Graaf, Tschichold) always
    # give a page's bottom margin more room than the top; a page whose
    # content presses closer to the bottom edge than the top reads as
    # bottom-heavy/cramped even when the imbalance is subtle. Left/right
    # stay symmetric (a single sheet, not a bound spread with a gutter).
    doc = SimpleDocTemplate(
        out_path, pagesize=letter, leftMargin=0.6 * inch, rightMargin=0.6 * inch,
        topMargin=0.3 * inch, bottomMargin=0.36 * inch, title=pdf_title)
    e = []

    # --- masthead: centered nameplate, classic newspaper folio treatment ---
    # (the face-icon-in-masthead treatment was tried and pulled — Josh's
    # call, 2026-07-07: "The Bad boys dont look good at all so take those
    # off." Small print at ~0.4in tall apparently doesn't hold up; text-only
    # nameplate again, back at full 42pt now that the icon isn't competing
    # for row height.)
    e.append(HRFlowable(width="100%", thickness=0.5, color=LINE, spaceAfter=6))
    e.append(Paragraph("THE DAILY MOG", S["masthead"]))
    e.append(Spacer(1, 3))
    # epigraph flanked by floral ornaments matching the SUB ROSA seal, so the
    # masthead and the footer rhyme — top and bottom of the page echo
    orn = '<font face="ZapfDingbats" size="9" color="#4B3F8F">&#10086;</font>'
    e.append(Paragraph(
        f'{orn}&nbsp;&nbsp;&#8220;{ctx["epigraph"]}&#8221;&nbsp;&nbsp;{orn}',
        S["epigraph"]))
    e.append(Spacer(1, 4))

    # timestamp sits right after the date — precise proof the page was
    # generated fresh this run, not reused from a prior boot (Josh's ask,
    # 2026-07-07, after catching a stale-date bug the morning before)
    folio = Table([[
        Paragraph("OKLAHOMA CITY, OKLA.", S["folio_side"]),
        [Paragraph(ctx["date_str"], S["folio_center"]),
         Paragraph(f'Generated {ctx["generated_at"]}', S["folio_timestamp"])],
        Paragraph(ctx["vol_no"], ParagraphStyle(
            "fsr", parent=S["folio_side"], alignment=TA_RIGHT)),
    ]], colWidths=[2.3 * inch, 2.3 * inch, 2.3 * inch])
    folio.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LINEABOVE", (0, 0), (-1, 0), 1.3, BRAND),
        ("LINEBELOW", (0, 0), (-1, 0), 0.5, LINE),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]))
    e.append(folio)
    e.append(Spacer(1, 4))

    # sky line: small sun-arc + moon-disk icons flanking their own text,
    # rather than one plain line of numbers — the "laws of the universe"
    # touch Josh asked for, kept tiny and neutral (no accent colors).
    # Columns rebalanced ~evenly (was 3.3in/2.68in, sun-heavy) since real
    # measurement showed moon_text is usually the WIDER of the two, not the
    # sun — the old split was starving the side that needed more room
    # (root cause of the "76d" orphan-wrap bug, 2026-07-08).
    sky_row = Table([[
        sun_arc(ctx["sun_progress_frac"]),
        Paragraph(ctx["sun_text"], S["almanac_line"]),
        moon_icon(ctx["moon_phase_frac"]),
        Paragraph(ctx["moon_text"], S["almanac_line"]),
    ]], colWidths=[0.72 * inch, 3.0 * inch, 0.2 * inch, 2.98 * inch])
    sky_row.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("ALIGN", (0, 0), (0, 0), "CENTER"),
        ("ALIGN", (2, 0), (2, 0), "CENTER"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 3),
    ]))
    e.append(sky_row)
    e.append(Spacer(1, 4))

    # ticker + Fear & Greed moved to the bottom of the page, by the
    # markets/quote close — Josh's call, 2026-07-07 ("bring fear and greed
    # index down to bottom + bring the tickers down there as well"). On
    # This Day now follows the sky line directly.
    e.append(Paragraph(
        f'ON THIS DAY &#8212; <b>{ctx["otd_year"]}</b>:{ctx["otd_rest"]}',
        S["otd_line"]))
    e.append(Spacer(1, 4))

    # two columns
    left = []
    left += sec("WEATHER — OKC")
    left.append(Paragraph(ctx["weather_headline"], S["body"]))
    left.append(Spacer(1, 2))
    left.append(Paragraph(ctx["uv_aqi_line"], S["muted_sm"]))
    left.append(Spacer(1, 2))
    left.append(Paragraph(
        f'<b>Primoscapes note:</b> {ctx["primoscapes_note"]}', S["muted_sm"]))

    left += sec("FIELD NOTES")
    left.append(Paragraph(ctx["fact"], S["body"]))

    left += sec("NURSERY NOTES")
    left.append(Paragraph(ctx["baby_tip"], S["body"]))

    wod_term, wod_pos, wod_def = ctx["word_of_day"]
    left += sec("VOCABULARY EXPANSION")
    left.append(Paragraph(
        f'{wod_term}  <font face="Times-Italic" color="#6B6255" size="9">'
        f'&#183; {wod_pos}</font>', S["wod_term"]))
    left.append(Spacer(1, 2))
    left.append(Paragraph(wod_def, S["body"]))

    right = []
    right += sec("THE MOG DIGEST")
    news = ctx["news"]
    for i, (tag, headline) in enumerate(news):
        right.append(Paragraph(tag, S["news_tag"]))
        right.append(Paragraph(headline, S["news_headline"]))
        if i < len(news) - 1:
            right.append(HRFlowable(width="100%", thickness=0.5, color=LINE,
                                    spaceBefore=4, spaceAfter=4))
    right.append(Spacer(1, 4))

    # DECIDE: was a full bordered box (title + context body) — collapsed to
    # one inline line, no separate section header or box padding (Josh's
    # call, 2026-07-08: "get rid of the Decide section or make it much
    # smaller"). Still the real top pending Gate Deck item, just quieter.
    right.append(Paragraph(
        f'<font face="Helvetica-Bold" color="#B8790A">DECIDE</font> '
        f'&#8212; {ctx["decide_title"]}',
        S["decide_inline"]))

    # MARKET NOTES: prose, like every other section on the page — the old
    # "Label: value" spec-sheet format broke the editorial voice (Josh's
    # call, 2026-07-07). The TVL sparkline rides as a small supporting
    # caption underneath, not a bolded headline stat.
    right += sec(ctx["feature_title"])
    right.append(Paragraph(ctx["feature_body"], S["body"]))
    if ctx.get("tvl_history"):
        right.append(Spacer(1, 3))
        spark_w = 0.5 * inch
        tvl_row = Table([[
            sparkline(ctx["tvl_history"], width=36, height=12),
            Paragraph(ctx["tvl_line"], S["muted_sm"]),
        ]], colWidths=[spark_w, COL_MINOR - 0.194 * inch - spark_w])
        tvl_row.setStyle(TableStyle([
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("TOPPADDING", (0, 0), (0, 0), 3),  # nudges the sparkline down
            ("TOPPADDING", (1, 0), (1, 0), 0),  # to sit on the text baseline
            ("LEFTPADDING", (0, 0), (-1, -1), 0),
            ("RIGHTPADDING", (0, 0), (0, 0), 4),  # small gap before the text
        ]))
        right.append(tvl_row)
    else:
        right.append(Paragraph(ctx["tvl_line"], S["muted_sm"]))

    # golden-ratio column split (phi = 1.618) instead of the earlier
    # near-even 3.55/3.35 — a "felt, not seen" proportion refinement
    cols = Table([[left, right]], colWidths=[COL_MAJOR, COL_MINOR])
    cols.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LINEAFTER", (0, 0), (0, 0), 0.5, LINE),
        ("RIGHTPADDING", (0, 0), (0, 0), 14),
        ("LEFTPADDING", (1, 0), (1, 0), 14),
    ]))
    e.append(cols)
    e.append(Spacer(1, 3))

    # --- FORBIDDEN WISDOM: full-width arcane inscription, the page's closing
    # seal (renamed from "Sub Rosa" — Josh's call, 2026-07-07; this is his
    # own original phrasing from when he first asked for the section) ---
    arc_quote, arc_src = ctx["arcana"]
    e.append(HRFlowable(width="100%", thickness=1.3, color=BRAND, spaceAfter=1.5))
    e.append(HRFlowable(width="100%", thickness=0.5, color=LINE, spaceAfter=5))
    e.append(Paragraph(
        '<font face="ZapfDingbats" size="8">&#10086;</font>&nbsp;&nbsp;&nbsp;'
        'FORBIDDEN WISDOM'
        '&nbsp;&nbsp;&nbsp;<font face="ZapfDingbats" size="8">&#10086;</font>',
        S["arcana_kicker"]))
    e.append(Spacer(1, 2))
    e.append(Paragraph(f"&#8220;{arc_quote}&#8221;", S["arcana_quote"]))
    e.append(Spacer(1, 2))
    e.append(Paragraph(f"&#8212; {arc_src}", S["arcana_attr"]))
    e.append(Spacer(1, 2))

    # --- MARKETS: ticker + SIGNALS strip + Fear & Greed/market cap/
    # dominance, relocated here from the top of the page — Josh's call,
    # 2026-07-07 ("bring fear and greed index down to bottom + bring the
    # tickers down there too") ---
    e.append(Spacer(1, 3))
    e.append(HRFlowable(width="100%", thickness=0.5, color=LINE, spaceAfter=4))
    e.append(ticker_strip(ctx["ticker_items"]))
    if ctx.get("signals_items"):
        e.append(signals_strip(ctx["signals_items"]))
    e.append(Spacer(1, 3))
    fg_color = FEAR_GREED_COLOR.get(ctx["fear_greed_label"].upper(), "#6B6255")
    e.append(Paragraph(
        f'<font face="Helvetica-Bold">CRYPTO FEAR &amp; GREED:</font> '
        f'{ctx["fear_greed_value"]} &#183; '
        f'<font color="{fg_color}"><b>{ctx["fear_greed_label"].upper()}</b></font>'
        f' &#183; Market Cap: {ctx["market_cap"]} &#183; BTC Dominance: '
        f'{ctx["btc_dominance"]}',
        S["index_line"]))
    e.append(Spacer(1, 3))

    # a fresh live fact every run, not a curated bank — pure delight, no
    # theme required (Josh's pick, 2026-07-07)
    orn_fact = '<font face="ZapfDingbats" size="7" color="#4B3F8F">&#10086;</font>'
    e.append(Paragraph(
        f'{orn_fact}&nbsp;&nbsp;{ctx["random_fact"]}&nbsp;&nbsp;{orn_fact}',
        S["random_fact"]))
    e.append(Spacer(1, 3))

    # closing quote: a real, attributed line from an actual historically
    # important person — distinct from FORBIDDEN WISDOM's esoteric bent
    # (Josh, 2026-07-07: "make it an actual quote from historically
    # important ppl"), replacing the source-name box he didn't like. (A
    # Bad Boys cast line alternated in here briefly — Josh killed it,
    # 2026-07-08: "take out the 'from the cast'".)
    hist_quote, hist_src = ctx["history_quote"]
    seal = Table([[
        [Paragraph(
            '<font face="ZapfDingbats" size="8">&#10086;</font>'
            '&nbsp;&nbsp;WORDS TO LIVE BY&nbsp;&nbsp;'
            '<font face="ZapfDingbats" size="8">&#10086;</font>',
            S["seal_kicker"]),
         Spacer(1, 3),
         Paragraph(f"&#8220;{hist_quote}&#8221;", S["history_quote"]),
         Spacer(1, 2),
         Paragraph(f"&#8212; {hist_src}", S["history_attr"])],
    ]], colWidths=[6.9 * inch])
    seal.setStyle(TableStyle([
        ("BOX", (0, 0), (-1, -1), 0.75, LINE),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING", (0, 0), (-1, -1), 16),
        ("RIGHTPADDING", (0, 0), (-1, -1), 16),
    ]))
    e.append(seal)

    doc.build(e)
