# =================================================================
# DSRPTV (dsrptv.co) -- Meta Multi-Agent Coding OS
# by DSRPT.AI -- https://dsrpt.ai
# GitHub: https://github.com/DSRPT/dsrptv
# Pinokio v7 Terminal Plugin
# -----------------------------------------------------------------
# graph.py -- LangGraph Meta Multi-Agent Core
# Supervisor + Coder (Aider) + Tester + Persistent Checkpointing
# =================================================================

import os
import sys
import subprocess
import json
from typing import TypedDict, Annotated, List, Optional
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.sqlite import SqliteSaver
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage
import operator

# ----------------------------------------------------------------
# Config from environment (passed from menu.js / launch.sh)
# ----------------------------------------------------------------
OLLAMA_HOST = os.environ.get('OLLAMA_API_BASE', 'http://localhost:11434')
PRIMARY_MODEL = os.environ.get('DSRPTV_PRIMARY', 'qwen2.5-coder:32b')
EDITOR_MODEL = os.environ.get('DSRPTV_EDITOR', 'qwen2.5-coder:14b')
CWD = os.environ.get('DSRPTV_CWD', os.getcwd())
MEMORY_DB = os.path.join(os.path.expanduser('~'), '.dsrptv_memory.db')

print(f"\n[DSRPTV] LangGraph Meta Multi-Agent Core")
print(f"[DSRPTV] Ollama: {OLLAMA_HOST}")
print(f"[DSRPTV] Architect: {PRIMARY_MODEL} | Editor: {EDITOR_MODEL}")
print(f"[DSRPTV] Working dir: {CWD}")
print(f"[DSRPTV] Memory DB: {MEMORY_DB}\n")


# ----------------------------------------------------------------
# State Definition
# ----------------------------------------------------------------
class DSRPTVState(TypedDict):
    messages: Annotated[List[BaseMessage], operator.add]
    task: str
    plan: str
    plan_score: float
    code_applied: bool
    test_result: str
    test_passed: bool
    iteration: int
    max_iterations: int


# ----------------------------------------------------------------
# LLM Clients
# ----------------------------------------------------------------
def make_llm(model: str) -> ChatOllama:
    return ChatOllama(
        model=model,
        base_url=OLLAMA_HOST,
        temperature=0.1,
        streaming=True,
    )

supervisor_llm = make_llm(PRIMARY_MODEL)
coder_llm = make_llm(PRIMARY_MODEL)
tester_llm = make_llm(EDITOR_MODEL)


# ----------------------------------------------------------------
# Node: Supervisor
# Plans the task, scores the plan, routes to coder or re-plans
# ----------------------------------------------------------------
def supervisor_node(state: DSRPTVState) -> dict:
    print("\n[SUPERVISOR] Planning task...")
    task = state.get('task', '')
    iteration = state.get('iteration', 0)
    prev_test = state.get('test_result', '')

    system_prompt = (
        "You are DSRPTV Supervisor -- an elite software architect built by DSRPT.AI (https://dsrpt.ai). "
        "Your role: decompose the user's task into a precise, actionable implementation plan. "
        "Output your plan as numbered steps. At the end, output exactly: SCORE: <0-100>. "
        "Be precise, proactive, and use engineering best practices."
    )

    user_msg = f"Task: {task}"
    if prev_test and 'FAIL' in prev_test.upper():
        user_msg += f"\n\nPrevious test result (FAILED -- revise plan):\n{prev_test}"

    response = supervisor_llm.invoke([
        HumanMessage(content=f"{system_prompt}\n\n{user_msg}")
    ])

    plan_text = response.content
    print(f"[SUPERVISOR] Plan:\n{plan_text[:500]}...\n")

    # Extract score
    score = 75.0
    for line in plan_text.split('\n'):
        if 'SCORE:' in line:
            try:
                score = float(line.split('SCORE:')[1].strip().split()[0])
            except Exception:
                pass

    return {
        'messages': [AIMessage(content=f"[SUPERVISOR]\n{plan_text}")],
        'plan': plan_text,
        'plan_score': score,
        'iteration': iteration + 1,
    }


# ----------------------------------------------------------------
# Node: Coder (calls Aider as a subprocess)
# ----------------------------------------------------------------
def coder_node(state: DSRPTVState) -> dict:
    print("\n[CODER] Running Aider to implement plan...")
    plan = state.get('plan', '')
    task = state.get('task', '')

    aider_msg = (
        f"You are DSRPTV Coder. Implement the following plan precisely.\n\n"
        f"ORIGINAL TASK: {task}\n\n"
        f"ARCHITECT PLAN:\n{plan}\n\n"
        f"Implement all steps. Use best practices."
    )

    cmd = [
        'aider',
        '--model', f'ollama/{PRIMARY_MODEL}',
        '--editor-model', f'ollama/{EDITOR_MODEL}',
        '--architect',
        '--auto-accept-architect',
        '--yes',
        '--stream',
        '--map',
        '--message', aider_msg,
    ]

    env = {**os.environ, 'OLLAMA_API_BASE': OLLAMA_HOST}

    try:
        result = subprocess.run(
            cmd,
            cwd=CWD,
            env=env,
            timeout=300,  # 5 min timeout per coding step
        )
        applied = result.returncode == 0
    except subprocess.TimeoutExpired:
        print("[CODER] Timeout -- partial implementation may have been applied.")
        applied = True
    except FileNotFoundError:
        print("[CODER] Aider not found. Install with: pip install aider-chat")
        applied = False

    return {
        'messages': [AIMessage(content=f"[CODER] Applied={applied}")],
        'code_applied': applied,
    }


