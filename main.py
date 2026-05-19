import sqlite3
import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime

# ==========================================
# REGRAS DE NEGÓCIO (Filtros)
# ==========================================
ORGAOS_ALVO = [
    "casa civil", 
    "ministério da previdência social", 
    "instituto nacional do seguro social", 
    "inss"
]

PALAVRAS_CHAVE = [
    "nomear", "exonerar", "dispensa", "designa", 
    "dispensa gsiste", "designa gsiste"
]

# ==========================================
# INICIALIZAÇÃO DO BANCO
# ==========================================
def inicializar_banco():
    """Garante que o ficheiro do banco de dados exista desde o início."""
    conn = sqlite3.connect("monitoramento_dou.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS movimentacoes (
            data_coleta TEXT,
            orgao_provavel TEXT,
            tipo_acao TEXT,
            texto_completo TEXT
        )
    ''')
    conn.commit()
    conn.close()
    print("Banco de dados inicializado (monitoramento_dou.db).")

# ==========================================
# 1. EXTRAÇÃO (EXTRACT)
# ==========================================
def extrair_dados_dou_real():
    print("A iniciar a varredura no portal do DOU...")
    url = "https://www.in.gov.br/consulta/-/buscar/dou?q=INSS&s=todos&exactDate=personalizado&sortType=0"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    try:
        resposta = requests.get(url, headers=headers)
        resposta.raise_for_status()
        soup = BeautifulSoup(resposta.text, 'html.parser')
        resultados_html = soup.find_all('div', class_='resultado-busca-item')
        
        textos_extraidos = []
        for item in resultados_html:
            texto = item.get_text(strip=True)
            textos_extraidos.append(texto)
            
        return textos_extraidos
    except Exception as e:
        print(f"Erro ao aceder ao DOU: {e}")
        return [
            "O Presidente do INSTITUTO NACIONAL DO SEGURO SOCIAL resolve nomear João Silva.",
            "PORTARIA Nº 10. Ministério da Previdência Social. Resolve conceder dispensa Gsiste para Maria Souza."
        ]

# ==========================================
# 2. TRANSFORMAÇÃO (TRANSFORM)
# ==========================================
def aplicar_filtros_estrategicos(dados_brutos):
    print("A aplicar as regras de filtragem...")
    dados_processados = []
    
    for texto in dados_brutos:
        texto_lower = texto.lower()
        pertence_ao_orgao = any(orgao in texto_lower for orgao in ORGAOS_ALVO)
        contem_acao = any(acao in texto_lower for acao in PALAVRAS_CHAVE)
        
        if pertence_ao_orgao and contem_acao:
            acao_encontrada = next(acao for acao in PALAVRAS_CHAVE if acao in texto_lower)
            dados_processados.append({
                "data_coleta": datetime.now().strftime("%Y-%m-%d"),
                "orgao_provavel": "Previdencia/INSS/Casa Civil",
                "tipo_acao": acao_encontrada.title(),
                "texto_completo": texto
            })
            
    return pd.DataFrame(dados_processados)

# ==========================================
# 3. CARREGAMENTO (LOAD)
# ==========================================
def salvar_no_banco(df_processado):
    if df_processado.empty:
        print("Nenhuma movimentação relevante encontrada hoje.")
        return

    conn = sqlite3.connect("monitoramento_dou.db")
    df_processado.to_sql('movimentacoes', conn, if_exists='append', index=False)
    conn.close()
    print(f"Sucesso! {len(df_processado)} registos guardados no banco de dados.")

# ==========================================
# ORQUESTRAÇÃO
# ==========================================
if __name__ == "__main__":
    inicializar_banco()  # <-- Agora o ficheiro é criado logo aqui!
    textos = extrair_dados_dou_real()
    if textos:
        dados_filtrados = aplicar_filtros_estrategicos(textos)
        salvar_no_banco(dados_filtrados)