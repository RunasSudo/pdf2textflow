# pdf2textflow

Extract text from PDF, automatically reflowing text.

## Example usage

    pdftohtml -f 17 -l 467 -i -xml -zoom 1 the_pdf_file.pdf

This will process pages 17 to 467 to an XML file for input to pdf2textflow.

    ./pdf2textflow.py the_pdf_file.xml 15 135 560 555 420 > the_pdf_file.txt

This will process a box 560 pt wide by 555 pt tall, offset by 15 pt along the x-axis and 135 pt along the y-axis. Text that extends past 420 pt along the x-axis will be automatically reflowed.

The coordinate system used is that of Inkscape – the origin (0, 0) is the ***bottom*** left of the page.
