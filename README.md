# 🔍 CVLI-EDA: Análise Exploratória de Crimes Violentos Letais Intencionais no Ceará

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-2.x-150458?style=for-the-badge&logo=pandas&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-1.x-013243?style=for-the-badge&logo=numpy&logoColor=white)
![Matplotlib](https://img.shields.io/badge/Matplotlib-3.x-11557C?style=for-the-badge&logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Concluído-brightgreen?style=for-the-badge)

**Uma análise estatística rigorosa dos registos de CVLI nos municípios de Caucaia e Sobral (2024–2025), com série histórica desde 2009.**

*Fonte dos dados: Secretaria da Segurança Pública e Defesa Social do Ceará (SSPDS-CE)*

</div>

---

## 📋 Descrição do Projeto

Este projeto conduz uma **Análise Exploratória de Dados (EDA)** completa sobre os registos de **Crimes Violentos Letais Intencionais (CVLI)** do estado do Ceará, disponibilizados pela **SSPDS-CE** para o período de 2009 a 2025.

O foco central da análise recai sobre os municípios de **Caucaia** e **Sobral** — dois dos principais centros urbanos do interior e da região metropolitana cearense — com granularidade temporal nos anos de **2024 e 2025**, complementada por uma **retrospectiva histórica de 16 anos** para contextualizar tendências de longo prazo.

### Objetivos

- 📌 Caracterizar o perfil sociodemográfico das vítimas (género, raça, escolaridade, idade).
- 📌 Identificar padrões temporais (hora do dia, dia da semana, mês e ano).
- 📌 Mapear os meios empregados e a natureza dos crimes registados.
- 📌 Produzir estatísticas descritivas robustas para subsidiar análises criminológicas e de segurança pública.

---

## 🔬 Metodologia e Abordagem

O pipeline analítico segue um fluxo estruturado em quatro etapas:

### 1. Ingestão, Limpeza e Filtragem

```python
df_raw = pd.read_excel("CVLI_2009-a-2025.xlsx")
df_raw["Data"] = pd.to_datetime(df_raw["Data"], dayfirst=True, errors="coerce")
```

- Leitura do ficheiro `.xlsx` com tratamento robusto de datas (`dayfirst=True`, `errors="coerce"`).
- Filtragem espacial por município (`Caucaia`, `Sobral`) e temporal por ano (`2024`, `2025`).
- Remoção implícita de registos com datas inválidas através de `coerce`.

### 2. Engenharia de Features (*Feature Engineering*)

Três variáveis derivadas são construídas a partir das colunas brutas:

| Feature Criada | Origem | Transformação |
|---|---|---|
| `Mes_Nome` | `Data` | Formato `Mmm/AAAA` via `strftime` |
| `Hora_Num` | `Hora` | Extração da hora inteira (`int`) |
| `Idade da Vítima` | `Idade da Vítima` | Coerção numérica (`pd.to_numeric`) |

### 3. Análise de Frequências e Tabelas Cruzadas

Distribuições univariadas são calculadas para seis variáveis categóricas-chave:

> `Natureza` · `Meio Empregado` · `Gênero` · `Escolaridade` · `Raça` · `Dia da Semana`

Adicionalmente, são geradas **tabelas de contingência** (crosstabs) para revelar interações entre variáveis:
- **Meio Empregado × Género** — análise da modalidade do crime por género da vítima.
- **Escolaridade × Raça** — exploração de interseccionalidade socioeconómica.

### 4. Estatística Descritiva — Idade da Vítima

A variável quantitativa contínua `Idade da Vítima` é caracterizada por um conjunto completo de medidas:

| Categoria | Métricas |
|---|---|
| **Tendência Central** | Média, Mediana, Moda |
| **Dispersão** | Desvio Padrão, Variância, Coeficiente de Variação, Amplitude, IQR |
| **Posição** | Q1, Q2, Q3 (Quartis) · D1, D5, D9 (Decis) |
| **Forma da Distribuição** | Assimetria (*Skewness*), Curtose (*Kurtosis*) |

---

## 📊 Visualizações Geradas

O script produz **8 visualizações** exportadas automaticamente como ficheiros `.png`:

| Nº | Tipo | Título | Ficheiro |
|---|---|---|---|
| 1 | 🟠 Setor | Distribuição por Género | `grafico_01_setor_gênero.png` |
| 2 | 🟠 Setor | Distribuição por Meio Empregado | `grafico_02_setor_meio_empregado.png` |
| 3 | 📊 Barras | Ocorrências por Dia da Semana | `grafico_03_barra_dia_da_semana.png` |
| 4 | 📊 Barras | Ocorrências por Escolaridade da Vítima | `grafico_04_barra_escolaridade_da_vít.png` |
| 5 | 📈 Linha | Evolução Mensal — 2024/2025 | `grafico_05_linha_mensal.png` |
| 6 | 📈 Linha | Evolução Anual — 2009/2025 | `grafico_06_linha_anual.png` |
| 7 | 📈 Linha | Distribuição por Hora do Dia | `grafico_07_linha_hora.png` |
| 8 | 🎯 Boxplot | Idade da Vítima | `grafico_08_boxplot_idade.png` |

> Todos os gráficos incluem anotações de valores, paleta de cores consistente e rodapé com indicação da fonte (SSPDS-CE).

---

## 🛠️ Tecnologias Utilizadas

```
pandas      — Manipulação e análise de dados tabulares
numpy       — Computação numérica e cálculo de percentis
matplotlib  — Visualização de dados e exportação de gráficos
openpyxl    — Leitura de ficheiros Excel (.xlsx)
```

---

## ▶️ Como Executar o Projeto

### Pré-requisitos

- Python **3.10+** instalado
- Ficheiro de dados `CVLI_2009-a-2025.xlsx` na raiz do projeto (fonte: SSPDS-CE)

### Passo a Passo

**1. Clonar o repositório**
```bash
git clone https://github.com/seu-usuario/cvli-eda-ceara.git
cd cvli-eda-ceara
```

**2. Criar e ativar um ambiente virtual**
```bash
# Linux / macOS
python -m venv .venv
source .venv/bin/activate

# Windows
python -m venv .venv
.venv\Scripts\activate
```

**3. Instalar as dependências**
```bash
pip install -r requirements.txt
```

**4. Adicionar o ficheiro de dados**
```bash
# Coloque o ficheiro Excel na raiz do projeto:
# CVLI_2009-a-2025.xlsx
```

**5. Executar o script principal**
```bash
python Met.py
```

> ✅ O script imprime as tabelas de frequência e estatísticas no terminal e exporta os 8 gráficos `.png` no diretório raiz.

---

## 📁 Estrutura do Projeto

```
cvli-eda-ceara/
│
├── Met.py                          # Script principal de análise
├── requirements.txt                # Dependências do projeto
├── CVLI_2009-a-2025.xlsx           # Dados brutos (não incluído no repositório)
├── README.md                       # Documentação do projeto
│
└── outputs/                        # Gráficos gerados (após execução)
    ├── grafico_01_setor_gênero.png
    ├── grafico_02_setor_meio_empregado.png
    ├── grafico_03_barra_dia_da_semana.png
    ├── grafico_04_barra_escolaridade_da_vít.png
    ├── grafico_05_linha_mensal.png
    ├── grafico_06_linha_anual.png
    ├── grafico_07_linha_hora.png
    └── grafico_08_boxplot_idade.png
```

---

## ⚖️ Licença

Este projeto está licenciado sob a **Licença MIT**. Consulte o ficheiro [`LICENSE`](LICENSE) para mais detalhes.

---

## 👤 Autor

<div align="center">

**Caio Alves**
*Estudante de Ciência da Computação | Apaixonado por IA e Análise de Dados*

[![GitHub](https://img.shields.io/badge/GitHub-CaioAllvs-181717?style=for-the-badge&logo=github)](https://github.com/seu-usuario)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-CaioAlves-0A66C2?style=for-the-badge&logo=linkedin)](https://linkedin.com/in/seu-perfil)

</div>

---

<div align="center">
<sub>Dados: SSPDS-CE / CVLI 2009–2025 · Análise realizada com fins académicos e de investigação.</sub>
</div>
