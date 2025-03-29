from sentence_transformers import SentenceTransformer
import chromadb
import logging

class FunctionFinder:
    def __init__(self, storage_path=None):
        logging.info("Setting up FunctionFinder...")
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.db = chromadb.Client() if not storage_path else chromadb.PersistentClient(path=storage_path)
        self.functions = self.db.get_or_create_collection("automation_functions")
        self.function_descriptions = {
            "open_chrome": "Opens Google Chrome web browser",
            "open_calculator": "Launches the system calculator application",
            "get_cpu_usage": "Retrieves current CPU usage percentage",
            "get_ram_usage": "Gets current RAM usage statistics",
            "run_shell_command": "Executes a system shell command",
            "open_notepad": "Opens the Notepad application"
        }
        self._load_functions()
        logging.info("FunctionFinder ready!")

    def _load_functions(self):
        logging.info("Refreshing vector store...")
        self.functions.delete(ids=list(self.function_descriptions.keys()))  # Clear old data
        descriptions = list(self.function_descriptions.values())
        embeddings = self.model.encode(descriptions)
        for i, (name, desc) in enumerate(self.function_descriptions.items()):
            self.functions.add(
                documents=[desc],
                embeddings=[embeddings[i].tolist()],
                ids=[name]
            )
        logging.info("Vector store refreshed with %d functions", len(self.function_descriptions))
    def find_function(self, user_prompt):
        prompt_embedding = self.model.encode([user_prompt])[0]
        result = self.functions.query(
            query_embeddings=[prompt_embedding.tolist()],
            n_results=1
        )
        return result['ids'][0][0]