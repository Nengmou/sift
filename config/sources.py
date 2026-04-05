"""
Curated source lists — the editorial heart of Sift.
Edit these lists to tune recommendation quality.
Bias toward: authentic practitioners, builders sharing real experience.
Avoid: pundits, engagement farmers, institutional PR accounts.
"""

# ---------------------------------------------------------------------------
# RSS / Substack feeds
# ---------------------------------------------------------------------------

RSS_FEEDS: list[str] = [
    # --- Practitioner blogs (highest signal) ---
    "https://simonwillison.net/atom/everything/",           # Simon Willison — builds with LLMs daily
    "https://karpathy.github.io/feed.xml",                  # Andrej Karpathy
    "https://eugeneyan.com/rss/",                           # Eugene Yan — applied ML, LLM evals
    "https://huyenchip.com/feed.xml",                       # Chip Huyen — ML systems, deployment
    "https://hamel.dev/feed.xml",                           # Hamel Husain — LLM evals, fine-tuning
    "https://vickiboykis.com/index.xml",                    # Vicki Boykis — low-hype ML/engineering
    "https://magazine.sebastianraschka.com/feed",           # Sebastian Raschka — Ahead of AI
    "https://lilianweng.github.io/index.xml",               # Lilian Weng — deep technical posts
    "https://jalammar.github.io/feed.xml",                  # Jay Alammar — transformer explainers
    "https://colah.github.io/rss.xml",                      # Chris Olah — interpretability
    "https://www.fast.ai/index.xml",                        # Jeremy Howard / fast.ai
    "https://timdettmers.com/feed/",                        # Tim Dettmers — quantization, efficient training
    "https://interconnects.ai/feed",                        # Nathan Lambert — RLHF, alignment
    "https://shreyashankar.substack.com/feed",              # Shreya Shankar — ML production, evals
    "https://joshtobin.com/feed.xml",                       # Josh Tobin — applied ML
    "https://blog.eleuther.ai/feed.xml",                    # EleutherAI — open source research

    # --- Technical newsletters ---
    "https://importai.substack.com/feed",                   # Jack Clark — Import AI weekly
    "https://www.latent.space/feed",                        # Latent Space — builders interviewing builders
    "https://thegradient.pub/rss/",                         # The Gradient — long-form technical
    "https://aisnakeoil.substack.com/feed",                 # Arvind Narayanan — skeptical counterbalance
    "https://www.deeplearning.ai/the-batch/feed/",          # The Batch — Andrew Ng
    "https://ethanmollick.substack.com/feed",               # Ethan Mollick — One Useful Thing
    "https://buttondown.email/ainews/rss",                  # AI News — daily research digest
    "https://nlp.elvissaravia.com/feed",                    # Elvis Saravia — NLP/LLM practitioner

    # --- Tool & infra team blogs ---
    "https://huggingface.co/blog/feed.xml",                 # Hugging Face
    "https://wandb.ai/fully-connected/feed",                # Weights & Biases — MLOps
    "https://blog.llamaindex.ai/feed",                      # LlamaIndex — RAG, agents
    "https://blog.langchain.dev/rss/",                      # LangChain — agent frameworks
    "https://www.anthropic.com/news/rss.xml",               # Anthropic research blog
    "https://modal.com/blog/feed",                          # Modal — GPU infra, deployment
    "https://replicate.com/blog/feed",                      # Replicate — model deployment
    "https://lightning.ai/blog/feed/",                      # Lightning AI — training infra
    "https://txt.cohere.com/rss/",                          # Cohere — enterprise LLM
    "https://mistral.ai/news/feed.xml",                     # Mistral — open model releases
    "https://www.together.ai/blog/feed",                    # Together AI — inference, fine-tuning
    "https://www.pinecone.io/blog/feed/",                   # Pinecone — vector search
    "https://weaviate.io/blog/feed.xml",                    # Weaviate — vector DB
    "https://www.trychroma.com/blog/feed",                  # Chroma — vector DB

    # --- Applied ML / engineering adjacent ---
    "https://blog.pragmaticengineer.com/rss/",              # The Pragmatic Engineer
    "https://jvns.ca/atom.xml",                             # Julia Evans — technical depth
    "https://danluu.com/atom.xml",                          # Dan Luu — systems depth
    "https://www.probably.overthinking.it/feed.xml",        # Allen Downey — statistical thinking
    "https://gregorygundersen.com/blog/rss.xml",            # Greg Gundersen — ML math
    "https://bounded-regret.ghost.io/rss/",                 # Jacob Steinhardt — ML safety
    "https://www.alignmentforum.org/feed.xml",              # Alignment Forum — safety research

    # --- Research blogs ---
    "https://openai.com/news/rss.xml",                      # OpenAI research
    "https://deepmind.google/blog/rss.xml",                 # Google DeepMind
    "https://ai.meta.com/blog/rss/",                        # Meta AI
    "https://research.google/blog/rss/",                    # Google Research
]

