
import pandas as pd
import numpy as np

file = pd.ExcelFile('data_classes.xlsm')

df_portuguese = file.parse('Português')
df_art = file.parse('Artes')
df_math = file.parse('Matemática')
df_science = file.parse('Ciências')
df_geography = file.parse('Geografia')
df_history = file.parse('História')
df_religion = file.parse('E. Religioso')

class_df_tpl = (df_portuguese, df_art, df_math, df_science, df_geography, df_history, df_religion)

def get_class_df():
    return get_class_df


