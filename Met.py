import sys
sys.stdout.reconfigure(encoding="utf-8")

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")

# ── Configuracao visual ────────────────────────────────────────────────────────
plt.rcParams.update({"font.family": "DejaVu Sans", "figure.dpi": 150})
CORES   = ["#2E86AB", "#A23B72", "#F18F01", "#C73E1D", "#44BBA4",
           "#E94F37", "#6B4226", "#393E41", "#F5A623", "#3B1F2B"]
FONTE   = "Fonte: SSPDS-CE / CVLI 2009 a 2025"
MUNICIP = ["Caucaia", "Sobral"]
ANOS    = [2024, 2025]


# ══════════════════════════════════════════════════════════════════════════════
# 1. LEITURA E FILTRO
# ══════════════════════════════════════════════════════════════════════════════
df_raw = pd.read_excel("CVLI_2009-a-2025.xlsx")
df_raw["Data"] = pd.to_datetime(df_raw["Data"], dayfirst=True, errors="coerce")
df_raw["Ano"]  = df_raw["Data"].dt.year

df = df_raw[
    df_raw["Município"].isin(MUNICIP) &
    df_raw["Ano"].isin(ANOS)
].copy()

print(f"Registros filtrados (Caucaia + Sobral | 2024-2025): {len(df)}")
print(df["Município"].value_counts().to_string())


# ══════════════════════════════════════════════════════════════════════════════
# 2. COLUNAS DERIVADAS
# ══════════════════════════════════════════════════════════════════════════════
df["Mes_Nome"] = df["Data"].dt.strftime("%b/%Y")
df["Hora_Num"] = pd.to_datetime(df["Hora"].astype(str), format="%H:%M:%S",
                                 errors="coerce").dt.hour
df["Idade da Vítima"] = pd.to_numeric(df["Idade da Vítima"], errors="coerce")


# ══════════════════════════════════════════════════════════════════════════════
# 3. FUNCOES AUXILIARES
# ══════════════════════════════════════════════════════════════════════════════
def tabela_freq(series, titulo):
    ft = series.value_counts(dropna=False).reset_index()
    ft.columns = ["Categoria", "Freq. Simples"]
    ft["Freq. Relativa (%)"] = (ft["Freq. Simples"] / len(series) * 100).round(2)
    print(f"\n--- {titulo} ---")
    print(ft.to_string(index=False))
    return ft

def salvar(fig, nome):
    fig.text(0.5, -0.02, FONTE, ha="center", fontsize=8, color="gray")
    plt.tight_layout()
    fig.savefig(nome, bbox_inches="tight")
    plt.close(fig)
    


# ══════════════════════════════════════════════════════════════════════════════
# 4. TABELAS DE FREQUENCIA
# ══════════════════════════════════════════════════════════════════════════════
print("\n" + "="*55)
print("TABELAS DE FREQUENCIA")
print("="*55)

tabela_freq(df["Natureza"],               "Natureza")
tabela_freq(df["Meio Empregado"],         "Meio Empregado")
tabela_freq(df["Gênero"],                "Genero")
tabela_freq(df["Escolaridade da Vítima"], "Escolaridade da Vitima")
tabela_freq(df["Raça da Vítima"],         "Raca da Vitima")
tabela_freq(df["Dia da Semana"],          "Dia da Semana")


# ===================================
# TABELAS CRUZADAS
# ==================================
print("\n" + "="*55)
print("TABELAS CRUZADAS")
print("="*55)

ct1 = pd.crosstab(df["Meio Empregado"], df["Gênero"], margins=True, margins_name= "Total")
print("\n--- Meio Empregado x Genero ---")
print(ct1.to_string())



ct2 = pd.crosstab(df["Escolaridade da Vítima"], df["Raça da Vítima"], margins=True)
print("\n--- Escolaridade da Vitima x Raca da Vitima ---")
print(ct2.to_string())


# =====================================================
# GRAFICOS DE SETOR
# =====================================================
for i, (col, titulo) in enumerate([
    ("Gênero",        "Grafico 1 - Genero"),
    ("Meio Empregado","Grafico 2 - Meio Empregado"),
], start=1):
    cnt = df[col].value_counts(dropna=True).head(8)
    fig, ax = plt.subplots(figsize=(7, 5))
    ax.pie(cnt, labels=cnt.index, autopct="%1.1f%%",
           colors=CORES[:len(cnt)], startangle=140,
           wedgeprops=dict(edgecolor="white", linewidth=1.2))
    ax.set_title(titulo, fontweight="bold", pad=12)
    salvar(fig, f"grafico_{i:02d}_setor_{col.lower().replace(' ','_')}.png")

# -------------------------
# GRAFICOS DE BARRA
# --------------------------
ordem_semana = ["Segunda","Terça","Quarta","Quinta","Sexta","Sábado","Domingo"]

for i, (col, titulo, rot) in enumerate([
    ("Dia da Semana",          "Grafico 3 - Dia da Semana",          20),
    ("Escolaridade da Vítima", "Grafico 4 - Escolaridade da Vitima", 30),
], start=3):
    cnt = df[col].value_counts(dropna=True)
    if col == "Dia da Semana": 
        cnt = cnt.reindex([d for d in ordem_semana if d in cnt.index])

    fig, ax = plt.subplots(figsize=(10, 5))
    bars = ax.bar(cnt.index.astype(str), cnt.values,
                  color=CORES[:len(cnt)], edgecolor="white")
    for bar in bars:
        ax.text(bar.get_x() + bar.get_width()/2,
                bar.get_height() + cnt.max()*0.01,
                str(int(bar.get_height())),
                ha="center", va="bottom", fontsize=8)
    ax.set_title(titulo, fontweight="bold", pad=12)
    ax.set_ylabel("Frequencia")
    ax.spines[["top","right"]].set_visible(False)
    plt.xticks(rotation=rot, ha="right")
    salvar(fig, f"grafico_{i:02d}_barra_{col.lower().replace(' ','_')[:20]}.png")


