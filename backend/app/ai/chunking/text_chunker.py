class TextChunker:

    @staticmethod
    def chunk_text(
        text: str,
        chunk_size: int = 30,
        overlap: int = 5
    ):

        words = text.split()

        chunks = []

        start = 0

        while start < len(words):

            end = start + chunk_size

            chunk = words[start:end]

            chunks.append(
                " ".join(chunk)
            )

            start += chunk_size - overlap

        return chunks