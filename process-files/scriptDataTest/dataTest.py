import sys
import re
# import os

sourceFile=sys.argv[1]

img_string = ""
inside_thumbnail = False

# Načtení souboru a zpracování řádků s thumbnail částí
with open(sourceFile, "r") as f:
    for line in f:
        # Odstranění bílých znaků na začátku a konci řádku
        line = line.strip()

        # Kontrola, zda začíná thumbnail část
        if line.startswith("; thumbnail begin 400x300"): # 32x32
            inside_thumbnail = True
            continue

        # Kontrola, zda končí thumbnail část
        if line.startswith("; thumbnail end"):
            inside_thumbnail = False
            break

        # Pokud jsme uvnitř thumbnail části, přidáme řádek do výsledného stringu
        if inside_thumbnail:
            img_string += line + '\n'

# Odstranění posledního nového řádku na konci stringu (volitelné)
img_string = img_string.rstrip()

img_Base64 = img_string.replace("; ", "")

# Test zápisu do souboru
with open(sourceFile, "w") as of:
    of.write("hello world\n")

# Logování výsledku
with open("E:\Ostatni - Soubory\projects\VisualStudioCodes\GcodePreview\scriptDataTest\output.txt", "w") as log:
    log.write(str(img_Base64))

log.close()
of.close()
f.close()