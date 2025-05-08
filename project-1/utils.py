import matplotlib.pyplot as plt

def plot_barras_categoricas(df, min_sup=0.4):
    """
    Plota gráficos de barras para variáveis categóricas com coloração condicional por proporção.

    Parâmetros:
    - df: DataFrame contendo apenas variáveis categóricas.
    - min_usp: limite inferior da proporção para coloração (padrão: 0.4).
    """
    num_cols = len(df.columns)
    linhas = (num_cols // 5) + (1 if num_cols % 5 else 0)
    
    fig, axes = plt.subplots(linhas, 5, figsize=(20, 5 * linhas))
    axes = axes.flatten()

    for idx, col in enumerate(df.columns):
        ax = axes[idx]
        total = len(df)
        counts = df[col].value_counts(normalize=True)

        for cat, prop in counts.items():
            color = 'red' if prop < min_sup else 'blue'
            ax.bar(cat, prop, color=color)
            ax.text(cat, prop + 0.01, f'{prop:.2%}', ha='center', va='bottom', fontsize=10)

        ax.set_title(col)
        ax.set_ylim(0, 1)
        ax.set_ylabel('Proporção')

    # Remove eixos extras
    for i in range(num_cols, len(axes)):
        fig.delaxes(axes[i])

    plt.tight_layout()
    plt.show()
