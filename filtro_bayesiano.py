import re
import unicodedata
from typing import Dict, List, Tuple


def remover_acentos(texto: str) -> str:
    """
    Remove acentos de qualquer texto (ex: 'grátis' vira 'gratis', 'reunião' vira 'reuniao').
    Evita qualquer problema de codificacao ou comparacao.
    """
    forma_normal = unicodedata.normalize("NFD", texto)
    return "".join(char for char in forma_normal if unicodedata.category(char) != "Mn")


# 1. Base de Conhecimento: Palavras-chave sem acento e seus pesos de risco
PESOS_SPAM: Dict[str, float] = {
    "pix": 0.9,
    "gratis": 0.8,
    "urgente": 0.7,
    "reuniao": 0.1,
    "aula": 0.05,
}

LIMIAR_SPAM = 0.50


def tokenizar(texto: str) -> List[str]:
    """
    Converte o texto para minusculas, remove acentos e extrai as palavras.
    """
    texto_sem_acento = remover_acentos(texto.lower())
    palavras = re.findall(r"\b[a-z0-9]+\b", texto_sem_acento)
    return palavras


def classificar_email(texto: str) -> Dict[str, object]:
    """
    Classifica um e-mail com base na media dos pesos das palavras detectadas.
    """
    palavras = tokenizar(texto)

    palavras_detectadas: List[Tuple[str, float]] = []
    for palavra in palavras:
        if palavra in PESOS_SPAM:
            palavras_detectadas.append((palavra, PESOS_SPAM[palavra]))

    total_detectadas = len(palavras_detectadas)

    if total_detectadas > 0:
        soma_pesos = sum(peso for _, peso in palavras_detectadas)
        media_pesos = soma_pesos / total_detectadas
    else:
        # Caso em que nenhuma palavra da base foi encontrada
        media_pesos = 0.0

    if media_pesos >= LIMIAR_SPAM:
        classificacao = "SPAM"
    else:
        classificacao = "E-MAIL NORMAL (HAM)"

    return {
        "texto": texto,
        "palavras_detectadas": palavras_detectadas,
        "total_detectadas": total_detectadas,
        "media_pesos": round(media_pesos, 4),
        "classificacao": classificacao,
    }


def exibir_relatorio(resultado: Dict[str, object], titulo: str = "Relatorio de Classificacao") -> None:
    """
    Exibe o relatorio formatado no console sem caracteres especiais ou acentos.
    """
    print("=" * 60)
    print(f" {titulo.upper()} ")
    print("=" * 60)
    print(f"Texto do E-mail: \"{resultado['texto']}\"")
    print("-" * 60)

    palavras_detectadas: List[Tuple[str, float]] = resultado["palavras_detectadas"]

    if palavras_detectadas:
        detalhe_palavras = ", ".join([f"{palavra} ({peso})" for palavra, peso in palavras_detectadas])
        print(f"-> Palavras detectadas: {detalhe_palavras}")

        pesos_str = " + ".join([str(peso) for _, peso in palavras_detectadas])
        n = resultado["total_detectadas"]
        print(f"-> Calculo da Media = ({pesos_str}) / {n} = {resultado['media_pesos']:.4f}")
    else:
        print("-> Nenhuma palavra da base de conhecimento foi detectada.")
        print(f"-> Media dos Pesos considerada: {resultado['media_pesos']:.4f}")

    print("-" * 60)
    print(f"-> Limiar de Decisao: >= {LIMIAR_SPAM:.2f} (SPAM) | < {LIMIAR_SPAM:.2f} (NORMAL)")
    print(f"-> Resultado Final : [{resultado['classificacao']}]")
    print("=" * 60)
    print("\n")


if __name__ == "__main__":
    print("\n" + "#" * 60)
    print("  TESTES AUTOMATIZADOS DO CLASSIFICADOR DE E-MAILS")
    print("#" * 60 + "\n")

    # Cenario de Teste 1: Esperado SPAM
    email_1 = "Urgente receba seu pix gratis agora"
    resultado_1 = classificar_email(email_1)
    exibir_relatorio(resultado_1, titulo="Cenario de Teste 1")

    # Cenario de Teste 2: Esperado NORMAL (HAM)
    email_2 = "Confirmacao de reuniao para a aula de amanha"
    resultado_2 = classificar_email(email_2)
    exibir_relatorio(resultado_2, titulo="Cenario de Teste 2")

    # Cenario de Teste 3: Caso de borda sem palavras conhecidas
    email_3 = "Ola amigo, tudo bem? Vamos almocar mais tarde?"
    resultado_3 = classificar_email(email_3)
    exibir_relatorio(resultado_3, titulo="Cenario de Teste 3 (Sem palavras na base)")