# ---------------------------------------------------------------------------
# Subreddits
# ---------------------------------------------------------------------------

SUBREDDITS: list[str] = [
    "MachineLearning",          # Research papers, implementation discussion
    "LocalLLaMA",               # Open model usage, benchmarks, hands-on
    "ExperiencedDevs",          # Senior engineer perspective on AI tooling
    "ClaudeAI",                 # Power user workflows, prompting patterns
    "ChatGPT",                  # Real usage patterns (filter for practitioner posts)
    "LanguageModelEvaluation",  # Evals, benchmarks, methodology
    "mlops",                    # Production ML, deployment, monitoring
    "learnmachinelearning",     # Tutorials, practitioner bridge
    "deeplearning",             # Architecture discussions
    "LLMDevs",                  # App builders, LLM integrations
    "PromptEngineering",        # Technique sharing, real examples
    "StableDiffusion",          # Image AI — practitioner-heavy community
    "datascience",              # Applied ML in industry
    "AIAssistants",             # Power user workflows
    "Python",                   # Python ecosystem, AI library releases
    "artificial",               # General AI — breadth
    "singularity",              # High-signal links (filter speculation)
    "opensource",               # Open source AI project launches
]

# ---------------------------------------------------------------------------
# Twitter/X accounts
# Used by TwitterConnector when TWITTER_BEARER_TOKEN is configured.
# Format: username only (no @)
# ---------------------------------------------------------------------------

TWITTER_ACCOUNTS: list[str] = [
    # Core practitioners — builders
    "simonw",           # Simon Willison — most prolific LLM builder
    "karpathy",         # Andrej Karpathy
    "eugeneyan",        # Eugene Yan
    "chiphuyen",        # Chip Huyen
    "rasbt",            # Sebastian Raschka
    "HamelHusain",      # Hamel Husain
    "vboykis",          # Vicki Boykis
    "fchollet",         # Francois Chollet
    "jeremyphoward",    # Jeremy Howard
    "thom_wolf",        # Thomas Wolf (HF)
    "osanseviero",      # Omar Sanseviero (HF)
    "joao_gante",       # HF transformers core
    "_philschmid",      # Philipp Schmid (HF)
    "ggerganov",        # Georgi Gerganov (llama.cpp)
    "jxnlco",           # Jason Liu (Instructor)
    "hwchase17",        # Harrison Chase (LangChain)
    "jerryjliu0",       # Jerry Liu (LlamaIndex)
    "swyx",             # AI engineer community builder
    "mckaywrigley",     # Builder, open source
    "danielhanchen",    # Fine-tuning practitioner
    "reach_vb",         # Vaibhav Srivastav (HF)
    "mattshumer_",      # AI product builder
    "GregKamradt",      # LLM use cases
    "rohanpaul_ai",     # Applied ML practitioner
    "svpino",           # Santiago Valdarrama — applied ML
    "skalskip92",       # Computer vision practitioner
    "marktenenholtz",   # ML practitioner

    # Researchers — honest, technical
    "ylecun",           # Yann LeCun — skeptical counterpoint
    "ilyasut",          # Ilya Sutskever
    "DrJimFan",         # NVIDIA researcher
    "kchonyc",          # Kyunghyun Cho
    "hardmaru",         # David Ha
    "natolambert",      # Nathan Lambert — RLHF, alignment
    "_jasonwei",        # Jason Wei — chain-of-thought
    "cwolferesearch",   # Chelsea Voss
    "ykilcher",         # Yannic Kilcher
    "random_walker",    # Arvind Narayanan — skeptical/critical
    "emollick",         # Ethan Mollick
    "GaryMarcus",       # Critical perspective on AI claims
    "burkov",           # Andriy Burkov
    "NathanLambert",    # Alignment, RLHF

    # MLOps / production ML
    "shreya_shankar",   # ML production, data quality
    "mihail_eric",      # LLM evals, quality
    "josephmisiti",     # ML infrastructure

    # AI power users & indie builders
    "tunguz",           # Bojan Tunguz — Kaggle grandmaster
    "willkurt",         # Will Kurt — probabilistic reasoning
    "AravSrinivas",     # Perplexity CEO
    "dottxtai",         # Structured generation
    "tim_dettmers",     # Quantization, efficient training

    # Open source / infra
    "lmsysorg",         # LM Systems — benchmarks, Chatbot Arena
    "alexalbert__",     # Anthropic — Claude updates

    # Curators / communities
    "latentspacepod",   # Latent Space podcast
    "weights_biases",   # W&B
    "huggingface",      # HF announcements
    "LangChainAI",      # LangChain
    "llama_index",      # LlamaIndex

    # Research labs (for releases, not PR)
    "GoogleDeepMind",
    "AIatMeta",
    "MistralAI",
    "AnthropicAI",
]

