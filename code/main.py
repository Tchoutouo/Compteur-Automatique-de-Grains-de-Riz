# ==========================
# 1. IMPORTS DES LIBRAIRIES
# ==========================
import cv2
import numpy as np
import matplotlib.pyplot as plt
import os

# ==========================
# 2. FONCTION DE TRAITEMENT PRINCIPALE
# ==========================
def count_rice_grains(image_path):
    """
    Fonction principale pour compter le nombre de grains de riz dans une image.
    Paramètre:
        image_path (str): Chemin vers l'image à traiter.
    Retourne:
        int: Nombre de grains détectés.
    """

    # ------------------------
    # 2.1 LECTURE DE L'IMAGE
    # ------------------------
    print(f"Traitement de l'image : {image_path}")
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    if img is None:
        raise ValueError(f"Impossible de charger l'image depuis {image_path}")

    # ------------------------
    # 2.2 PRÉ-TRAITEMENT : RÉDUCTION DU BRUIT
    # ------------------------
    blurred = cv2.medianBlur(img, 5)
    # ------------------------
    # 2.3 SEGMENTATION : SEUILAGE ADAPTATIF
    # ------------------------
    # Pour gérer la variation d'éclairage , on utilise un seuillage adaptatif.
    # `ADAPTIVE_THRESH_GAUSSIAN_C` calcule un seuil local basé sur une moyenne gaussienne pondérée.
    # `blockSize=11` définit la taille de la fenêtre de calcul locale.
    # `C=2` est une constante qui ajuste le seuil final (soustraction).
    thresholded = cv2.adaptiveThreshold(blurred, 255,
                                        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                        cv2.THRESH_BINARY, 11, 2)

    # ------------------------
    # 2.4 POST-TRAITEMENT : NETTOYAGE MORPHOLOGIQUE
    # ------------------------
    # Érosion + Dilatation (Ouverture) : supprime les petits points de bruit.
    # Dilatation + Érosion (Fermeture) : remplit les petits trous à l'intérieur des grains.
    kernel = np.ones((2, 2), np.uint8)
    opened = cv2.morphologyEx(thresholded, cv2.MORPH_OPEN, kernel)
    closed = cv2.morphologyEx(opened, cv2.MORPH_CLOSE, kernel)

    # ------------------------
    # 2.5 ÉTIQUETAGE DES COMPOSANTES CONNEXES
    # ------------------------
    # Identification de toutes les régions (grains) dans l'image binaire.
    # `connectivity=8` permet une meilleure connexion des pixels adjacents (incluant diagonales).
    num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(closed, connectivity=8)

    # ------------------------
    # 2.6 FILTRAGE DES RÉGIONS
    # ------------------------
    # Suppression des petites régions (bruit) en filtrant par aire minimale.
    # Une région doit avoir au moins 50 pixels pour être considérée comme un grain.
    min_area = 50
    valid_grains = []
    for i in range(1, num_labels): 
        area = stats[i, cv2.CC_STAT_AREA]
        if area > min_area:
            valid_grains.append(i)

    # ------------------------
    # 2.7 RETOURNER LE RÉSULTAT
    # ------------------------
    count = len(valid_grains)
    print(f"Nombre de grains détectés : {count}")
    return count, img, blurred, thresholded, opened, closed, labels, valid_grains, centroids

# ==========================
# 3. FONCTION D'AFFICHAGE DES RÉSULTATS
# ==========================
def display_results(original, blurred, thresholded, opened, closed, labels, valid_grains, centroids):
    """
    Affiche les étapes intermédiaires du traitement.
    Paramètres:
        original, blurred, ... : Images de chaque étape.
        labels : Image des étiquettes.
        valid_grains : Liste des indices des grains valides.
        centroids: Coordonnées des centres de gravité.
    """
    fig, axes = plt.subplots(2, 4, figsize=(14, 8))
    fig.suptitle('Chaîne de Traitement - Comptage des Grains de Riz', fontsize=16)

    # Ajouter les images aux sous-graphiques
    axes[0, 0].imshow(original, cmap='gray')
    axes[0, 0].set_title('Image Originale')
    axes[0, 0].axis('off')

    axes[0, 1].imshow(blurred, cmap='gray')
    axes[0, 1].set_title('Après Flou Gaussien')
    axes[0, 1].axis('off')

    axes[0, 2].imshow(thresholded, cmap='gray')
    axes[0, 2].set_title('Seuillage Adaptatif')
    axes[0, 2].axis('off')

    axes[0, 3].imshow(opened, cmap='gray')
    axes[0, 3].set_title('Ouverture Morphologique')
    axes[0, 3].axis('off')

    axes[1, 0].imshow(closed, cmap='gray')
    axes[1, 0].set_title('Fermeture Morphologique')
    axes[1, 0].axis('off')

    # Créer une image colorée pour visualiser les grains valides
    color_labels = np.zeros_like(labels, dtype=np.uint8)
    for i in valid_grains:
        color_labels[labels == i] = 255
    axes[1, 1].imshow(color_labels, cmap='gray')
    axes[1, 1].set_title('Grains Validés')
    axes[1, 1].axis('off')

    # Visualiser les contours des grains
    contours, _ = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contour_image = cv2.cvtColor(closed, cv2.COLOR_GRAY2BGR)
    cv2.drawContours(contour_image, contours, -1, (0, 255, 0), 1)
    axes[1, 2].imshow(contour_image)
    axes[1, 2].set_title('Contours des Grains')
    axes[1, 2].axis('off')

    # Visualiser les centres de gravité des grains
    centroid_image = cv2.cvtColor(closed, cv2.COLOR_GRAY2BGR)
    for i in valid_grains:
        x, y = centroids[i]
        cv2.circle(centroid_image, (int(x), int(y)), 4, (255, 0, 0), -1)
    axes[1, 3].imshow(centroid_image)
    axes[1, 3].set_title('Centres de Gravité')
    axes[1, 3].axis('off')

    plt.figtext(0.5, 0.02 * 0.7, f"Image : Nombre de grains détectés : {count}", ha='center', fontsize=12, fontweight='bold', bbox=dict(boxstyle="round,pad=0.3", facecolor="lightblue"))

    plt.tight_layout()
    plt.show()

# ==========================
# 4. CODE PRINCIPAL
# ==========================

image_paths = [
    'images/1_wIXlvBeAFtNVgJd49VObgQ_sinus.png', 
    'images/1_wIXlvBeAFtNVgJd49VObgQ.png',  
    'images/1_wIXlvBeAFtNVgJd49VObgQ.png_Salt_Pepper_Noise1.png', 
    'images/1_zd6ypc20QAIFMzrbCmJRMg.png'
]

# === EXÉCUTION ===
for path in image_paths:
    try:
        # Appeler la fonction de traitement
        count, original, blurred, thresholded, opened, closed, labels, valid_grains, centroids = count_rice_grains(path)

        # Afficher les résultats
        display_results(original, blurred, thresholded, opened, closed, labels, valid_grains, centroids)

    except Exception as e:
        print(f"Erreur lors du traitement de {path}: {e}")