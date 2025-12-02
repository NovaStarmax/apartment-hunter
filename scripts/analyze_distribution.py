import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

def analyze_column_distribution(filepath, column_name, save_plot=True):
    """
    Analyse la distribution d'une colonne et identifie les outliers.
    
    Args:
        filepath (str): Chemin vers le fichier CSV
        column_name (str): Nom de la colonne à analyser
        save_plot (bool): Si True, sauvegarde les graphiques
    """
    # Charger le dataset
    df = pd.read_csv(filepath)
    
    # Vérifier que la colonne existe
    if column_name not in df.columns:
        print(f"❌ Erreur: La colonne '{column_name}' n'existe pas dans le dataset.")
        print(f"Colonnes disponibles: {', '.join(df.columns)}")
        return
    
    # Extraire la colonne
    data = df[column_name].dropna()
    
    if len(data) == 0:
        print(f"❌ Erreur: La colonne '{column_name}' ne contient aucune valeur non-nulle.")
        return
    
    print("=" * 80)
    print(f"ANALYSE DE DISTRIBUTION: {column_name}")
    print("=" * 80)
    
    # Déterminer le type de la colonne
    col_type = df[column_name].dtype
    print(f"\nType de variable: {col_type}")
    print(f"Nombre de valeurs non-nulles: {len(data)}")
    print(f"Nombre de valeurs manquantes: {df[column_name].isnull().sum()}")
    
    # Analyse selon le type de variable
    if np.issubdtype(col_type, np.number):
        analyze_numeric_column(data, column_name, save_plot)
    else:
        analyze_categorical_column(data, column_name, save_plot)

def analyze_numeric_column(data, column_name, save_plot):
    """Analyse une colonne numérique."""
    
    print("\n" + "-" * 80)
    print("STATISTIQUES DESCRIPTIVES")
    print("-" * 80)
    
    stats_dict = {
        'Moyenne': data.mean(),
        'Médiane': data.median(),
        'Écart-type': data.std(),
        'Minimum': data.min(),
        'Q1 (25%)': data.quantile(0.25),
        'Q2 (50%)': data.quantile(0.50),
        'Q3 (75%)': data.quantile(0.75),
        'Maximum': data.max(),
        'Étendue': data.max() - data.min()
    }
    
    for stat, value in stats_dict.items():
        print(f"{stat:20s}: {value:,.2f}")
    
    # Détection des outliers avec la méthode IQR
    print("\n" + "-" * 80)
    print("DÉTECTION DES OUTLIERS (Méthode IQR)")
    print("-" * 80)
    
    Q1 = data.quantile(0.25)
    Q3 = data.quantile(0.75)
    IQR = Q3 - Q1
    
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    
    outliers = data[(data < lower_bound) | (data > upper_bound)]
    
    print(f"\nQ1 (25%): {Q1:,.2f}")
    print(f"Q3 (75%): {Q3:,.2f}")
    print(f"IQR: {IQR:,.2f}")
    print(f"Limite inférieure: {lower_bound:,.2f}")
    print(f"Limite supérieure: {upper_bound:,.2f}")
    print(f"\nNombre d'outliers: {len(outliers)} ({len(outliers)/len(data)*100:.2f}%)")
    
    if len(outliers) > 0:
        print(f"Valeurs outliers (min-max): {outliers.min():,.2f} - {outliers.max():,.2f}")
        print(f"\nPremiers outliers détectés:")
        print(outliers.head(10).to_string())
    
    # Détection des outliers avec Z-score
    print("\n" + "-" * 80)
    print("DÉTECTION DES OUTLIERS (Méthode Z-score)")
    print("-" * 80)
    
    z_scores = np.abs(stats.zscore(data))
    outliers_z = data[z_scores > 3]
    
    print(f"Nombre d'outliers (|z| > 3): {len(outliers_z)} ({len(outliers_z)/len(data)*100:.2f}%)")
    
    # Visualisations
    if save_plot:
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle(f'Distribution de {column_name}', fontsize=16, fontweight='bold')
        
        # 1. Histogramme
        axes[0, 0].hist(data, bins=50, edgecolor='black', alpha=0.7, color='skyblue')
        axes[0, 0].axvline(data.mean(), color='red', linestyle='--', label=f'Moyenne: {data.mean():.2f}')
        axes[0, 0].axvline(data.median(), color='green', linestyle='--', label=f'Médiane: {data.median():.2f}')
        axes[0, 0].set_xlabel(column_name)
        axes[0, 0].set_ylabel('Fréquence')
        axes[0, 0].set_title('Histogramme')
        axes[0, 0].legend()
        axes[0, 0].grid(True, alpha=0.3)
        
        # 2. Box plot
        box = axes[0, 1].boxplot(data, vert=True, patch_artist=True)
        box['boxes'][0].set_facecolor('lightblue')
        axes[0, 1].set_ylabel(column_name)
        axes[0, 1].set_title('Box Plot (avec outliers)')
        axes[0, 1].grid(True, alpha=0.3)
        
        # 3. Distribution cumulée
        sorted_data = np.sort(data)
        cumulative = np.arange(1, len(sorted_data) + 1) / len(sorted_data)
        axes[1, 0].plot(sorted_data, cumulative, linewidth=2, color='purple')
        axes[1, 0].set_xlabel(column_name)
        axes[1, 0].set_ylabel('Probabilité cumulée')
        axes[1, 0].set_title('Fonction de Distribution Cumulée')
        axes[1, 0].grid(True, alpha=0.3)
        
        # 4. Q-Q Plot (normalité)
        stats.probplot(data, dist="norm", plot=axes[1, 1])
        axes[1, 1].set_title('Q-Q Plot (Test de normalité)')
        axes[1, 1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        # Sauvegarder
        output_file = f'/Users/antoinegobbe/Desktop/Plateforme/apartment-hunter/data/{column_name}_distribution.png'
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"\n✓ Graphiques sauvegardés dans: {output_file}")
        plt.close()
    
    # Recommandations
    print("\n" + "-" * 80)
    print("RECOMMANDATIONS")
    print("-" * 80)
    
    if len(outliers) > len(data) * 0.05:
        print(f"⚠️  Attention: {len(outliers)/len(data)*100:.1f}% d'outliers détectés (>5%)")
        print("   → Considérer un filtrage ou une transformation des données")
    
    if data.std() / data.mean() > 1:
        print(f"⚠️  Forte variabilité détectée (CV = {data.std()/data.mean():.2f})")
        print("   → Considérer une transformation logarithmique")
    
    print(f"\n💡 Pour filtrer les outliers, vous pouvez utiliser:")
    print(f"   df = df[(df['{column_name}'] >= {lower_bound:.2f}) & (df['{column_name}'] <= {upper_bound:.2f})]")

