import machine
import time

# Configuration des broches
i2c = machine.I2C(1, scl=machine.Pin(15), sda=machine.Pin(14))
bouton = machine.Pin(16, machine.Pin.IN, machine.Pin.PULL_UP)

# Adresse du module RTC
adresse_rtc = 0x68

def convertir_bcd_vers_decimal(bcd):
    """Convertit un nombre BCD en décimal"""
    dizaines = (bcd >> 4) * 10
    unites = bcd & 0x0F
    return dizaines + unites

def convertir_decimal_vers_bcd(decimal):
    """Convertit un nombre décimal en BCD"""
    dizaines = decimal // 10
    unites = decimal % 10
    return (dizaines << 4) | unites

def lire_temps_rtc():
    """Lit l'heure et la date depuis le RTC"""
    # Demander à lire à partir du registre 0 (secondes)
    i2c.writeto(adresse_rtc, bytes([0x00]))
    # Lire 7 registres (secondes à année)
    donnees = i2c.readfrom(adresse_rtc, 7)
    
    secondes = convertir_bcd_vers_decimal(donnees[0] & 0x7F)
    minutes = convertir_bcd_vers_decimal(donnees[1] & 0x7F)
    heures = convertir_bcd_vers_decimal(donnees[2] & 0x3F)  # Mode 24h
    
    # Ignorer le jour de la semaine (registre 3)
    jour = convertir_bcd_vers_decimal(donnees[4] & 0x3F)
    mois = convertir_bcd_vers_decimal(donnees[5] & 0x1F)
    annee = convertir_bcd_vers_decimal(donnees[6]) + 2000
    
    return annee, mois, jour, heures, minutes, secondes

def formater_temps():
    """Retourne l'heure sous forme de texte"""
    annee, mois, jour, heures, minutes, secondes = lire_temps_rtc()
    return f"{annee:04d}-{mois:02d}-{jour:02d} {heures:02d}:{minutes:02d}:{secondes:02d}"

def attendre_bouton(message=None):
    """Attend que le bouton soit appuyé"""
    if message:
        print(message)
    
    # Attendre que le bouton soit relâché (au cas où)
    while bouton.value() == 0:
        time.sleep(0.01)
    
    # Attendre l'appui sur le bouton
    while bouton.value() == 1:
        time.sleep(0.01)
    
    # Anti-rebond
    time.sleep(0.05)
    
    # Attendre que le bouton soit relâché
    while bouton.value() == 0:
        time.sleep(0.01)

def calculer_difference_temps(debut, fin):
    """Calcule la différence entre deux heures en secondes"""
    # Convertir en secondes depuis minuit
    debut_sec = debut[3] * 3600 + debut[4] * 60 + debut[5]
    fin_sec = fin[3] * 3600 + fin[4] * 60 + fin[5]
    
    difference = fin_sec - debut_sec
    
    # Si on passe à minuit, ajouter 24 heures
    if difference < 0:
        difference += 24 * 3600
    
    return difference

def verifier_rtc():
    """Vérifie si le RTC fonctionne bien"""
    peripheriques = i2c.scan()
    if adresse_rtc not in peripheriques:
        print("ERREUR: RTC non trouvé!")
        return False
    
    print("RTC détecté")
    return True

def ecrire_log(numero_essai, duree, debut_str, fin_str):
    """Écrit le résultat dans le fichier log"""
    try:
        with open("log.txt", "a") as fichier:
            ligne = f"Essai {numero_essai}: {duree:.2f} secondes (debut={debut_str}, fin={fin_str})\n"
            fichier.write(ligne)
        print("Résultat sauvegardé dans log.txt")
    except:
        print("Erreur pour écrire dans le log")

def jeu_principal():
    """Fonction principale du jeu"""
    numero_essai = 1
    
    print("=== Jeu de perception du temps ===")
    print("But: compter 15 secondes mentalement")
    
    while True:
        try:
            # Premier appui - début
            print(f"\n--- Essai {numero_essai} ---")
            attendre_bouton("Appuyez sur le bouton pour commencer...")
            
            temps_debut = lire_temps_rtc()
            texte_debut = formater_temps()
            print(f"Départ: {texte_debut}")
            
            # Deuxième appui - fin
            attendre_bouton("Comptez 15 secondes dans votre tête... puis appuyez!")
            
            temps_fin = lire_temps_rtc()
            texte_fin = formater_temps()
            print(f"Arrêt: {texte_fin}")
            
            # Calcul du temps écoulé
            duree = calculer_difference_temps(temps_debut, temps_fin)
            print(f"Temps écoulé: {duree:.2f} secondes")
            
            # Évaluation
            if 14.5 <= duree <= 15.5:
                print("Super! Très précis!")
            elif 14.0 <= duree <= 16.0:
                print("Bien joué!")
            else:
                print("Essayez encore!")
            
            # Sauvegarde
            ecrire_log(numero_essai, duree, texte_debut, texte_fin)
            
            numero_essai += 1
            time.sleep(2)
            
        except KeyboardInterrupt:
            print("\nAu revoir!")
            break

# Démarrage du programme
if verifier_rtc():
    jeu_principal()
else:
    print("Vérifiez les connexions du RTC")