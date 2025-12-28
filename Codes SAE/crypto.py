import sympy
import math
import random

def generer_clefs():
    """
    Fabrique une clef publique et une clef privée.
    """
    p = sympy.randprime(500, 1000)
    q = sympy.randprime(500, 1000)
    
    while p == q:
        q = sympy.randprime(500, 1000)
    
    n = p * q
    phi = (p - 1) * (q - 1)
    
    e = 65537
    while math.gcd(e, phi) != 1:
        e = random.randint(3, phi - 1)
    
    d = pow(e, -1, phi)
    return ((e, n), (d, n))

def chiffrer(message_texte, clef_publique):
    """
    Chiffrement Hybride (RSA + XOR).
    Permet de chiffrer des messages longs sans augmenter excessivement la taille.
    Le message est chiffré par XOR avec une clef aléatoire, elle-même chiffrée par RSA.
    """
    e, n = clef_publique
    
    clef_secrete = random.randint(1, 10000)
    
    clef_chiffree = pow(clef_secrete, e, n)
    
    message_xor = []
    for lettre in message_texte:
        valeur = ord(lettre)
        valeur_chiffree = valeur ^ clef_secrete 
        message_xor.append(str(valeur_chiffree))
        
    message_xor_str = ",".join(message_xor)
    
    return f"{clef_chiffree}::{message_xor_str}"

def dechiffrer(message_chiffre_str, clef_privee):
    """
    Déchiffre le format "CLEF_RSA::MESSAGE_XOR"
    """
    d, n = clef_privee
    
    try:
        parties = message_chiffre_str.split("::")
        if len(parties) != 2:
            return "Erreur format"
            
        clef_chiffree = int(parties[0])
        message_xor_str = parties[1]
        
        clef_secrete = pow(clef_chiffree, d, n)
        nombres_str = message_xor_str.split(",")
        message_clair = ""
        
        for n_str in nombres_str:
            if n_str == "": continue
            valeur_chiffree = int(n_str)
            valeur = valeur_chiffree ^ clef_secrete
            message_clair += chr(valeur)
            
        return message_clair
    except Exception as e:
        print(f"Erreur dechiffrage : {e}")
        return "Erreur"
