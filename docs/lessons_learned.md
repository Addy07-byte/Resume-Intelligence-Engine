# Lessons Learned

_To be updated as lessons are discovered during development._# Lessons Learned

## 1. Critical facts bypass retrieval
Contact info, job titles, and dates must be injected directly into the 
prompt — not retrieved semantically. Retrieval is similarity-based, so 
chunks that don't match the JD get filtered out even if they contain 
critical grounding facts. Assuming the system would preserve job titles 
without explicit grounding led to hallucinated titles in early outputs.

## 2. Always confirm your branch before committing
Committing to the wrong branch causes diverged histories, merge conflicts, 
and wasted time untangling git state. The fix is simple: run `git branch` 
before every `git add`. This one habit prevents the majority of git 
workflow problems when working solo or on a team.

## 3. Environment hygiene before you write code
Missing API keys, unactivated virtual environments, and uninstalled 
dependencies cause errors that look like code bugs but aren't. Always 
verify prerequisites — activate `.venv`, confirm `.env` is loaded, and 
check `requirements.txt` is complete — before debugging logic.

## 4. Retrieval problems and prompt problems are different failures
A retrieval problem means the right context never reached the LLM — no 
amount of prompt engineering fixes missing context. A prompt problem means 
the context is there but the LLM isn't being told explicitly what to do 
with it. Diagnosing which failure you have before trying to fix it saves 
significant debugging time.