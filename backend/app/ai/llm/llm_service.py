import ollama


class LLMService:

    @staticmethod
    def generate_response(
        question: str,
        context: str
    ):

        prompt = f"""
You are ODIN, an intelligent cognitive knowledge assistant.

Use:
1. conversation history
2. retrieved semantic memory
3. knowledge graph relationships

to answer intelligently and coherently.

Explain relationships between concepts when relevant.

If the answer is not present in the provided context, say:
"I could not find relevant information in your notes."

Context:
{context}

Question:
{question}
"""

        response = ollama.chat(
            model="gemma3:4b",

            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response["message"]["content"]
    @staticmethod
    def stream_response(
        question: str,
        context: str
    ):

        prompt = f"""
You are ODIN, an intelligent cognitive knowledge assistant.

Use:
1. conversation history
2. retrieved semantic memory
3. knowledge graph relationships

to answer intelligently and coherently.

Context:
{context}

Question:
{question}
"""

        stream = ollama.chat(
            model="gemma3:4b",

            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],

            stream=True
        )

        for chunk in stream:

            yield chunk["message"]["content"]