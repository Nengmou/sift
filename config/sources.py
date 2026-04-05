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
    "OpenAI",                   # API / product usage patterns
    "ClaudeAI",                 # Power user workflows, prompting patterns
    "ClaudeCode",               # AI coding workflows
    "cursor",                   # AI IDE workflows
    "ChatGPTCoding",            # Coding-specific prompting and usage
    "ChatGPT",                  # Broad user patterns; keep ranked cautiously
    "mlops",                    # Production ML, deployment, monitoring
    "dataengineering",          # Pipelines, infra, data systems
    "devops",                   # Platform and deployment workflows
    "learnmachinelearning",     # Tutorials, practitioner bridge
    "deeplearning",             # Architecture discussions
    "LLMDevs",                  # App builders, LLM integrations
    "PromptEngineering",        # Technique sharing, real examples
    "datascience",              # Applied ML in industry
    "Python",                   # Python ecosystem, AI library releases
    "programming",              # Broad engineering discourse and tooling launches
    "webdev",                   # Frontend + AI-tooling workflows
    "artificial",               # Broad AI discussion; rank conservatively
    "selfhosted",               # Local tooling and self-hosted model workflows
    "opensource",               # Open source AI project launches
]

# ---------------------------------------------------------------------------
# Twitter/X accounts
# Used by TwitterConnector when TWITTER_BEARER_TOKEN is configured.
# Format: username only (no @)
# Prefer builders, infra maintainers, evaluators, and technical educators.
# ---------------------------------------------------------------------------

TWITTER_ACCOUNTS: list[str] = [
    "simonw",
    "karpathy",
    "eugeneyan",
    "chiphuyen",
    "rasbt",
    "HamelHusain",
    "vboykis",
    "jeremyphoward",
    "thom_wolf",
    "osanseviero",
    "joao_gante",
    "_philschmid",
    "ggerganov",
    "jxnlco",
    "hwchase17",
    "jerryjliu0",
    "goodside",
    "teortaxesTex",
    "abacaj",
    "nrehiew_",
    "shreya_shankar",
    "huyenchip",
    "mihail_eric",
    "humanloop",
    "langfuse",
    "basetenlabs",
    "modal_labs",
    "anyscalecompute",
    "togethercompute",
    "replicate",
    "weights_biases",
    "vllm_project",
    "sglangai",
    "OpenAIDevs",
    "ollama",
    "lmsysorg",
    "huggingface",
    "OpenAI",
    "AnthropicAI",
    "GoogleDeepMind",
    "MistralAI",
    "LangChainAI",
    "llama_index",
    "ClementDelangue",
    "AlexAlbert__",     # Anthropic developer relations / release details
    "shanselman",
    "addyosmani",
    "leeerob",
    "steipete",
    "theo",
    "fchollet",
    "swyx",
    "mckaywrigley",
    "danielhanchen",
    "reach_vb",
    "mattshumer_",
    "GregKamradt",
    "rohanpaul_ai",
    "svpino",
    "DrJimFan",
    "hardmaru",
    "natolambert",
    "_jasonwei",
    "ykilcher",
    "emollick",
    "burkov",
    "tim_dettmers",
    "elvis_saravia",
    "LatentSpacePod",
    "cohere",
    "groqinc",
    "perplexity_ai",
    "dottxtai",
    "rowancheung",
    "TheTuringPost",
    "AravSrinivas",
    "AndrewYNg",
    "sama",
    "Fireship_dev",
    "levelsio",
    "danshipper",
    "LennyRachitsky",
    "packym",
    "every",
    "fortelabs",
    "NatEliason",
    "heynikihey",
]

# ---------------------------------------------------------------------------
# YouTube channels
# Used by YouTubeConnector when YOUTUBE_API_KEY is configured.
# Prefer tutorials, technical talks, and implementation-heavy explainers.
# Format: YouTube channel ID (UCxxxxxxxx) or a stable handle (@name).
# ---------------------------------------------------------------------------

YOUTUBE_CHANNEL_IDS: list[str] = [
    "UCPk8m_r6fkUSWebbjWSS8Dw",  # Andrej Karpathy
    "UCNJ1Ymd5yFuUPtn21xtRbbw",  # Yannic Kilcher
    "UCbmNph6atAoGfqLoCL_duAg",  # Aleksa Gordić — The AI Epiphany
    "UCZHmQk67mSJgfCCTn7xBfew",  # Umar Jamil — paper implementations
    "UCfzlCWGWYyIQ0aLC5w48gBQ",  # Sentdex
    "UCX7oe66V8zyFpAJyMfPL9VA",  # Jeremy Howard / fast.ai
    "UCq6XkhO5SZ66N04IcPbqNcw",  # Full Stack Deep Learning
    "UC_1lhF3hn-ZIRnSzbIiEMdg",  # DataTalks.Club
    "UCYasrbSOs9bx0X1mNkhHCRQ",  # MLOps Community
    "UCvmINlrza7JHB1zkIOuXEbw",  # Hugging Face
    "UCBcRF18a7Qf58cCRy5xuWwQ",  # Weights & Biases
    "UCnUYZLuoy1rq1aVMwx4aTzw",  # Google DeepMind
    "UCoh6pEyM-NxQ3fePM4p1biA",  # Stanford HAI
    "UCV6J_jJa8GJqFwQNgNrMuww",  # PyData
    "UCTTdSBjXxXCQJR0OoFnMoBA",  # Machine Learning Street Talk
    "UCzLqOSZPtUKrmSEnlH4LAvw",  # Latent Space
    "@PracticalAI",             # Applied AI engineering discussions
    "@AssemblyAI",              # Speech / applied AI tutorials
    "@HuggingFace",             # Product demos and tutorials
    "@MLOpsCommunity",          # Practitioner-heavy talks
    "@deeplearningai",          # Short practical AI explainers and courses
    "@IBMTechnology",           # Clear technical explainers on AI systems
    "@YannicKilcher",           # Research deep dives
    "@AndrejKarpathy",          # LLM / foundation model intuition
    "UCWX3yGbODI3HLSzg0GR9oNg",  # 3Blue1Brown
    "UCgBVkKoOAr3ajSdXLDBChvA",  # Sam Witteveen — LLM building
    "UCyIe-61Y8C4_o-zZCtO4ETQ",  # AI Jason
    "UCzWQYUVCpZqtN93H8RR44Qw",  # Nicholas Renotte
    "UCVhQ2NnY5Rskt6UjCUkJ_DA",  # Replicate
    "@LangChain",               # Agent framework walkthroughs
    "@LlamaIndex",              # Retrieval and agents walkthroughs
    "@WeightsBiases",           # Evals / observability / practical ML
    "@PyDataTV",                # Conference talks and tutorials
    "@OpenAI",                  # Product and research presentations
    "@AnthropicAI",             # Claude and agent-oriented content
    "UCSHZKyawb77ixDdsGog4iWA",  # Lex Fridman
    "UCKkSHBGBCH-LqMFRPqYBb1A",  # TWIML AI Podcast
    "UCGq-a57w-aPwyi3pW7XLiHw",  # Cognitive Revolution
    "@Fireship",                # Fast-moving dev + AI tooling updates
    "@NetworkChuck",            # Broad dev tooling; useful for power users
    "@freecodecamp",            # Long-form implementation tutorials
    "@TheCognitiveRevolutionPodcast",  # Longer-form context and interviews
]
