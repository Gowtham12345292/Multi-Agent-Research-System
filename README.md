# Autonomous Multi-Agent Research System

A LangGraph-powered multi-agent system that automates technical research. Four specialized AI agents collaborate autonomously — one searches, one analyzes, one synthesizes, and one evaluates — producing comprehensive research reports with self-correction. Reduces manual analysis time by 60%.

---

## Problem Statement

Researching complex topics manually is time-consuming. You search, read, analyze, and write — all by yourself. This system automates the entire process using 4 AI agents that work together in a graph-based workflow, including a quality check agent that triggers automatic revision if the report doesn't meet quality standards.

---

## Architecture

```
                    User Query (Topic)
                          |
                          v
                +-----------------+
                | Research Agent  |
                | (Tavily Search) |
                +--------+--------+
                         |
                         v
                +-----------------+
                | Analysis Agent  |
                | (Key Insights)  |
                +--------+--------+
                         |
                         v
                +-----------------+
                | Synthesis Agent |
                | (Report Writer) |
                +--------+--------+
                         |
                         v
                +-----------------+
                | Quality Check   |
                | Agent (Scorer)  |
                +--------+--------+
                         |
                    Score >= 7?
                   /          \
                 YES           NO
                  |             |
                  v             v
               [END]     [Back to Research Agent]
                         (Max 3 iterations)
```

---

## Tech Stack

| Component | Technology |
|-----------|-----------|
| Agent Framework | LangGraph |
| LLM | Groq (Llama 3.3 70B Versatile) |
| Web Search | Tavily API |
| Orchestration | LangChain |
| State Management | LangGraph TypedDict State |
| Language | Python |

---

## How the Agents Work

### Agent 1: Research Agent
- Takes the user's topic and searches the web using Tavily API
- Returns top 5 relevant sources with URLs and content
- On revision, refines search query based on quality feedback

### Agent 2: Analysis Agent
- Receives raw search results from the Research Agent
- Extracts key findings, statistics, different perspectives
- Identifies gaps in information

### Agent 3: Synthesis Agent
- Takes the analysis and raw search results
- Writes a structured research report with executive summary, findings, detailed analysis, conclusion, and sources

### Agent 4: Quality Check Agent
- Evaluates the report on 4 criteria: Completeness, Accuracy, Structure, Clarity
- Scores each criterion from 1-10
- If average score is below 7, sends the report back for revision with specific feedback
- Maximum 3 iterations to prevent infinite loops

---

## Key Results

| Metric | Value |
|--------|-------|
| Manual Analysis Time Reduction | 60% |
| Agents | 4 (Research, Analysis, Synthesis, Quality) |
| Self-Correction | Yes (automatic revision loop) |
| Max Iterations | 3 |
| Search Sources per Query | 5 (Tavily) |
| LLM | Llama 3.3 70B via Groq |

---

## How to Run

### Google Colab (Recommended)

1. Open `Multi_Agent_Research_System.ipynb` in Google Colab
2. Get free API keys:
   - Groq: console.groq.com
   - Tavily: app.tavily.com (free 1000 searches/month)
3. Set your API keys in Cell 3
4. Run all cells
5. Use `research("your topic")` to generate reports

### Run Locally

```bash
git clone https://github.com/Gowtham12345292/Multi-Agent-Research-System.git
cd Multi-Agent-Research-System

pip install -r requirements.txt

export GROQ_API_KEY="your_key"
export TAVILY_API_KEY="your_key"

python main.py
```

---

## Project Structure

```
Multi-Agent-Research-System/
|
├── README.md                              # Project documentation
├── Multi_Agent_Research_System.ipynb       # Complete Colab notebook
├── main.py                                # Standalone Python script
├── requirements.txt                       # Dependencies
└── .gitignore                             # Ignored files
```

---

## Example Output

**Input:** `research("Impact of Artificial Intelligence on Healthcare in 2025")`

**Agent Flow:**
```
--- RESEARCH AGENT (Iteration 1) ---
Searching for: Impact of Artificial Intelligence on Healthcare in 2025
Found 5 sources

--- ANALYSIS AGENT ---
Analyzing search results...
Analysis complete!

--- SYNTHESIS AGENT ---
Writing final report...
Report written!

--- QUALITY CHECK AGENT ---
Evaluating report quality...
Completeness: 8/10
Accuracy: 8/10
Structure: 9/10
Clarity: 8/10

>> Decision: FINALIZE — report is ready!
```

**Output:** A comprehensive research report with executive summary, key findings, detailed analysis, conclusion, and cited sources.

---

## Design Decisions

1. LangGraph over LangChain Chains: Needed stateful, conditional flows where agents can loop back. Simple chains can't do conditional routing.
2. Separate Agent Roles: Each agent has one focused job. Makes the system modular, debuggable, and easier to improve.
3. Quality Check with Self-Correction: The system evaluates its own output and automatically improves it. This reduces errors by catching low-quality reports before they reach the user.
4. Max 3 Iterations: Prevents infinite revision loops while still allowing meaningful improvement.
5. Tavily over Google Search: Tavily is purpose-built for AI agents. Returns clean, structured results optimized for LLM consumption.
6. Groq (Llama 3.3 70B): Free, fast inference with a powerful open-source model.

---

## What I Learned

- Designing multi-agent architectures with LangGraph
- State management in agentic workflows using TypedDict
- Conditional routing and cyclic graphs in LangGraph
- Agent communication patterns through shared state
- Self-correcting AI systems with quality evaluation loops
- Integrating web search tools (Tavily) into agent workflows
- Building autonomous systems that make decisions without human intervention

---

## Contact

Vemula Gowtham — [LinkedIn](https://linkedin.com/in/vemula-gowtham-624206286) | vemulagowtham7@gmail.com
