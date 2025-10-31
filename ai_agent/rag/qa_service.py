from ai_agent.vector_store.db import VectorStore
from ai_agent.artifacts.generator import ArtifactGenerator
from openai import OpenAI

class QAService:
    def __init__(self, openrouter_api_key, indexer):
        self.vector_store = VectorStore()
        self.openrouter_client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=openrouter_api_key,
        )
        self.artifact_generator = ArtifactGenerator()
        self.indexer = indexer

    def answer_query(self, query):
        # 1. Search for relevant documents
        search_results = self.vector_store.search(query)

        # 2. Build the prompt and generate artifacts
        context = ""
        matches = []
        for doc_id, doc_text in zip(search_results['ids'][0], search_results['documents'][0]):
            context += doc_text + "\n\n"

            file_path = self.indexer.get_file_path(doc_id)

            if file_path:
                images = self.artifact_generator.generate_highlighted_image(file_path, doc_text)
                matches.append({
                    "document_id": doc_id,
                    "images": images
                })

        prompt = f"""Based on the following context, please answer the question.

        Context:
        {context}

        Question: {query}
        """

        # 3. Call OpenRouter
        response = self.openrouter_client.chat.completions.create(
            model="mistralai/mistral-7b-instruct-v0.2",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt},
            ],
        )

        return {
            "answer": response.choices[0].message.content,
            "matches": matches
        }
