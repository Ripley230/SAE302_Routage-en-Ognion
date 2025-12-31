# =========================
# Imports
# =========================

import sympy     # Utilisé pour générer des nombres premiers
import math      # Fonctions mathématiques (PGCD)
import random    # Génération de valeurs aléatoires


def generer_clefs():
    """
    Génère une paire de clefs RSA :
    - une clef publique (e, n)
    - une clef privée (d, n)
    """

    # Génération de deux nombres premiers p et q
    p = sympy.randprime(500, 1000)
    q = sympy.randprime(500, 1000)

    # On s'assure que p et q sont différents
    while p == q:
        q = sympy.randprime(500, 1000)

    # Calcul de n (partie commune aux clefs)
    n = p * q

    # Calcul de l'indicatrice d'Euler
    phi = (p - 1) * (q - 1)

    # Choix classique de l'exposant public
    e = 65537

    # Vérification que e est premier avec phi
    while math.gcd(e, phi) != 1:
        e = random.randint(3, phi - 1)

    # Calcul de l'exposant privé d
    d = pow(e, -1, phi)

    # Retourne la clef publique et la clef privée
    return ((e, n), (d, n))


def chiffrer(message_texte, clef_publique):
    """
    Chiffrement hybride :
    - RSA pour chiffrer une clef secrète
    - XOR pour chiffrer le message
    """

    e, n = clef_publique

    # Génération d'une clef secrète aléatoire
    clef_secrete = random.randint(1, 10000)

    # Chiffrement de la clef secrète avec RSA
    clef_chiffree = pow(clef_secrete, e, n)

    # Chiffrement du message caractère par caractère avec XOR
    message_xor = []
    for lettre in message_texte:
        valeur = ord(lettre)           # Code ASCII du caractère
        valeur_chiffree = valeur ^ clef_secrete
        message_xor.append(str(valeur_chiffree))

    # Transformation de la liste en chaîne de caractères
    message_xor_str = ",".join(message_xor)

    # Format final : CLEF_RSA::MESSAGE_XOR
    return f"{clef_chiffree}::{message_xor_str}"


def dechiffrer(message_chiffre_str, clef_privee):
    """
    Déchiffrement du message :
    - déchiffre la clef secrète avec RSA
    - déchiffre le message avec XOR
    """

    d, n = clef_privee

    try:
        # Séparation de la clef RSA et du message XOR
        parties = message_chiffre_str.split("::")
        if len(parties) != 2:
            return "Erreur format"

        clef_chiffree = int(parties[0])
        message_xor_str = parties[1]

        # Déchiffrement de la clef secrète
        clef_secrete = pow(clef_chiffree, d, n)

        # Reconstruction du message clair
        nombres_str = message_xor_str.split(",")
        message_clair = ""

        for n_str in nombres_str:
            if n_str == "":
                continue
            valeur_chiffree = int(n_str)
            valeur = valeur_chiffree ^ clef_secrete
            message_clair += chr(valeur)

        return message_clair

    except Exception as e:
        print(f"Erreur dechiffrage : {e}")
        return "Erreur"
