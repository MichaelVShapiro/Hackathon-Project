import vector_db
import numpy as np
from sentence_transformers import SentenceTransformer
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
import torch

DB_DIR = "./db/"
# MODEL_NAME = "HuggingFaceH4/zephyr-7b-beta"
MODEL_NAME = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"


class RAGQuery:
    def __init__(self, k_retrieval=3):
        self.k = k_retrieval
        self.index, self.metadata = vector_db.load_db()
        print("Vector db loaded")
        self.embedder = SentenceTransformer('all-MiniLM-L6-v2')
        self.generator = self._load_llm()
        print("LLM loaded")

    def _load_llm(self):
        tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME,
                                                  trust_remote_code=True)
        model = AutoModelForCausalLM.from_pretrained(
            MODEL_NAME,
            device_map="cpu",
            torch_dtype=torch.float32,
            trust_remote_code=True,
        )
        return pipeline(
            "text-generation",
            model=model,
            tokenizer=tokenizer,
            max_new_tokens=512,
            temperature=0.2,
            top_p=0.95,
            repetition_penalty=1.1
        )

    def query(self, user_query):
        query_embedding = self.embedder.encode([user_query])
        D, I = self.index.search(np.array(query_embedding), self.k)
        retrieved_meta = [self.metadata[i] for i in I[0]]

        # Build prompt in zephyr format
        # prompt = "<|system|>You are a helpful assistant answering based on the retrieved documents.<|user|>\n"
        prompt = "Use the following documents to answer the question accurately:\n\n"
        for idx, meta in enumerate(retrieved_meta, 1):
            prompt += f"Source: {meta['source']}\nChunk {idx}: {meta['chunk_text']}\n\n"
        prompt += f"User Question: {user_query}"

        response = self.generator(prompt, max_length=512, do_sample=False)[0]['generated_text']
        return response, retrieved_meta


def _prompt_test():
    rag = RAGQuery()

    while True:
        user_input = input("\nQuestion (type 'exit' to quit): ")
        if user_input.lower() == "exit":
            break

        answer, sources = rag.query(user_input)

        print("\n--- Query related metadata ---")
        for meta in sources:
            print(f"{meta['source']}: {meta['chunk_text'][:100]}...")

        print("\n--- Generated answer ---")
        print(answer)


if __name__ == "__main__":
    _prompt_test()
