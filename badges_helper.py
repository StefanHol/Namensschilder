#!/usr/bin/env python

import os
from PyPDF2 import PdfWriter
import pandas as pd
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF


__version__ = "0.0.3"
__author__ = "Stefan Holstein"
__based_author__ = "Unknown"
__repo__ = r"https://github.com/StefanHol/Namensschilder"


class badges_helper():
    def __init__(self, TEMPLATE='Namensschilder_PythonCamp (87x53).svg',
                 datei_userdaten=r"Demo_data.xls",
                 output_folder_name="output",
                 all_badges_output_name="Badges.pdf"):
        self.PATTERN_VORNAME = 'firstname'
        self.PATTERN_NACHNAME = 'lastname'
        self.PATTERN_ORGA = "orga"
        self.TEMPLATE = TEMPLATE
        # # csv eingabe datei
        self.datei_userdaten = datei_userdaten
        # # Ausgabe Ordner
        self.output_folder_name = output_folder_name
        # alle badges zusammengefasst.
        self.all_badges_output_name = all_badges_output_name

    def load_template(self, TEMPLATE=None):
        if TEMPLATE is None:
            TEMPLATE = self.TEMPLATE
        with open(TEMPLATE) as f:
            template = f.read()
        return template

    def save_output(self, data, num, folder_name=None):
        if folder_name is None:
            folder_name = self.output_folder_name
        print(f"save: {num}")
        if not os.path.isdir(folder_name):
            os.mkdir(folder_name)
        with open(folder_name + os.path.sep + 'n_%d.svg' % num, 'w') as f:
            f.write(data)

    def check_create_folder(self, folder_name=None):
        if folder_name is None:
            folder_name = self.output_folder_name
        if not os.path.exists(os.getcwd() + os.path.sep + folder_name):
            os.makedirs(os.getcwd() + os.path.sep + folder_name, exist_ok=True)

    def convert_svg_to_pdf(self, folder, filename):
        try:
            drawing = svg2rlg(folder + os.path.sep + filename)
            base = os.path.splitext(filename)[0]
            pdf_filename = f"{base}.pdf"
            renderPDF.drawToFile(drawing, folder + os.path.sep + pdf_filename)
            return pdf_filename
        except Exception as e:
            print("Error in convert_svg_to_pdf" + f"{e}")
        return

    def read_BarCamp_data_csv(self, datei_userdaten=None):
        if datei_userdaten is None:
            datei_userdaten = self.datei_userdaten
        df = pd.read_csv(datei_userdaten, sep=";", encoding='utf-8')
        df = df[(df[['Status']] != "canceled").all(axis=1)]
        df.reset_index(drop=True, inplace=True)
        for index, row in df.iterrows():
            name = row["Name"].strip().split(" ")
            firstname = name[0]
            lastname = " ".join(name[1:])
            df.loc[df.index[index], 'firstname'] = firstname
            df.loc[df.index[index], 'lastname'] = lastname
            # print(index, name,  firstname,": ", lastname)
        for index, row in df.iterrows():
            ticket = row["Ticket"]
            if "Organisationsmitglied" in ticket:
                df.loc[df.index[index], 'orga'] = "Orga"
                # print(index, row["Name"], ticket)
            else:
                df.loc[df.index[index], 'orga'] = " "
                # print(index, row["Name"], " ")
        return df

    def read_BarCamp_data_excel(self, datei_userdaten=None):
        if datei_userdaten is None:
            datei_userdaten = self.datei_userdaten
        df = pd.read_excel(datei_userdaten)
        df = df[(df[['Status']] != "canceled").all(axis=1)]
        df.reset_index(drop=True, inplace=True)
        for index, row in df.iterrows():
            name = row["Name"].strip().split(" ")
            firstname = name[0]
            lastname = " ".join(name[1:])
            df.loc[df.index[index], 'firstname'] = firstname
            df.loc[df.index[index], 'lastname'] = lastname
            # print(index, name,  firstname,": ", lastname)
        for index, row in df.iterrows():
            ticket = row["Ticket"]
            if "Organisationsmitglied" in ticket:
                df.loc[df.index[index], 'orga'] = "Orga"
                # print(index, row["Name"], ticket)
            else:
                df.loc[df.index[index], 'orga'] = " "
                # print(index, row["Name"], " ")
        return df

    def read_pdf_files_in_folder(self, pdf_folder=None):
        '''Function return all PDFs-files in folder "pdf_folder".
        input: FolderName with pdf files
        return: array
        '''
        if pdf_folder is None:
            pdf_folder = self.output_folder_name
        extention = ".pdf"
        if os.path.exists(pdf_folder):
            pdf_file_name_array = []
            for filename in os.listdir(pdf_folder):
                if filename.lower().endswith(extention):
                    pdf_file_name_array.append(filename)
            all_pdf_names = []
            for actual_pdf_file_name in pdf_file_name_array:
                all_pdf_names.append(actual_pdf_file_name)
                # print(PDFFolder + os.path.sep + ActualPDFFileName)
        else:
            print(f"Folder {pdf_folder} not found")
        return all_pdf_names

    def merge_all_pdfs_in_folder(self, pdf_folder, pdf_output_name):
        all_pdf_names = self.read_pdf_files_in_folder(pdf_folder)
        try:
            merger = PdfWriter()
            for pdf in all_pdf_names:
                merger.append(pdf_folder + os.path.sep + pdf)
            merger.write(pdf_output_name)
        except Exception as e:
            print(e)
        finally:
            merger.close()
        return pdf_output_name

    def convert_all_svg_to_pdf(self, output_folder_name=None):
        """Find all svg files in given folder and convert each file to pdf.
        """
        if output_folder_name is None:
            output_folder_name = self.output_folder_name
        ext = ('.svg')
        svg_filenames = []
        for files in os.listdir(output_folder_name):
            if files.endswith(ext):
                svg_filenames.append(files)
            else:
                continue
        pdf_filenames = []
        for filename in svg_filenames:
            pdf_file = self.convert_svg_to_pdf(output_folder_name, filename)
            print(f"{filename} -> {pdf_file}")
            if os.path.exists(output_folder_name + os.path.sep + pdf_file):
                pdf_filenames.append(pdf_file)
        return [svg_filenames, pdf_filenames]

    def main(self, df, svg_template=None, enable_clear_template=True):
        if svg_template is None:
            svg_template = self.TEMPLATE
        current = template = self.load_template(svg_template)
        num = 1
        for index, row in df.iterrows():
            firstname = str(row['firstname'])
            lastname = str(row['lastname'])
            orga = str(row['orga'])
            print(f"{lastname}, {firstname}, '{orga}'")
            if ((not (self.PATTERN_NACHNAME in current)) and
                    (not (self.PATTERN_VORNAME in current))):
                self.save_output(current, index+1)
                num += 1
                current = template
            current = current.replace(self.PATTERN_VORNAME, firstname, 1)
            current = current.replace(self.PATTERN_NACHNAME, lastname, 1)
            current = current.replace(self.PATTERN_ORGA, orga, 1)
            # print(firstname, lastname, orga)

        if enable_clear_template:
            clear_template = True
            while clear_template:
                if ((self.PATTERN_NACHNAME in current) and
                        (self.PATTERN_VORNAME in current)):
                    firstname = " "
                    lastname = " "
                    orga = " "
                    current = current.replace(self.PATTERN_VORNAME,
                                              firstname, 1)
                    current = current.replace(self.PATTERN_NACHNAME,
                                              lastname, 1)
                    current = current.replace(self.PATTERN_ORGA,
                                              orga, 1)
                if ((not (self.PATTERN_NACHNAME in current)) and
                        (not (self.PATTERN_VORNAME in current))):
                    clear_template = False
                    break
        self.save_output(current, index+1+num)
