import ollama


class LLMService:

    @staticmethod
    def generate_response(
        question: str,
        context: str
    ):

        prompt = f"""
You are ODIN, an intelligent personal knowledge assistant.

Answer the user's question ONLY using the provided context.

If the answer is not in the context, say:
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