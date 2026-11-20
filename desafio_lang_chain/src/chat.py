"""Interactive grounded question-answering CLI."""

import click
from pathlib import Path
import sys
from langchain_core.messages import HumanMessage, SystemMessage

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.config import get_chat_model, get_settings
from src.search import search

NO_ANSWER = "Não tenho informações necessárias para responder sua pergunta."
SYSTEM_PROMPT = f'''Você responde perguntas usando exclusivamente o contexto fornecido.\n\nCONTEXTO:\n{{context}}\n\nREGRAS:\n- Responda somente com base no CONTEXTO.\n- Se a informação não estiver explicitamente no CONTEXTO, responda exatamente: "{NO_ANSWER}"\n- Nunca invente ou use conhecimento externo.\n- Nunca produza opiniões ou interpretações além do que está escrito.'''


def _response_text(content: object) -> str:
    """Return only textual answer blocks, excluding provider metadata."""
    if isinstance(content, str):
        return content.strip()
    if isinstance(content, dict):
        if content.get("type") == "text" and isinstance(content.get("text"), str):
            return content["text"].strip()
        return ""
    if isinstance(content, list):
        text_blocks = []
        for block in content:
            if isinstance(block, str):
                text_blocks.append(block)
            elif isinstance(block, dict) and block.get("type") == "text" and isinstance(block.get("text"), str):
                text_blocks.append(block["text"])
        return "\n".join(text.strip() for text in text_blocks if text.strip())
    return ""


def answer(question: str) -> str:
    results = search(question, k=10)
    if not results:
        return NO_ANSWER
    context = "\n\n---\n\n".join(doc.page_content for doc, _score in results)
    settings = get_settings()
    response = get_chat_model(settings).invoke([
        SystemMessage(content=SYSTEM_PROMPT.format(context=context)),
        HumanMessage(content=f"PERGUNTA DO USUÁRIO:\n{question}\n\nRESPONDA A PERGUNTA DO USUÁRIO."),
    ])
    return _response_text(response.content) or NO_ANSWER


@click.command()
def main() -> None:
    """Ask questions about the ingested PDF. Type 'sair' to quit."""
    click.echo("Pergunte qualquer coisa sobre o PDF. Digite 'sair' para encerrar.")
    while True:
        try:
            question = click.prompt("PERGUNTA", prompt_suffix=": ", default="", show_default=False).strip()
            if question.lower() in {"sair", "exit", "quit"}:
                click.echo("Até mais!")
                return
            if not question:
                continue
            click.echo(f"RESPOSTA: {answer(question)}")
        except Exception as exc:
            # Keep the interactive session usable after transient DB/provider errors.
            click.echo(f"Erro: {exc}", err=True)


if __name__ == "__main__":
    main()
