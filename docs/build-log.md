# Build log

## 2026-10-08 — M0: owner-only echo bot

**Built:** Anna (`@Patrobotics_Assistant_Bot`) echoes back whatever I send her. She only answers my chat ID. Anyone else can message her, but she ignores them and logs a warning, without the message text. The token and chat ID live in a gitignored `config.toml`, and `config.example.toml` with placeholders is committed.

**Broke:**
- `import tomlib` gave `ModuleNotFoundError`. It's `tomllib`, with two L's.
- `TOMLDecodeError` in `config.toml`: I'd written `:` instead of `=` and left the token without quotes.
- `KeyError`: the code read `owner_id`, but the config key is `owner_chat_id`.
- In review, an edited message crashed `echo`. Edits reach the handler with `update.message` set to `None`.

**Fixed:**
- Read the tracebacks: the error type and message pointed straight at the problem each time. The `TOMLDecodeError` even gave the line and column.
- Added `filters.UpdateType.MESSAGE` to the owner handler so edits are ignored. That also prevents duplicate tasks later, when an edited `/add` would run twice.
- Tested three paths: owner (reply), edited message (no reply, no crash), and stranger (temporarily set `owner_chat_id = 1`: no reply, WARNING logged).

**Learned:**
- Test edge cases, not just the happy path. The edit crash only showed up because someone tried it.
- Never log secrets. I check the token loaded by printing its length, and the `httpx` logger is set to WARNING because its INFO logs include the token in URLs.
- Telegram filters combine with `&` and `~`, and the first matching handler wins.

**Next (M1):** store tasks in SQLite with `/add`, `/list` and `/done`, plus tests for the parsing. Before writing tests: load the config inside `main()` instead of at import time, and give every command handler the owner filter.