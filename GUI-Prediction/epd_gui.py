# -*- coding: utf-8 -*-
"""
Created on Sat Apr 13 11:32:41 2024

@author: drewm
"""

import customtkinter as ctk
import epd_prediction as epd
import pandas as pd
from CTkListbox import CTkListbox

# We can scan this state matches list to find the column name
#   that matches our desired state
stateMatches = [
    ("state_AL", "Alabama"),              ("state_AR", "Arkansas"),
    ("state_AZ", "Arizona"),              ("state_CA", "California"),
    ("state_CO", "Colorado"),             ("state_CT", "Connecticut"),
    ("state_DC", "District of Columbia"), ("state_DE", "Delaware"),
    ("state_FL", "Florida"),              ("state_GA", "Georgia"),
    ("state_IA", "Iowa"),                 ("state_ID", "Idaho"),
    ("state_IL", "Illinois"),             ("state_IN", "Indiana"),
    ("state_KS", "Kansas"),               ("state_KY", "Kentucky"),
    ("state_LA", "Louisiana"),            ("state_MA", "Massachusetts"),
    ("state_MD", "Maryland"),             ("state_ME", "Maine"),
    ("state_MN", "Minnesota"),            ("state_MO", "Missouri"),
    ("state_MS", "Mississippi"),          ("state_MT", "Montana"),
    ("state_NC", "North Carolina"),       ("state_ND", "North Dakota"),
    ("state_NE", "Nebraska"),             ("state_NH", "New Hampshire"),
    ("state_NJ", "New Jersey"),           ("state_NM", "New Mexico"),
    ("state_NV", "Nevada"),               ("state_NY", "New York"),
    ("state_OH", "Ohio"),                 ("state_OK", "Oklahoma"),
    ("state_OR", "Oregon"),               ("state_PA", "Pennsylvania"),
    ("state_SC", "South Carolina"),       ("state_TN", "Tennessee"),
    ("state_TX", "Texas"),                ("state_UT", "Utah"),
    ("state_VA", "Virginia"),             ("state_WA", "Washington"),
    ("state_WI", "Wisconsin"),            ("state_WY", "Wyoming")
]

# State list used for populating listbox options
stateList = [
    "Alabama", "Arkansas", "Arizona", "California", "Colorado", "Connecticut",
    "District of Columbia", "Delaware", "Florida", "Georgia", "Iowa", "Idaho",
    "Illinois", "Indiana", "Kansas", "Kentucky", "Louisiana", "Massachusetts",
    "Maryland", "Maine", "Minnesota", "Missouri", "Mississippi", "Montana",
    "North Carolina", "North Dakota", "Nebraska", "New Hampshire",
    "New Jersey", "New Mexico", "Nevada", "New York", "Ohio", "Oklahoma",
    "Oregon", "Pennsylvania", "South Carolina", "Tennessee", "Texas", "Utah",
    "Virginia", "Washington", "Wisconsin", "Wyoming"
]

# Performance grade list used for populating listbox options
pgList = [
    "PG_PG 52-22 ", "PG_PG 52-28 ", "PG_PG 52-34 ", "PG_PG 58-16 ",
    "PG_PG 58-22 ", "PG_PG 58-28 ", "PG_PG 58-34 ", "PG_PG 58H-34 ",
    "PG_PG 58S-28 ", "PG_PG 58V-34 ", "PG_PG 64-10 ", "PG_PG 64-16 ",
    "PG_PG 64-22 ", "PG_PG 64-28 ", "PG_PG 64-34 ", "PG_PG 64E-28 ",
    "PG_PG 64H-22 ", "PG_PG 64S-22 ", "PG_PG 67-22 ", "PG_PG 70-10 ",
    "PG_PG 70-22 ", "PG_PG 70-22 M.", "PG_PG 70-28 ", "PG_PG 76-22 ",
    "PG_PG 76-28 ", "PG_PG 76-34 ", "PG_PG 82-22 "
]

gradList = [
    "gradation_dense", "gradation_gap", "gradation_open",
    "gradation_other", "gradation_permeable", "gradation_porous"
]

mdList = [
    "mix_design_hveem", "mix_design_marshall", "mix_design_other",
    "mix_design_performance", "mix_design_superpave"
]

binderList = [
    "binder type_GTR", "binder type_PPA", "binder type_SBS",
    "binder type_Unmodified"
]