# ----------------------------------------------------------------
# Node: Tester
# Runs pytest + ruff, returns structured result
# ----------------------------------------------------------------
def tester_node(state: DSRPTVState) -> dict:
    print("\n[TESTER] Running tests and lint...")

    results = []
    passed = True

    # Run pytest if available
    try:
        r = subprocess.run(
            ['pytest', '--tb=short', '-q'],
            cwd=CWD,
            capture_output=True,
            text=True,
            timeout=120,
        )
        results.append(f"PYTEST:\n{r.stdout[-1000:]}\n{r.stderr[-500:]}")
        if r.returncode != 0:
            passed = False
    except FileNotFoundError:
        results.append("PYTEST: not installed (skipped)")
    except subprocess.TimeoutExpired:
        results.append("PYTEST: timeout")
        passed = False

    # Run ruff lint if available
    try:
        r = subprocess.run(
            ['ruff', 'check', '.', '--fix'],
            cwd=CWD,
            capture_output=True,
            text=True,
            timeout=30,
        )
        results.append(f"RUFF:\n{r.stdout[-500:]}")
    except FileNotFoundError:
        results.append("RUFF: not installed (skipped)")
    except subprocess.TimeoutExpired:
        results.append("RUFF: timeout")

    result_text = '\n'.join(results)
    status = 'PASS' if passed else 'FAIL'
    print(f"[TESTER] Result: {status}")

    return {
        'messages': [AIMessage(content=f"[TESTER] {status}\n{result_text}")],
        'test_result': result_text,
        'test_passed': passed,
    }


# ----------------------------------------------------------------
# Routing Logic
# ----------------------------------------------------------------
def route_supervisor(state: DSRPTVState) -> str:
    score = state.get('plan_score', 0)
    iteration = state.get('iteration', 0)
    max_iter = state.get('max_iterations', 5)
    if score >= 60 and iteration <= max_iter:
        return 'coder'
    elif iteration > max_iter:
        print("[ROUTER] Max iterations reached -- ending session.")
        return END
    else:
        print(f"[ROUTER] Plan score {score} too low -- re-planning...")
        return 'supervisor'


def route_tester(state: DSRPTVState) -> str:
    passed = state.get('test_passed', False)
    iteration = state.get('iteration', 0)
    max_iter = state.get('max_iterations', 5)
    if passed:
        print("[ROUTER] Tests passed! Task complete.")
        return END
    elif iteration >= max_iter:
        print("[ROUTER] Max iterations reached -- ending.")
        return END
    else:
        print("[ROUTER] Tests failed -- sending back to supervisor for revision.")
        return 'supervisor'


# ----------------------------------------------------------------
# Build Graph
# ----------------------------------------------------------------
def build_graph():
    graph = StateGraph(DSRPTVState)

    graph.add_node('supervisor', supervisor_node)
    graph.add_node('coder', coder_node)
    graph.add_node('tester', tester_node)

    graph.add_edge(START, 'supervisor')
    graph.add_conditional_edges('supervisor', route_supervisor, {'coder': 'coder', END: END, 'supervisor': 'supervisor'})
    graph.add_edge('coder', 'tester')
    graph.add_conditional_edges('tester', route_tester, {END: END, 'supervisor': 'supervisor'})

    return graph


# ----------------------------------------------------------------
# Main Entry Point
# ----------------------------------------------------------------
def main():
    # Get task from CLI args or prompt
    if len(sys.argv) > 1:
        task = ' '.join(sys.argv[1:])
    else:
        task = input("\n[DSRPTV] Enter your task for the meta multi-agent system:\n> ").strip()

    if not task:
        print("[DSRPTV] No task provided. Exiting.")
        sys.exit(0)

    print(f"\n[DSRPTV] Starting Meta Multi-Agent Loop")
    print(f"[DSRPTV] Task: {task}")
    print("=" * 60)

    graph = build_graph()

    # Persistent SQLite checkpointing (durable -- survives restarts)
    with SqliteSaver.from_conn_string(MEMORY_DB) as memory:
        app = graph.compile(checkpointer=memory)

        initial_state: DSRPTVState = {
            'messages': [HumanMessage(content=task)],
            'task': task,
            'plan': '',
            'plan_score': 0.0,
            'code_applied': False,
            'test_result': '',
            'test_passed': False,
            'iteration': 0,
            'max_iterations': 5,
        }

        config = {'configurable': {'thread_id': 'dsrptv-session-1'}}

        print("\n[DSRPTV] Running graph...\n")
        for chunk in app.stream(initial_state, config):
            for node_name, node_output in chunk.items():
                msgs = node_output.get('messages', [])
                for msg in msgs:
                    if hasattr(msg, 'content') and msg.content:
                        print(f"\n{'=' * 40}")
                        print(msg.content[:800])

    print("\n[DSRPTV] Meta Multi-Agent session complete.")
    print(f"[DSRPTV] Memory saved to: {MEMORY_DB}")


if __name__ == '__main__':
    main()
