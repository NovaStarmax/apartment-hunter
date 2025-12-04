import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


def plot_boxplots(df):
    fig, axes = plt.subplots(1, 4, figsize=(16, 4))
    fig.suptitle("Boxplots - Identification des outliers", fontsize=16)

    for i, col in enumerate(["buy_price", "sq_mt_built", "n_rooms", "n_bathrooms"]):
        sns.boxplot(y=df[col], ax=axes[i], color="skyblue")
        axes[i].set_title(col)
        axes[i].set_ylabel("Valeur")

    plt.tight_layout()
    plt.show()


def remove_outliers_iqr(df, factor=1.5, logs=False):
    """
    Supprime les outliers en utilisant la méthode IQR
    factor=1.5 : standard (modéré)
    factor=3.0 : conservateur (garde plus de données)
    """
    df_clean = df.copy()

    # Sélectionne automatiquement toutes les colonnes numériques
    numeric_columns = df_clean.select_dtypes(include=["number"]).columns

    for col in numeric_columns:
        Q1 = df_clean[col].quantile(0.25)
        Q3 = df_clean[col].quantile(0.75)
        IQR = Q3 - Q1

        lower_bound = Q1 - factor * IQR
        upper_bound = Q3 + factor * IQR

        df_clean = df_clean[
            (df_clean[col] >= lower_bound) & (df_clean[col] <= upper_bound)
        ]

    if logs:
        print(f"📊 Avant : {len(df)} lignes")
        print(f"✅ Après : {len(df_clean)} lignes")
        print(
            f"🗑️  Supprimés : {len(df) - len(df_clean)} lignes ({100*(len(df)-len(df_clean))/len(df):.1f}%)"
        )

    return df_clean


def _split_features_target(df):
    target_column = "buy_price"
    X = df.drop(columns=[target_column])
    y = df[target_column]
    return X, y


def train_decision_tree_regressor(df, test_size=0.2, random_state=42, **dt_params):
    X, y = _split_features_target(df)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state
    )

    model = DecisionTreeRegressor(**dt_params)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    r2 = r2_score(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)

    metrics = {"R2 Score": r2, "Mean Absolute Error": mae, "Mean Squared Error": mse}

    return model, metrics


