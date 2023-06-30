import export as export

export OPENAI_API_KEY='...'
export GITHUB_TOKEN='...'

import pickle
from llama_index import download_loader, GPTVectorStoreIndex
import os
from llama_hub.github_repo import GithubClient, GithubRepositoryReader

os.environ['OPENAI_API_KEY'] = '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'



download_loader("GithubRepositoryReader")

docs = None
if os.path.exists("docs.pkl"):
    with open("docs.pkl", "rb") as f:
        docs = pickle.load(f)

if docs is None:
    github_client = GithubClient(os.getenv("GITHUB_TOKEN"))
    loader = GithubRepositoryReader(
        github_client,
        owner="jerryjliu",
        repo="llama_index",
        filter_directories=(["gpt_index", "docs"], GithubRepositoryReader.FilterType.INCLUDE),
        filter_file_extensions=([".py"], GithubRepositoryReader.FilterType.INCLUDE),
        verbose=True,
        concurrent_requests=10,
    )

    docs = loader.load_data(branch="main")

    with open("docs.pkl", "wb") as f:
        pickle.dump(docs, f)

index = GPTVectorStoreIndex.from_documents(docs)

query_engine = index.as_query_engine()
response = query_engine.query("Explain each LlamaIndex class?")
print(response)