# ---------------------------------------------------------------------------
# YouTube channel IDs
# Used by YouTubeConnector when YOUTUBE_API_KEY is configured.
# Format: YouTube channel ID (UCxxxxxxxx)
# ---------------------------------------------------------------------------

YOUTUBE_CHANNEL_IDS: list[str] = [
    # Deep technical — highest priority
    "UCPk8m_r6fkUSWebbjWSS8Dw",  # Andrej Karpathy
    "UCNJ1Ymd5yFuUPtn21xtRbbw",  # Yannic Kilcher
    "UCbmNph6atAoGfqLoCL_duAg",  # Aleksa Gordić — The AI Epiphany
    "UCZHmQk67mSJgfCCTn7xBfew",  # Umar Jamil — paper implementations
    "UCWX3yGbODI3HLSzg0GR9oNg",  # 3Blue1Brown
    "UCfzlCWGWYyIQ0aLC5w48gBQ",  # Sentdex
    "UCSHZKyawb77ixDdsGog4iWA",  # Lex Fridman

    # Practitioner / builder focus
    "UCgBVkKoOAr3ajSdXLDBChvA",  # Sam Witteveen — LLM building
    "UCyIe-61Y8C4_o-zZCtO4ETQ",  # AI Jason
    "UCzWQYUVCpZqtN93H8RR44Qw",  # Nicholas Renotte
    "UCtatfZMf-8EkIwASXM4ts0A",  # AssemblyAI
    "UCBcRF18a7Qf58cCRy5xuWwQ",  # Weights & Biases
    "UCvmINlrza7JHB1zkIOuXEbw",  # Hugging Face
    "UCX7oe66V8zyFpAJyMfPL9VA",  # Jeremy Howard / fast.ai
    "UCq6XkhO5SZ66N04IcPbqNcw",  # Full Stack Deep Learning
    "UC_1lhF3hn-ZIRnSzbIiEMdg",  # DataTalks.Club
    "UCYasrbSOs9bx0X1mNkhHCRQ",  # MLOps Community

    # Conference / talks
    "UCnUYZLuoy1rq1aVMwx4aTzw",  # Google DeepMind
    "UCoh6pEyM-NxQ3fePM4p1biA",  # Stanford HAI

    # Podcast-style
    "UCTTdSBjXxXCQJR0OoFnMoBA",  # Machine Learning Street Talk
    "UCzLqOSZPtUKrmSEnlH4LAvw",  # Latent Space
    "UCKkSHBGBCH-LqMFRPqYBb1A",  # TWIML AI Podcast
    "UCGq-a57w-aPwyi3pW7XLiHw",  # Cognitive Revolution
]
