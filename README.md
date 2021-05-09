# Reduce pdf file

reducePDF.py deletes redundant slides from a slide deck. Often, in decks exported to PDF, multiple pages are dedicated to the same slide, because sentences pop up one after another. This program deletes the uncomplete pages.


## Limitations

This code was written for 'cumulative' animations. It only works when the changes between frames are additions.

The code doesn't work when
- information is removed between two frames of the same slide (the last slide with less information will be kept)
- different parts of text are added on backgrounds of different colors at the same time (in this case too many slides will be kept)

## Usage
### Dependencies

To use the code, you need the following libraries
- numpy
- PyPDF2
- pdf2image
- tqdm

### Run

```
./reducePDF.py "filepath of the initial slide deck" "filepath where you want to save the reduced slide deck"
```
The last argument is optional. If you don't give an output filepath, the new slides will be saved in {filepath}_reduced.pdf.