---
name: Sergei Khorev
whoami: capital-markets technologist / physicist — pricing engines to quantum circuits
role: Capital markets technologist — physicist by training. Twenty-plus years moving between pricing engines, risk systems, and the odd compiler bug, with a quantum computing habit that keeps growing modules.
badges: Calypso · FO / BO / Technical certified | Basics of Quantum Information | Fundamentals of Quantum Algorithms | MSc Hons, Theoretical Physics | 20+ years | CSPO (lapsed)
github: https://github.com/khorser
linkedin: https://www.linkedin.com/in/sergeykhorev/
email: sergey.khorev@gmail.com
location: Serbia · remote or hybrid
---

## Core Expertise: Calypso & Capital Markets Risk {#expertise}

Certified across all three Calypso tracks — Front Office, Back Office, Technical. Principal-level implementation consultant delivering greenfield deployments, upgrades, and reconfigurations for banks and hedge funds globally.

- Deep hands-on work in trade pricing, P&L, market risk, VaR, and xVA/CVA.
- Independent CVA validation: built a Python/pandas/QuantLib tool from scratch that surfaced a discrepancy no client-side review had caught.
- Also worked with Murex MX.3, Kondor+, NumeriX, and Scila Risk — enough exposure to know where Calypso's model assumptions diverge from the rest of the field.

## Risk Management & Regulatory {#risk}

Led Basel II/III credit risk and regulatory market risk implementations — CEM, S-CVA, RWA — as risk system owner at a major sell-side bank. Delivered limits management, P&L control, and VaR frameworks as risk management product owner for a trading firm moving from crypto-only into traditional markets.

Worked directly with CROs and trading desks to turn risk requirements into working systems — the translation layer between what a regulator asks for and what a system can actually compute.

## Technical Depth {#technical}

Twenty-plus years of commercial development — deeper than a typical consultant's toolkit. Comfortable reading a system's source when there isn't a spec, and comfortable when there isn't source either.

### Languages
C++ | Java | Python — pandas, NumPy, QuantLib | Rust | Haskell | PL/SQL | Scheme/Lisp | Prolog | Perl | Lua | VBA

### Databases
Oracle | MS SQL | Sybase | PostgreSQL

### Platforms
Linux & Unix-likes (FreeBSD, Solaris) | macOS | Windows/Cygwin

### Low-level
Memory debugging | Compiler bugs | OS internals | Java decompilation & reverse engineering without source access

## Projects {#projects}

```project
name: qstudy — Qiskit study toolkit
tag: public
link: https://github.com/khorser/qstudy
linktext: github.com/khorser/qstudy
tags: Qiskit, Python, Ollama, qwen2.5
```
A portfolio of interconnected Python modules for studying quantum algorithms from the inside out. Built around **CircuitSlicer**, a barrier-delimited circuit inspection tool that shows statevectors, density matrices, purity, entanglement, and unitaries at every slice — plus implementations of Deutsch-Jozsa, Bernstein-Vazirani, Simon's algorithm (with GF(2) postprocessing), and Grover's with geometric visualization.

Extended with seven modules layered on top without modifying the core: resource estimation, grounded local-LLM narration, an AI-enhanced widget subclass, a duck-typed Ollama adapter, a headless simulation path, and a multi-step tool-use agent for circuit analysis.

```project
name: hasquant
tag: public
link: https://github.com/khorser/hasquant
linktext: github.com/khorser/hasquant
tags: Haskell, C++, FFI, QuantLib
```
A Haskell/C++ FFI binding to QuantLib. Conceptual architecture is mine; boilerplate FFI generation is delegated to an AI coding agent (Aider, running against a local Ollama model) working inside that architecture rather than improvising its own.

```project
name: Local semantic search agent
tag: private
tags: SQLite FTS5, Embeddings, Ollama
```
A retrieval agent over a large vendor documentation corpus, running entirely locally: SQLite FTS5 for lexical search combined with `nomic-embed-text` embeddings for semantic matching.

```project
name: Serbian pronunciation trainer
tag: side project
tags: whisper.cpp, Piper TTS, Ollama
```
A local language-practice loop built from parts that were never meant to work together: `whisper.cpp` for speech recognition, Ollama for feedback, and Piper TTS for spoken correction.

## AI & Quantum Computing {#ai-quantum}

Quantum computing is a side interest with the same habit behind it as everything else here: go deep on an unfamiliar domain until it's possible to build with it, not just talk about it.

- Practical judgment on when an agentic workflow earns its complexity, versus when a deterministic script or plain code does the job better.
- Explicit choices about which local models are trustworthy for grounded, non-reasoning narration tasks versus which are worth reserving for agentic planning.
- Comfortable at every layer of a local AI stack: model choice, embeddings, retrieval, tool-calling agents, TTS/STT pipelines — not just the prompt.

## Delivery & Leadership {#leadership}

I can read code even when I'm not the one shipping it — it's the fastest way to know what a system can actually do, independent of what anyone says it does. Sole functional analyst on some projects, mentored developers and analysts on others, ran internal knowledge bases, and acted as client advocate in vendor relationships when the vendor and the client stopped speaking the same language.

CSPO (lapsed), fluent with Jira/Confluence, and comfortable running with distributed teams across time zones.

## What I'm looking for {#contact}

Remote or hybrid capital markets tech roles — Calypso implementation, risk system ownership, xVA/CVA, front-to-back trading system integration, or roles at the intersection of quantitative finance and AI/quantum computing.
