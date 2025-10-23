import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter

# Carrega dados de candles (exemplo CSV)
df = pd.read_csv("candles.csv")

# Cria colunas de variação
df["variation"] = df["close"] - df["open"]
df["direction"] = np.where(df["variation"] > 0, "B", "S")  # B = alta, S = baixa

# Identifica padrões de 3 candles seguidos
patterns = []
for i in range(len(df) - 3):
    seq = "".join(df["direction"].iloc[i:i+3])
    patterns.append(seq)

# Conta frequência dos padrões
counts = Counter(patterns)
print("\nPadrões encontrados:\n")
for k, v in counts.items():
    print(f"{k}: {v} vezes")

# Plota gráfico simples
plt.figure(figsize=(10,5))
plt.plot(df["close"], label="Preço de Fechamento")
plt.legend()
plt.title("Fechamento dos Candles")
plt.show()
