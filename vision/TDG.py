from vision import Obr
import os
import pandas as pd

name = f"J4.mp4"
mname = "csrt"  # bloob , csrt , kfc
from tkinter import Tk
from tkinter.filedialog import askopenfilename

Tk().withdraw() # werdon't want a full GUI, so keep the root window from appearing
filename = askopenfilename()
name = filename.split("/")[-1]
if __name__ == "__main__":
    for mname in ["csrt"]:

        x, y, t = Obr(name, 1, mname, 1)
        df = pd.DataFrame({"mes": x, "y": y, "t": t})

        dir = os.path.join("Output", "Data", f'{name[:-4]}')
        if not os.path.exists(dir):
            os.mkdir(dir)
        fname = os.path.join("Output", "Data", f'{name[:-4]}', f'{name[:-4]}.xlsx')
        try:
            with pd.ExcelWriter(fname, mode='a', if_sheet_exists='replace', engine="openpyxl") as writer:
                df.to_excel(writer, sheet_name=mname)
        except:
            with pd.ExcelWriter(fname, mode='w', engine="openpyxl") as writer:
                df.to_excel(writer, sheet_name=mname)