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
    "https://simonwillison.net/atom/everything/",           # Simon Willison — LLMs daily
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
    "https://timdettmers.com/feed/",                        # Tim Dettmers — quantization
    "https://interconnects.ai/feed",                        # Nathan Lambert — RLHF, alignment
    "https://shreyashankar.substack.com/feed",              # Shreya Shankar — ML production, evals
    "https://joshtobin.com/feed.xml",                       # Josh Tobin — applied ML
    "https://blog.eleuther.ai/feed.xml",                    # EleutherAI — open source research

    # --- Technical newsletters ---
    "https://importai.substack.com/feed",                   # Jack Clark — Import AI weekly
    "https://www.latent.space/feed",                        # Latent Space — builder interviews
    "https://thegradient.pub/rss/",                         # The Gradient — long-form technical
    "https://aisnakeoil.substack.com/feed",                 # Arvind Narayanan — skeptical takes
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
    # Foundation models & LLMs
    "GPT", "Claude", "Gemini", "Grok", "model releases", "context window",
    "model capabilities", "foundation model research", "model architecture",
    "transformer architecture", "model scaling", "reasoning models",
    # Open-source AI
    "Llama", "Mistral", "Gemma", "DeepSeek", "model fine-tuning", "LoRA", "PEFT",
    "Hugging Face", "open weights models", "model merging",
    # Multimodal AI
    "image generation", "video generation", "diffusion models",
    "vision-language models", "audio AI", "speech recognition", "image understanding",
    "Sora", "Runway",
    # AI research & papers
    "deep learning research", "NeurIPS", "ICML", "ICLR", "research papers", "ML theory",
    # Evaluation & benchmarks
    "LLM evaluation", "benchmarks", "red teaming", "safety evaluation",
    "model comparison", "evaluation frameworks", "hallucination detection",
    "evals",
    # AI agents & automation
    "AI agents", "multi-agent systems", "RAG", "function calling", "tool use",
    "agent memory", "agent orchestration", "agentic workflows", "MCP",
    "computer use", "LangChain", "LlamaIndex", "CrewAI", "AutoGen",
    # AI infrastructure & compute
    "inference serving", "model quantization", "GPU infrastructure", "vLLM",
    "llama.cpp", "GGUF", "ONNX", "distributed training", "edge inference",
    "KV cache", "throughput optimization", "model batching", "speculative decoding",
    # Training & fine-tuning
    "model training", "RLHF", "DPO", "instruction tuning", "dataset curation",
    "synthetic data", "pretraining", "model distillation",
    # MLOps & deployment
    "model deployment", "model monitoring", "experiment tracking", "ML pipelines",
    "model versioning", "data drift detection", "A/B testing for ML",
    "Weights & Biases", "MLflow", "feature stores",
    # Data & knowledge
    "data pipelines", "ETL", "stream processing", "data lakes", "data quality",
    "Apache Spark", "dbt", "workflow orchestration", "Kafka", "Airflow",
    # AI tools & productivity
    "AI coding tools", "workflow automation", "AI writing tools",
    "AI assistants", "AI search", "knowledge management", "AI for business",
    "Claude Code", "Cursor", "Copilot",
    # Creative AI
    "generative art", "AI music", "AI video", "AI writing", "creative tools", "Midjourney",
    # AI in science
    "AI drug discovery", "protein folding", "climate AI", "materials science AI",
    "computational biology", "scientific ML",
    # Robotics & embodied AI
    "robot learning", "robot manipulation", "autonomous vehicles", "drone AI",
    "embodied agents", "sim-to-real",
    # AI safety & alignment
    "interpretability", "mechanistic interpretability", "RLHF safety",
    "constitutional AI", "AI alignment", "alignment research",
    # AI policy & regulation
    "EU AI Act", "AI governance", "AI ethics", "AI standards", "responsible AI",
    # AI economics & society
    "AI and jobs", "AI productivity impact", "AI investment", "AI adoption",
    "future of work",
    # AI in business & industry
    "enterprise AI", "AI ROI", "AI strategy", "vertical AI", "AI transformation",
    # Prompt engineering & AI UX
    "prompting techniques", "chain-of-thought", "few-shot learning", "system prompts",
    "prompt optimization", "structured output", "context window management",
    "prompt injection",
    # AI hardware & chips
    "NVIDIA GPUs", "custom AI chips", "TPU", "AI accelerators",
    # Software engineering
    "React", "TypeScript", "UI/UX design", "web performance", "CSS frameworks",
    "frontend tooling", "accessibility", "Next.js",
    "distributed systems", "API design", "microservices", "scalability",
    "caching strategies", "message queues", "database design", "system architecture",
    "Rust", "Go", "Python ecosystem", "compiler design", "WebAssembly",
    "developer productivity", "open source",
    # Cybersecurity
    "vulnerability research", "penetration testing", "supply chain security",
    "zero-day exploits", "threat intelligence", "cryptography", "network security",
    "identity management", "security auditing", "malware analysis",
    "bug bounty", "DevSecOps",
    # Cloud computing
    "Kubernetes", "serverless", "AWS", "Google Cloud", "Azure",
    "infrastructure as code", "Terraform", "cloud cost optimization",
    "container orchestration", "service mesh",
    # Space & astronomy
    "rocket propulsion", "satellite technology", "space exploration",
    "astrophysics", "SpaceX",
    # Biotech & life sciences
    "drug discovery", "genomics", "CRISPR", "synthetic biology", "clinical trials",
    "digital health", "longevity research",
    # Climate & environment
    "clean energy", "carbon capture", "climate modeling", "green tech", "sustainability",
    # Startups & venture capital
    "startup fundraising", "venture capital", "Y Combinator", "product-market fit",
    "growth hacking", "bootstrapping", "startup operations",
    # Career & professional growth
    "technical interviews", "engineering management", "career transitions",
    "mentorship", "salary negotiation",
    # Personal finance & investing
    "investing", "personal budgeting", "FIRE movement", "real estate investing",
    "tax optimization",
    # Economics & markets
    "macroeconomics", "cryptocurrency", "fintech", "financial markets",
    "central banks", "DeFi", "quantitative finance",
    # Geopolitics & international affairs
    "US-China tech", "national security", "trade policy", "digital sovereignty",
    "tech regulation",
    # Health & wellness
    "mental health", "fitness", "nutrition", "sleep science", "preventive medicine",
    # Education & learning
    "online learning", "EdTech", "learning science", "MOOCs", "technical education",
    # Design & creativity
    "product design", "typography", "design systems", "UX research",
    "visual storytelling", "generative design",
    # Science & research
    "physics", "neuroscience", "materials science", "mathematics", "chemistry",
    "scientific computing", "research methodology", "open science",
]

