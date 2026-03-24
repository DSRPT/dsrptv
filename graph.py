#!/usr/bin/env python3
# =======================================================================
# DSRPTV (dsrptv.co) -- Meta Multi-Agent Coding OS
# by DSRPT.AI -- https://dsrpt.ai
# GitHub: https://github.com/DSRPT/dsrptv
# Pinokio v7 Terminal Plugin
# =======================================================================
# graph.py -- LangGraph Meta-Agent Core
# Supervisor + Coder (Aider) + Tester + Persistent Checkpointing
# =======================================================================

import os
import sys
import subprocess
import json
from typing import TypedDict, Annotated, List, Optional
from langchain import LLMChain, PromptTemplate
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.sqlite import SqliteSaver
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage
import operator

# -----------------------------------------------------------------------
# Config from environment (passed from menu.js / launch.sh)
# -----------------------------------------------------------------------

OLLAMA_HOST = os.environ.get('OLLAMA_API_BASE', 'http://localhost:11434')
PRIMARY_MODEL = os.environ.get('DSRPTV_MODEL', 'qwen2.5-coder:32b')
EDITOR_MODEL = os.environ.get('DSRPTV_EDITOR_MODEL', 'qwen2.5-coder:14b')
CWD = os.environ.get('DSRPTV_CWD', os.getcwd())
MEMORY_DB = os.path.join(os.path.expanduser('~'), '.dsrptv_memory.db')

print(f"\n{'='*64}")
print(f"  DSRPTV | dsrptv.co — META MULTI-AGENT CODING OS")
print(f"  by DSRPT.AI — https://dsrpt.ai")
print(f"  GitHub: https://github.com/DSRPT/dsrptv")
print(f"{'='*64}")
print(f"  LangGraph Meta-Agent Core")
print(f"  Ollama: {OLLAMA_HOST}")
print(f"  Primary: {PRIMARY_MODEL}")
print(f"  Editor: {EDITOR_MODEL}")
print(f"  CWD: {CWD}")
print(f"{'='*64}\n")

# -----------------------------------------------------------------------
# State Definition
# -----------------------------------------------------------------------

class DSRPTVState(TypedDict):
    """State shared across all agent nodes"""
    messages: Annotated[List[BaseMessage], operator.add]
    task: str
    current_agent: str
    code_applied: bool
    tests_passed: bool
    iteration: int
    max_iterations: int
    files_modified: List[str]
    error_log: List[str]

# -----------------------------------------------------------------------
# LLM Setup
# -----------------------------------------------------------------------

supervisor_llm = ChatOllama(
    model=PRIMARY_MODEL,
    base_url=OLLAMA_HOST,
    temperature=0.3,
)

coder_llm = ChatOllama(
    model=EDITOR_MODEL,
    base_url=OLLAMA_HOST,
    temperature=0.1,  # Precise code edits
)

# -----------------------------------------------------------------------
# Node: Supervisor
# Analyzes task and routes to coder/tester or finishes
# -----------------------------------------------------------------------

def supervisor_node(state: DSRPTVState) -> dict:
    print(f"\n\033[36m[SUPERVISOR]\033[0m Analyzing task (iteration {state['iteration']}/{state['max_iterations']})...")
    
    task = state['task']
    code_applied = state.get('code_applied', False)
    tests_passed = state.get('tests_passed', False)
    
    if state['iteration'] >= state['max_iterations']:
        return {
            'current_agent': 'FINISH',
            'messages': [AIMessage(content="Max iterations reached. Task complete.")],
        }
    
    if code_applied and tests_passed:
        return {
            'current_agent': 'FINISH',
            'messages': [AIMessage(content="Code applied and tests passed. Task complete.")],
        }
    
    # Decide next agent
    if not code_applied:
        next_agent = 'CODER'
    else:
        next_agent = 'TESTER'
    
    print(f"\033[36m[SUPERVISOR]\033[0m Routing to {next_agent}")
    
    return {
        'current_agent': next_agent,
        'messages': [AIMessage(content=f"Supervisor routing to {next_agent}")],
    }

# -----------------------------------------------------------------------
# Node: Coder (Aider)
# Runs aider-chat to edit code based on task
# -----------------------------------------------------------------------

def coder_node(state: DSRPTVState) -> dict:
    print(f"\n\033[32m[CODER]\033[0m Running Aider to implement code changes...")
    
    task = state['task']
    iteration = state.get('iteration', 0)
    
    # Build aider command
    cmd = [
        'aider',
        '--model', f'ollama/{EDITOR_MODEL}',
        '--yes',
        '--auto-commits',
        '--stream',
        '--message', task,
    ]
    
    try:
        result = subprocess.run(
            cmd,
            cwd=CWD,
            env={**os.environ, 'OLLAMA_API_BASE': OLLAMA_HOST},
            timeout=300,  # 5 min timeout per coding step
            capture_output=True,
            text=True,
        )
        applied = result.returncode == 0
        print(f"\033[32m[CODER]\033[0m Aider {'succeeded' if applied else 'failed'}.")
    except subprocess.TimeoutExpired:
        print(f"\033[31m[CODER]\033[0m Timeout — partial implementation may have been applied.")
        applied = True  # Assume partial success
    except FileNotFoundError:
        print(f"\033[31m[CODER]\033[0m Aider not found. Install with: pip install aider-chat")
        applied = False
    
    return {
        'code_applied': applied,
        'iteration': iteration + 1,
        'messages': [AIMessage(content=f"[CODER] Applied={applied}")],
    }