def train_and_evaluate_model(
    df,
    model,
    columns_to_scale=None,  # ← NOUVEAU : spécifiez les colonnes à scaler
    test_size=0.2,
    random_state=42,
    plot=True,
):
    """
    Pipeline complète : préparation, entraînement, évaluation, visualisation

    Args:
        df: DataFrame avec les données
        model: Modèle sklearn (ex: DecisionTreeRegressor, RandomForestRegressor)
        columns_to_scale: Liste des colonnes à normaliser (None = toutes les colonnes)
                         Ex: ['sq_mt_built'] pour scaler uniquement la surface
        test_size: Proportion du test set
        random_state: Seed pour la reproductibilité
        plot: Afficher les graphiques

    Returns:
        pipeline: Pipeline entraînée (prête pour la production)
        metrics: Dictionnaire avec toutes les métriques

    Exemples:
        # Scaler toutes les colonnes
        pipeline, metrics = train_and_evaluate_model(df, model)

        # Scaler uniquement la surface
        pipeline, metrics = train_and_evaluate_model(df, model, columns_to_scale=['sq_mt_built'])

        # Ne rien scaler (utile pour les arbres)
        pipeline, metrics = train_and_evaluate_model(df, model, columns_to_scale=[])
    """
    # 1. PRÉPARATION DES DONNÉES
    X, y = _split_features_target(df)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state
    )

    # 2. CRÉATION DE LA PIPELINE AVEC PREPROCESSING INTELLIGENT
    if columns_to_scale is None:
        # Par défaut : scaler TOUTES les colonnes
        pipeline = Pipeline([("scaler", StandardScaler()), ("model", model)])
    elif len(columns_to_scale) == 0:
        # Si liste vide : NE RIEN scaler
        pipeline = Pipeline([("model", model)])
    else:
        # Scaler UNIQUEMENT les colonnes spécifiées
        columns_not_to_scale = [col for col in X.columns if col not in columns_to_scale]

        preprocessor = ColumnTransformer(
            [
                ("scaler", StandardScaler(), columns_to_scale),
                ("passthrough", "passthrough", columns_not_to_scale),
            ]
        )

        pipeline = Pipeline([("preprocessor", preprocessor), ("model", model)])

    # 3. ENTRAÎNEMENT
    pipeline.fit(X_train, y_train)

    # 4. PRÉDICTIONS
    y_pred_train = pipeline.predict(X_train)
    y_pred_test = pipeline.predict(X_test)

    # 5. MÉTRIQUES
    metrics = {
        "train": {
            "R2": r2_score(y_train, y_pred_train),
            "MAE": mean_absolute_error(y_train, y_pred_train),
            "RMSE": np.sqrt(mean_squared_error(y_train, y_pred_train)),
        },
        "test": {
            "R2": r2_score(y_test, y_pred_test),
            "MAE": mean_absolute_error(y_test, y_pred_test),
            "RMSE": np.sqrt(mean_squared_error(y_test, y_pred_test)),
        },
    }

    # 6. CROSS-VALIDATION
    cv_scores = cross_val_score(pipeline, X, y, cv=5, scoring="r2")
    metrics["cv_r2_mean"] = cv_scores.mean()
    metrics["cv_r2_std"] = cv_scores.std()

    # 7. VISUALISATIONS
    if plot:
        fig, axes = plt.subplots(1, 2, figsize=(14, 5))

        # Plot 1 : Prédictions vs Réalité
        axes[0].scatter(y_test, y_pred_test, alpha=0.5, edgecolors="k", linewidths=0.5)
        axes[0].plot(
            [y_test.min(), y_test.max()],
            [y_test.min(), y_test.max()],
            "r--",
            lw=2,
            label="Prédiction parfaite",
        )
        axes[0].set_xlabel("Prix réels (€)")
        axes[0].set_ylabel("Prix prédits (€)")
        axes[0].set_title(f'Prédictions vs Réalité (R² = {metrics["test"]["R2"]:.3f})')
        axes[0].legend()
        axes[0].grid(alpha=0.3)

        # Plot 2 : Distribution des erreurs
        residuals = y_test - y_pred_test
        axes[1].hist(residuals, bins=30, edgecolor="black", alpha=0.7)
        axes[1].axvline(
            0, color="red", linestyle="--", linewidth=2, label="Erreur nulle"
        )
        axes[1].set_xlabel("Erreur de prédiction (€)")
        axes[1].set_ylabel("Fréquence")
        axes[1].set_title("Distribution des erreurs")
        axes[1].legend()
        axes[1].grid(alpha=0.3)

        plt.tight_layout()
        plt.show()

    # 8. AFFICHAGE DES MÉTRIQUES
    print("📊 RÉSULTATS D'ENTRAÎNEMENT")
    print(f"Train R² : {metrics['train']['R2']:.3f}")
    print(f"Train MAE : {metrics['train']['MAE']:,.0f} €")
    print(f"Train RMSE : {metrics['train']['RMSE']:,.0f} €")
    print("\n📊 RÉSULTATS DE TEST")
    print(f"Test R² : {metrics['test']['R2']:.3f}")
    print(f"Test MAE : {metrics['test']['MAE']:,.0f} €")
    print(f"Test RMSE : {metrics['test']['RMSE']:,.0f} €")
    print("\n🔄 CROSS-VALIDATION")
    print(
        f"R² moyen (CV) : {metrics['cv_r2_mean']:.3f} (+/- {metrics['cv_r2_std']:.3f})"
    )

    # Détection d'overfitting
    if metrics["train"]["R2"] - metrics["test"]["R2"] > 0.1:
        print("\n⚠️  ATTENTION : Possibilité d'overfitting (écart train/test > 0.1)")

    return pipeline, metrics