TAG_VOCABULARY_SET: set[str] = set(TAG_VOCABULARY)

TAG_TO_INTEREST: dict[str, str] = {
    # Foundation models & LLMs
    "GPT": "Foundation models & LLMs",
    "Claude": "Foundation models & LLMs",
    "Gemini": "Foundation models & LLMs",
    "Grok": "Foundation models & LLMs",
    "reasoning models": "Foundation models & LLMs",
    "model releases": "Foundation models & LLMs",
    "context window": "Foundation models & LLMs",
    "model capabilities": "Foundation models & LLMs",
    "foundation model research": "Foundation models & LLMs",
    "model architecture": "Foundation models & LLMs",
    "transformer architecture": "Foundation models & LLMs",
    "model scaling": "Foundation models & LLMs",
    # Open-source AI
    "Llama": "Open-source AI",
    "Mistral": "Open-source AI",
    "Gemma": "Open-source AI",
    "DeepSeek": "Open-source AI",
    "model fine-tuning": "Open-source AI",
    "LoRA": "Open-source AI",
    "PEFT": "Open-source AI",
    "Hugging Face": "Open-source AI",
    "open weights models": "Open-source AI",
    "model merging": "Open-source AI",
    # Multimodal AI
    "image generation": "Multimodal AI",
    "video generation": "Multimodal AI",
    "diffusion models": "Multimodal AI",
    "vision-language models": "Multimodal AI",
    "audio AI": "Multimodal AI",
    "speech recognition": "Multimodal AI",
    "image understanding": "Multimodal AI",
    "Sora": "Multimodal AI",
    "Runway": "Multimodal AI",
    # AI research & papers
    "deep learning research": "AI research & papers",
    "NeurIPS": "AI research & papers",
    "ICML": "AI research & papers",
    "ICLR": "AI research & papers",
    "research papers": "AI research & papers",
    "ML theory": "AI research & papers",
    # Evaluation & benchmarks
    "LLM evaluation": "Evaluation & benchmarks",
    "benchmarks": "Evaluation & benchmarks",
    "red teaming": "Evaluation & benchmarks",
    "safety evaluation": "Evaluation & benchmarks",
    "model comparison": "Evaluation & benchmarks",
    "evaluation frameworks": "Evaluation & benchmarks",
    "hallucination detection": "Evaluation & benchmarks",
    "evals": "Evaluation & benchmarks",
    # AI agents & automation
    "AI agents": "AI agents & automation",
    "multi-agent systems": "AI agents & automation",
    "RAG": "AI agents & automation",
    "function calling": "AI agents & automation",
    "tool use": "AI agents & automation",
    "agent memory": "AI agents & automation",
    "agent orchestration": "AI agents & automation",
    "agentic workflows": "AI agents & automation",
    "MCP": "AI agents & automation",
    "computer use": "AI agents & automation",
    "LangChain": "AI agents & automation",
    "LlamaIndex": "AI agents & automation",
    "CrewAI": "AI agents & automation",
    "AutoGen": "AI agents & automation",
    # AI infrastructure & compute
    "inference serving": "AI infrastructure & compute",
    "model quantization": "AI infrastructure & compute",
    "GPU infrastructure": "AI infrastructure & compute",
    "vLLM": "AI infrastructure & compute",
    "llama.cpp": "AI infrastructure & compute",
    "GGUF": "AI infrastructure & compute",
    "ONNX": "AI infrastructure & compute",
    "distributed training": "AI infrastructure & compute",
    "edge inference": "AI infrastructure & compute",
    "KV cache": "AI infrastructure & compute",
    "throughput optimization": "AI infrastructure & compute",
    "model batching": "AI infrastructure & compute",
    "speculative decoding": "AI infrastructure & compute",
    # Training & fine-tuning
    "model training": "Training & fine-tuning",
    "RLHF": "Training & fine-tuning",
    "DPO": "Training & fine-tuning",
    "instruction tuning": "Training & fine-tuning",
    "dataset curation": "Training & fine-tuning",
    "synthetic data": "Training & fine-tuning",
    "pretraining": "Training & fine-tuning",
    "model distillation": "Training & fine-tuning",
    # MLOps & deployment
    "model deployment": "MLOps & deployment",
    "model monitoring": "MLOps & deployment",
    "experiment tracking": "MLOps & deployment",
    "ML pipelines": "MLOps & deployment",
    "model versioning": "MLOps & deployment",
    "data drift detection": "MLOps & deployment",
    "A/B testing for ML": "MLOps & deployment",
    "Weights & Biases": "MLOps & deployment",
    "MLflow": "MLOps & deployment",
    "feature stores": "MLOps & deployment",
    # Data & knowledge
    "data pipelines": "Data & knowledge",
    "ETL": "Data & knowledge",
    "stream processing": "Data & knowledge",
    "data lakes": "Data & knowledge",
    "data quality": "Data & knowledge",
    "Apache Spark": "Data & knowledge",
    "dbt": "Data & knowledge",
    "workflow orchestration": "Data & knowledge",
    "Kafka": "Data & knowledge",
    "Airflow": "Data & knowledge",
    # AI tools & productivity
    "AI coding tools": "AI tools & productivity",
    "workflow automation": "AI tools & productivity",
    "AI writing tools": "AI tools & productivity",
    "AI assistants": "AI tools & productivity",
    "AI search": "AI tools & productivity",
    "knowledge management": "AI tools & productivity",
    "AI for business": "AI tools & productivity",
    "Claude Code": "AI tools & productivity",
    "Cursor": "AI tools & productivity",
    "Copilot": "AI tools & productivity",
    # Creative AI
    "generative art": "Creative AI",
    "AI music": "Creative AI",
    "AI video": "Creative AI",
    "AI writing": "Creative AI",
    "creative tools": "Creative AI",
    "Midjourney": "Creative AI",
    # AI in science
    "AI drug discovery": "AI in science",
    "protein folding": "AI in science",
    "climate AI": "AI in science",
    "materials science AI": "AI in science",
    "computational biology": "AI in science",
    "scientific ML": "AI in science",
    # Robotics & embodied AI
    "robot learning": "Robotics & embodied AI",
    "robot manipulation": "Robotics & embodied AI",
    "autonomous vehicles": "Robotics & embodied AI",
    "drone AI": "Robotics & embodied AI",
    "embodied agents": "Robotics & embodied AI",
    "sim-to-real": "Robotics & embodied AI",
    # AI safety & alignment
    "interpretability": "AI safety & alignment",
    "mechanistic interpretability": "AI safety & alignment",
    "RLHF safety": "AI safety & alignment",
    "constitutional AI": "AI safety & alignment",
    "AI alignment": "AI safety & alignment",
    "alignment research": "AI safety & alignment",
    # AI policy & regulation
    "EU AI Act": "AI policy & regulation",
    "AI governance": "AI policy & regulation",
    "AI ethics": "AI policy & regulation",
    "AI standards": "AI policy & regulation",
    "responsible AI": "AI policy & regulation",
    # AI economics & society
    "AI and jobs": "AI economics & society",
    "AI productivity impact": "AI economics & society",
    "AI investment": "AI economics & society",
    "AI adoption": "AI economics & society",
    "future of work": "AI economics & society",
    # AI in business & industry
    "enterprise AI": "AI in business & industry",
    "AI ROI": "AI in business & industry",
    "AI strategy": "AI in business & industry",
    "vertical AI": "AI in business & industry",
    "AI transformation": "AI in business & industry",
    # Prompt engineering & AI UX
    "prompting techniques": "Prompt engineering & AI UX",
    "chain-of-thought": "Prompt engineering & AI UX",
    "few-shot learning": "Prompt engineering & AI UX",
    "system prompts": "Prompt engineering & AI UX",
    "prompt optimization": "Prompt engineering & AI UX",
    "structured output": "Prompt engineering & AI UX",
    "context window management": "Prompt engineering & AI UX",
    "prompt injection": "Prompt engineering & AI UX",
    # AI hardware & chips
    "NVIDIA GPUs": "AI hardware & chips",
    "custom AI chips": "AI hardware & chips",
    "TPU": "AI hardware & chips",
    "AI accelerators": "AI hardware & chips",
    # Software engineering
    "React": "Software engineering",
    "TypeScript": "Software engineering",
    "UI/UX design": "Software engineering",
    "web performance": "Software engineering",
    "CSS frameworks": "Software engineering",
    "frontend tooling": "Software engineering",
    "accessibility": "Software engineering",
    "Next.js": "Software engineering",
    "distributed systems": "Software engineering",
    "API design": "Software engineering",
    "microservices": "Software engineering",
    "scalability": "Software engineering",
    "caching strategies": "Software engineering",
    "message queues": "Software engineering",
    "database design": "Software engineering",
    "system architecture": "Software engineering",
    "Rust": "Software engineering",
    "Go": "Software engineering",
    "Python ecosystem": "Software engineering",
    "compiler design": "Software engineering",
    "WebAssembly": "Software engineering",
    "developer productivity": "Software engineering",
    "open source": "Software engineering",
    # Cybersecurity
    "vulnerability research": "Cybersecurity",
    "penetration testing": "Cybersecurity",
    "supply chain security": "Cybersecurity",
    "zero-day exploits": "Cybersecurity",
    "threat intelligence": "Cybersecurity",
    "cryptography": "Cybersecurity",
    "network security": "Cybersecurity",
    "identity management": "Cybersecurity",
    "security auditing": "Cybersecurity",
    "malware analysis": "Cybersecurity",
    "bug bounty": "Cybersecurity",
    "DevSecOps": "Cybersecurity",
    # Cloud computing
    "Kubernetes": "Cloud computing",
    "serverless": "Cloud computing",
    "AWS": "Cloud computing",
    "Google Cloud": "Cloud computing",
    "Azure": "Cloud computing",
    "infrastructure as code": "Cloud computing",
    "Terraform": "Cloud computing",
    "cloud cost optimization": "Cloud computing",
    "container orchestration": "Cloud computing",
    "service mesh": "Cloud computing",
    # Space & astronomy
    "rocket propulsion": "Space & astronomy",
    "satellite technology": "Space & astronomy",
    "space exploration": "Space & astronomy",
    "astrophysics": "Space & astronomy",
    "SpaceX": "Space & astronomy",
    # Biotech & life sciences
    "drug discovery": "Biotech & life sciences",
    "genomics": "Biotech & life sciences",
    "CRISPR": "Biotech & life sciences",
    "synthetic biology": "Biotech & life sciences",
    "clinical trials": "Biotech & life sciences",
    "digital health": "Biotech & life sciences",
    "longevity research": "Biotech & life sciences",
    # Climate & environment
    "clean energy": "Climate & environment",
    "carbon capture": "Climate & environment",
    "climate modeling": "Climate & environment",
    "green tech": "Climate & environment",
    "sustainability": "Climate & environment",
    # Startups & venture capital
    "startup fundraising": "Startups & venture capital",
    "venture capital": "Startups & venture capital",
    "Y Combinator": "Startups & venture capital",
    "product-market fit": "Startups & venture capital",
    "growth hacking": "Startups & venture capital",
    "bootstrapping": "Startups & venture capital",
    "startup operations": "Startups & venture capital",
    # Career & professional growth
    "technical interviews": "Career & professional growth",
    "engineering management": "Career & professional growth",
    "career transitions": "Career & professional growth",
    "mentorship": "Career & professional growth",
    "salary negotiation": "Career & professional growth",
    # Personal finance & investing
    "investing": "Personal finance & investing",
    "personal budgeting": "Personal finance & investing",
    "FIRE movement": "Personal finance & investing",
    "real estate investing": "Personal finance & investing",
    "tax optimization": "Personal finance & investing",
    # Economics & markets
    "macroeconomics": "Economics & markets",
    "cryptocurrency": "Economics & markets",
    "fintech": "Economics & markets",
    "financial markets": "Economics & markets",
    "central banks": "Economics & markets",
    "DeFi": "Economics & markets",
    "quantitative finance": "Economics & markets",
    # Geopolitics & international affairs
    "US-China tech": "Geopolitics & international affairs",
    "national security": "Geopolitics & international affairs",
    "trade policy": "Geopolitics & international affairs",
    "digital sovereignty": "Geopolitics & international affairs",
    "tech regulation": "Geopolitics & international affairs",
    # Health & wellness
    "mental health": "Health & wellness",
    "fitness": "Health & wellness",
    "nutrition": "Health & wellness",
    "sleep science": "Health & wellness",
    "preventive medicine": "Health & wellness",
    # Education & learning
    "online learning": "Education & learning",
    "EdTech": "Education & learning",
    "learning science": "Education & learning",
    "MOOCs": "Education & learning",
    "technical education": "Education & learning",
    # Design & creativity
    "product design": "Design & creativity",
    "typography": "Design & creativity",
    "design systems": "Design & creativity",
    "UX research": "Design & creativity",
    "visual storytelling": "Design & creativity",
    "generative design": "Design & creativity",
    # Science & research
    "physics": "Science & research",
    "neuroscience": "Science & research",
    "materials science": "Science & research",
    "mathematics": "Science & research",
    "chemistry": "Science & research",
    "scientific computing": "Science & research",
    "research methodology": "Science & research",
    "open science": "Science & research",
}
