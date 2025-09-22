# 🍚 Compteur Automatique de Grains de Riz

Ce projet implémente une **chaîne de traitement d'images robuste** en Python pour compter automatiquement le nombre de grains de riz dans une image, même en présence de différents types de bruits (fond non-uniforme, bruit "poivre et sel", etc.).

Développé dans le cadre du cours **Traitement d'Images (SIM28)** à l'**Institut Francophone International (IFI), VNU, Vietnam**.

---

## 🎯 Objectif du Projet

Créer un algorithme unique capable de traiter **4 types d'images** présentant des défis variés :
1.  Image de référence (fond homogène).
2.  Image avec bruit "poivre et sel".
3.  Image à fond non-uniforme (variation d'éclairage sinusoïdale).
4.  Image à grains sombres sur fond clair.

L'algorithme doit être **entièrement automatisé** : aucun paramètre ne doit être ajusté manuellement par l'utilisateur en fonction de l'image d'entrée.

---

## 🛠️ Chaîne de Traitement

L'algorithme suit une séquence de 4 étapes clés :

1.  **Pré-traitement : Réduction du Bruit**
    *   **Technique :** `Filtre Médian` (noyau 5x5).
    *   **Justification :** Élimine efficacement le bruit impulsionnel ("poivre et sel") tout en préservant les contours nets des grains.

2.  **Segmentation : Séparation des Objets**
    *   **Technique :** `Seuillage Adaptatif Gaussien` (`cv2.ADAPTIVE_THRESH_GAUSSIAN_C`).
    *   **Paramètres :** `blockSize=11`, `C=2`.
    *   **Justification :** Calcule un seuil local pour chaque pixel, ce qui est essentiel pour gérer les variations d'éclairage du fond (ex: image sinusoïdale).

3.  **Post-traitement : Nettoyage du Masque**
    *   **Techniques :**
        *   `Ouverture Morphologique` (noyau 2x2) : Supprime les petits artefacts de bruit.
        *   `Fermeture Morphologique` (noyau 2x2) : Comble les petits trous à l'intérieur des grains pour les rendre solides.
    *   **Justification :** Améliore la qualité du masque binaire avant le comptage final.

4.  **Analyse : Comptage des Objets**
    *   **Technique :** `Étiquetage des Composantes Connexes` (`cv2.connectedComponentsWithStats`).
    *   **Paramètre :** `connectivité=8`, `aire_minimale=50 pixels`.
    *   **Justification :** Identifie chaque grain comme une région distincte. Le filtrage par aire élimine les derniers résidus de bruit.

---

## 📊 Résultats

| Type d'Image                 | Résultat du Comptage | Analyse                                                                 |
| ---------------------------- | -------------------- | ----------------------------------------------------------------------- |
| **Référence (Fond Homogène)**| 110 grains           | ✅ Résultat optimal. Sert de baseline.                                  |
| **Bruit "Poivre et Sel"**    | 110 grains           | ✅ Excellent. Le filtre médian a parfaitement éliminé le bruit.         |
| **Fond Non-Uniforme**        | 54 grains            | ⚠️ Mitigé. Le seuillage adaptatif a supprimé des grains dans les zones sombres. |
| **Grains Sombres**           | 80 grains            | ❌ Échec partiel. Le seuillage adaptatif standard est inadapté aux objets sombres. |

> **Conclusion :** L'algorithme est **très performant** pour les objets **clairs** sur fond **sombre**. Il échoue partiellement sur les objets **sombres** et les variations d'éclairage **extrêmes**.

---

## 🚀 Comment Utiliser

### Prérequis

Assurez-vous d'avoir Python 3.7+ installé.

### Installation

1.  Clonez ce dépôt :
    ```bash
    git clone https://github.com/Tchoutouo/Compteur-Automatique-de-Grains-de-Riz.git
    cd Compteur-Automatique-de-Grains-de-Riz
    ```

2.  Installez les dépendances :
    ```bash
    pip install -r requirements.txt
    ```

### Exécution

Exécutez le script principal `main.py` :
```bash
python main.py

