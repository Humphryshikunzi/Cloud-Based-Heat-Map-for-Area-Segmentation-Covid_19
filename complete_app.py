import requests
from bs4 import BeautifulSoup
from PIL import Image
import pytesseract
from pdf2image import convert_from_path

host_url = "https://www.health.go.ke/press-releases/"


def get_pdf_links():
    print("Requesting to download pdf files...")
    try: 
        # create response object called r
        r = requests.get(host_url)

        # create beautiful soup object
        soup = BeautifulSoup(r.content, 'html5lib')

        # find all links on web page
        links = soup.find_all('a')

        # filter links ending with '.pdf'
        pdf_links = [link['href'] for link in links if link['href'].endswith('pdf')]

        return pdf_links
    except requests.exceptions.ConnectionError as e:
        print(e)
        raise SystemExit("Could not download files, Please Check your connection")

def download_pdf_files(links):

    pdf_file_names = []

    for link in links:
        # obtain file name by splitting url and getting
        # last string
        file_name = link.split('/')[-1]
        print(f"Downloading file {file_name}")

        try:
            # create response object
            r = requests.get(link, stream=True)
        except requests.exceptions.InvalidURL as e:
            raise SystemExit(e)

        # download started
        with open(file_name, 'wb') as pdf:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    pdf.write(chunk)
        print(f"{file_name} downloaded")

        pdf_file_names.append(file_name)

    print("All files downloaded")
    return pdf_file_names


def pdf_to_txt(pdf_files):

    # Loop over every pdf
    for pdf_file in pdf_files:

        # Get all the pages of the pdf file
        pages = convert_from_path(pdf_file)

        image_counter = 1

        for page in pages:
            # Generate a file name
            filename = "page_" + str(image_counter) + ".jpg"
            # Save each page as a jpeg file
            page.save(filename, "JPEG")
            image_counter += 1

        # Generate output file with txt extension
        separator = '.'
        temp_name = pdf_file.split(separator)
        temp_name[-1] = "txt"
        outfile = separator.join(temp_name)

        # Open file for appending
        f = open(file=outfile, mode="a", encoding='utf-8')

        # Loop over ever generated image to extract text
        for i in range(1, image_counter):
            filename = "page_" + str(i) + ".jpg"
            text = str(pytesseract.image_to_string(Image.open(filename)))

            # Replace newline with nothing
            text = text.replace("-\n", "")
            # Append the extracted text to the text file
            f.write(text)

        f.close()
    return


def main():
    # Download pdf from retrieved pdf links
    pdfs = download_pdf_files(get_pdf_links())

    # convert all pdf's to txt
    pdf_to_txt(pdfs)


if __name__ == "__main__":
    main()
