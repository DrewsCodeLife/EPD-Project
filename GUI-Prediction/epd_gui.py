# -*- coding: utf-8 -*-
"""
Created on Sat Apr 13 11:32:41 2024

@author: drewm
"""

import customtkinter as ctk
import epd_prediction as epd
import pandas as pd
import tooltipGen as ttg
import threading
import queue
from CTkListbox import CTkListbox

ctk.set_appearance_mode("dark")

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
    ("state_WI", "Wisconsin"),            ("state_WY", "Wyoming"),
    ("NA", "Not listed")
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
    "Virginia", "Washington", "Wisconsin", "Wyoming", "Not listed"
]

# Performance grade list used for populating listbox options
pgList = [
    "PG_PG 52-22 ", "PG_PG 52-28 ", "PG_PG 52-34 ", "PG_PG 58-16 ",
    "PG_PG 58-22 ", "PG_PG 58-28 ", "PG_PG 58-34 ", "PG_PG 58H-34 ",
    "PG_PG 58S-28 ", "PG_PG 58V-34 ", "PG_PG 64-10 ", "PG_PG 64-16 ",
    "PG_PG 64-22 ", "PG_PG 64-28 ", "PG_PG 64-34 ", "PG_PG 64E-28 ",
    "PG_PG 64H-22 ", "PG_PG 64S-22 ", "PG_PG 67-22 ", "PG_PG 70-10 ",
    "PG_PG 70-22 ", "PG_PG 70-22 M", "PG_PG 70-28 ", "PG_PG 76-22 ",
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

result_queue = queue.Queue()

gwpSum = None
gwpA1 = None
gwpA2 = None
gwpA3 = None


def findStateMatch(stateName):
    for code, name in stateMatches:
        if name == stateName:
            return code
        

class missingDataPopup(ctk.CTkToplevel):
    def __init__(self, missing, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("400x300")
        
        print("Missing: " + str(missing))
        
        missingStrings = ""
        
        while len(missing) > 0:
            missingStrings = missingStrings + ", " + str(missing.pop())
        
        missingStrings = missingStrings[2:]
        
        print("Missing Strings: " + missingStrings)
        
        self.missingLabel = ctk.CTkLabel(
            self,
            text="Missing values for: " + missingStrings,
            wraplength=300)
        self.missingLabel.place(relx=.5, rely=.5, anchor=ctk.CENTER)
        
        self.after(10, self.lift)


class mainApp(ctk.CTkFrame):
    def __init__(self, parent, *args, **kwargs):
        ctk.CTkFrame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
        self.leftFrame = ctk.CTkFrame(self, height=720, width=350)
        self.leftFrame.grid(row=0, column=0, sticky="nsew")
        
        self.rightFrame = ctk.CTkFrame(self, height=720, width=350)
        self.rightFrame.grid(row=0, column=1, sticky="nsew")
        self.rightFrame.grid_rowconfigure(0, weight=1)
        self.rightFrame.grid_rowconfigure(1, weight=1)
        self.rightFrame.grid_columnconfigure(0, weight=1)
        self.rightFrame.grid_columnconfigure(1, weight=1)
        
        self.rightFrame.topFrame = ctk.CTkFrame(self.rightFrame,
                                                width=300,
                                                height=210)
        self.rightFrame.topFrame.grid(row=0, column=0)
        self.rightFrame.topFrame.grid_propagate(False)
        
        self.rightFrame.bottomFrame = ctk.CTkFrame(self.rightFrame,
                                                   width=300,
                                                   height=220)
        self.rightFrame.bottomFrame.grid(row=1, column=0)
        self.rightFrame.bottomFrame.grid_propagate(False)
        
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
        
        self.leftFrame.binderChoice.insert(0, "Unmodified")
        self.leftFrame.binderChoice.insert(1, "GTR")
        self.leftFrame.binderChoice.insert(2, "PPA")
        self.leftFrame.binderChoice.insert(3, "SBS")
        
        self.leftFrame.mdChoice.insert(0, "Superpave")
        self.leftFrame.mdChoice.insert(1, "Marshall")
        self.leftFrame.mdChoice.insert(2, "Hveem")
        self.leftFrame.mdChoice.insert(3, "Performance")
        self.leftFrame.mdChoice.insert(4, "Other")
        
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
        self.rightFrame.topFrame.numInstruct = ctk.CTkLabel(
            self.rightFrame.topFrame,
            text="(Press Enter to Submit)",
            font=("Segoe UI", 12, "bold"))
        self.rightFrame.topFrame.numInstruct.grid(row=0,
                                                  column=0,
                                                  padx=5,
                                                  pady=2.5,
                                                  sticky="NW")
        
        # Aggregate Content
        self.rightFrame.topFrame.aggLabel = ctk.CTkLabel(
            self.rightFrame.topFrame,
            text="Aggregate %: " + str(data.at[0, "Agg_content"]))
        self.rightFrame.topFrame.aggLabel.grid(row=0,
                                               column=1,
                                               padx=5,
                                               pady=2.5,
                                               sticky="NW")
        
        # NMAS
        self.rightFrame.topFrame.nmasEntry = ctk.CTkEntry(
            self.rightFrame.topFrame,
            placeholder_text="Enter NMAS (inches)...")
        self.rightFrame.topFrame.nmasEntry.grid(row=1,
                                                column=0,
                                                padx=5,
                                                pady=2.5,
                                                sticky="NW")
        
        self.rightFrame.topFrame.nmasLabel = ctk.CTkLabel(
            self.rightFrame.topFrame,
            text="NMAS (in): " + str(data.at[0, "NMAS"]))
        self.rightFrame.topFrame.nmasLabel.grid(row=1,
                                                column=1,
                                                padx=5,
                                                pady=2.5,
                                                sticky="NW")
        
        # RAP Content
        self.rightFrame.topFrame.rapEntry = ctk.CTkEntry(
            self.rightFrame.topFrame,
            placeholder_text="Enter RAP (%)...")
        self.rightFrame.topFrame.rapEntry.grid(row=2,
                                               column=0,
                                               padx=5,
                                               pady=2.5,
                                               sticky="NW")
        
        self.rightFrame.topFrame.rapLabel = ctk.CTkLabel(
            self.rightFrame.topFrame,
            text="RAP       %: " + str(data.at[0, "RAP_content"]))
        self.rightFrame.topFrame.rapLabel.grid(row=2,
                                               column=1,
                                               padx=5,
                                               pady=2.5,
                                               sticky="NW")
        
        # RAS Content
        self.rightFrame.topFrame.rasEntry = ctk.CTkEntry(
            self.rightFrame.topFrame,
            placeholder_text="Enter RAS (%)...")
        self.rightFrame.topFrame.rasEntry.grid(row=3,
                                               column=0,
                                               padx=5,
                                               pady=2.5,
                                               sticky="NW")
        
        self.rightFrame.topFrame.rasLabel = ctk.CTkLabel(
            self.rightFrame.topFrame,
            text="RAS       %: " + str(data.at[0, "RAS_content"]))
        self.rightFrame.topFrame.rasLabel.grid(row=3,
                                               column=1,
                                               padx=5,
                                               pady=2.5,
                                               sticky="NW")
        
        # Binder Content
        self.rightFrame.topFrame.binderEntry = ctk.CTkEntry(
            self.rightFrame.topFrame,
            placeholder_text="Enter Binder (%)...")
        self.rightFrame.topFrame.binderEntry.grid(row=4,
                                                  column=0,
                                                  padx=5,
                                                  pady=2.5,
                                                  sticky="NW")
        
        self.rightFrame.topFrame.binderLabel = ctk.CTkLabel(
            self.rightFrame.topFrame,
            text="Binder    %: " + str(data.at[0, "Binder_content"]))
        self.rightFrame.topFrame.binderLabel.grid(row=4,
                                                  column=1,
                                                  padx=5,
                                                  pady=2.5,
                                                  sticky="NW")
        
        # Lime Content
        self.rightFrame.topFrame.limeEntry = ctk.CTkEntry(
            self.rightFrame.topFrame,
            placeholder_text="Enter Lime (%)...")
        self.rightFrame.topFrame.limeEntry.grid(row=5,
                                                column=0,
                                                padx=5,
                                                pady=2.5,
                                                sticky="NW")
        
        self.rightFrame.topFrame.limeLabel = ctk.CTkLabel(
            self.rightFrame.topFrame,
            text="Lime      %: " + str(data.at[0, "lime"]))
        self.rightFrame.topFrame.limeLabel.grid(row=5,
                                                column=1,
                                                padx=5,
                                                pady=2.5,
                                                sticky="NW")
        
        # SUMMARY AND RESULTS (right frame)
        self.rightFrame.bottomFrame.runButton = ctk.CTkButton(
            self.rightFrame.bottomFrame,
            text="Predict",
            command=self.runPred)
        self.rightFrame.bottomFrame.runButton.grid(row=0,
                                                   column=0,
                                                   padx=5,
                                                   pady=2.5,
                                                   sticky="NW")
        
        self.rightFrame.bottomFrame.gwpA1Label = ctk.CTkLabel(
            self.rightFrame.bottomFrame,
            text="Predicted GWP-100-A1: N/A")
        self.rightFrame.bottomFrame.gwpA1Label.grid(row=1,
                                                    column=0,
                                                    padx=5,
                                                    sticky="NW")
        
        self.rightFrame.bottomFrame.gwpA2Label = ctk.CTkLabel(
            self.rightFrame.bottomFrame,
            text="Predicted GWP-100-A2: N/A")
        self.rightFrame.bottomFrame.gwpA2Label.grid(row=2,
                                                    column=0,
                                                    padx=5,
                                                    sticky="NW")
        
        self.rightFrame.bottomFrame.gwpA3Label = ctk.CTkLabel(
            self.rightFrame.bottomFrame,
            text="Predicted GWP-100-A3: N/A")
        self.rightFrame.bottomFrame.gwpA3Label.grid(row=3,
                                                    column=0,
                                                    padx=5,
                                                    sticky="NW")
        
        self.rightFrame.bottomFrame.gwpCumul = ctk.CTkLabel(
            self.rightFrame.bottomFrame,
            text="Sum of A1, A2, and A3: N/A")
        self.rightFrame.bottomFrame.gwpCumul.grid(row=4,
                                                  column=0,
                                                  padx=5,
                                                  sticky="NW")
        
        self.rightFrame.bottomFrame.gwpTotalLabel = ctk.CTkLabel(
            self.rightFrame.bottomFrame,
            text="Predicted sum of A1, A2, and A3: N/A")
        self.rightFrame.bottomFrame.gwpTotalLabel.grid(row=5,
                                                       column=0,
                                                       padx=5,
                                                       sticky="NW")
        
        self.rightFrame.bottomFrame.diffTip1 = ttg.CreateToolTip(
            self.rightFrame.bottomFrame.gwpTotalLabel,
            "This value is predicted separately from the other values, and"
            " can be utilized to validate that the model is making accurate"
            " predictions. This value should match the cumulative sum above.")
        
        self.rightFrame.bottomFrame.diffTip2 = ttg.CreateToolTip(
            self.rightFrame.bottomFrame.gwpCumul,
            "This value is generated by building a cumulative sum of the "
            "predicted values for A1, A2, and A3. It should closely match"
            " the value immediately below it, which is a separately "
            "predicted total.")
        
        self.rightFrame.bottomFrame.unitLabel = ctk.CTkLabel(
            self.rightFrame.bottomFrame,
            text="All values are in kg of CO2 equivalence "
                "per ton of asphalt mix",
            wraplength=300,
            font=("Segoe UI", 12, "bold"))
        self.rightFrame.bottomFrame.unitLabel.grid(row=6,
                                                   column=0,
                                                   padx=5,
                                                   sticky="NW")
        
    def runPred(self):
        t = threading.Thread(
            target=epd.runPrediction, args=(data, result_queue), daemon=True)
        
        i = 0
        isMissing = False
        missingList = set()
        for i in range(0, 93):
            if str(data.at[0, colNames[i]]) == "nan":
                if colNames[i][:6] == "state_":
                    missingList.add("State")
                elif colNames[i][:5] == "PG_PG":
                    missingList.add("Performance Grade")
                elif colNames[i][:5] == "Mix_t":
                    missingList.add("Mix Type")
                elif colNames[i][:5] == "mix_d":
                    missingList.add("Mix Design")
                elif colNames[i][:10] == "gradation_":
                    missingList.add("Gradation Type")
                else:
                    missingList.add("Binder Type")
                isMissing = True
        if not isMissing:
            if not t.is_alive():
                t.start()
                self.awaitResults(thread=t)
        else:
            missingDataWindow = missingDataPopup(missingList)
            pass
    
    def awaitResults(self, thread=threading.Thread()):
        if not thread.is_alive():
            results = result_queue.get()
            gwpSum, gwpA1, gwpA2, gwpA3 = results
            
            self.rightFrame.bottomFrame.gwpA1Label.configure(
                text="Predicted GWP-100-A1: "
                + str("{:.2f}".format(float(gwpA1))))
            self.rightFrame.bottomFrame.gwpA2Label.configure(
                text="Predicted GWP-100-A2: "
                + str("{:.2f}".format(float(gwpA2))))
            self.rightFrame.bottomFrame.gwpA3Label.configure(
                text="Predicted GWP-100-A3: "
                + str("{:.2f}".format(float(gwpA3))))
            self.rightFrame.bottomFrame.gwpTotalLabel.configure(
                text="Predicted sum of A1, A2, and A3: "
                + str("{:.2f}".format(float(gwpSum))))
            self.rightFrame.bottomFrame.gwpCumul.configure(
                text="Sum of A1, A2, and A3: "
                + str("{:.2f}".format(float(gwpA1 + gwpA2 + gwpA3))))
        else:
            root.after(100, self.awaitResults)
        
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
        
        if matchedName != "NA":
            for itr in colNames:
                if itr[:6] == "state_":
                    if itr == matchedName:
                        data.at[0, itr] = 1
                    else:
                        data.at[0, itr] = 0
        else:
            # If matchedName == "NA", the state was not listed.
            #   Reference category is 0 for all state columns
            for itr in colNames:
                if itr[:6] == "state_":
                    data.at[0, itr] = 0
    
    def clearEntries(self, event):
        newVal = self.rightFrame.topFrame.nmasEntry.get()
        if newVal != "":
            try:
                data.at[0, "NMAS"] = abs(float(newVal))
                self.rightFrame.topFrame.nmasEntry.delete(0, 'end')
            except ValueError:
                print("Do something: nmas")
        
        newVal = self.rightFrame.topFrame.rapEntry.get()
        if newVal != "":
            try:
                newVal = abs(float(newVal))
                agg_content = data.at[0, "Agg_content"]
                
                # If the new value is smaller than the old value, we add
                #   the difference to agg_content instead of subtracting
                if newVal < data.at[0, "RAP_content"]:
                    data.at[0, "Agg_content"] = agg_content \
                        + data.at[0, "RAP_content"]         \
                        - newVal
                    data.at[0, "RAP_content"] = newVal
                    self.rightFrame.topFrame.rapEntry.delete(0, 'end')
                elif (agg_content + data.at[0, "RAP_content"] - newVal) >= 0:
                    data.at[0, "Agg_content"] = agg_content \
                        + data.at[0, "RAP_content"]           \
                        - newVal
                    data.at[0, "RAP_content"] = newVal
                    self.rightFrame.topFrame.rapEntry.delete(0, 'end')
            except ValueError:
                print("Do something: rap")
        
        newVal = self.rightFrame.topFrame.rasEntry.get()
        if newVal != "":
            try:
                newVal = abs(float(newVal))
                agg_content = data.at[0, "Agg_content"]
                
                if newVal < data.at[0, "RAS_content"]:
                    data.at[0, "Agg_content"] = agg_content \
                        + data.at[0, "RAS_content"]         \
                        - newVal
                    data.at[0, "RAS_content"] = newVal
                    self.rightFrame.topFrame.rasEntry.delete(0, 'end')
                elif (agg_content + data.at[0, "RAS_content"] - newVal) >= 0:
                    data.at[0, "Agg_content"] = agg_content \
                        + data.at[0, "RAS_content"]         \
                        - newVal
                    data.at[0, "RAS_content"] = newVal
                    self.rightFrame.topFrame.rasEntry.delete(0, 'end')
            except ValueError:
                print("Do something: ras")
        
        newVal = self.rightFrame.topFrame.binderEntry.get()
        if newVal != "":
            try:
                newVal = abs(float(newVal))
                agg_content = data.at[0, "Agg_content"]
                
                if newVal < data.at[0, "Binder_content"]:
                    data.at[0, "Agg_content"] = agg_content \
                        + data.at[0, "Binder_content"]      \
                        - newVal
                    data.at[0, "Binder_content"] = newVal
                    self.rightFrame.topFrame.binderEntry.delete(0, 'end')
                elif (agg_content + data.at[0, "Binder_content"] - newVal) \
                        >= 0:
                    data.at[0, "Agg_content"] = agg_content \
                        + data.at[0, "Binder_content"]      \
                        - newVal
                    data.at[0, "Binder_content"] = newVal
                    self.rightFrame.topFrame.binderEntry.delete(0, 'end')
            except ValueError:
                print("Do something: binder")
        
        newVal = self.rightFrame.topFrame.limeEntry.get()
        if newVal != "":
            try:
                newVal = abs(float(newVal))
                agg_content = data.at[0, "Agg_content"]
                
                if newVal < data.at[0, "lime"]:
                    data.at[0, "Agg_content"] = agg_content \
                        + data.at[0, "lime"]      \
                        - newVal
                    data.at[0, "lime"] = newVal
                    self.rightFrame.topFrame.limeEntry.delete(0, 'end')
                elif (agg_content + data.at[0, "lime"] - newVal) >= 0:
                    data.at[0, "Agg_content"] = agg_content \
                        + data.at[0, "lime"]                \
                        - newVal
                    data.at[0, "lime"] = newVal
                    self.rightFrame.topFrame.limeEntry.delete(0, 'end')
            except ValueError:
                print("Do something: lime")

        self.rightFrame.topFrame.nmasLabel.configure(
            text="NMAS (in): " + str(data.at[0, "NMAS"]))
        self.rightFrame.topFrame.rapLabel.configure(
            text="RAP       %: " + str(data.at[0, "RAP_content"]))
        self.rightFrame.topFrame.rasLabel.configure(
            text="RAS       %: " + str(data.at[0, "RAS_content"]))
        self.rightFrame.topFrame.binderLabel.configure(
            text="Binder    %: " + str(data.at[0, "Binder_content"]))
        self.rightFrame.topFrame.limeLabel.configure(
            text="Lime      %: " + str(data.at[0, "lime"]))
        self.rightFrame.topFrame.aggLabel.configure(
            text="Aggregate %: " + str(data.at[0, "Agg_content"]))
    
    def _quit(self):
        root.quit()
        root.destroy()
        

def main():
    root.mainloop()


if __name__ == "__main__":
    root = ctk.CTk()
    root.geometry("720x540")
    root.resizable(False, False)
    
    app = mainApp(root)
    
    app.pack(side="top", fill="both", expand=True)
    root.bind('<Return>', app.clearEntries)
    
    root.protocol("WM_DELETE_WINDOW", app._quit)
    main()
