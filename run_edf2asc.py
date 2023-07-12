import subprocess

chemin_fichier_edf = input("\nEnter .edf file path : ")

print(f"Conversion of {chemin_fichier_edf}...")
try:
    subprocess.check_call(['edf2asc.exe ' ,chemin_fichier_edf])
    print(f"{chemin_fichier_edf} converted succesfully in .asc !")
except subprocess.CalledProcessError:
    print(f"error in converting {chemin_fichier_edf} to .asc")