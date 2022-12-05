import numpy as np

class Page:
    def __init__(self, file_text):
        self.text = file_text.split("\n")
        self.df = np.array([])

    # Check if the page is front
    def check_front_page(self):
        pass

    def convert_metadata_to_array(self):
        # Journal name
        np.append(self.df, self.text[0].replace("© ", ""))
        del self.text[0]

        # Publication time (year, volume, number, index)
        publication_info = self.text[0].split(" ")
        del self.text[0]
        np.append(self.df, publication_info[0])
        np.append(self.df, publication_info[1])
        np.append(self.df, publication_info[2])
        np.append(self.df, publication_info[3])

        # DOI
        np.append(self.df, self.text[0])
        del self.text[0]

        # Clean up text
        while self.text[0] == " " or self.text[0] == "Cite Article":
            del self.text[0]

        # Title
        title = ""

