import os
import re
from fastapi import HTTPException
from langchain_google_genai import ChatGoogleGenerativeAI


# Lista de stopwords
STOPWORDS = {
    'o', 'a', 'os', 'as', 'um', 'uma', 'uns', 'umas',
    'de', 'da', 'do', 'das', 'dos',
    'em', 'na', 'no', 'nas', 'nos',
    'para', 'por', 'com', 'sem', 'sob', 'sobre',
    'e', 'ou', 'mas', 'que', 'se', 'como',
    'eu', 'tu', 'ele', 'ela', 'nós', 'vocês', 'eles', 'elas',
    'me', 'te', 'lhe', 'nos', 'vos', 'lhes',
    'meu', 'minha', 'meus', 'minhas',
    'seu', 'sua', 'seus', 'suas',
    'este', 'esta', 'estes', 'estas',
    'esse', 'essa', 'esses', 'essas',
    'aquele', 'aquela', 'aqueles', 'aquelas',
    'ser', 'estar', 'ter', 'haver', 'fazer',
    'é', 'são', 'foi', 'foram', 'será', 'serão',
    'está', 'estão', 'estava', 'estavam',
    'tem', 'têm', 'tinha', 'tinham',
    'há', 'houve', 'havia', 'haviam',
    'ao', 'aos', 'à', 'às', 'pelo', 'pela', 'pelos', 'pelas',
    'num', 'numa', 'nuns', 'numas',
    'dum', 'duma', 'duns', 'dumas',
    'num', 'numa', 'nuns', 'numas',
    'entre', 'contra', 'até', 'desde', 'durante',
    'através', 'mediante', 'conforme', 'segundo',
    'quando', 'enquanto', 'onde', 'aonde',
    'porque', 'pois', 'portanto', 'assim',
    'também', 'ainda', 'já', 'sempre', 'nunca',
    'muito', 'mais', 'menos', 'muito', 'pouco',
    'tudo', 'todos', 'todas', 'todo', 'toda',
    'nada', 'ninguém', 'nenhum', 'nenhuma',
    'algum', 'alguma', 'alguns', 'algumas',
    'qualquer', 'quaisquer',
    'cada', 'ambos', 'ambas'
}


# Define uma instância da llm
def get_llm():
    """
    Carrega as variáveis, valida, configura a llm e a retorna.

    Return: llm -> ChatGoogleGenerativeAI
    """

    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    MAX_TOKENS = os.getenv("MAX_TOKENS")
    if not GOOGLE_API_KEY:
        raise HTTPException(
            status_code=500,
            detail="GOOGLE_API_KEY não configurada."
        )

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature="0.2",
        # max_output_tokens=MAX_TOKENS,
    )

    return llm


# Sanitiza PII (dados pessoais) antes de enviar ao modelo
def sanitize_pii(text: str) -> str:
    """
    Remove dados pessoais identificáveis do texto antes de enviar ao Gemini.

    Args:
        text: Texto original

    Returns:
        str: Texto com PII removido
    """
    # Remove emails
    text = re.sub(r'\b[\w.-]+@[\w.-]+\.\w+\b', '[EMAIL]', text)
    # Remove telefones (formatos BR: 11999999999, 11 99999-9999, (11) 99999-9999)
    text = re.sub(r'\(?\d{2}\)?[-.\s]?\d{4,5}[-.\s]?\d{4}\b', '[TELEFONE]', text)
    # Remove CPF (123.456.789-00 ou 12345678900)
    text = re.sub(r'\b\d{3}\.?\d{3}\.?\d{3}-?\d{2}\b', '[CPF]', text)
    # Remove CNPJ (12.345.678/0001-00 ou 12345678000100)
    text = re.sub(r'\b\d{2}\.?\d{3}\.?\d{3}/?\d{4}-?\d{2}\b', '[CNPJ]', text)
    return text


# Aplica remoção de caracteres inúteis
def refine_text(text: str) -> str:
    """
    Normalização básica, remoção de espaços múltiplos, pontuações repetidas, URLs e emails

    Args: text -> str "olá, meu email é ranalisesaldanha@gmail.com!!!"

    Return: str "olá, meu email é ranalisesaldanha@gmail.com!"
    """

    # Remove espaços múltiplos
    processed_text = re.sub(r'\s+', ' ', text)

    # Remove pontuação repetida
    processed_text = re.sub(r'[!]{2,}', '.', processed_text)
    processed_text = re.sub(r'[?]{2,}', '.', processed_text)    
    processed_text = re.sub(r'[.]{2,}', '.', processed_text)    

    # Remove URLs
    processed_text = re.sub(r'https?://\S+|www\.\S+', '[URL]', processed_text)    

    # Remove emails
    processed_text = re.sub(r'\b[\w\.-]+\.\w+\b', '[EMAIL]', processed_text)    
    
    return processed_text


# Aplica remoção de stopwords no texto
def remove_stopwords(text: str) -> str:
    """
    Remove paravras que não agregam significado para a classificação.

    
    Args: text -> str "olá, meu email é ranalisesaldanha@gmail.com "

    Return: str "olá email ranalisesaldanha@gmail.com"
    """
    
    # Tokeniza o texto
    tokens = re.findall(r'\b\w+\b', text)

    # Remove stopwords
    filtered_tokens = [
        word for word in tokens
        if word not in STOPWORDS
    ]

    # Reconstroi o texto
    processed_text = ' '.join(filtered_tokens)

    # Remove espaços extras finais
    processed_text = processed_text.strip()

    return processed_text


# Efetua o pré-processamento do texto para maximizar a performace e custo
def pre_process_text(text: str) -> str:
    """
    Recebe o texto e aplica estratégias de pré processamento de texto para melhorar a legibilidade e reduzir tokens

    Args: text -> str - "texto de entrada de parâmetro"

    Return: text-> str - "texto já aplicado os pré processadores
    """

    # Aplica lowercase
    lower_text = text.lower()

    # Aplica remoção de caracteres inúteis
    processed_text = refine_text(lower_text)

    # Remoção de stopwords
    processed_text = remove_stopwords(processed_text)

    return processed_text