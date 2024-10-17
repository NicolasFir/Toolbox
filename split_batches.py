import os
import glob

# Repertoire contenant les fichiers fastq.gz
source_dir = "/data/ADDIA_PBMC_transposon/01_concat_sample"  # repertoire source

# Repertoire ou les dossiers avec les liens symboliques seront crees
target_base_dir = "/Clients/FIRALIS/NeurolincPaper/on_going/02_fastq/NLC_102024_008_PBMC/Batches/"  # Remplace par ton repertoire cible

# Creer les 20 dossiers avec 50 IDs (chaque ID a deux fichiers R1 et R2)
batch = 1
id_count = 0

# Recuperer la liste des fichiers R1
files_r1 = sorted(glob.glob(os.path.join(source_dir, "*_R1_*.fastq.gz")))

# Verifier s'il y a assez de paires
if len(files_r1) < 764:
    print("Il n'y a pas assez de paires de fichiers dans le repertoire source.")
    exit(1)

# Traiter chaque fichier R1 et trouver son R2 correspondant
for file_r1 in files_r1:
    # Extraire l'ID (ex: F2010829001) du fichier R1
    base_name = os.path.basename(file_r1)
    file_id = base_name.split('_')[0]  # L'ID est avant le premier '_'

    # Trouver le fichier R2 correspondant
    file_r2_pattern = os.path.join(source_dir, f"{file_id}_*_R2_*.fastq.gz")
    file_r2 = glob.glob(file_r2_pattern)
    
    if not file_r2:
        print(f"Fichier R2 manquant pour l'ID {file_id}")
        continue
    
    file_r2 = file_r2[0]  # Prendre le premier (et unique) fichier R2 trouve

    # Creer un nouveau dossier tous les 50 IDs
    if id_count % 50 == 0:
        batch_dir = os.path.join(target_base_dir, f"batch_{batch:02d}")
        os.makedirs(batch_dir, exist_ok=True)
        batch += 1

    # Creer des liens symboliques pour R1 et R2 dans le dossier batch courant
    os.symlink(file_r1, os.path.join(batch_dir, os.path.basename(file_r1)))
    os.symlink(file_r2, os.path.join(batch_dir, os.path.basename(file_r2)))

    # Incrementer le compteur d'ID
    id_count += 1

    # Arreter apres avoir traite 1000 IDs (soit 2000 fichiers)
    if id_count == 1000:
        break

print(f"Liens symboliques crees dans {batch-1} dossiers.")
