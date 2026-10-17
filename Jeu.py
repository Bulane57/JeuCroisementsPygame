import pygame
import sys
from random import randint

# Joue le bruit quand le carré se téléporte
pygame.mixer.init()
tp=pygame.mixer.music.load('teleport.mp3')
tp=pygame.mixer.music.set_volume(0.2)


# Initialisation de Pygame
pygame.init()

# Définis la taille de la fenêtre
window_width, window_height = 600, 300
mafenetre = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('Jeu de Croisements')

#Les couleurs
NOIR = (0, 0, 0)
VIOLET = (255, 0, 255)
CYAN = (0, 255, 255)
BLANC = (255, 255, 255)
ROUGE = (255, 0, 0)


# Création des barres sous forme de rectangles
a = pygame.Rect(0, 0, 350, 10)  # Barre de gauche
b = pygame.Rect(0, 0, 10, 350)  # Barre de droite

# Distance de déplacement
distance_de_deplacement = 10

# Taille et position initiale aléatoire du carré bleu
taille_carre = 10
L = randint(0, (350 - taille_carre) // taille_carre) * taille_carre
l = randint(0, (250 - taille_carre) // taille_carre) * taille_carre
carre = pygame.Rect(L, l, taille_carre, taille_carre)  # Carré bleu

# Initialise les polices pour le texte
font1 = pygame.font.Font(None, 23)
font2 = pygame.font.Font(None, 25)
font3 = pygame.font.Font(None, 21)
font_minuteur = pygame.font.Font(None, 30)
font_end = pygame.font.Font(None, 80)
font_button = pygame.font.Font(None, 45)

# On démarre le chronomètre
démarrage_temps = pygame.time.get_ticks()


# Initialisation du compteur de croisements
passage = 5  # Le nombre de croisements qu'on doit faire

# Compteur pour le nombre de mouvements des barres
nombre_de_mouvements = 0  # Compteur de mouvements

# Variable pour suivre la fin du jeu
game_over = False

# On définit le bouton "Recommencer"
button_rect = pygame.Rect(200, 200, 200, 50)

# Variables pour le record
record_temps = None
record_mouvement = None

# Fonction de réinitialisation du jeu
def restart_game():
    global a, b, carre, passage, démarrage_temps, game_over, nombre_de_mouvements

    # Réinitialise les positions des barres et du carré
    a.topleft = (0, 0)
    b.topleft = (0, 0)
    carre.x = randint(0, (350 - taille_carre) // taille_carre) * taille_carre
    carre.y = randint(0, (250 - taille_carre) // taille_carre) * taille_carre

    # Réinitialise le compteur de croisements et l'état du jeu
    passage = 5
    game_over = False

    # Réinitialise le chronomètre
    démarrage_temps = pygame.time.get_ticks()

    # Réinitialise le compteur de mouvements
    nombre_de_mouvements = 0

# Fonction pour mettre à jour le record
def mis_a_jour_record():
    global record_temps, record_mouvement

    # Temps écoulé actuel
    temps_ecoule = (pygame.time.get_ticks() - démarrage_temps) // 1000

    # Vérifier et mettre à jour le record de temps
    if record_temps is None or temps_ecoule < record_temps:
        record_temps = temps_ecoule

    # Vérifie et mettre à jour le record de mouvements
    if record_mouvement is None or nombre_de_mouvements < record_mouvement:
        record_mouvement = nombre_de_mouvements

# Boucle de jeu
while True:
    # Gestion des événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Détecte un clic de souris pour redémarrer le jeu
        if event.type == pygame.MOUSEBUTTONDOWN:
            if game_over and button_rect.collidepoint(event.pos):
                restart_game()


    # Vérifie les touches maintenues pour les mouvements continus
    touche = pygame.key.get_pressed()

    # Déplacement de la barre A (barre de gauche)
    if touche[pygame.K_UP]:
        a.y -= distance_de_deplacement # Vers la haut
        nombre_de_mouvements += 1  # Augmente le compteur de mouvements
    if touche[pygame.K_DOWN]:
        a.y += distance_de_deplacement # Vers la bas
        nombre_de_mouvements += 1  # Augmente le compteur de mouvements

    # Déplacement de la barre B (barre de droite)
    if touche[pygame.K_LEFT]:  # Vers la gauche
        b.x -= distance_de_deplacement
        nombre_de_mouvements += 1  # Augmente le compteur de mouvements
    if touche[pygame.K_RIGHT]:  # Vers la droite
        b.x += distance_de_deplacement
        nombre_de_mouvements += 1  # Augmente le compteur de mouvements

    # Limitation pour empêcher les barres de sortir de l'écran
    a.y = max(0, min(window_height - a.height, a.y))
    b.y = max(0, min(window_height - b.height, b.y))
    a.x = max(0, min(window_width - a.width, a.x))
    b.x = max(0, min(350 - b.width, b.x))  # Limite pour la barre B à gauche de la ligne de séparation

    # Détection de collision entre les deux barres et le carré
    if not game_over and a.colliderect(carre) and b.colliderect(carre):


        tp=pygame.mixer.music.play()
        # fait réapparaître le carré
        carre.x = randint(0, (350 - taille_carre) // taille_carre) * taille_carre
        carre.y = randint(0, (250 - taille_carre) // taille_carre) * taille_carre

        # Soustrait le compteur de croisements
        passage-= 1

        #On s'assure que le compteur ne descend pas en dessous de 0
        passage = max(0, passage)

        # Vérifie si le nombre de croisements est à zéro, ce qui signale la fin du jeu
        if passage == 0:
            mis_a_jour_record()  # Mets à jour le record avant de terminer le jeu
            game_over = True


    # Si le jeu est terminé, on affiche un écran noir avec le message "BRAVOOO!!!"
    if game_over:
        mafenetre.fill(NOIR)  #Remplis la fenêtre de noir
        fin_surface = font_end.render("BRAVOOO!!!", True, ROUGE)  # Crée une surface de texte "BRAVOOO!!!"
        mafenetre.blit(fin_surface, (150, 120))  #Positionne le texte aux coordonnées indiquées.

        # Affiche les records
        record_surface = font1.render(f"Record Temps: {record_temps} s | Record Mouvements: {record_mouvement}", True, BLANC)
        mafenetre.blit(record_surface, (160, 50))  # Affiche le texte des records

        # Dessine le bouton "Recommencer"
        pygame.draw.rect(mafenetre, NOIR, button_rect)  # Dessine le rectangle du bouton
        button_text_surface = font_button.render("Recommencer", True, BLANC)  # Crée la surface de texte "Recommencer"
        button_text_rect = button_text_surface.get_rect(center=button_rect.center)  # Centre le texte dans le bouton
        mafenetre.blit(button_text_surface, button_text_rect)  # Affiche le texte du bouton

    else:
        # Remplis la fenêtre de noir
        mafenetre.fill(NOIR)

        # Dessine une ligne de séparation à 350 pixels avec une largeur de 5 pixels
        pygame.draw.rect(mafenetre, BLANC, (350, 0, 5, window_height))  # Ligne de séparation

        # Dessine les barres et le carré si le jeu n'est pas terminé
        pygame.draw.rect(mafenetre, VIOLET, a)  # Dessine la barre A
        pygame.draw.rect(mafenetre, VIOLET, b)  # Dessine la barre B
        pygame.draw.rect(mafenetre, CYAN, carre)  # Dessine le carré avec la nouvelle position

        # Rends et dessine le texte pour les croisements restants
        texte_surface = font1.render(f"Il te reste encore {passage} croisements", True, BLANC)
        mafenetre.blit(texte_surface, (368, 10))  # Dessine le texte à droite
         # Affiche le compteur de mouvements
        mouvement_surface = font1.render(f"Nombre de mouvements: {nombre_de_mouvements}", True, BLANC)
        mafenetre.blit(mouvement_surface, (368, 130))  # Affiche le nombre de mouvements en dessous


        # Chronomètre
        temps_ecoule = (pygame.time.get_ticks() - démarrage_temps) // 1000  # Convertis en secondes
        heures = temps_ecoule // 3600 # Heures
        minutes = (temps_ecoule % 3600) // 60 # Minutes
        secondes = temps_ecoule % 60 # Secondes
        minuteur_surface = font_minuteur.render(f"Temps: {heures:02}h {minutes:02}m {secondes:02}s", True, BLANC)
        mafenetre.blit(minuteur_surface, (368, 80))  # Dessine le chronomètre juste en dessous de "Temps"
        record_title_surface = font1.render("RECORD : ", True, BLANC)  # Crée une surface de texte "RECORD"
        mafenetre.blit(record_title_surface, (440, 200))  # Positionne le texte "RECORD" à droite, en dessous du chronomètre
        # Affiche les records actuels si disponibles
        if record_temps is not None and record_mouvement is not None:
            record_surface = font3.render(f"Temps: {record_temps} s | Mouvements: {record_mouvement}", True, BLANC)
            mafenetre.blit(record_surface, (369, 220))  # Positionne les records à droite


    # Mise à jour de l'affichage
    pygame.display.flip()

    # Ajoute un délai pour ralentir le déplacement
    pygame.time.delay(100)  # Délai de 100ms