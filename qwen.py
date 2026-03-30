from openai import OpenAI
import os
import streamlit as st
import json

client = OpenAI(
    api_key= st.secrets["qwenAPI"],
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)


PROMPT_TICKET_EXTRACTION = """
You are an OCR extraction assistant.

Task:
Extract ONE multiple-choice question from the provided image.

Rules:
1. If multiple questions are present, select the question that appears completely.
2. Ignore any partial, cut-off, or surrounding questions.
3. Extract:
   - The full question text
   - Exactly 5 answer choices (A–E)
4. If fewer than 5 choices are visible, fill missing ones with "?".
5. Clean the text:
   - Fix obvious OCR errors (spacing, symbols, formatting)
   - Remove irrelevant noise
6. Mathematical expressions:
   - Convert mathematical expressions into LaTeX format
   - Integrate LaTeX directly into the question and choices (do NOT separate them)

Output format (STRICT JSON):
{
  "question": "...",
  "choiceA": "...",
  "choiceB": "...",
  "choiceC": "...",
  "choiceD": "...",
  "choiceE": "..."
}

Constraints:
- Do NOT include explanations
- Do NOT include extra text
- Output ONLY valid JSON
"""

def ocr(encodedImage):

    completion = client.chat.completions.create(
        model="qwen-vl-ocr-2025-11-20",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/png;base64,{encodedImage}"},
                        "min_pixels": 32 * 32 * 3,

                        "max_pixels": 32 * 32 * 8192
                    },
                    {"type": "text",
                     "text": PROMPT_TICKET_EXTRACTION}
                ]
            }
        ],
        response_format = {"type": "json_object"}
    )
    return(json.loads(completion.choices[0].message.content))
