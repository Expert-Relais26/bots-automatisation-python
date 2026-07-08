# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

This repository is a single-page Streamlit chat application ("Mon Hub d'Experts Digital") that lets a user pick one of several predefined business "expert" personas from a sidebar and chat with it. Each persona is just a system prompt sent to the OpenAI Chat Completions API. All UI copy and expert prompts are in French.

## Codebase structure

- `app.py` — the entire application: page config, the `experts` dict mapping persona names to system prompts, the sidebar selector, chat history state, and the chat loop that calls the OpenAI API.
- `requirements.txt` — `streamlit`, `openai`, `pinecone-client`. Note `pinecone-client` is a dependency but is not yet imported/used in `app.py` — likely reserved for a future retrieval/vector-search feature.

There is no test suite, linter config, CI pipeline, or build step in this repository.

## Running the app

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Configuration

The app reads the OpenAI key from Streamlit secrets (`st.secrets["OPENAI_API_KEY"]`), not from an environment variable. For local runs, create `.streamlit/secrets.toml`:

```toml
OPENAI_API_KEY = "sk-..."
```

In production this is set via the Streamlit Cloud secrets UI (per the comment in `app.py`). Never hardcode the key in `app.py`.

## Key conventions

- **Adding a new expert**: add an entry to the `experts` dict in `app.py` (key = display name shown in the sidebar selectbox, value = the system prompt used for that persona). No other wiring is needed — the selectbox and API call both read from this dict.
- **Chat state**: conversation history lives in `st.session_state.messages` as a list of `{"role", "content"}` dicts, following the OpenAI chat message format. The persona's system prompt is injected fresh on every API call (not stored in `messages`), so switching experts mid-conversation changes the system prompt without clearing prior turns.
- **Model**: currently `gpt-3.5-turbo`, set as a literal string in the `client.chat.completions.create` call — change it there if switching models.
- Commit messages and in-app text in this repo are written in French; match that convention for user-facing strings.
