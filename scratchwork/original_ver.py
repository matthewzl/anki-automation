"""
Meant to be run on a Python IDE with the directory string changed manually...
"""

import genanki  # pip install genanki
import random
import pandas as pd  # pip install pandas, pip install openpyxl
import fitz  # pip install PyMuPDF
import os
import warnings

# CHANGE HERE ######################################################################################
####################################################################################################

input_directory: str = '/Users/matthewliu/Desktop/test'  # should have 1 xlsx and 1 pdf
output_directory = input_directory  # change if you want

####################################################################################################
####################################################################################################

warnings.filterwarnings('ignore', category=FutureWarning)  # suppress warnings (specifically from pandas)
generated_image_paths = set()


def find_excel_and_pdf(directory):
    excel_file = None
    pdf_file = None

    for file in os.listdir(directory):
        if file.endswith('.xlsx') or file.endswith('.xls'):
            if excel_file is not None:
                raise Exception("Multiple Excel files found.")
            excel_file = os.path.join(directory, file)

        elif file.endswith('.pdf'):
            if pdf_file is not None:
                raise Exception("Multiple PDF files found.")
            pdf_file = os.path.join(directory, file)

    if excel_file is None or pdf_file is None:
        raise Exception("Either Excel or PDF file is missing.")

    return excel_file, pdf_file


def process_pdf_page(pdf_path, page_num, output_directory):
    # Construct the PNG filename
    pdf_basename = os.path.splitext(os.path.basename(pdf_path))[0]
    png_filename = f"{pdf_basename}_{page_num}.png"
    png_filepath = os.path.join(output_directory, png_filename)

    # Check if PNG already exists
    if not os.path.exists(png_filepath):
        # Open the PDF and extract the page
        doc = fitz.open(pdf_path)
        page = doc.load_page(page_num - 1)  # Adjust for 0-based indexing
        pix = page.get_pixmap()
        pix.save(png_filepath)
        doc.close()

    return png_filepath


if __name__ == "__main__":
    excel_path, pdf_path = find_excel_and_pdf(input_directory)

    # Step 1: Read the Excel file
    df = pd.read_excel(excel_path, header=None)

    # Step 2: Remove 1st row titles (if present) and merge the first two columns
    if isinstance(df.iloc[0, 2], str):
        df = df.drop(df.index[0]).reset_index(drop=True)
    df[0] = df[0] + " <br><br> {{c1::" + df[1].astype(str) + "}} <br>"

    # Step 3: Update third column and process PDF pages
    for index, row in df.iterrows():
        page_num = row[2]
        try:
            png_path = process_pdf_page(pdf_path, int(page_num), input_directory)
            generated_image_paths.add(png_path)
            df.at[index, 2] = f"<img src=\"{os.path.basename(png_path)}\" />"
        except ValueError as e:
            df.at[index, 2] = "  "  # needs empty space or else won't be registered

    # Step 4: Keep only the first and updated third columns
    final_df = df[[0, 2]]

    cloze_model = genanki.Model(
        model_id=random.randrange(1 << 30, 1 << 31),
        name='Cloze Model with Image',
        fields=[
            {'name': 'Text'},  # the cloze text field
            {'name': 'Extra'},  # additional field for extra info or media
        ],
        templates=[
            {
                'name': 'Cloze Card',
                'qfmt': '{{cloze:Text}}',  # front of card
                'afmt': '{{cloze:Text}}<hr id="answer">{{Extra}}',  # back of card
            },
        ],
        css="""
        .card {
         font-family: arial;
         font-size: 20px;
         text-align: center;
         color: black;
         background-color: white;
        }
        .cloze {
            font-weight: bold;
            color: blue;
        }
        """
    )

    # Create a new genanki Deck
    pdf_basename = os.path.splitext(os.path.basename(pdf_path))[0]
    my_deck = genanki.Deck(
        random.randrange(1 << 30, 1 << 31),
        f"{pdf_basename} Deck"
    )

    # Add notes to the Deck
    for index, row in final_df.iterrows():
        my_note = genanki.Note(
            model=cloze_model,
            fields=[row[0], row[2]]  # row[0] is the front text, row[2] (1 is gone) is the back image
        )
        my_deck.add_note(my_note)

    # Create a genanki Package
    my_package = genanki.Package(my_deck)
    my_package.media_files = generated_image_paths  # List all image files

    # Save the package to an .apkg file
    output_apkg_path = os.path.join(output_directory, f"{pdf_basename}_deck.apkg")
    my_package.write_to_file(output_apkg_path)

    # Delete the generated PNG images
    for image_path in generated_image_paths:
        os.remove(image_path)
