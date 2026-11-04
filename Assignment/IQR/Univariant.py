import pandas as pd
import numpy as np
class Univariant:
    def quanqual(dataset):
        qual = []
        quan = []
        for columnName in dataset.columns:
            if(dataset[columnName].dtype.name == "str"):
              # print("Qual")
               qual.append(columnName) 
            else:
               #print("Quan")
               quan.append(columnName)
        return quan,qual  
        
    def Univariate(dataset,quan):
       descriptive = pd.DataFrame(index = ["Mean","Median","Mode","Q1:25","Q2:50","Q3:75","Q4:100","IQR","1.5rule","Lesser","Greater","Min","Max"], columns = quan)
       for columnName in quan:
            descriptive.loc["Mean",columnName] = dataset[columnName].mean()
            descriptive.loc["Median",columnName] = dataset[columnName].median()
            descriptive.loc["Mode",columnName] = dataset[columnName].mode()[0]
            descriptive.loc["Q1:25",columnName] = dataset.describe()[columnName]["25%"]
            descriptive.loc["Q2:50",columnName] = dataset.describe()[columnName]["50%"]
            descriptive.loc["Q3:75",columnName] = dataset.describe()[columnName]["75%"]
            #descriptive.loc["99%",columnName] = np.percentile(dataset[columnName],99)
            descriptive.loc["Q4:100",columnName] = dataset.describe()[columnName]["max"]
            descriptive.loc["IQR",columnName] =  descriptive.loc["Q3:75",columnName] - descriptive.loc["Q1:25",columnName]
            descriptive.loc["1.5rule",columnName] = 1.5* descriptive.loc["IQR",columnName]
            descriptive.loc["Lesser",columnName] = descriptive.loc["Q1:25",columnName] - descriptive.loc["1.5rule",columnName]
            descriptive.loc["Greater",columnName] = descriptive.loc["Q3:75",columnName] + descriptive.loc["1.5rule",columnName]
            descriptive.loc["Min",columnName] = dataset[columnName].min()
            descriptive.loc["Max",columnName] = dataset[columnName].max()
       return descriptive

    def freqTable(columnName,dataset):
        freqTable = pd.DataFrame(columns= ["unique_values","Frequency","Relative Frequency","Cumsum"])
        freqTable["unique_values"] = dataset["ssc_p"].value_counts().index
        freqTable["Frequency"] = dataset["ssc_p"].value_counts().values
        freqTable["Relative Frequency"] = freqTable["Frequency"]/103
        freqTable["Cumsum"] = freqTable["Relative Frequency"].cumsum()
        return freqTable

    def outlier_column(descriptive , quan):
      lesser = []
      greater = []
      for columnName in quan:
          if descriptive.loc["Min", columnName] < descriptive.loc["Lesser", columnName]:
             lesser.append(columnName)
    
          if descriptive.loc["Max", columnName] > descriptive.loc["Greater", columnName]:
            greater.append(columnName)           
      return lesser, greater

    def replacement_outlier(dataset, descriptive, lesser, greater):

        for columnName in lesser:
            condition = dataset[columnName] < descriptive.loc["Lesser", columnName]
            dataset.loc[condition, columnName] = descriptive.loc["Lesser", columnName]
    
        for columnName in greater:
            condition = dataset[columnName] > descriptive.loc["Greater", columnName]
            dataset.loc[condition, columnName] = descriptive.loc["Greater", columnName]
        return descriptive