def corrompre_fichier(chemin_fichier):
    with open(chemin_fichier, 'rb') as f:
        contenu = f.read()

    contenu_corrompu = bytes([b ^ 0xFF for b in contenu])  # Inversion des bits

    with open(chemin_fichier + ".corrompu", 'wb') as f:
        f.write(contenu_corrompu)

    print(f"[OK] Fichier corrompu : {chemin_fichier}.corrompu")


def restaurer_fichier(chemin_corrompu):
    with open(chemin_corrompu, 'rb') as f:
        contenu = f.read()

    contenu_restaure = bytes([b ^ 0xFF for b in contenu])  # Inversion des bits à nouveau

    chemin_original = chemin_corrompu.replace(".corrompu", ".restaure")
    with open(chemin_original, 'wb') as f:
        f.write(contenu_restaure)

    print(f"[OK] Fichier restauré : {chemin_original}")


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage : python simulateur_corruption.py [corrupt|restore] <fichier>")
        exit(1)

    action, chemin = sys.argv[1], sys.argv[2]

    if action == "corrupt":
        corrompre_fichier(chemin)
    elif action == "restore":
        restaurer_fichier(chemin)
    else:
        print("Action inconnue : utiliser 'corrupt' ou 'restore'")
