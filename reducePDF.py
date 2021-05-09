import sys

import numpy as np
from PyPDF2 import PdfFileReader, PdfFileWriter
from pdf2image import convert_from_path
from tqdm import tqdm


def substract_PIL_images(image1, image2):
    array1 = np.asarray(image1, dtype='int32')
    array2 = np.asarray(image2, dtype='int32')

    return array1 - array2


def compare_images(image1, image2):
    diff = substract_PIL_images(image1, image2)

    neg_vals = np.count_nonzero(diff < 0)
    pos_vals = np.count_nonzero(diff > 0)

    return pos_vals, neg_vals


def discard_slide(image1, image2):
    pos_vals, neg_vals = compare_images(image1, image2)
    return neg_vals == 0 or pos_vals == 0


def deduplicate_pdf(input_file_path, output_file_path=""):
    if output_file_path == "":
        base, _, file = input_file_path.rpartition('/')
        name, _, extensions = file.partition('.')
        output_file_path = f'{base}/{name}_reduced.{extensions}'

    with open(input_file_path, 'rb') as f:
        pdf_reader = PdfFileReader(f)  # original slides
        pdf_writer = PdfFileWriter()

        num_slides = pdf_reader.getNumPages()

        images = convert_from_path(input_file_path, dpi=50, grayscale=True)  # slides as images
        for i in tqdm(range(len(images) - 1)):
            if not discard_slide(images[i], images[i + 1]):
                pdf_writer.addPage(pdf_reader.getPage(i))
        pdf_writer.addPage(pdf_reader.getPage(num_slides - 1))  # add last page

        with open(output_file_path, 'wb') as out:
            pdf_writer.write(out)

        print(f"Slide deck of {num_slides} slides reduced to {pdf_writer.getNumPages()} slides")


if __name__ == '__main__':
    deduplicate_pdf(*sys.argv[1:])
