import pandas as pd
import numpy as np

def analyze_dataset(filepath):
    """
    Analyse un dataset pour identifier les valeurs manquantes et les types de variables.
    
    Args:
        filepath (str): Chemin vers le fichier CSV
    """
    # Charger le dataset
    df = pd.read_csv(filepath)
    
    print("=" * 80)
    print("ANALYSE DU DATASET MADRID")
    print("=" * 80)
    print(f"\nNombre total de lignes: {len(df)}")
    print(f"Nombre total de colonnes: {len(df.columns)}")
    
    # Créer un DataFrame récapitulatif
    analysis = pd.DataFrame({
        'Colonne': df.columns,
        'Type': df.dtypes.values,
        'Valeurs_Manquantes': df.isnull().sum().values,
        'Pourcentage_Manquant': (df.isnull().sum().values / len(df) * 100).round(2),
        'Valeurs_Uniques': [df[col].nunique() for col in df.columns],
        'Exemples': [str(df[col].dropna().iloc[0]) if len(df[col].dropna()) > 0 else 'N/A' 
                     for col in df.columns]
    })
    
    # Trier par pourcentage de valeurs manquantes (décroissant)
    analysis = analysis.sort_values('Pourcentage_Manquant', ascending=False)
    
    print("\n" + "=" * 80)
    print("RÉSUMÉ PAR TYPE DE VARIABLE")
    print("=" * 80)
    
    # Catégoriser les types de variables
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    string_cols = df.select_dtypes(include=['object']).columns.tolist()
    bool_cols = df.select_dtypes(include=['bool']).columns.tolist()
    
    print(f"\nVariables numériques ({len(numeric_cols)}): int64, float64")
    print(f"Variables textuelles ({len(string_cols)}): object (string)")
    print(f"Variables booléennes ({len(bool_cols)}): bool")
    
    print("\n" + "=" * 80)
    print("DÉTAIL DES VALEURS MANQUANTES PAR COLONNE")
    print("=" * 80)
    print()
    
    # Afficher le tableau complet
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    print(analysis.to_string(index=False))
    
    # Statistiques supplémentaires
    print("\n" + "=" * 80)
    print("STATISTIQUES SUPPLÉMENTAIRES")
    print("=" * 80)
    
    total_missing = df.isnull().sum().sum()
    total_cells = df.shape[0] * df.shape[1]
    
    print(f"\nTotal de cellules manquantes: {total_missing:,}")
    print(f"Total de cellules: {total_cells:,}")
    print(f"Pourcentage global de données manquantes: {(total_missing/total_cells*100):.2f}%")
    
    # Colonnes avec plus de 50% de valeurs manquantes
    high_missing = analysis[analysis['Pourcentage_Manquant'] > 50]
    print(f"\nNombre de colonnes avec >50% de valeurs manquantes: {len(high_missing)}")
    if len(high_missing) > 0:
        print("Colonnes concernées:")
        for col in high_missing['Colonne'].values:
            pct = high_missing[high_missing['Colonne'] == col]['Pourcentage_Manquant'].values[0]
            print(f"  - {col}: {pct}%")
    
    # Sauvegarder le rapport
    output_file = filepath.replace('.csv', '_analysis_report.csv')
    analysis.to_csv(output_file, index=False)
    print(f"\n✓ Rapport sauvegardé dans: {output_file}")
    
    return analysis

if __name__ == "__main__":
    # Chemin vers le fichier
    filepath = "/Users/antoinegobbe/Desktop/Plateforme/apartment-hunter/data/houses_Madrid.csv"
    
    # Exécuter l'analyse
    analysis_df = analyze_dataset(filepath)
