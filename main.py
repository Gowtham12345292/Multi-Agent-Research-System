"""
Autonomous Multi-Agent Research System
Built with LangGraph, Groq (Llama 3.3), and Tavily Search
Author: Vemula Gowtham
"""

import os
from typing import TypedDict
from langgraph.graph import StateGraph, END
from langchain_groq import ChatGroq
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.messages import HumanMessage


# ============================================================
# Configuration
# ============================================================

os.environ["GROQ_API_KEY"] = os.environ.get("GROQ_API_KEY", "YOUR_GROQ_KEY")
os.environ["TAVILY_API_KEY"] = os.environ.get("TAVILY_API_KEY", "YOUR_TAVILY_KEY")

llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.3)
search_tool = TavilySearchResults(max_results=5)


# ============================================================
# State Definition
# ============================================================

class ResearchState(TypedDict):
    topic: str
    search_results: str
    analysis: str
    final_report: str
    revision_needed: bool
    revision_feedback: str
    iteration: int


# ============================================================
# Agent 1: Research Agent
# ============================================================

def research_agent(state: ResearchState) -> ResearchState:
    """Searches the web for information on the topic."""

    topic = state["topic"]
    iteration = state.get("iteration", 0)

    print(f"\n--- RESEARCH AGENT (Iteration {iteration + 1}) ---")

    if state.get("revision_needed") and state.get("revision_feedback"):
        search_query = f"{topic} {state['revision_feedback']}"
    else:
        search_query = topic

    results = search_tool.invoke(search_query)

    formatted = ""
    for i, result in enumerate(results, 1):
        formatted += f"\nSource {i}: {result.get('url', 'N/A')}\n"
        formatted += f"Content: {result.get('content', 'N/A')}\n"
        formatted += "-" * 40

    print(f"Found {len(results)} sources")

    return {**state, "search_results": formatted, "iteration": iteration + 1}


# ============================================================
# Agent 2: Analysis Agent
# ============================================================

def analysis_agent(state: ResearchState) -> ResearchState:
    """Analyzes search results and extracts key insights."""

    print(f"\n--- ANALYSIS AGENT ---")

    prompt = f"""Analyze the following search results on: "{state['topic']}"

Search Results:
{state['search_results']}

Provide:
1. Key Findings (bullet points)
2. Important Statistics or Data
3. Different Perspectives
4. Gaps in Information"""

    response = llm.invoke([HumanMessage(content=prompt)])
    print("Analysis complete!")

    return {**state, "analysis": response.content}


# ============================================================
# Agent 3: Synthesis Agent
# ============================================================

def synthesis_agent(state: ResearchState) -> ResearchState:
    """Synthesizes analysis into a final report."""

    print(f"\n--- SYNTHESIS AGENT ---")

    prompt = f"""Write a comprehensive research report on: "{state['topic']}"

Analysis:
{state['analysis']}

Search Results:
{state['search_results']}

Structure:
1. Executive Summary
2. Introduction
3. Key Findings
4. Detailed Analysis
5. Conclusion
6. Sources"""

    response = llm.invoke([HumanMessage(content=prompt)])
    print("Report written!")

    return {**state, "final_report": response.content}


# ============================================================
# Agent 4: Quality Check Agent
# ============================================================

def quality_check_agent(state: ResearchState) -> ResearchState:
    """Evaluates report quality and decides if revision is needed."""

    print(f"\n--- QUALITY CHECK AGENT ---")

    prompt = f"""Evaluate this research report on: "{state['topic']}"

Report:
{state['final_report']}

Rate (1-10): Completeness, Accuracy, Structure, Clarity.

If average < 7: REVISION_NEEDED: YES and give FEEDBACK.
If average >= 7: REVISION_NEEDED: NO"""

    response = llm.invoke([HumanMessage(content=prompt)])
    evaluation = response.content

    revision_needed = "REVISION_NEEDED: YES" in evaluation.upper()

    if state.get("iteration", 0) >= 3:
        revision_needed = False
        print("Max iterations reached. Finalizing.")

    feedback = ""
    if "FEEDBACK:" in evaluation:
        feedback = evaluation.split("FEEDBACK:")[-1].strip()

    return {**state, "revision_needed": revision_needed, "revision_feedback": feedback}


# ============================================================
# Router
# ============================================================

def should_revise(state: ResearchState) -> str:
    if state.get("revision_needed", False):
        print(">> Decision: REVISE")
        return "revise"
    print(">> Decision: FINALIZE")
    return "finalize"


# ============================================================
# Build Graph
# ============================================================

workflow = StateGraph(ResearchState)

workflow.add_node("researcher", research_agent)
workflow.add_node("analyzer", analysis_agent)
workflow.add_node("synthesizer", synthesis_agent)
workflow.add_node("quality_checker", quality_check_agent)

workflow.set_entry_point("researcher")
workflow.add_edge("researcher", "analyzer")
workflow.add_edge("analyzer", "synthesizer")
workflow.add_edge("synthesizer", "quality_checker")

workflow.add_conditional_edges(
    "quality_checker",
    should_revise,
    {"revise": "researcher", "finalize": END}
)

app = workflow.compile()


# ============================================================
# Run
# ============================================================

def research(topic: str):
    """Run the multi-agent research system."""

    print("=" * 60)
    print(f"  MULTI-AGENT RESEARCH SYSTEM")
    print(f"  Topic: {topic}")
    print("=" * 60)

    result = app.invoke({
        "topic": topic,
        "search_results": "",
        "analysis": "",
        "final_report": "",
        "revision_needed": False,
        "revision_feedback": "",
        "iteration": 0
    })

    print("\n" + "=" * 60)
    print("  FINAL REPORT")
    print("=" * 60)
    print(result["final_report"])
    print(f"\nIterations: {result['iteration']}")

    return result


if __name__ == "__main__":
    research("Impact of Artificial Intelligence on Healthcare in 2025")
