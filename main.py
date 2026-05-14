import sqlite3
import pandas as pd
from datetime import datetime

# ==========================================
# 1. EXTRAÇÃO (EXTRACT)
# ==========================================
def extrair_dados_dou():
    """
    Simula a extração de dados de uma fonte (API, HTML ou Arquivo).
    Aqui, retornamos uma lista de textos brutos simulando publicações.
    """
    print("Iniciando Extração...")
    # Em um cenário real, aqui entraria o web scraping (BeautifulSoup/Selenium)
    dados_brutos = [
        "PORTARIA Nº 123. O MINISTRO resolve: Nomear João Silva para o INSS.",
        "Aviso de licitação para compra de equipamentos de TI.",
        "PORTARIA Nº 124. Resolve conceder exoneração a Maria Souza do Ministério da Previdência Social.",
        "Retificação do edital de concurso público."
    ]
    return dados_brutos

# ==========================================
# 2. TRANSFORMAÇÃO (TRANSFORM)
# ==========================================
def transformar_dados(dados_brutos):
    """
    Limpa e filtra os dados, buscando apenas termos de interesse.
    """
    print("Iniciando Transformação...")
    dados_processados = []
    termos_chave = ['nomeação', 'nomear', 'exoneração', 'exonerar']
    
    for texto in dados_brutos:
        texto_lower = texto.lower()
        
        # Lógica de negócio: Filtrar apenas publicações com os termos-chave
        if any(termo in texto_lower for termo in termos_chave):
            
            # Classificar o tipo de movimentação
            tipo = "Nomeação" if "nomea" in texto_lower else "Exoneração"
            
            # Estruturar o dado limpo
            dado_limpo = {
                "data_processamento": datetime.now().strftime("%Y-%m-%d"),
                "tipo_movimentacao": tipo,
                "texto_publicacao": texto.strip()
            }
            dados_processados.append(dado_limpo)
            
    return pd.DataFrame(dados_processados)

# ==========================================
# 3. CARREGAMENTO (LOAD)
# ==========================================
def carregar_dados(df_processado, nome_banco="dados_governamentais.db"):
    """
    Carrega os dados transformados em um banco de dados SQLite.
    """
    print("Iniciando Carregamento...")
    if df_processado.empty:
        print("Nenhum dado relevante para carregar hoje.")
        return

    # Conecta ao SQLite (cria o arquivo se não existir)
    conn = sqlite3.connect(nome_banco)
    
    # Salva o DataFrame como uma tabela no banco de dados
    df_processado.to_sql('movimentacoes_pessoal', conn, if_exists='append', index=False)
    conn.close()
    print(f"Sucesso! {len(df_processado)} registros carregados no banco de dados.")

# ==========================================
# ORQUESTRAÇÃO DO PIPELINE
# ==========================================
if __name__ == "__main__":
    print("--- Iniciando Pipeline ETL ---")
    
    # Fluxo contínuo dos dados
    dados_extraidos = extrair_dados_dou()
    dados_transformados = transformar_dados(dados_extraidos)
    carregar_dados(dados_transformados)
    
    print("--- Pipeline ETL Finalizado ---") 

    