# This absolute mess prepares column names for the dataframe.
#   The same could be done by loading from a file,
#       but this direct assignment should be quicker.
colNames = ["NMAS", "RAP_content", "RAS_content", "Binder_content", "lime",
            "Agg_content", "state_AL", "state_AR", "state_AZ", "state_CA",
            "state_CO", "state_CT", "state_DC", "state_DE", "state_FL",
            "state_GA", "state_IA", "state_ID", "state_IL", "state_IN",
            "state_KS", "state_KY", "state_LA", "state_MA", "state_MD",
            "state_ME", "state_MN", "state_MO", "state_MS", "state_MT",
            "state_NC", "state_ND", "state_NE", "state_NH", "state_NJ",
            "state_NM", "state_NV", "state_NY", "state_OH", "state_OK",
            "state_OR", "state_PA", "state_SC", "state_TN", "state_TX",
            "state_UT", "state_VA", "state_WA", "state_WI", "state_WY",
            "gradation_dense", "gradation_gap", "gradation_open",
            "gradation_other", "gradation_permeable", "gradation_porous",
            "mix_design_hveem", "mix_design_marshall", "mix_design_other",
            "mix_design_performance", "mix_design_superpave", "PG_PG 52-22 ",
            "PG_PG 52-28 ", "PG_PG 52-34 ", "PG_PG 58-16 ", "PG_PG 58-22 ",
            "PG_PG 58-28 ", "PG_PG 58-34 ", "PG_PG 58H-34 ", "PG_PG 58S-28 ",
            "PG_PG 58V-34 ", "PG_PG 64-10 ", "PG_PG 64-16 ", "PG_PG 64-22 ",
            "PG_PG 64-28 ", "PG_PG 64-34 ", "PG_PG 64E-28 ", "PG_PG 64H-22 ",
            "PG_PG 64S-22 ", "PG_PG 67-22 ", "PG_PG 70-10 ", "PG_PG 70-22 ",
            "PG_PG 70-22 M", "PG_PG 70-28 ", "PG_PG 76-22 ", "PG_PG 76-28 ",
            "PG_PG 76-34 ", "PG_PG 82-22 ", "Mix_type_HMA", "Mix_type_WMA",
            "binder type_GTR", "binder type_PPA", "binder type_SBS",
            "binder type_Unmodified"]

selectedState = None

data = pd.DataFrame(data=None, columns=colNames)

data.at[0, "NMAS"] = 0
data.at[0, "RAP_content"] = 0
data.at[0, "RAS_content"] = 0
data.at[0, "Binder_content"] = 0
data.at[0, "lime"] = 0
data.at[0, "Agg_content"] = 100


def findStateMatch(stateName):
    for code, name in stateMatches:
        if name == stateName:
            return code
        

