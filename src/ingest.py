"""Load a PDF path, split it, and persist its embeddings in pgVector."""

from pathlib import Path
import sys

import click
from langchain_community.document_loaders import PyPDFLoader
from langchain_postgres import PGVector
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Support both direct script execution and `python -m src.ingest`.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.config import ConfigurationError, get_embeddings, get_settings

@click.command()
@click.argument("pdf_path", type=click.Path(path_type=Path))
def main(pdf_path: Path) -> None:
    """Ingest PDF_PATH into PostgreSQL with pgVector."""
    if not pdf_path.is_file():
        raise click.ClickException(f"Arquivo PDF não encontrado: {pdf_path}.")
    if pdf_path.suffix.lower() != ".pdf":
        raise click.ClickException(f"O arquivo informado não tem extensão .pdf: {pdf_path}.")
    try:
        settings = get_settings()
        docs = PyPDFLoader(str(pdf_path)).load()
        if not docs:
            raise click.ClickException("O PDF não contém páginas legíveis.")
        chunks = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150).split_documents(docs)
        if not chunks:
            raise click.ClickException("Não foi possível extrair texto do PDF.")

        # Rebuild the collection so reruns replace old content and remove stale chunks.
        store = PGVector(
            embeddings=get_embeddings(settings), collection_name=settings.collection,
            connection=settings.database_url, use_jsonb=True,
        )
        store.delete_collection()
        store = PGVector(
            embeddings=get_embeddings(settings), collection_name=settings.collection,
            connection=settings.database_url, use_jsonb=True,
        )
        store.add_documents(chunks)
        click.echo(f"Ingestão concluída: {len(chunks)} chunks salvos na collection '{settings.collection}'.")
    except ConfigurationError as exc:
        raise click.ClickException(str(exc)) from exc
    except click.ClickException:
        raise
    except Exception as exc:
        raise click.ClickException(f"Falha na ingestão. Verifique o banco, a configuração e a compatibilidade da dimensão dos embeddings: {exc}") from exc


if __name__ == "__main__":
    main()
