# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project overview

"Mon Hub d'Experts Digital" is a single-page Streamlit chat app that lets a user pick one of 10 business "expert" personas and chat with it via the OpenAI API. The entire application lives in `app.py`; there is no package structure, no tests, and no CI.

## Running the app

```bash
pip install -r requirements.txt
streamlit run app.py
```

The app requires an `OPENAI_API_KEY` in Streamlit secrets (`.streamlit/secrets.toml` locally, or the Streamlit Cloud secrets UI in production):

```toml
OPENAI_API_KEY = "sk-..."
```

There are no lint, test, or build commands configured in this repo.

## Architecture

- `app.py` is a monolithic Streamlit script structured top-to-bottom as: page config → OpenAI client init → `experts` dict → sidebar expert selector → chat history render loop → chat input handler that calls `client.chat.completions.create`.
- `experts` (a `dict[str, str]`) maps a display name to the system prompt used for that persona. The selected expert's prompt is injected as the `system` message on every request; adding a new expert means adding one entry to this dict — no other code changes are needed.
- Conversation state is kept in `st.session_state.messages` (list of `{"role", "content"}` dicts) and persists only for the current browser session (Streamlit's per-session state, not a database).
- Model is currently hardcoded to `gpt-3.5-turbo` in the `chat.completions.create` call (commit history shows this has been changed before, e.g. to `gpt-4o-mini` — check before assuming it's fixed).
- `pinecone-client` is listed in `requirements.txt` but not yet imported/used in `app.py` — likely groundwork for future retrieval-augmented (vector search) functionality.

## Conventions

- Comments and UI copy are in French; keep new comments/UI text consistent with that unless told otherwise.
- Deployment target is Streamlit Cloud (per the comment in `app.py` about configuring secrets there).

## n8n/ directory

`n8n/post-call-agent.json` is an importable N8N workflow export (unrelated to the Streamlit app's runtime) implementing a post-call automation: Fireflies transcript → OpenRouter-generated follow-up email drafted in Gmail → coaching recap posted to Slack. See `n8n/README.md` for import steps and required credentials. No API keys are stored in this repo — credentials are attached inside N8N after import.
