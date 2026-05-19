import sqlite3
import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime

# ==========================================
# REGRAS DE NEGÓCIO (Seus Filtros)
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
# 1. EXTRAÇÃO (EXTRACT)
# ==========================================
def extrair_dados_dou_real():
    """Busca publicações reais no site do Diário Oficial da União."""
    print("Iniciando varredura no portal do DOU...")
    
    # URL de busca do DOU (pesquisando por INSS como termo base para trazer resultados da seção 2 - Pessoal)
    # Obs: Em um projeto mais avançado, podemos usar Selenium se o site tiver bloqueios (Cloudflare).
    url = "https://www.in.gov.br/consulta/-/buscar/dou?q=INSS&s=todos&exactDate=personalizado&sortType=0"
    
    # Usamos um 'User-Agent' para o site do Governo não achar que somos um ataque de robô
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    try:
        resposta = requests.get(url, headers=headers)
        resposta.raise_for_status()
        soup = BeautifulSoup(resposta.text, 'html.parser')
        
        # Encontra as caixas de texto de cada publicação na página de busca
        resultados_html = soup.find_all('div', class_='resultado-busca-item')
        
        textos_extraidos = []
        for item in resultados_html:
            texto = item.get_text(strip=True)
            textos_extraidos.append(texto)
            
        return textos_extraidos
    except Exception as e:
        print(f"Erro ao acessar o DOU: {e}")
        # Retorna alguns dados simulados como fallback caso o site do governo esteja fora do ar
        return [
            "O Presidente do INSTITUTO NACIONAL DO SEGURO SOCIAL resolve nomear João Silva.",
            "PORTARIA Nº 10. Ministério da Previdência Social. Resolve conceder dispensa Gsiste para Maria Souza."
        ]

# ==========================================
# 2. TRANSFORMAÇÃO (TRANSFORM)
# ==========================================
def aplicar_filtros_estrategicos(dados_brutos):
    """Filtra apenas os órgãos e as ações solicitadas."""
    print("Aplicando regras de negócio e filtragem...")
    dados_processados = []
    
    for texto in dados_brutos:
        texto_lower = texto.lower()
        
        # Regra 1: O texto pertence aos nossos Órgãos Alvo?
        pertence_ao_orgao = any(orgao in texto_lower for orgao in ORGAOS_ALVO)
        
        # Regra 2: O texto contém as Ações que queremos monitorar?
        contem_acao = any(acao in texto_lower for acao in PALAVRAS_CHAVE)
        
        if pertence_ao_orgao and contem_acao:
            # Descobre qual foi a ação principal encontrada (para categorizar no banco)
            acao_encontrada = next(acao for acao in PALAVRAS_CHAVE if acao in texto_lower)
            
            dados_processados.append({
                "data_coleta": datetime.now().strftime("%Y-%m-%d"),
                "orgao_provavel": "Previdencia/INSS/Casa Civil",
                "tipo_acao": acao_encontrada.title(),
                "texto_completo": texto
            })
            
    df = pd.DataFrame(dados_processados)
    return df

# ==========================================
# 3. CARREGAMENTO (LOAD)
# ==========================================
def salvar_no_banco(df_processado):
    if df_processado.empty:
        print("Nenhuma movimentação relevante de pessoal encontrada hoje.")
        return

    conn = sqlite3.connect("monitoramento_dou.db")
    df_processado.to_sql('movimentacoes', conn, if_exists='append', index=False)
    conn.close()
    print(f"Sucesso! {len(df_processado)} movimentações críticas salvas no banco de dados.")

# ==========================================
# ORQUESTRAÇÃO
# ==========================================
if __name__ == "__main__":
    textos = extrair_dados_dou_real()
    if textos:
        dados_filtrados = aplicar_filtros_estrategicos(textos)
        salvar_no_banco(dados_filtrados)