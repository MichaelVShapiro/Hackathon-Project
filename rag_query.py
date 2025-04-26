import vector_db
import numpy as np
from sentence_transformers import SentenceTransformer
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

DB_DIR = "./db/"
MODEL_NAME = "HuggingFaceH4/zephyr-7b-alpha"
# MODEL_NAME = "HuggingFaceH4/zephyr-7b-beta"
# MODEL_NAME = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

ZEPHYR_ASSISTANT = "<|assistant|>"

class RAGQuery:
    def __init__(self, k_retrieval=3):
        self.k = k_retrieval
        self.index, self.metadata = vector_db.load_db()
        print("Vector db loaded")
        self.embedder = SentenceTransformer('all-MiniLM-L6-v2')
        self.model, self.tokenizer = self._load_llm()
        print("LLM loaded")

    def _load_llm(self):
        tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME,
                                                  trust_remote_code=True)
        model = AutoModelForCausalLM.from_pretrained(
            MODEL_NAME,
            device_map={"": DEVICE},
            torch_dtype=torch.float16 if DEVICE.type == "cuda" else torch.float32,
            trust_remote_code=True,
        )
        model.eval()
        return model, tokenizer

    def _build_zephyr_prompt(self, retrieved_meta, user_query):
        prompt = "<|system|>You are a helpful assistant. Use the provided documents to answer user's question accurately and concisely.\n<|user|>\n"
        prompt += "Documents:\n"
        for idx, meta in enumerate(retrieved_meta, 1):
            prompt += f"- Document {idx} from {meta['source']}: {meta['chunk_text']}\n"
        prompt += f"\nQuestion: {user_query}\n"
        prompt += "<|assistant|>"
        return prompt        

    def _generate_response(self, prompt):
        inputs = self.tokenizer(prompt, return_tensor="pt", padding=True).to(DEVICE)
        outputs = self.model.generate(
            **inputs,
            max_new_tokens=512,
            do_sample=False,
            repetition_penalty=1.1,
            eos_token_id=self.tokenizer.eos_token_id
        )
        full_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        if ZEPHYR_ASSISTANT in full_text:
            return full_text.split(ZEPHYR_ASSISTANT)[-1].strip()
        return full_text.strip()

    def query(self, user_query):
        query_embedding = self.embedder.encode([user_query])
        D, I = self.index.search(np.array(query_embedding), self.k)
        retrieved_meta = [self.metadata[i] for i in I[0]]

        # prompt = "Use the following documents to answer the question accurately:\n\n"
        # Build prompt in zephyr format
        prompt = self._build_zephyr_prompt(retrieved_meta, user_query)
        response = self._generate_response(prompt)

        return response, retrieved_meta


def _prompt_test():
    rag = RAGQuery()

    while True:
        user_input = input("\nQuestion (type 'exit' to quit): ")
        if user_input.lower() == "exit":
            break

        answer, sources = rag.query(user_input)

#        print("\n--- Query related metadata ---")
#        for meta in sources:
#            print(f"{meta['source']}: {meta['chunk_text'][:100]}...")

        print("\n--- Generated answer ---")
        print(answer)


if __name__ == "__main__":
    _prompt_test()
