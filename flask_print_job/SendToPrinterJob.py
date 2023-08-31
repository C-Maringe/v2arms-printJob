import os
from time import sleep
import subprocess


def command_print(event=None):
    command = "{} {}".format('PDFtoPrinter.exe', 'receipt.pdf')
    subprocess.call(command, shell=True)
    print("Pdf Printed")


def PrintTrigger():
    test = os.listdir('./')
    if test == []:
        print("No files found in the directory.")
    else:
        for item in test:
            if item.endswith(".pdf"):
                command_print()
                # sleep(2)
                os.remove(os.path.join('./', item))
                print("pdf removed")
