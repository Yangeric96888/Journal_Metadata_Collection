import numpy as np
import pandas as pd

class Page:
    def __init__(self, file_text):
        self.text = []
        self.text = file_text.split("\n")   # Splits up the text into a list
        self.df = {"Journal": "", "Year": "", "Volume": "", "Number": "", "Index": "", "DOI": "", "Title": ""}
        self.convert_metadata_to_array()

    def convert_metadata_to_array(self):
        # Organizes the metadata by going through the page's text list one-by-one

        # Journal name
        self.df["Journal"] = self.text[0].replace("© ", "")
        del self.text[0]

        # Publication time (year, volume, number, index)
        publication_info = self.text[0].replace(",", "").replace(".", "").split(" ")
        self.df["Year"] = publication_info[0]   # Year
        self.df["Volume"] = publication_info[2] # Volume
        self.df["Number"] = publication_info[4]   # Number
        self.df["Index"] = publication_info[5]   # Index
        del self.text[0]

        # DOI
        self.df["DOI"] = self.text[0]
        del self.text[0]

        # Clean up text
        self.text = [current_value for current_value in self.text if current_value != ""]
        self.text = [current_value for current_value in self.text if current_value != " "]
        self.text = [current_value for current_value in self.text if current_value != "Cite Article"]
        self.text = [current_value for current_value in self.text if current_value != "and"]
        self.text = [current_value for current_value in self.text if current_value != "&"]

        # Title
        title = ""
        while self.text[1] != "INSEAD" and self.text[1].isupper():
            title += self.text[0] + " "
            del self.text[0]
        title = title[:-1].replace("  ", " ")   # Replaces any double spaces and the last hanging space
        self.df["Title"] = title

        # Author + Institution
        author_list = []
        institution_list = []
        char_limit = 60 # If a text is this long, then it is recognized as the abstract
        while len(self.text[1]) < char_limit:   # Avoid abstract by checking length of next string
            print(self.text)
            current_list = []
            if (not self.text[0].isupper() or self.text[0] == "INSEAD") and len(self.text[1]) < char_limit:
                while (not self.text[0].isupper() or self.text[0] == "INSEAD") and len(self.text[1]) < char_limit:
                    current_list.append(self.text[0])
                    del self.text[0]
                institution_list.append(current_list)
            elif (self.text[0].isupper() and self.text[0] != "INSEAD") and len(self.text[1]) < char_limit:
                while (self.text[0].isupper() and self.text[0] != "INSEAD") and len(self.text[1]) < char_limit:
                    current_list.append(self.text[0])
                    del self.text[0]
                author_list.append(current_list)


        if len(author_list) > len(institution_list):    # Adds the final university, which is not processed above
            institution_list.append([self.text[0]])
            del self.text[0]
        else:
            institution_list[-1].append(self.text[0])
            del self.text[0]

        for i in range(len(author_list)):   # Add author + institution to dictionary
            self.df["Author %s" % str(i + 1)] = author_list[i]
            self.df["University %s" % str(i + 1)] = institution_list[i]

    def write_to_csv(self, file_path):
        pd.DataFrame.from_dict(data=self.df, orient="index").to_csv(file_path, header=False, mode="a")
    #, mode="a"