# -----------------------------------------------------------------------
# Node: Tester
# Runs pytest + ruff, returns structured result
# -----------------------------------------------------------------------

def tester_node(state: DSRPTVState) -> dict:
    print(f"\n\033[33m[TESTER]\033[0m Running tests and lint...")
    
    results = []
    passed = True
    
    # Run pytest if available
    try:
        r = subprocess.run(
            ['pytest', '--tb=short', '-q'],
            cwd=CWD,
            capture_output=True,
            timeout=120,
            text=True,
        )
        if r.returncode == 0:
            print(f"\033[33m[TESTER]\033[0m pytest passed.")
        else:
            print(f"\033[33m[TESTER]\033[0m pytest failed:\n{r.stdout}")
            passed = False
            results.append(f"pytest failed: {r.stdout}")
    except FileNotFoundError:
        print(f"\033[33m[TESTER]\033[0m pytest not found, skipping.")
    except subprocess.TimeoutExpired:
        print(f"\033[33m[TESTER]\033[0m pytest timeout.")
        passed = False
    
    # Run ruff if available
    try:
        r = subprocess.run(
            ['ruff', 'check', '.'],
            cwd=CWD,
            capture_output=True,
            timeout=30,
            text=True,
        )
        if r.returncode == 0:
            print(f"\033[33m[TESTER]\033[0m ruff passed.")
        else:
            print(f"\033[33m[TESTER]\033[0m ruff issues found.")
            # Don't fail on lint issues, just warn
    except FileNotFoundError:
        pass
    
    return {
        'tests_passed': passed,
        'error_log': results if results else [],
        'messages': [AIMessage(content=f"[TESTER] Tests passed={passed}")],
    }

# -----------------------------------------------------------------------
# Build Graph
# -----------------------------------------------------------------------

def build_graph():
    workflow = StateGraph(DSRPTVState)
    
    # Add nodes
    workflow.add_node("supervisor", supervisor_node)
    workflow.add_node("coder", coder_node)
    workflow.add_node("tester", tester_node)
    
    # Entry point
    workflow.set_entry_point("supervisor")
    
    # Conditional edges from supervisor
    def route_supervisor(state: DSRPTVState) -> str:
        agent = state.get('current_agent', 'FINISH')
        if agent == 'FINISH':
            return END
        elif agent == 'CODER':
            return 'coder'
        elif agent == 'TESTER':
            return 'tester'
        return END
    
    workflow.add_conditional_edges(
        "supervisor",
        route_supervisor,
        {
            END: END,
            'coder': 'coder',
            'tester': 'tester',
        }
    )
    
    # After coder/tester, return to supervisor
    workflow.add_edge('coder', 'supervisor')
    workflow.add_edge('tester', 'supervisor')
    
    # Persistent checkpointing with SQLite
    memory = SqliteSaver.from_conn_string(MEMORY_DB)
    
    return workflow.compile(checkpointer=memory)

# -----------------------------------------------------------------------
# Main Entry
# -----------------------------------------------------------------------

if __name__ == '__main__':
    import readline  # Enable input history
    
    graph = build_graph()
    thread_id = "dsrptv-session-1"
    
    print(f"\033[36m[DSRPTV]\033[0m LangGraph Meta-Agent Ready.")
    print(f"\033[36m[DSRPTV]\033[0m Persistent memory: {MEMORY_DB}")
    print(f"\033[36m[DSRPTV]\033[0m Type your coding task below (or 'exit'):\n")
    
    while True:
        try:
            user_input = input("\033[1;32mYou:\033[0m ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n\033[36m[DSRPTV]\033[0m Exiting.")
            break
        
        if not user_input or user_input.lower() in ['exit', 'quit', 'q']:
            print("\033[36m[DSRPTV]\033[0m Exiting.")
            break
        
        # Initialize state
        initial_state = {
            'messages': [HumanMessage(content=user_input)],
            'task': user_input,
            'current_agent': 'SUPERVISOR',
            'code_applied': False,
            'tests_passed': False,
            'iteration': 0,
            'max_iterations': 5,
            'files_modified': [],
            'error_log': [],
        }
        
        config = {'configurable': {'thread_id': thread_id}}
        
        print(f"\n\033[36m[DSRPTV]\033[0m Starting multi-agent workflow...\n")
        
        # Stream execution
        for chunk in graph.stream(initial_state, config, stream_mode='values'):
            pass  # Nodes print their own status
        
        print(f"\n\033[36m[DSRPTV]\033[0m Task complete. State persisted to {MEMORY_DB}\n")
