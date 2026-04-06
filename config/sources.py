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
]

# Additional curated X accounts kept here for later re-enable if API budget allows:
# "joao_gante",
# "_philschmid",
# "ggerganov",
# "jxnlco",
# "hwchase17",
# "jerryjliu0",
# "goodside",
# "teortaxesTex",
# "abacaj",
# "nrehiew_",
# "shreya_shankar",
# "huyenchip",
# "mihail_eric",
# "humanloop",
# "langfuse",
# "basetenlabs",
# "modal_labs",
# "anyscalecompute",
# "togethercompute",
# "replicate",
# "weights_biases",
# "vllm_project",
# "sglangai",
# "OpenAIDevs",
# "ollama",
# "lmsysorg",
# "huggingface",
# "OpenAI",
# "AnthropicAI",
# "GoogleDeepMind",
# "MistralAI",
# "LangChainAI",
# "llama_index",
# "ClementDelangue",
# "AlexAlbert__",     # Anthropic developer relations / release details
# "shanselman",
# "addyosmani",
# "leeerob",
# "steipete",
# "theo",
# "fchollet",
# "swyx",
# "mckaywrigley",
# "danielhanchen",
# "reach_vb",
# "mattshumer_",
# "GregKamradt",
# "rohanpaul_ai",
# "svpino",
# "DrJimFan",
# "hardmaru",
# "natolambert",
# "_jasonwei",
# "ykilcher",
# "emollick",
# "burkov",
# "tim_dettmers",
# "elvis_saravia",
# "LatentSpacePod",
# "cohere",
# "groqinc",
# "perplexity_ai",
# "dottxtai",
# "rowancheung",
# "TheTuringPost",
# "AravSrinivas",
# "AndrewYNg",
# "sama",
# "Fireship_dev",
# "levelsio",
# "danshipper",
# "LennyRachitsky",
# "packym",
# "every",
# "fortelabs",
# "NatEliason",
# "heynikihey",

# ---------------------------------------------------------------------------
# YouTube channels
# Used by YouTubeConnector when YOUTUBE_API_KEY is configured.
# Prefer tutorials, technical talks, and implementation-heavy explainers.
# Verified ingest list.
# ---------------------------------------------------------------------------

YOUTUBE_CHANNEL_IDS: list[str] = [
    "UCXUPKJO5MZQN11PqgIvyuvQ",  # Andrej Karpathy
    "UCZHmQk67mSJgfCCTn7xBfew",  # Yannic Kilcher
    "UCfzlCWGWYyIQ0aLC5w48gBQ",  # sentdex
    "UCG6qpjVnBTTT8wLGBygANOQ",  # MLOps.community
    "UCHlNU7kIZhRgSbhHvFoy72w",  # Hugging Face
    "UCBp3w4DCEC64FZr4k9ROxig",  # Weights & Biases
    "UCcIXc5mJsHVYTZR1maL5l9w",  # DeepLearningAI
    "UCGbmaIsLSPMgO9mMaFqvP7g",  # Practical AI
    "UCKWaEZ-_VweaEx1j62do_vQ",  # IBM Technology
    "UCtatfZMf-8EkIwASXM4ts0A",  # AssemblyAI
    "UCC-lyoTfSrcJzA1ab3APAgw",  # LangChain
    "UCeRjipR4_SsCddq9VZ2AeKg",  # LlamaIndex
    "UCOjD18EJYcsBog4IozkF_7w",  # PyData
    "UCXZCJLdBC09xxGZ6gcdrc6A",  # OpenAI
    "UCrDwWp7EBBv4NwvScIpBDOA",  # Anthropic
    "UCSHZKyawb77ixDdsGog4iWA",  # Lex Fridman
    "UC8butISFwT-Wl7EV0hUK0BQ",  # freeCodeCamp.org
    "UC9x0AN7BWHpCDHSm9NiJFJQ",  # NetworkChuck
    "UCsBjURrPoezykLs9EqgamOA",  # Fireship
    "UCKNF1Pm-M-lvJ_LTELoQ4Ig",  # Jing Shi
    "UC6t1O76G0jYXOAoYCm153dA",  # Lenny's Podcast
    "UC1UNB6Gy11umcbEj_hqIwhw",  # Little Chinese Everywhere
    "UC_5lJHgnMP_lb_VpIiXV0hQ",  # 课代表立正
    "UCQgFQdqiFQ_LfFBGP6z9dqQ",  # Manus AI
    "UC3Sv1JuKpbOx3csUO8FAo5g",  # Zhang Xiaojun Podcast
]

# ---------------------------------------------------------------------------
# Tag vocabulary for LLM-based semantic tagging
# TAG_VOCABULARY: granular tags the LLM assigns to each item at score time.
# TAG_TO_INTEREST: maps each tag to its parent TOPIC_CARD (user interest).
# ---------------------------------------------------------------------------