# ===========================
# GRAFICOS DE LINHA
# ===========================

# Mensal (apenas 2024-2025)
ordem_mes = df.dropna(subset=["Data"]).sort_values("Data")["Mes_Nome"].unique()
serie_mes = df.groupby("Mes_Nome").size().reindex(ordem_mes).fillna(0)

fig, ax = plt.subplots(figsize=(12, 4))
ax.plot(serie_mes.index, serie_mes.values, marker="o", color=CORES[0], linewidth=2)
ax.fill_between(range(len(serie_mes)), serie_mes.values, alpha=0.12, color=CORES[0])
ax.set_title("Grafico 5 - Evolucao Mensal de CVLI (Caucaia + Sobral | 2024-2025)",
             fontweight="bold", pad=12)
ax.set_ylabel("Ocorrencias")
ax.spines[["top","right"]].set_visible(False)
plt.xticks(range(len(serie_mes)), serie_mes.index, rotation=45, ha="right", fontsize=7)
salvar(fig, "grafico_05_linha_mensal.png")

# Anual (serie historica completa: Caucaia + Sobral 2009-2025)
df_hist  = df_raw[df_raw["Município"].isin(MUNICIP)].copy()
serie_ano = df_hist.groupby("Ano").size()

fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(serie_ano.index, serie_ano.values, marker="o", color=CORES[1], linewidth=2)
ax.fill_between(serie_ano.index, serie_ano.values, alpha=0.12, color=CORES[1])
ax.set_title("Grafico 6 - Evolucao Anual de CVLI (Caucaia + Sobral | 2009-2025)",
             fontweight="bold", pad=12)
ax.set_ylabel("Ocorrencias")
ax.spines[["top","right"]].set_visible(False)
plt.xticks(serie_ano.index, rotation=45)
salvar(fig, "grafico_06_linha_anual.png")

# Por hora do dia
serie_hora = df.groupby("Hora_Num").size().reindex(range(24), fill_value=0)

fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(serie_hora.index, serie_hora.values, marker="o", color=CORES[2], linewidth=2)
ax.fill_between(serie_hora.index, serie_hora.values, alpha=0.12, color=CORES[2])
ax.set_title("Grafico 7 - Distribuicao por Hora do Dia", fontweight="bold", pad=12)
ax.set_xlabel("Hora")
ax.set_ylabel("Ocorrencias")
ax.set_xticks(range(24))
ax.spines[["top","right"]].set_visible(False)
salvar(fig, "grafico_07_linha_hora.png")


# ========================================
# 9. MEDIDAS ESTATISTICAS — IDADE DA VITIMA
# ======================================
print("\n" + "="*55)
print("MEDIDAS ESTATISTICAS — IDADE DA VITIMA")
print("="*55)


idade = df["Idade da Vítima"].dropna()
q1, q2, q3 = np.percentile(idade, [25, 50, 75])
d1, d5, d9 = np.percentile(idade, [10, 50, 90])

medidas = {
    "N validos":           int(len(idade)),
    "Minimo":              round(idade.min(), 1),
    "Maximo":              round(idade.max(), 1),
    "Media":               round(idade.mean(), 2),
    "Mediana":             round(q2, 1),
    "Moda":                round(idade.mode().iloc[0], 1),
    "Desvio Padrao":       round(idade.std(), 2),
    "Variancia":           round(idade.var(), 2),
    "Coef. Variacao (%)":  round(idade.std() / idade.mean() * 100, 2),
    "Amplitude":           round(idade.max() - idade.min(), 1),
    "IQR (Q3-Q1)":         round(q3 - q1, 1),
    "Assimetria":          round(idade.skew(), 4),
    "Curtose":             round(idade.kurtosis(), 4),
    "Q1 (25%)":            round(q1, 1),
    "Q2 (50%)":            round(q2, 1),
    "Q3 (75%)":            round(q3, 1),
    "D1 (10%)":            round(d1, 1),
    "D5 (50%)":            round(d5, 1),
    "D9 (90%)":            round(d9, 1),
}

for k, v in medidas.items():
    print(f"  {k:<25s}: {v}")


# ===============================
# 10. BOXPLOT — IDADE DA VITIMA
#===============================
fig, ax = plt.subplots(figsize=(7, 5))
ax.boxplot(
    idade, vert=True, patch_artist=True,
    boxprops=dict(facecolor=CORES[0], color="navy", linewidth=1.5),
    medianprops=dict(color="orange", linewidth=2.5),
    whiskerprops=dict(color="navy", linewidth=1.5),
    capprops=dict(color="navy", linewidth=2),
    flierprops=dict(marker="o", color=CORES[3], alpha=0.4, markersize=4),
)
for label, val in [("Q1", q1), ("Mediana", q2), ("Media", idade.mean()), ("Q3", q3)]:
    ax.axhline(val, color="gray", linestyle="--", linewidth=0.7, alpha=0.5)
    ax.text(1.42, val, f"{label}: {val:.1f}", va="center", fontsize=9)

ax.set_title("Grafico 8 - Boxplot: Idade da Vitima", fontweight="bold", pad=12)
ax.set_ylabel("Idade (anos)")
ax.set_xticks([])
ax.spines[["top","right"]].set_visible(False)
salvar(fig, "grafico_08_boxplot_idade.png")

print("\n" + "="*55)
print(f"ANALISE CONCLUIDA — {len(df)} registros | Caucaia + Sobral | 2024-2025")
print("="*55)