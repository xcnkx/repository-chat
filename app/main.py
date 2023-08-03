import os
from app.retriver import create_retriever
from langchain.embeddings.openai import OpenAIEmbeddings
import argparse

from langchain.document_loaders import GitLoader

from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI


def qa(
    question: str, repo_path: str, clone_url: str | None = None, branch: str = "master"
) -> str:
    if os.path.exists(repo_path):
        clone_url = None

    loader = GitLoader(
        repo_path=repo_path,
        branch=branch,
        clone_url=clone_url,
        file_filter=lambda x: x.endswith(".py") or x.endswith(".md"),
    )
    embeddings = OpenAIEmbeddings()  # type: ignore
    retriver = create_retriever(embeddings, loader.load_and_split())

    llm = ChatOpenAI(model="gpt-3.5-turbo-16k", temperature=0)
    qa_chain = RetrievalQA.from_chain_type(llm, retriever=retriver)
    return qa_chain({"query": question})["result"]


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--question", type=str, help="Question to ask")
    parser.add_argument("--repo-path", type=str, help="Path to repo")
    parser.add_argument("--clone-url", type=str, help="Clone url", default=None)
    parser.add_argument("--branch", type=str, help="Branch", default="master")
    args = parser.parse_args()
    print(qa(args.question, args.repo_path, args.clone_url, args.branch))
