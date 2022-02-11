
import pandas as pd 

file = pd.ExcelFile('data\data_classes.xlsm')

df_portuguese = file.parse('Português')
df_art = file.parse('Artes')
df_math = file.parse('Matemática')
df_science = file.parse('Ciências')
df_geography = file.parse('Geografia')
df_history = file.parse('História')
df_religion = file.parse('E. Religioso')

class_df_dict = {
    'portuguese': df_portuguese, 
    'art': df_art,
    'math':df_math,
    'science': df_science,
    'geography': df_geography,
    'history': df_history,
    'religion': df_religion
}

def get_class_df() -> dict:
    return class_df_dict

def get_sheet_names() -> list:
    return file.sheet_names