TAG_VOCABULARY: list[str] = [
    # LLM infrastructure
    "inference serving", "model quantization", "GPU infrastructure", "vLLM",
    "llama.cpp", "GGUF", "ONNX", "distributed training", "edge inference",
    "KV cache", "throughput optimization", "model batching", "speculative decoding",
    # AI agents
    "AI agents", "multi-agent systems", "RAG", "function calling", "tool use",
    "agent memory", "agent orchestration", "agentic workflows", "LangChain",
    "LlamaIndex", "CrewAI", "AutoGen",
    # MLOps
    "model deployment", "model monitoring", "experiment tracking", "ML pipelines",
    "model versioning", "data drift detection", "A/B testing for ML",
    "Weights & Biases", "MLflow", "feature stores",
    # Prompt engineering
    "prompting techniques", "chain-of-thought", "few-shot learning", "system prompts",
    "prompt optimization", "structured output", "context window management",
    "prompt injection", "jailbreaking",
    # Frontend development
    "React", "TypeScript", "UI/UX design", "web performance", "CSS frameworks",
    "frontend tooling", "accessibility", "Next.js",
    # Systems design
    "distributed systems", "API design", "microservices", "scalability",
    "caching strategies", "message queues", "database design", "system architecture",
    # Data engineering
    "data pipelines", "ETL", "stream processing", "data lakes", "data quality",
    "Apache Spark", "dbt", "workflow orchestration", "Kafka", "Airflow",
    # AI for productivity
    "AI coding tools", "workflow automation", "AI writing tools",
    "AI assistants", "AI search", "knowledge management", "AI for business",
    "Claude Code", "Cursor",
    # Open-source models
    "Llama", "Mistral", "Gemma", "model fine-tuning", "LoRA", "PEFT",
    "Hugging Face", "open weights models", "model merging",
    # Evaluation and testing
    "LLM evaluation", "benchmarks", "red teaming", "safety evaluation",
    "model comparison", "evaluation frameworks", "hallucination detection",
    "alignment research", "evals",
]

TAG_VOCABULARY_SET: set[str] = set(TAG_VOCABULARY)

TAG_TO_INTEREST: dict[str, str] = {
    # LLM infrastructure
    "inference serving": "LLM infrastructure",
    "model quantization": "LLM infrastructure",
    "GPU infrastructure": "LLM infrastructure",
    "vLLM": "LLM infrastructure",
    "llama.cpp": "LLM infrastructure",
    "GGUF": "LLM infrastructure",
    "ONNX": "LLM infrastructure",
    "distributed training": "LLM infrastructure",
    "edge inference": "LLM infrastructure",
    "KV cache": "LLM infrastructure",
    "throughput optimization": "LLM infrastructure",
    "model batching": "LLM infrastructure",
    "speculative decoding": "LLM infrastructure",
    # AI agents
    "AI agents": "AI agents",
    "multi-agent systems": "AI agents",
    "RAG": "AI agents",
    "function calling": "AI agents",
    "tool use": "AI agents",
    "agent memory": "AI agents",
    "agent orchestration": "AI agents",
    "agentic workflows": "AI agents",
    "LangChain": "AI agents",
    "LlamaIndex": "AI agents",
    "CrewAI": "AI agents",
    "AutoGen": "AI agents",
    # MLOps
    "model deployment": "MLOps",
    "model monitoring": "MLOps",
    "experiment tracking": "MLOps",
    "ML pipelines": "MLOps",
    "model versioning": "MLOps",
    "data drift detection": "MLOps",
    "A/B testing for ML": "MLOps",
    "Weights & Biases": "MLOps",
    "MLflow": "MLOps",
    "feature stores": "MLOps",
    # Prompt engineering
    "prompting techniques": "Prompt engineering",
    "chain-of-thought": "Prompt engineering",
    "few-shot learning": "Prompt engineering",
    "system prompts": "Prompt engineering",
    "prompt optimization": "Prompt engineering",
    "structured output": "Prompt engineering",
    "context window management": "Prompt engineering",
    "prompt injection": "Prompt engineering",
    "jailbreaking": "Prompt engineering",
    # Frontend development
    "React": "Frontend development",
    "TypeScript": "Frontend development",
    "UI/UX design": "Frontend development",
    "web performance": "Frontend development",
    "CSS frameworks": "Frontend development",
    "frontend tooling": "Frontend development",
    "accessibility": "Frontend development",
    "Next.js": "Frontend development",
    # Systems design
    "distributed systems": "Systems design",
    "API design": "Systems design",
    "microservices": "Systems design",
    "scalability": "Systems design",
    "caching strategies": "Systems design",
    "message queues": "Systems design",
    "database design": "Systems design",
    "system architecture": "Systems design",
    # Data engineering
    "data pipelines": "Data engineering",
    "ETL": "Data engineering",
    "stream processing": "Data engineering",
    "data lakes": "Data engineering",
    "data quality": "Data engineering",
    "Apache Spark": "Data engineering",
    "dbt": "Data engineering",
    "workflow orchestration": "Data engineering",
    "Kafka": "Data engineering",
    "Airflow": "Data engineering",
    # AI for productivity
    "AI coding tools": "AI for productivity",
    "workflow automation": "AI for productivity",
    "AI writing tools": "AI for productivity",
    "AI assistants": "AI for productivity",
    "AI search": "AI for productivity",
    "knowledge management": "AI for productivity",
    "AI for business": "AI for productivity",
    "Claude Code": "AI for productivity",
    "Cursor": "AI for productivity",
    # Open-source models
    "Llama": "Open-source models",
    "Mistral": "Open-source models",
    "Gemma": "Open-source models",
    "model fine-tuning": "Open-source models",
    "LoRA": "Open-source models",
    "PEFT": "Open-source models",
    "Hugging Face": "Open-source models",
    "open weights models": "Open-source models",
    "model merging": "Open-source models",
    # Evaluation and testing
    "LLM evaluation": "Evaluation and testing",
    "benchmarks": "Evaluation and testing",
    "red teaming": "Evaluation and testing",
    "safety evaluation": "Evaluation and testing",
    "model comparison": "Evaluation and testing",
    "evaluation frameworks": "Evaluation and testing",
    "hallucination detection": "Evaluation and testing",
    "alignment research": "Evaluation and testing",
    "evals": "Evaluation and testing",
}
