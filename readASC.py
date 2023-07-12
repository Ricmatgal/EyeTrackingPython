import numpy as np
import pandas as pd
# from pandasgui import show
import matplotlib.pyplot as plt

def lire_fichier_asc(chemin_fichier_asc, flag):
    # Lire le fichier ASC et extraire les données pertinentes
    with open(chemin_fichier_asc, 'r') as fichier:
        lignes = fichier.readlines()

    # Données fixes
    liste_de_data_types = ["GAZE", "HREF", "PUPIL"]
    choix_eye = ["LEFT", "RIGHT"]
    liste_de_samples_rate =  [250.00, 500.00, 1000.0, 2000.0]
    liste_de_tracking_mode = ["L", "CR"]
    liste_de_filter_level = [0, 1, 2]

    # Nos différentes données
    time_message = []
    data_message = []
    time_start = 0
    time_end = 0
    event_eye = choix_eye[0]
    sample_eye = choix_eye[0]
    samples = False
    events = False
    prescaler = 1
    vprescaler = 1
    event_data_types = liste_de_data_types[0]
    sample_data_types = liste_de_data_types[0]
    event_resolution = 36 #average resolution for Eyelink-1000
    sample_resolution = 36 #average resolution for Eyelink-1000
    event_samples_rate = liste_de_samples_rate[0]
    sample_samples_rate = liste_de_samples_rate[0]
    event_tracking_mode = liste_de_tracking_mode[0]
    sample_tracking_mode = liste_de_tracking_mode[0]
    event_filter_level = liste_de_filter_level[0]
    sample_filter_level = liste_de_filter_level[0]
    sample_velocity = 0

    # Pour les samples
    samples_time_check_left = []
    samples_time_check_right = []
    samples_xpl = []
    samples_ypl = []
    samples_xpr = []
    samples_ypr = []
    samples_pupil_r = []
    samples_pupil_l = []
    samples_xvelocity_r = []
    samples_yvelocity_r = []
    samples_xvelocity_l = []
    samples_yvelocity_l = []
    samples_resolution_x = []
    samples_resolution_y = []

    # Pour les fixations
    time_eye_fix_left = []
    time_eye_fix_right = []
    eye_fix_left_duration = []
    eye_fix_right_duration = []
    eye_fix_left_pos_x = []
    eye_fix_left_pos_y = []
    eye_fix_right_pos_x = []
    eye_fix_right_pos_y = []
    eye_fix_left_pupil = []
    eye_fix_right_pupil = []

    # Pour les saccades
    time_eye_sacc_left = []
    time_eye_sacc_right = []
    eye_sacc_left_duration = []
    eye_sacc_right_duration = []
    eye_sacc_left_start_pos_x = []
    eye_sacc_left_start_pos_y = []
    eye_sacc_right_start_pos_x = []
    eye_sacc_right_start_pos_y = []
    eye_sacc_left_end_pos_x = []
    eye_sacc_left_end_pos_y = []
    eye_sacc_right_end_pos_x = []
    eye_sacc_right_end_pos_y = []
    eye_sacc_left_angle = []
    eye_sacc_right_angle = []
    eye_sacc_left_vmax = []
    eye_sacc_right_vmax = []

    # Pour les blink
    time_eye_blink_left = []
    time_eye_blink_right = []
    end_time_eye_blink_left = []
    end_time_eye_blink_right = []
    eye_blink_left_duration = []
    eye_blink_right_duration = []

    # Pour les boutons
    button_time = []
    button_type = []
    button_action = []

    # Parcourir les lignes du fichier
    for ligne in lignes:
        if ligne.startswith('*') or ligne.startswith('#') or ligne.startswith('/') or ligne.startswith(';') or ligne.startswith(' '):
            # Ignorer les lignes de commentaire ou de description de fichier
            continue
        elif ligne.startswith('MSG'):
            # Récupère les messages
            ligne_complete = ligne.split()
            time_message.append(float(ligne_complete[1]))
            data_message.append(ligne_complete[2:])
        elif ligne.startswith('INPUT'):
            # Pas d'indications
            continue
        elif ligne.startswith('START'):
            # Début d'une collecte de données
            ligne_complete = ligne.split()
            time_start = float(ligne_complete[1])
            eye = ligne_complete[2]
            if len(ligne_complete) == 5 :
                samples = True
                events = True
            else :
                if ligne_complete[3] == "SAMPLES":
                    samples = True
                elif ligne_complete[3] == "EVENTS":
                    events = True
                else :
                    print("\nErreur dans le START, <types> manquant ! \n")
        elif ligne.startswith('END'):
            # Fin d'une collecte de données
            ligne_complete = ligne.split()
            time_end = float(ligne_complete[1])
            if len(ligne_complete) == 7 :
                samples = False
                events = False
            else :
                if ligne_complete[2] == "SAMPLES":
                    samples = False
                elif ligne_complete[2] == "EVENTS":
                    events = False
                else :
                    print("\nErreur dans le START, <types> manquant ! \n")
        elif ligne.startswith('PRESCALER'):
            # Valeur de l'échelle (pour la division)
            prescaler = float(ligne.split()[1])
        elif ligne.startswith('VPRESCALER'):
            # Valeur de l'échelle de vitesse (pour la division)
            vprescaler = float(ligne.split()[1])
        elif ligne.startswith('EVENTS'):
            # Evenement
            if events == True :
                ligne_complete = ligne.split()
                event_data_types = ligne_complete[1]
                event_eye = ligne_complete[2]
                position = 3
                while position < len(ligne_complete) :
                    if ligne_complete[position] == "RES" :
                        event_resolution = float(ligne_complete[position + 1])
                        position += 2
                    elif ligne_complete[position] == "RATE" :
                        event_samples_rate = float(ligne_complete[position + 1])
                        position += 2
                    elif ligne_complete[position] == "TRACKING" :
                        event_tracking_mode = ligne_complete[position + 1]
                        position += 2
                    elif ligne_complete[position] == "FILTER" :
                        event_filter_level = float(ligne_complete[position + 1])
                        position += 2
                    else :
                        print("\nErreur dans le EVENTS, <data options> non connu ! \n")

        
        elif ligne.startswith('SAMPLES'):
            # Ligne de données d'échantillon
            if samples == True :
                ligne_complete = ligne.split()
                sample_data_types = ligne_complete[1]
                sample_eye = ligne_complete[2]
                position = 3
                while position < len(ligne_complete) :
                    if ligne_complete[position] == "VEL" :
                        sample_velocity = float(ligne_complete[position + 1])  / vprescaler
                        position += 2
                    elif ligne_complete[position] == "RES" :
                        sample_resolution = float(ligne_complete[position + 1])
                        position += 2
                    elif ligne_complete[position] == "RATE" :
                        sample_samples_rate = float(ligne_complete[position + 1])
                        position += 2
                    elif ligne_complete[position] == "TRACKING" :
                        sample_tracking_mode = ligne_complete[position + 1]
                        position += 2
                    elif ligne_complete[position] == "FILTER" :
                        sample_filter_level = float(ligne_complete[position + 1])
                        position += 2
                    else :
                        print("\nErreur dans le SAMPLES, <data options> non connu ! \n")

        elif ligne.startswith('SFIX') :
            # Début d'une fixation
            if events == True :
                ligne_complete = ligne.split()
                if ligne_complete[1] == "L" :
                    time_eye_fix_left.append(float(ligne_complete[2]) - time_start)
                elif ligne_complete[1] == "R" :
                    time_eye_fix_right.append(float(ligne_complete[2]) - time_start)
                else :
                    print("\nErreur dans SFIX, <eye> non connu ! \n")
        elif ligne.startswith('EFIX') :
            # Fin d'une fixation
            if events == True :
                ligne_complete = ligne.split()
                if ligne_complete[1] == "L" :
                    #time_eye_fix_left.append(float(ligne_complete[3]) - time_start)   # Ajoute la fin (inutile pour notre utilisation)
                    eye_fix_left_duration.append(float(ligne_complete[4]))
                    eye_fix_left_pos_x.append(float(ligne_complete[5]))
                    eye_fix_left_pos_y.append(float(ligne_complete[6]))
                    eye_fix_left_pupil.append(float(ligne_complete[7]))
                elif ligne_complete[1] == "R" :
                    #time_eye_fix_right.append(float(ligne_complete[3]) - time_start)   # Ajoute la fin (inutile pour notre utilisation)
                    eye_fix_right_duration.append(float(ligne_complete[4]))
                    eye_fix_right_pos_x.append(float(ligne_complete[5]))
                    eye_fix_right_pos_y.append(float(ligne_complete[6]))
                    eye_fix_right_pupil.append(float(ligne_complete[7]))
                else :
                    print("\nErreur dans SFIX, <eye> non connu ! \n")
            
                # Résolution ignoré

        elif ligne.startswith('SSACC') :
            # Début d'une saccade
            if events == True :
                ligne_complete = ligne.split()
                if ligne_complete[1] == "L" :
                    time_eye_sacc_left.append(float(ligne_complete[2]) - time_start)
                elif ligne_complete[1] == "R" :
                    time_eye_sacc_right.append(float(ligne_complete[2]) - time_start)
                else :
                    print("\nErreur dans SSACC, <eye> non connu ! \n")
        elif ligne.startswith('ESACC') :
            # Fin d'une saccade
            if events == True :
                ligne_complete = ligne.split()
                arg5 = float(ligne_complete[5])
                arg6 = float(ligne_complete[6])
                arg7 = float(ligne_complete[7])
                arg8 = float(ligne_complete[8])
                if event_data_types == "GAZE" :
                    arg5 = arg5 / prescaler
                    arg6 = arg6 / prescaler
                    arg7 = arg7 / prescaler
                    arg8 = arg8 / prescaler

                if ligne_complete[1] == "L" :
                    #time_eye_sacc_left.append(float(ligne_complete[3]) - time_start)   # Ajoute la fin (inutile pour notre utilisation)
                    eye_sacc_left_duration.append(float(ligne_complete[4]))
                    eye_sacc_left_start_pos_x.append(arg5)
                    eye_sacc_left_start_pos_y.append(arg6)
                    eye_sacc_left_end_pos_x.append(arg7)
                    eye_sacc_left_end_pos_y.append(arg8)
                    eye_sacc_left_angle.append(float(ligne_complete[9]))
                    eye_sacc_left_vmax.append(float(ligne_complete[10]) / vprescaler)
                elif ligne_complete[1] == "R" :
                    #time_eye_sacc_right.append(float(ligne_complete[3]) - time_start)   # Ajoute la fin (inutile pour notre utilisation)
                    eye_sacc_right_duration.append(float(ligne_complete[4]))
                    eye_sacc_right_start_pos_x.append(arg5)
                    eye_sacc_right_start_pos_y.append(arg6)
                    eye_sacc_right_end_pos_x.append(arg7)
                    eye_sacc_right_end_pos_y.append(arg8)
                    eye_sacc_right_angle.append(float(ligne_complete[9]))
                    eye_sacc_right_vmax.append(float(ligne_complete[10]) / vprescaler)
                else :
                    print("\nErreur dans ESACC, <eye> non connu ! \n")
                
                # Résolution ignoré

        elif ligne.startswith('SBLINK') :
            # Début d'un blink
            if events == True :
                ligne_complete = ligne.split()
                if ligne_complete[1] == "L" :
                    time_eye_blink_left.append(float(ligne_complete[2]) - time_start)
                elif ligne_complete[1] == "R" :
                    time_eye_blink_right.append(float(ligne_complete[2]) - time_start)
                else :
                    print("\nErreur dans SBLINK, <eye> non connu ! \n")
        elif ligne.startswith('EBLINK') :
            #Fin d'un blink
            if events == True :
                ligne_complete = ligne.split()
                if ligne_complete[1] == "L" :
                    end_time_eye_blink_left.append(float(ligne_complete[3]) - time_start)
                    eye_blink_left_duration.append(float(ligne_complete[4]))
                elif ligne_complete[1] == "R" :
                    end_time_eye_blink_right.append(float(ligne_complete[3]) - time_start)
                    eye_blink_right_duration.append(float(ligne_complete[4]))
                else :
                    print("\nErreur dans EBLINK, <eye> non connu ! \n")
        elif ligne.startswith('BUTTON') :
            # Bouton
            if events == True :
                ligne_complete = ligne.split()
                button_time.append(float(ligne_complete[1]) - time_start)
                button_type.append(ligne_complete[2])
                if ligne_complete[3] == "0" :
                    button_action.append("RELEASED")
                elif ligne_complete[3] == "1" :
                    button_action.append("PRESSED")
                else :
                    print("\nErreur dans BUTTON, <state> non connu ! \n")

        elif ligne.startswith('1') or ligne.startswith('2') or ligne.startswith('3') or ligne.startswith('4') or ligne.startswith('5') or ligne.startswith('6') or ligne.startswith('7') or ligne.startswith('8') or ligne.startswith('9') or ligne.startswith('0'):
            #Sample line, ligne de données
            if samples == True :
                ligne_complete = ligne.split()
                if "." in ligne_complete :
                    #on saute la ligne si des informations sont manquantes
                    continue
                else :
                    longueur = len(ligne_complete)
                    #De quel type de Sample il s'agit
                    if longueur == 4 :
                        #Monocular
                        if sample_eye == "LEFT" :
                            samples_time_check_left.append(float(ligne_complete[0]) - time_start)
                            samples_xpl.append(float(ligne_complete[1]))
                            samples_ypl.append(float(ligne_complete[2]))
                            samples_pupil_l.append(float(ligne_complete[3]))
                        elif sample_eye == "RIGHT" :
                            samples_time_check_right.append(float(ligne_complete[0]) - time_start)
                            samples_xpr.append(float(ligne_complete[1]))
                            samples_ypr.append(float(ligne_complete[2]))
                            samples_pupil_r.append(float(ligne_complete[3]))
                        else :
                            print("\nErreur dans le type 'sample_eye', n'appartient pas à [LEFT, RIGHT] ! \n")
                    elif longueur == 6 :
                        #Monocular, with velocity ou Monocular, with resolution 
                        if sample_eye == "LEFT" :
                            samples_time_check_left.append(float(ligne_complete[0]) - time_start)
                            samples_xpl.append(float(ligne_complete[1]))
                            samples_ypl.append(float(ligne_complete[2]))
                            samples_pupil_l.append(float(ligne_complete[3]))
                        elif sample_eye == "RIGHT" :
                            samples_time_check_right.append(float(ligne_complete[0]) - time_start)
                            samples_xpr.append(float(ligne_complete[1]))
                            samples_ypr.append(float(ligne_complete[2]))
                            samples_pupil_r.append(float(ligne_complete[3]))
                        else :
                            print("\nErreur dans le type 'sample_eye', n'appartient pas à [LEFT, RIGHT] ! \n")


                        #Ne sait pas comment différencier <xv> ou <xr>

                        #A compléter pour "ligne_complete[4]" et "ligne_complete[5]"


                    elif longueur == 8 :
                        #Monocular, with velocity and resolution
                        samples_resolution_x.append(float(ligne_complete[6]))
                        samples_resolution_y.append(float(ligne_complete[7]))
                        if sample_eye == "LEFT" :
                            samples_time_check_left.append(float(ligne_complete[0]) - time_start)
                            samples_xpl.append(float(ligne_complete[1]))
                            samples_ypl.append(float(ligne_complete[2]))
                            samples_pupil_l.append(float(ligne_complete[3]))
                            samples_xvelocity_l.append(float(ligne_complete[4]) / vprescaler)
                            samples_yvelocity_l.append(float(ligne_complete[5]) / vprescaler)
                        elif sample_eye == "RIGHT" :
                            samples_time_check_right.append(float(ligne_complete[0]) - time_start)
                            samples_xpr.append(float(ligne_complete[1]))
                            samples_ypr.append(float(ligne_complete[2]))
                            samples_pupil_r.append(float(ligne_complete[3]))
                            samples_xvelocity_r.append(float(ligne_complete[4]) / vprescaler)
                            samples_yvelocity_r.append(float(ligne_complete[5]) / vprescaler)
                        else :
                            print("\nErreur dans le type 'sample_eye', n'appartient pas à [LEFT, RIGHT] ! \n")
                    elif longueur == 7 :
                        #Binocular 
                        samples_time_check_left.append(float(ligne_complete[0]) - time_start)
                        samples_time_check_right.append(float(ligne_complete[0]) - time_start)
                        samples_xpl.append(float(ligne_complete[1]))
                        samples_ypl.append(float(ligne_complete[2]))
                        samples_pupil_l.append(float(ligne_complete[3]))
                        samples_xpr.append(float(ligne_complete[4]))
                        samples_ypr.append(float(ligne_complete[5]))
                        samples_pupil_r.append(float(ligne_complete[6]))
                    elif longueur == 11 :
                        #Binocular, with velocity
                        samples_time_check_left.append(float(ligne_complete[0]) - time_start)
                        samples_time_check_right.append(float(ligne_complete[0]) - time_start)
                        samples_xpl.append(float(ligne_complete[1]))
                        samples_ypl.append(float(ligne_complete[2]))
                        samples_pupil_l.append(float(ligne_complete[3]))
                        samples_xpr.append(float(ligne_complete[4]))
                        samples_ypr.append(float(ligne_complete[5]))
                        samples_pupil_r.append(float(ligne_complete[6]))
                        samples_xvelocity_l.append(float(ligne_complete[7]) / vprescaler)
                        samples_yvelocity_l.append(float(ligne_complete[8]) / vprescaler)
                        samples_xvelocity_r.append(float(ligne_complete[9]) / vprescaler)
                        samples_yvelocity_r.append(float(ligne_complete[10]) / vprescaler)
                    elif longueur == 9 :
                        #Binocular, with and resolution 
                        samples_time_check_left.append(float(ligne_complete[0]) - time_start)
                        samples_time_check_right.append(float(ligne_complete[0]) - time_start)
                        samples_xpl.append(float(ligne_complete[1]))
                        samples_ypl.append(float(ligne_complete[2]))
                        samples_pupil_l.append(float(ligne_complete[3]))
                        samples_xpr.append(float(ligne_complete[4]))
                        samples_ypr.append(float(ligne_complete[5]))
                        samples_pupil_r.append(float(ligne_complete[6]))
                        samples_resolution_x.append(float(ligne_complete[7]))
                        samples_resolution_y.append(float(ligne_complete[8]))
                    elif longueur == 13 :
                        #Binocular, with velocity and resolution
                        samples_time_check_left.append(float(ligne_complete[0]) - time_start)
                        samples_time_check_right.append(float(ligne_complete[0]) - time_start)
                        samples_xpl.append(float(ligne_complete[1]))
                        samples_ypl.append(float(ligne_complete[2]))
                        samples_pupil_l.append(float(ligne_complete[3]))
                        samples_xpr.append(float(ligne_complete[4]))
                        samples_ypr.append(float(ligne_complete[5]))
                        samples_pupil_r.append(float(ligne_complete[6]))
                        samples_xvelocity_l.append(float(ligne_complete[7]) / vprescaler)
                        samples_yvelocity_l.append(float(ligne_complete[8]) / vprescaler)
                        samples_xvelocity_r.append(float(ligne_complete[9]) / vprescaler)
                        samples_yvelocity_r.append(float(ligne_complete[10]) / vprescaler)
                        samples_resolution_x.append(float(ligne_complete[11]))
                        samples_resolution_y.append(float(ligne_complete[12]))
    
    
    



    # Créer un DataFrame pandas pour les messages si désiré
    # Pour avoir le temps des messages en fonctions de notre enregistrement
    for i in range(len(time_message)):
        time_message[i] -= time_start
    message = {'Time': time_message, 'Message': data_message}
    message_df = pd.DataFrame(message)
    
    # Paramètres de la heatmap                                                  <-- can be modified to upgrade quality and/or size
    heatmap_size_x = (-30000, 30000) # Taille de l'écran dans le manuel Eyelink 
    heatmap_size_y = (-30000, 30000) # Taille de l'écran dans le manuel Eyelink
    heatmap_bins = 500  # Nombre de bins pour la heatmap
    
    # Créer un DataFrame pandas pour les données d'échantillons si désiré
    sample_left_colonnes = {}
    if samples_time_check_left :
        sample_left_colonnes['Time'] = samples_time_check_left
        # Ajoute position gauche
        sample_left_colonnes['Left Pos. x'] = samples_xpl
        sample_left_colonnes['Left Pos. y'] = samples_ypl

        # Création de l'histogramme 2D
        heatmap_left, xedges_left, yedges_left = np.histogram2d(samples_xpl, samples_ypl, bins=heatmap_bins, range=(heatmap_size_x, heatmap_size_y))
        if flag[1] :
            
            # Création de la heatmap
            extent = [xedges_left[0], xedges_left[-1], yedges_left[0], yedges_left[-1]]
            plt.imshow(heatmap_left.T, extent=extent, origin='lower', cmap='hot')
            plt.colorbar()
            plt.xlabel('X')
            plt.ylabel('Y')
            plt.title('Heatmap Left Eye')
            plt.show(block=False)
        
        if samples_pupil_l :
            # Ajoute pupille gauche
            sample_left_colonnes['Left Pupil Size'] = samples_pupil_l

        if samples_xvelocity_l :
            # Ajoute vitesse gauche
            sample_left_colonnes['Left Vel. x'] = samples_xvelocity_l
            sample_left_colonnes['Left Vel. y'] = samples_yvelocity_l
    else :
        print("\nNo Samples on Left Eye !")
    
    sample_right_colonnes = {}
    if samples_time_check_right :
        sample_right_colonnes['Time'] = samples_time_check_right
        # Ajoute position droite
        sample_right_colonnes['Right Pos. x'] = samples_xpr
        sample_right_colonnes['Right Pos. y'] = samples_ypr

        # Création de l'histogramme 2D
        heatmap_right, xedges_right, yedges_right = np.histogram2d(samples_xpr, samples_ypr, bins=heatmap_bins, range=(heatmap_size_x, heatmap_size_y))
        if flag[1] :

            # Création de la heatmap
            extent = [xedges_right[0], xedges_right[-1], yedges_right[0], yedges_right[-1]]
            plt.imshow(heatmap_right.T, extent=extent, origin='lower', cmap='hot')
            plt.colorbar()
            plt.xlabel('X')
            plt.ylabel('Y')
            plt.title('Heatmap Right Eye')
            plt.show(block=False)

        if samples_pupil_r :
            # Ajoute pupille droite
            sample_right_colonnes['Right Pupil Size'] = samples_pupil_r
        
        if samples_xpr :
            # Ajoute vitesse droite
            sample_right_colonnes['Right Vel. x'] = samples_xvelocity_r
            sample_right_colonnes['Right Vel. y'] = samples_yvelocity_r
    else :
        print("\nNo Samples on Right Eye !")
        
    if samples_resolution_x :
        #Ajoute resolution
        sample_left_colonnes['Res. x'] = samples_resolution_x
        sample_left_colonnes['Res. y'] = samples_resolution_y
        sample_right_colonnes['Res. x'] = samples_resolution_x
        sample_right_colonnes['Res. y'] = samples_resolution_y
            
    sample_left_eye_df = pd.DataFrame(sample_left_colonnes)
    sample_right_eye_df = pd.DataFrame(sample_right_colonnes)


    # Supprime les fixations qui ont lieu moins de 120 millisecondes avant ou après un clignement
    # Gauche
    index_a_supp = []
    if len(time_eye_blink_left) != len(end_time_eye_blink_left) :
        print("\nErreur, il n'y a pas le même nombre d'ouverture que de fermeture d'oeil gauche !")
    for t in range(len(time_eye_blink_left)) :
        for i in range(len(time_eye_fix_left)) :
            valeur_compare = time_eye_fix_left[i]
            if valeur_compare <= time_eye_blink_left[t] and valeur_compare > time_eye_blink_left[t] - 120 :
                index_a_supp.append(i)
            elif valeur_compare < end_time_eye_blink_left[t] + 120 and valeur_compare >= end_time_eye_blink_left[t] :
                index_a_supp.append(i)
    #On supprime d'abord les index grands pour pas modifier les plus petits
    for index in reversed(index_a_supp) :
        del time_eye_fix_left[index]
        del eye_fix_left_duration[index]
        del eye_fix_left_pos_x[index]
        del eye_fix_left_pos_y[index]
        del eye_fix_left_pupil[index]
    # Droite
    index_a_supp = []
    if len(time_eye_blink_right) != len(end_time_eye_blink_right) :
        print("\nErreur, il n'y a pas le même nombre d'ouverture que de fermeture d'oeil droit !")
    for t in range(len(time_eye_blink_right)) :
        for i in range(len(time_eye_fix_right)) :
            valeur_compare = time_eye_fix_right[i]
            if valeur_compare <= time_eye_blink_right[t] and valeur_compare > time_eye_blink_right[t] - 120 :
                index_a_supp.append(i)
            elif valeur_compare < end_time_eye_blink_right[t] + 120 and valeur_compare >= end_time_eye_blink_right[t] :
                index_a_supp.append(i)
    #On supprime d'abord les index grands pour pas modifier les plus petits
    for index in reversed(index_a_supp) :
        del time_eye_fix_right[index]
        del eye_fix_right_duration[index]
        del eye_fix_right_pos_x[index]
        del eye_fix_right_pos_y[index]
        del eye_fix_right_pupil[index]


    # Créer un DataFrame pandas pour les fixations si désiré
    fix_left_colonnes = {}
    fix_right_colonnes = {}
    if time_eye_fix_left :
        # Ajoute fixations gauche
        fix_left_colonnes['Start Time'] = time_eye_fix_left
        fix_left_colonnes['Duration'] = eye_fix_left_duration
        fix_left_colonnes['Avg. Left Pos. x'] = eye_fix_left_pos_x
        fix_left_colonnes['Avg. Left Pos. y'] = eye_fix_left_pos_y
        fix_left_colonnes['Avg. Left Pupil Size'] = eye_fix_left_pupil
    else :
        print("\nNo Fixations on Left Eye !")
    fixations_left_eye_df = pd.DataFrame(fix_left_colonnes)

    if time_eye_fix_right :
        # Ajoute fixations droite
        fix_right_colonnes['Start Time'] = time_eye_fix_right
        fix_right_colonnes['Duration'] = eye_fix_right_duration
        fix_right_colonnes['Avg. Right Pos. x'] = eye_fix_right_pos_x
        fix_right_colonnes['Avg. Right Pos. y'] = eye_fix_right_pos_y
        fix_right_colonnes['Avg. Right Pupil Size'] = eye_fix_right_pupil
    else :
        print("\nNo Fixations on Right Eye !")
    fixations_right_eye_df = pd.DataFrame(fix_right_colonnes)

    # Créer un DataFrame pandas pour les saccades si désiré
    sacc_left_colonnes = {}
    sacc_right_colonnes = {}
    if time_eye_sacc_left :
        # Ajoute saccade gauche
        sacc_left_colonnes['Start Time'] = time_eye_sacc_left
        sacc_left_colonnes['Duration'] = eye_sacc_left_duration
        sacc_left_colonnes['Start Left Pos. x'] = eye_sacc_left_start_pos_x
        sacc_left_colonnes['Start Left Pos. y'] = eye_sacc_left_start_pos_y
        sacc_left_colonnes['End Left Pos. x'] = eye_sacc_left_end_pos_x
        sacc_left_colonnes['End Left Pos. y'] = eye_sacc_left_end_pos_y
        sacc_left_colonnes['Angle Covered'] = eye_sacc_left_angle
        sacc_left_colonnes['Peak Velocity'] = eye_sacc_left_vmax
        
    else :
        print("\nNo Saccades on Left Eye !")
    saccades_left_eye_df = pd.DataFrame(sacc_left_colonnes)

    if time_eye_sacc_right :
        # Ajoute saccade droite
        sacc_right_colonnes['Start Time'] = time_eye_sacc_right
        sacc_right_colonnes['Duration'] = eye_sacc_right_duration
        sacc_right_colonnes['Start Right Pos. x'] = eye_sacc_right_start_pos_x
        sacc_right_colonnes['Start Right Pos. y'] = eye_sacc_right_start_pos_y
        sacc_left_colonnes['End Right Pos. x'] = eye_sacc_right_end_pos_x
        sacc_left_colonnes['End Right Pos. y'] = eye_sacc_right_end_pos_y
        sacc_right_colonnes['Angle Covered'] = eye_sacc_right_angle
        sacc_left_colonnes['Peak Velocity'] = eye_sacc_right_vmax
    else :
        print("\nNo Saccades on Right Eye !")
    saccades_right_eye_df = pd.DataFrame(sacc_right_colonnes)

    # Créer un DataFrame pandas pour les blink si désiré

    blink_left_colonnes = {}
    blink_right_colonnes = {}
    if time_eye_blink_left :
        # Ajoute clignemment gauche
        blink_left_colonnes['Start Time'] = time_eye_blink_left
        blink_left_colonnes['End Time'] = end_time_eye_blink_left
        blink_left_colonnes['Duration'] = eye_blink_left_duration
    else :
        print("\nNo Blinks on Left Eye !")
    blink_left_eye_df = pd.DataFrame(blink_left_colonnes)

    if time_eye_blink_right :
        # Ajoute clignemment droite
        blink_right_colonnes['Start Time'] = time_eye_blink_right
        blink_right_colonnes['End Time'] = end_time_eye_blink_right
        blink_right_colonnes['Duration'] = eye_blink_right_duration
    else :
        print("\nNo Blinks on Right Eye !")
    blink_right_eye_df = pd.DataFrame(blink_right_colonnes)

    # Créer un DataFrame pandas pour les button si désiré
    button_colonnes = {}
    if button_time :
        button_colonnes['Start Time'] = button_time
        button_colonnes['Button Nbr.'] = button_type
        button_colonnes['State'] = button_action
    else :
        print("\nNo Buttons used !")
    button_df = pd.DataFrame(button_colonnes)

    # Affichage des informations souhaitées/disponibles
    # if flag[0] and flag[1] and flag[2]:
    #     show(message_df, sample_left_eye_df, sample_right_eye_df, fixations_left_eye_df, fixations_right_eye_df, saccades_left_eye_df, saccades_right_eye_df, blink_left_eye_df, blink_right_eye_df, button_df)
    # elif not flag[0] and flag[1] and flag[2]:
    #     show(sample_left_eye_df, sample_right_eye_df, fixations_left_eye_df, fixations_right_eye_df, saccades_left_eye_df, saccades_right_eye_df, blink_left_eye_df, blink_right_eye_df, button_df)
    # elif not flag[0] and not flag[1] and flag[2]:
    #     show(fixations_left_eye_df, fixations_right_eye_df, saccades_left_eye_df, saccades_right_eye_df, blink_left_eye_df, blink_right_eye_df, button_df)
    # elif not flag[0] and flag[1] and not flag[2]:
    #     show(sample_left_eye_df, sample_right_eye_df)
    # elif flag[0] and not flag[1] and flag[2]:
    #     show(message_df, fixations_left_eye_df, fixations_right_eye_df, saccades_left_eye_df, saccades_right_eye_df, blink_left_eye_df, blink_right_eye_df, button_df)
    # elif flag[0] and flag[1] and not flag[2]:
    #     show(message_df, sample_left_eye_df, sample_right_eye_df)

    # Pour sauvegarder les DataFrames dans des fichiers
    save = input("\nDo you want to save some data, if yes precision later (y/n) : ")
    if save == "y" :
        path_to_save = chemin_fichier_asc[:-4] 
        # Messages
        flag_save_messages = input("\nDo you want to save messages dataframe (y/n) : ")
        if flag_save_messages == "y" :
            message_df.to_csv(path_to_save + '_messages.csv', index=False)
            print("Messages saved !")
        elif flag_save_messages == "n" :
            print("Messages not saved !")
        else :
            print("Value not valable. Messages not saved !")
        
        # Samples
        flag_save_samples = input("\nDo you want to save samples dataframe + heatmap (y/n) : ")
        if flag_save_samples == "y" :
            if samples_time_check_left :
                sample_left_eye_df.to_csv(path_to_save + '_samples_left_eye.csv', index=False)
                # Chaque ligne du fichier texte équivaudra à une ligne de la heatmap
                np.savetxt(path_to_save + '_heatmap_left_eye.txt', heatmap_left)
                print("Samples saved for left eye !")
            else :
                print("No samples to save for left eye !")
            if samples_time_check_right :
                sample_right_eye_df.to_csv(path_to_save + '_samples_right_eye.csv', index=False)
                np.savetxt(path_to_save + '_heatmap_right_eye.txt', heatmap_right)
                print("Samples saved for right eye !")
            else :
                print("No samples to save for right eye !")
        elif flag_save_samples == "n" :
            print("Samples not saved !")
        else :
            print("Value not valable. Samples not saved !")

        # Fixations
        flag_save_fix = input("\nDo you want to save fixations dataframe (y/n) : ")
        if flag_save_fix == "y" :
            if time_eye_fix_left :
                fixations_left_eye_df.to_csv(path_to_save + '_fixations_left_eye.csv', index=False)
                print("Fixations saved for left eye !")
            else :
                print("No fixations to save for left eye !")
            if time_eye_fix_right :
                fixations_right_eye_df.to_csv(path_to_save + '_fixations_right_eye.csv', index=False)
                print("Fixations saved for right eye !")
            else :
                print("No fixations to save for right eye !")
        elif flag_save_fix == "n" :
            print("Fixations not saved !")
        else :
            print("Value not valable. Fixations not saved !")
        
        # Saccades
        flag_save_sacc = input("\nDo you want to save saccades dataframe (y/n) : ")
        if flag_save_sacc == "y" :
            if time_eye_sacc_left :
                saccades_left_eye_df.to_csv(path_to_save + '_saccades_left_eye.csv', index=False)
                print("Saccades saved for left eye !")
            else :
                print("No saccades to save for left eye !")
            if time_eye_sacc_right :
                saccades_right_eye_df.to_csv(path_to_save + '_saccades_right_eye.csv', index=False)
                print("Saccades saved for right eye !")
            else :
                print("No saccades to save for right eye !")
        elif flag_save_sacc == "n" :
            print("Saccades not saved !")
        else :
            print("Value not valable. Saccades not saved !")
        
        # Blinks
        flag_save_blinks = input("\nDo you want to save blinks dataframe (y/n) : ")
        if flag_save_blinks == "y" :
            if time_eye_blink_left :
                blink_left_eye_df.to_csv(path_to_save + '_blinks_left_eye.csv', index=False)
                print("Blinks saved for left eye !")
            else :
                print("No blinks to save for left eye !")
            if time_eye_blink_right :
                blink_right_eye_df.to_csv(path_to_save + '_blinks_right_eye.csv', index=False)
                print("Blinks saved for right eye !")
            else :
                print("No blinks to save for right eye !")
        elif flag_save_blinks == "n" :
            print("Blinks not saved !")
        else :
            print("Value not valable. Blinks not saved !")
        
        # Button
        flag_save_button = input("\nDo you want to save button dataframe (y/n) : ")
        if flag_save_button == "y" :
            button_df.to_csv(path_to_save + '_button.csv', index=False)
            print("Button saved !")
        elif flag_save_button == "n" :
            print("Button not saved !")
        else :
            print("Value not valable. Button not saved !")
    elif save == "n" :
        print("Nothing to save !\nEnd of program.\n")
    else :
        print("Value not valable. Nothing to save !\nEnd of program.\n")


# Chemin vers le fichier .asc
chemin_fichier_asc = input("\nEnter .asc file path : ")

# Flag d'affichage
# [MSG, SAMPLES, EVENTS]
flag_affichage = [False, False, False]

# MSG
flag_message = input("\nDo you want to see messages (y/n) : ")
if flag_message == "y" :
    flag_affichage[0] = True
elif flag_message == "n" :
    flag_affichage[0] = False
else :
    flag_affichage[0] = False
    print("Value not valable. Not printed !")

#SAMPLES
flag_samples = input("\nDo you want to see samples (y/n) : ")
if flag_samples == "y" :
    flag_affichage[1] = True
elif flag_samples == "n" :
    flag_affichage[1] = False
else :
    flag_affichage[1] = False
    print("Value not valable. Not printed !")

#EVENTS
flag_events = input("\nDo you want to see events (y/n) : ")
if flag_events == "y" :
    flag_affichage[2] = True
elif flag_events == "n" :
    flag_affichage[2] = False
else :
    flag_affichage[2] = False
    print("Value not valable. Not printed !")


# Lecture du fichier .asc
lire_fichier_asc(chemin_fichier_asc, flag_affichage)

