"""
plot_histogram.py
Script de visualisation pour le Laboratoire 5 - SED1515
Analyse le fichier log.txt et génère un histogramme des durées mesurées
"""

import re
import matplotlib.pyplot as plt
import statistics
import os

def extract_times_from_log(filename):
    """
    Extrait les durées mesurées depuis le fichier log
    
    Args:
        filename (str): Nom du fichier log à analyser
        
    Returns:
        list: Liste des durées en secondes (float)
    """
    times = []
    
    # Vérifier si le fichier existe
    if not os.path.exists(filename):
        print(f"❌ Erreur: Le fichier '{filename}' n'existe pas.")
        return times
    
    # Vérifier si le fichier est vide
    if os.path.getsize(filename) == 0:
        print(f"❌ Erreur: Le fichier '{filename}' est vide.")
        return times
    
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            for line_num, line in enumerate(file, 1):
                line = line.strip()
                
                # Ignorer les lignes vides
                if not line:
                    continue
                
                # Expression régulière pour trouver les durées
                # Cherche un nombre décimal avant le mot "secondes"
                pattern = r'(\d+\.\d+|\d+)\s*secondes'
                match = re.search(pattern, line)
                
                if match:
                    try:
                        duration = float(match.group(1))
                        times.append(duration)
                        print(f"✅ Ligne {line_num}: Durée extraite = {duration} s")
                    except ValueError:
                        print(f"⚠️  Ligne {line_num}: Impossible de convertir '{match.group(1)}' en nombre")
                else:
                    print(f"❌ Ligne {line_num}: Aucune durée trouvée - '{line}'")
                    
    except Exception as e:
        print(f"❌ Erreur lors de la lecture du fichier: {e}")
    
    return times

def plot_histogram(times):
    """
    Crée et sauvegarde un histogramme des durées mesurées
    
    Args:
        times (list): Liste des durées en secondes
    """
    if not times:
        print("❌ Aucune donnée à afficher.")
        return
    
    # Configuration du style du graphique
    plt.style.use('default')
    plt.figure(figsize=(10, 6))
    
    # Création de l'histogramme
    n, bins, patches = plt.hist(times, bins=10, color='lightblue', 
                               edgecolor='black', alpha=0.7)
    
    # Calcul des statistiques
    mean_duration = statistics.mean(times)
    std_duration = statistics.stdev(times) if len(times) > 1 else 0
    
    # Ajout de la ligne de moyenne
    plt.axvline(mean_duration, color='red', linestyle='--', linewidth=2,
                label=f'Moyenne = {mean_duration:.1f} s')
    
    # Personnalisation du graphique
    plt.xlabel('Durée mesurée (secondes)', fontsize=12)
    plt.ylabel('Nombre d\'essais', fontsize=12)
    plt.title('Histogramme des durées mesurées – Lab 5 SED1515', fontsize=14, fontweight='bold')
    
    # Ajout de la grille
    plt.grid(True, alpha=0.3)
    
    # Ajout de la légende
    plt.legend()
    
    # Affichage des statistiques sur le graphique
    stats_text = f'Moyenne: {mean_duration:.2f} s\nÉcart-type: {std_duration:.2f} s\nTotal: {len(times)} essais'
    plt.annotate(stats_text, xy=(0.02, 0.98), xycoords='axes fraction',
                bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.8),
                verticalalignment='top', fontsize=10)
    
    # Ajustement des limites pour meilleure visibilité
    plt.xlim(min(times) - 1, max(times) + 1)
    
    # Sauvegarde de l'image
    output_filename = 'histogram.png'
    plt.savefig(output_filename, dpi=300, bbox_inches='tight')
    print(f"📊 Histogramme enregistré sous '{output_filename}'")
    
    # Affichage à l'écran
    plt.show()

def main():
    """
    Fonction principale du script
    """
    log_filename = 'log.txt'
    
    print("=" * 60)
    print("ANALYSE DU FICHIER LOG - LAB 5 SED1515")
    print("=" * 60)
    
    # Extraction des durées
    print(f"\n📖 Lecture du fichier '{log_filename}'...")
    times = extract_times_from_log(log_filename)
    
    if not times:
        print("\n❌ Aucune durée valide n'a pu être extraite.")
        return
    
    # Affichage des résultats dans la console
    print(f"\n📊 RÉSULTATS EXTRACTIONS:")
    print(f"Durées extraites : {times}")
    print(f"Nombre d'essais valides : {len(times)}")
    
    # Calcul des statistiques
    mean_val = statistics.mean(times)
    std_val = statistics.stdev(times) if len(times) > 1 else 0
    
    print(f"\n📈 STATISTIQUES:")
    print(f"Moyenne : {mean_val:.2f} s")
    print(f"Écart-type : {std_val:.2f} s")
    
    # Génération de l'histogramme
    print(f"\n🎨 Génération de l'histogramme...")
    plot_histogram(times)
    
    print(f"\n✅ Analyse terminée avec succès!")

if __name__ == "__main__":
    main()