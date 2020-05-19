# Cloud-Based-Heat-Map-for-Area-Segmentation-Covid_19
This repo will be a collaborative platform for work on Analysing and Predicting the Spread of Covid 19 using mappings, segmentation and number of reported cases.

# 1. pdf downloader and reader


We need to work with txt file format because the scanned pdf is not directly editable.

## Installation

The requirements are to be downloaded with [pip](https://pip.pypa.io/en/stable/) to be able to continue with project

```bash
pip install -r requirements.txt
```
or 

```bash
pip install beautifulsoup4==4.9.0
pip install pdf2image==1.13.1
pip install pytesseract==0.3.4
pip install Pillow==7.1.2
pip install requests==2.23.0
```

## Usage

1. Download [pytesseract](https://sourceforge.net/projects/tesseract-ocr/) and add {path installation} to PATH
2. Also add TESSDATA_PREFIX={path installation}/tessdata to PATH
3. Download [poppler](http://blog.alivate.com.au/poppler-windows/) extract it to {any file location} and add it to PATH



## The Dash App
The Dash app displays the graphs, where Kenya is Compared against other Countries in terms of Covid 19 Cases that have been reported since each Country reported the first case.