class mainApp(ctk.CTkFrame):
    def __init__(self, parent, *args, **kwargs):
        ctk.CTkFrame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        
        self.leftFrame = ctk.CTkFrame(self, height=720, width=420)
        self.leftFrame.pack(side="left", padx=5, expand=True)
        
        self.middleFrame = ctk.CTkFrame(self, height=720, width=420)
        self.middleFrame.pack(side="left", padx=5, expand=True)
        
        self.rightFrame = ctk.CTkFrame(self, height=720, width=420)
        self.rightFrame.pack(side="left", padx=5, expand=True)
        
        # CATEGORICAL DATA INPUT (left frame)
        # State selection
        self.leftFrame.stateChosen = ctk.CTkLabel(
            self.leftFrame,
            width=200,
            text="Selected State: -----")
        self.leftFrame.stateChosen.grid(row=0, column=0)
        
        self.leftFrame.stateChoice = CTkListbox(
            self.leftFrame,
            width=200,
            height=200,
            command=self.submitState)
        self.leftFrame.stateChoice.grid(row=1, column=0)
        
        # PG selection
        self.leftFrame.pgChosen = ctk.CTkLabel(
            self.leftFrame,
            text="Performance Grade: -----")
        self.leftFrame.pgChosen.grid(row=0, column=2)
        
        self.leftFrame.pgChoice = CTkListbox(
            self.leftFrame,
            height=200,
            command=self.submitPG)
        self.leftFrame.pgChoice.grid(row=1, column=2)
        
        # Gradation selection
        self.leftFrame.gradChosen = ctk.CTkLabel(
            self.leftFrame,
            text="Gradation Type: -----")
        self.leftFrame.gradChosen.grid(row=2, column=0, sticky="NW")
        
        self.leftFrame.gradChoice = CTkListbox(
            self.leftFrame,
            command=self.submitGrad)
        self.leftFrame.gradChoice.grid(row=3, column=0, sticky="NW")
        
        # Mix design method
        self.leftFrame.mdChosen = ctk.CTkLabel(
            self.leftFrame,
            text="Mix Design Method: -----")
        self.leftFrame.mdChosen.grid(row=2, column=2, sticky="NW")
        
        self.leftFrame.mdChoice = CTkListbox(
            self.leftFrame,
            command=self.submitMD)
        self.leftFrame.mdChoice.grid(row=3, column=2, sticky="NW")
        
        # Binder type
        self.leftFrame.binderChosen = ctk.CTkLabel(
            self.leftFrame,
            text="Binder Type: -----")
        self.leftFrame.binderChosen.grid(row=4, column=0, sticky="NW")
        
        self.leftFrame.binderChoice = CTkListbox(
            self.leftFrame,
            command=self.submitBinder)
        self.leftFrame.binderChoice.grid(row=5, column=0, sticky="NW")
        
        # Mix type
        self.leftFrame.mixChosen = ctk.CTkLabel(
            self.leftFrame,
            text="Mix Type: -----")
        self.leftFrame.mixChosen.grid(row=4, column=2, sticky="NW")
        
        self.leftFrame.mixChoice = CTkListbox(
            self.leftFrame,
            command=self.submitMix)
        self.leftFrame.mixChoice.grid(row=5, column=2, sticky="NW")
        
        # Loading listbox values
        self.leftFrame.mixChoice.insert(0, "HMA")
        self.leftFrame.mixChoice.insert(1, "WMA")
        
        self.leftFrame.binderChoice.insert(0, "GTR")
        self.leftFrame.binderChoice.insert(1, "PPA")
        self.leftFrame.binderChoice.insert(2, "SBS")
        self.leftFrame.binderChoice.insert(3, "Unmodified")
        
        self.leftFrame.mdChoice.insert(0, "Hveem")
        self.leftFrame.mdChoice.insert(1, "Marshall")
        self.leftFrame.mdChoice.insert(2, "Performance")
        self.leftFrame.mdChoice.insert(3, "Superpave")
        self.leftFrame.mdChoice.insert(5, "Other")
        
        self.leftFrame.gradChoice.insert(0, "Dense")
        self.leftFrame.gradChoice.insert(1, "Gap")
        self.leftFrame.gradChoice.insert(2, "Open")
        self.leftFrame.gradChoice.insert(3, "Permeable")
        self.leftFrame.gradChoice.insert(4, "Porous")
        self.leftFrame.gradChoice.insert(5, "Other")
        
        i = 0
        for itr in stateList:
            self.leftFrame.stateChoice.insert(i, itr)
            i = i + 1
        
        i = 0
        for itr in pgList:
            self.leftFrame.pgChoice.insert(i, itr[3:])
            i = i + 1
        
        # NUMERIC DATA INPUT (middle frame)
        # NMAS
        self.middleFrame.nmasEntry = ctk.CTkEntry(
            self.middleFrame,
            placeholder_text="Enter NMAS (inches)...")
        self.middleFrame.nmasEntry.grid(row=0, column=0, sticky="NW")
        
        self.middleFrame.nmasLabel = ctk.CTkLabel(
            self.middleFrame,
            text="NMAS: " + str(data.at[0, "NMAS"]))
        self.middleFrame.nmasLabel.grid(row=0, column=1, sticky="NW")
        
        # RAP Content
        self.middleFrame.rapEntry = ctk.CTkEntry(
            self.middleFrame,
            placeholder_text="Enter RAP (%)...")
        self.middleFrame.rapEntry.grid(row=1, column=0, sticky="NW")
        
        self.middleFrame.rapLabel = ctk.CTkLabel(
            self.middleFrame,
            text="RAP %: " + str(data.at[0, "RAP_content"]))
        self.middleFrame.rapLabel.grid(row=1, column=1, sticky="NW")
        
        # RAS Content
        self.middleFrame.rasEntry = ctk.CTkEntry(
            self.middleFrame,
            placeholder_text="Enter RAS (%)...")
        self.middleFrame.rasEntry.grid(row=2, column=0, sticky="NW")
        
        self.middleFrame.rasLabel = ctk.CTkLabel(
            self.middleFrame,
            text="RAS %: " + str(data.at[0, "RAS_content"]))
        self.middleFrame.rasLabel.grid(row=2, column=1, sticky="NW")
        
        # Binder Content
        self.middleFrame.binderEntry = ctk.CTkEntry(
            self.middleFrame,
            placeholder_text="Enter Binder (%)...")
        self.middleFrame.binderEntry.grid(row=3, column=0, sticky="NW")
        
        self.middleFrame.binderLabel = ctk.CTkLabel(
            self.middleFrame,
            text="Binder %: " + str(data.at[0, "Binder_content"]))
        self.middleFrame.binderLabel.grid(row=3, column=1, sticky="NW")
        
        # Lime Content
        self.middleFrame.limeEntry = ctk.CTkEntry(
            self.middleFrame,
            placeholder_text="Enter Lime (%)...")
        self.middleFrame.limeEntry.grid(row=4, column=0, sticky="NW")
        
        self.middleFrame.limeLabel = ctk.CTkLabel(
            self.middleFrame,
            text="Lime %: " + str(data.at[0, "lime"]))
        self.middleFrame.limeLabel.grid(row=4, column=1, sticky="NW")
        
        # Aggregate Content
        self.middleFrame.aggLabel = ctk.CTkLabel(
            self.middleFrame,
            text="Aggregate %: " + str(data.at[0, "Agg_content"]))
        self.middleFrame.aggLabel.grid(row=5, column=1, stick="NW")
        
        # SUMMARY AND RESULTS (right frame)
        self.rightFrame.runButton = ctk.CTkButton(
            self.rightFrame,
            text="Predict",
            command=self.runPred)
        self.rightFrame.runButton.grid(row=0, column=0)
        
    def runPred(self):
        i = 0
        for i in range(0, 93):
            if data.at[0, colNames[i]] == "NaN":
                print("Handle lacking data")
            else:
                epd.runPrediction(data)
        
    def submitMix(self, selectedMix):
        self.leftFrame.mixChosen.configure(
            text="Mix Type: " + selectedMix)

        actualMix = "Mix_type_" + selectedMix
        
        if actualMix == "Mix_type_HMA":
            data.at[0, "Mix_type_HMA"] = 1
            data.at[0, "Mix_type_WMA"] = 0
        else:
            data.at[0, "Mix_type_WMA"] = 1
            data.at[0, "Mix_type_HMA"] = 0
        
    def submitBinder(self, selectedBinder):
        self.leftFrame.binderChosen.configure(
            text="Binder Type: " + selectedBinder)
        
        actualBinder = "binder type_" + selectedBinder
        
        for itr in binderList:
            if itr == actualBinder:
                data.at[0, itr] = 1
            else:
                data.at[0, itr] = 0
        
    def submitMD(self, selectedMD):
        self.leftFrame.mdChosen.configure(
            text="Mix Design Method: " + selectedMD)
        
        actualMD = "mix_design_" + selectedMD.lower()
        
        for itr in mdList:
            if itr == actualMD:
                data.at[0, itr] = 1
            else:
                data.at[0, itr] = 0
        
    def submitGrad(self, selectedGrad):
        self.leftFrame.gradChosen.configure(
            text="Gradation Type: " + selectedGrad)
        
        actualGrad = "gradation_" + selectedGrad.lower()
        
        for itr in gradList:
            if itr == actualGrad:
                data.at[0, itr] = 1
            else:
                data.at[0, itr] = 0
    
    def submitPG(self, selectedPG):
        self.leftFrame.pgChosen.configure(
            text="Performance Grade: " + selectedPG)
        
        actualPG = "PG_" + selectedPG
        
        for itr in pgList:
            if itr == actualPG:
                data.at[0, itr] = 1
            else:
                data.at[0, itr] = 0
    
    def submitState(self, selectedState):
        self.leftFrame.stateChosen.configure(
            text="Selected State: " + selectedState)
        
        matchedName = findStateMatch(selectedState)
        
        for itr in colNames:
            if itr[:6] == "state_":
                if itr == matchedName:
                    data.at[0, itr] = 1
                else:
                    data.at[0, itr] = 0
    
    def clearEntries(self, event):
        newVal = self.middleFrame.nmasEntry.get()
        if newVal != "":
            try:
                data.at[0, "NMAS"] = abs(float(newVal))
                self.middleFrame.nmasEntry.delete(0, 'end')
            except ValueError:
                print("Do something: nmas")
        
        newVal = self.middleFrame.rapEntry.get()
        if newVal != "":
            try:
                newVal = abs(int(newVal))
                agg_content = data.at[0, "Agg_content"]
                
                # If the new value is smaller than the old value, we add
                #   the difference to agg_content instead of subtracting
                if newVal < data.at[0, "RAP_content"]:
                    data.at[0, "Agg_content"] = agg_content \
                        + data.at[0, "RAP_content"]         \
                        - newVal
                    data.at[0, "RAP_content"] = newVal
                    self.middleFrame.rapEntry.delete(0, 'end')
                elif (agg_content + data.at[0, "RAP_content"] - newVal) >= 0:
                    data.at[0, "Agg_content"] = agg_content \
                        + data.at[0, "RAP_content"]           \
                        - newVal
                    data.at[0, "RAP_content"] = newVal
                    self.middleFrame.rapEntry.delete(0, 'end')
            except ValueError:
                print("Do something: rap")
        
        newVal = self.middleFrame.rasEntry.get()
        if newVal != "":
            try:
                newVal = abs(int(newVal))
                agg_content = data.at[0, "Agg_content"]
                
                if newVal < data.at[0, "RAS_content"]:
                    data.at[0, "Agg_content"] = agg_content \
                        + data.at[0, "RAS_content"]         \
                        - newVal
                    data.at[0, "RAS_content"] = newVal
                    self.middleFrame.rasEntry.delete(0, 'end')
                elif (agg_content + data.at[0, "RAS_content"] - newVal) >= 0:
                    data.at[0, "Agg_content"] = agg_content \
                        + data.at[0, "RAS_content"]         \
                        - newVal
                    data.at[0, "RAS_content"] = newVal
                    self.middleFrame.rasEntry.delete(0, 'end')
            except ValueError:
                print("Do something: ras")
        
        newVal = self.middleFrame.binderEntry.get()
        if newVal != "":
            try:
                newVal = abs(int(newVal))
                agg_content = data.at[0, "Agg_content"]
                
                if newVal < data.at[0, "Binder_content"]:
                    data.at[0, "Agg_content"] = agg_content \
                        + data.at[0, "Binder_content"]      \
                        - newVal
                    data.at[0, "Binder_content"] = newVal
                    self.middleFrame.binderEntry.delete(0, 'end')
                elif (agg_content + data.at[0, "Binder_content"] - newVal) \
                        >= 0:
                    data.at[0, "Agg_content"] = agg_content \
                        + data.at[0, "Binder_content"]      \
                        - newVal
                    data.at[0, "Binder_content"] = newVal
                    self.middleFrame.binderEntry.delete(0, 'end')
            except ValueError:
                print("Do something: binder")
        
        newVal = self.middleFrame.limeEntry.get()
        if newVal != "":
            try:
                newVal = abs(int(newVal))
                agg_content = data.at[0, "Agg_content"]
                
                if newVal < data.at[0, "lime"]:
                    data.at[0, "Agg_content"] = agg_content \
                        + data.at[0, "lime"]      \
                        - newVal
                    data.at[0, "lime"] = newVal
                    self.middleFrame.limeEntry.delete(0, 'end')
                elif (agg_content + data.at[0, "lime"] - newVal) >= 0:
                    data.at[0, "Agg_content"] = agg_content \
                        + data.at[0, "lime"]                \
                        - newVal
                    data.at[0, "lime"] = newVal
                    self.middleFrame.limeEntry.delete(0, 'end')
            except ValueError:
                print("Do something: lime")

        self.middleFrame.nmasLabel.configure(
            text="NMAS: " + str(data.at[0, "NMAS"]))
        self.middleFrame.rapLabel.configure(
            text="RAP %: " + str(data.at[0, "RAP_content"]))
        self.middleFrame.rasLabel.configure(
            text="RAS %: " + str(data.at[0, "RAS_content"]))
        self.middleFrame.binderLabel.configure(
            text="Binder %: " + str(data.at[0, "Binder_content"]))
        self.middleFrame.limeLabel.configure(
            text="Lime %: " + str(data.at[0, "lime"]))
        self.middleFrame.aggLabel.configure(
            text="Aggregate %: " + str(data.at[0, "Agg_content"]))
    
    def _quit(self):
        root.quit()
        root.destroy()
        

def main():
    root.mainloop()


if __name__ == "__main__":
    root = ctk.CTk()
    root.geometry("1280x720")
    
    app = mainApp(root)
    app.pack(side="top", fill="both", expand=True)
    root.bind('<Return>', app.clearEntries)
    
    root.protocol("WM_DELETE_WINDOW", app._quit)
    main()
