# 🚀 Pipeline ETL com IA: Santander Dev Week 2023 & Monitoramento do DOU

## 📌 Sobre o Projeto
Este repositório concentra minhas soluções de **Pipeline ETL (Extração, Transformação e Carregamento)**, demonstrando a aplicação prática de Python e Ciência de Dados para resolver problemas reais de negócios.

## 🎯 O Desafio (Contexto de Negócios)**

Acompanhar publicações diárias no Diário Oficial da União é uma tarefa crítica para diversos setores, mas a leitura manual de milhares de páginas em busca de informações específicas é um processo lento, exaustivo e sujeito a falhas humanas. O desafio era encontrar uma forma de monitorar movimentações estratégicas de pessoal (como no Ministério da Previdência Social, INSS, Concursos ) sem depender da leitura "linha por linha" todos os dias.

### 🏛️ 1. Monitoramento do Diário Oficial da União (DOU)
Robô de automação e web scraping construído para monitorar atos de pessoal (Nomeações, Exonerações, Dispensas e Designações de Gsiste) na Casa Civil, Ministério da Previdência Social e INSS. 
* **Automação:** Configurado via GitHub Actions para rodar de forma 100% autônoma na nuvem todos os dias úteis.
* **Tecnologias:** Python, BeautifulSoup4, Requests, Pandas, SQLite e GitHub Actions.

### ⚙️ A Solução: Automação e Filtragem Inteligente

Para otimizar esse processo, desenvolvi um robô em Python capaz de varrer os textos do DOU e aplicar regras de negócio estritas. O script atua como um filtro cirúrgico estruturado nos seguintes passos:
 I.Rastreio de Palavras-Chave: O algoritmo analisa o texto bruto e identifica termos críticos predefinidos, focando exclusivamente em publicações que contenham "nomeação" e "exoneração".
 II. Estruturação de Dados: O que antes era um bloco de texto denso é transformado em dados tabulares. O script classifica o tipo de movimentação e registra a data do processamento.
 III.Armazenamento Seguro: As informações filtradas são automaticamente carregadas em um banco de dados estruturado, criando um histórico organizado e pronto para consultas ou integração com dashboards.


### 📊 2. Integração com IA (Santander Dev Week)
Pipeline que consome dados de clientes via API REST e utiliza a inteligência do GPT-4 (OpenAI) para gerar mensagens de marketing personalizadas em escala.

### 💡 Impacto e Visão Profissional

A verdadeira inovação não é apenas escrever um script, mas traduzir a necessidade de conformidade e monitoramento da empresa em uma solução ágil. Este projeto reduz horas de trabalho manual para uma execução de poucos segundos, mitigando o risco de perda de informações importantes e permitindo que os profissionais foquem na análise estratégica dos dados em vez da coleta operacional.
