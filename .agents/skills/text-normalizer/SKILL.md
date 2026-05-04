---
name: text-normalizer
description: Normalize a user-provided plain text snippet by trimming leading/trailing whitespace, collapsing consecutive half-width spaces to one space, preserving Chinese punctuation, and returning exactly one Markdown fenced code block. Use when the user asks to normalize text, remove surrounding whitespace, collapse spaces, or output normalized plain text in a Markdown code block, including explicit requests to use text-normalizer. Do not use for translation, rewriting, polishing, summarization, correction, code/JSON/Markdown/table/config formatting, conceptual discussion without concrete input text, or requests to alter punctuation, convert full-width/half-width characters, delete punctuation, or change writing style.
---

# Text Normalizer

## Workflow

1. Identify the exact text snippet supplied by the user. Exclude the user's instruction text unless they explicitly mark it as part of the input.
2. Trim leading and trailing whitespace. Treat an empty result as `EMPTY_INPUT`.
3. Replace each run of consecutive half-width spaces (`U+0020`) inside the text with one half-width space.
4. Preserve all other content, especially Chinese punctuation such as `，。！？；：“”‘’、（）《》`. Do not translate, rewrite, correct, re-punctuate, or convert full-width/half-width characters.
5. Return only one Markdown fenced code block. Put no explanation, labels, debug text, paths, timestamps, or extra prose before or after it.

## Fence Selection

Use a backtick fence of length 3 unless the normalized text contains a run of 3 or more backticks. In that case, use a fence one backtick longer than the longest backtick run in the normalized text.

## Deterministic Helper

For tricky whitespace or backtick cases, run the helper from this skill directory and copy its stdout exactly as the final answer:

```bash
python3 scripts/normalize_text.py
```

The script reads the raw input text from stdin and emits the required single Markdown code block.
