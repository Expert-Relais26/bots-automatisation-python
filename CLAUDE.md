# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project overview

A single-page Streamlit chat app ("Mon Hub d'Experts Digital") that lets a user pick one of several
predefined "expert" personas from a sidebar and chat with it via the OpenAI API. The entire
application currently lives in `app.py`.

## Commands

```bash
pip install -r requirements.txt   # install dependencies
streamlit run app.py              # run the app locally (http://localhost:8501)
```

There is no build step, linter, or test suite in this repository at present.

## Configuration / secrets

- The OpenAI API key is read via `st.secrets["OPENAI_API_KEY"]` (Streamlit's secrets mechanism), not
  from an environment variable. Locally this means a `.streamlit/secrets.toml` file with:
  ```toml
  OPENAI_API_KEY = "sk-..."
  ```
- In production the app is deployed on Streamlit Community Cloud, where this secret is configured in
  the app's dashboard settings (see the comment in `app.py`).
- Never hardcode the API key in `app.py` or commit a `secrets.toml` file.

## Architecture

`app.py` follows Streamlit's single-script, top-to-bottom rerun model — the whole file re-executes on
every user interaction:

1. **Page setup** — `st.set_page_config` and an `OpenAI` client instantiated once per rerun.
2. **`experts` dict** — maps a display name (French, with an emoji-free label) to the system prompt
   that defines that expert's persona. This is the source of truth for available experts; add a new
   expert by adding a new key/value pair here.
3. **Sidebar** — `st.selectbox` lets the user pick the active expert from `experts.keys()`.
4. **Chat history** — persisted in `st.session_state.messages` as a list of `{"role", "content"}`
   dicts (Streamlit's standard pattern for surviving reruns within a session).
5. **Chat loop** — on new input via `st.chat_input`, the user message is appended to history, then the
   full conversation is sent to `client.chat.completions.create` with the selected expert's prompt
   injected as the `system` message and the entire `messages` history replayed as context. The model
   is currently `gpt-3.5-turbo`.

Notes for future changes:
- `requirements.txt` includes `pinecone-client`, which is not yet used in `app.py` — likely reserved
  for a planned retrieval/vector-search feature.
- User-facing strings and expert prompts are in French; keep new UI text and persona prompts
  consistent with that language unless told otherwise.