def analyze_categorical_column(data, column_name, save_plot):
    """Analyse une colonne catégorielle."""
    
    print("\n" + "-" * 80)
    print("STATISTIQUES DESCRIPTIVES")
    print("-" * 80)
    
    value_counts = data.value_counts()
    
    print(f"Nombre de catégories uniques: {len(value_counts)}")
    print(f"Catégorie la plus fréquente: {value_counts.index[0]}")
    print(f"Fréquence max: {value_counts.iloc[0]} ({value_counts.iloc[0]/len(data)*100:.2f}%)")
    
    print("\n" + "-" * 80)
    print("DISTRIBUTION DES VALEURS (Top 20)")
    print("-" * 80)
    
    top_20 = value_counts.head(20)
    for idx, (value, count) in enumerate(top_20.items(), 1):
        pct = count / len(data) * 100
        print(f"{idx:2d}. {str(value):40s}: {count:5d} ({pct:5.2f}%)")
    
    # Visualisation
    if save_plot and len(value_counts) <= 50:
        fig, axes = plt.subplots(1, 2, figsize=(15, 6))
        fig.suptitle(f'Distribution de {column_name}', fontsize=16, fontweight='bold')
        
        # Bar plot (top 20)
        top_20.plot(kind='bar', ax=axes[0], color='steelblue', edgecolor='black')
        axes[0].set_xlabel('Valeurs')
        axes[0].set_ylabel('Fréquence')
        axes[0].set_title(f'Top 20 des valeurs')
        axes[0].tick_params(axis='x', rotation=45)
        axes[0].grid(True, alpha=0.3, axis='y')
        
        # Pie chart (top 10)
        top_10 = value_counts.head(10)
        axes[1].pie(top_10.values, labels=top_10.index, autopct='%1.1f%%', startangle=90)
        axes[1].set_title('Top 10 (en %)')
        
        plt.tight_layout()
        
        output_file = f'/Users/antoinegobbe/Desktop/Plateforme/apartment-hunter/data/{column_name}_distribution.png'
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"\n✓ Graphiques sauvegardés dans: {output_file}")
        plt.close()

if __name__ == "__main__":
    # Chemin vers le fichier
    filepath = "/Users/antoinegobbe/Desktop/Plateforme/apartment-hunter/data/houses_Madrid.csv"
    
    # EXEMPLES D'UTILISATION
    
    # Exemple 1: Analyser le prix d'achat
    print("\n" + "="*80)
    print("ANALYSE 1: Prix d'achat")
    print("="*80)
    analyze_column_distribution(filepath, 'buy_price')
    
    # Exemple 2: Analyser la surface construite
    # print("\n" + "="*80)
    # print("ANALYSE 2: Surface construite")
    # print("="*80)
    # analyze_column_distribution(filepath, 'sq_mt_built')
    
    # Exemple 3: Analyser le nombre de chambres
    # print("\n" + "="*80)
    # print("ANALYSE 3: Nombre de chambres")
    # print("="*80)
    # analyze_column_distribution(filepath, 'n_rooms')
    
    # Exemple 4: Analyser les quartiers (catégoriel)
    # print("\n" + "="*80)
    # print("ANALYSE 4: Quartiers")
    # print("="*80)
    # analyze_column_distribution(filepath, 'neighborhood_id')
