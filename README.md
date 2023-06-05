# Namensschilder Drucken

Hiermit habe ich die Namensschilder für das [Python BarCamp](https://barcamps.eu/pyr2023/) angelegt.


![Gedruckte Badges](/img/Badges.jpeg "Gedruckte Badges"){width=250}


## Raster / Größe festlegen

- Mit dem Notebook [Berechnung Inkscape Grid.ipynb] wird eine Incskape SVG Template Datei erzeugt.
    - Papierformat `A4`
    - Die Größe der Namensschilder / Badges werden mit den beiden Variablen `badge_width` und `bagde_height` in `mm` festgelegt
    - Es wird ein Raster berechnet und mittig auf dem A4 Blatt angeordnet.
        - Horrizontales- / Vertikales Raster
    - Der Name der Ausgabedatei kann über `tamplate_dateiname` angepasst werden.
    - ![Raw Template](/img/Template_img.png "Raw Template"){width=500}

---

## Anpassungen

- Das Template kann nun umbenannt und nach eigenen Wünschen angepasst werden. -> Dateiname muss später im [NamenschilderPythonCamp.ipynb] angepasst werden
- Dazu kann aus der Beiliegenden Vorlage Datei `Zeichnung-demo_1.svg` ein 'Badge' herauskopiert und nach eigenen Wünschen angepasst werden.
- Die die Textfelder `firstname`, `lastname` und `orga` sind erforderlich.
- Bilder, Positionen, Größe und zusätzliche Inhalte können nach belieben gestaltet werden.

- Alternativ kann das die Vorlage `Namensschilder_PythonCamp (87x53).svg` verwendet werden.
- ![Angepasste Vorlage](/img/Filled_Template_img.png "Angepasste Vorlage"){width=500}

---

## Eingangsdaten

- Die Teilnehmerliste kann aus dem BarCamp Tool https://barcamps.eu/ , im Administrationebereich heruntergeladen werden.
    - ![Teilnehmer herunterladen](/img/Teinmehmer_herunterladen.png "Teilnehmer herunterladen"){width=250}
    - Diese Excel Datei kann direkt mit der Funktion `read_BarCamp_data_excel(datei_userdaten)` eingelesen werden und liefert das `df` mit 3 neuen Spalten zurück (firstname, lastname, orga) 

---

## Namensschilder befüllen und drucken

- Mit dem Notebook [NamenschilderPythonCamp.ipynb] können nun die Badges mit Inhalten gefüllt werden.
- Das oben bearbeitete Template muss der Variablen `TEMPLATE` zugewiesn werden.
- Wenn alles vorbereitet ist, einfach durchlaufen lassen. und wahlweise die SVG/PDFs einzeln oder drucken.
    - je nach Vorlage, kann der automatische export von SVG -> PDF zu fehlerhaften ergebnissen führen. Dann entweder das SVG aus Incskape heraus drucken oder mit Incskape das PDF exportieren.
Code
``` py
# Import
from badges_helper import BadgesHelper as badges_helper

#######################################################
# Beispiel Daten
#######################################################

# # *.svg Template Daten
template_file = 'Namensschilder_PythonCamp (87x53).svg'

# # csv eingabe datei
datei_userdaten = r"23-05-30-participants.xls"
datei_userdaten = r"Demo_data.xls"

# # Ausgabe Ordner
output_folder_name = "output"
# alle badges zusammengefasst.
all_badges_output_name = "Badges.pdf"
#######################################################

# Erstelle Badges handler
badges_handler = badges_helper(template = template_file,
                       datei_userdaten = datei_userdaten,
                       output_folder_name = output_folder_name,
                       all_badges_output_name = all_badges_output_name)

# Erstelle den Ausgabe-Ordner, falls er nicht existiert.
#  -> output_folder_name
badges_handler.check_create_folder()

# Daten lesen und dem `df` zuweisen
df = badges_handler.read_bar_camp_data_excel()

# Daten in die finalen SVG Dateie übertragen. 
badges_handler.main(df=df)

# Umwandlung SVG -> PDF
badges_handler.convert_all_svg_to_pdf()

# Optional alle PDFs zusammenfassen.
badges_handler.read_pdf_files_in_folder()
badges_handler.merge_all_pdfs_in_folder(output_folder_name, all_badges_output_name)

```
- ![Filled Badges](/img/Filled_Badges_img.png "Filled Badges"){width=500}


  
## Zuschneiden und Einlegen

- ![Gedruckte Badges](/img/Badges.jpeg "Gedruckte Badges"){width=500}

---


