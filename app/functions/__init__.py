from tkinter.messagebox import showinfo
import pandas as pd
import numpy as np
import pyperclip3 as pc
from data import get_sheet_names, get_class_df

class FilterWidgetValues:
    
    df_filtered = None
    df_backup = None
    serie = pd.Series([], dtype='O')  
    list_header = None
    
    wid_value = None
    previous_column_name = None
    current_column_name = None
    
    used_filters = {}
    
    def __select_class_df(self, class_name):
        match class_name:
            case 'Português':
                internal_class_name = 'portuguese'
            case 'Artes':
                internal_class_name = 'art'
            case 'Matemática':
                internal_class_name = 'math'
            case 'Ciências':
                internal_class_name = 'science'
            case 'Geografia':
                internal_class_name = 'geography'
            case 'História':
                internal_class_name = 'history'
            case 'E. Religioso':
                internal_class_name = 'religion'
        
        self.df_backup = self.df_filtered = get_class_df()[internal_class_name]
        self.list_header = [i for i in self.df_backup.columns]
        self.class_name = class_name
        
    def fill_widget(self, evt, widget_to_fill=None):
        self.wid_value = evt.widget.get()
        if widget_to_fill == None:
            self.__select_class_df(self.wid_value)
            self.current_column_name = self.list_header[0]
            serie = self.df_filtered[self.current_column_name]
            serie = serie.drop_duplicates()
            values = [i for i in serie.values]
            return values
        elif widget_to_fill.winfo_class() != 'Listbox':
            self.__update_used_filter()
            cur_column = self.__set_current_column_name()
            self.serie = self.df_filtered[cur_column]
            self.serie = self.serie.drop_duplicates()                
            values = [i for i in self.serie.values]
            widget_to_fill.config(values=values)
        else:
            self.__update_used_filter()
            cur_column = self.__set_current_column_name()
            self.serie = self.df_filtered[cur_column]
            self.serie = self.serie.drop_duplicates()
            values = [i for i in self.serie.values]
            widget_to_fill.delete(0, 'end')
            for i in values:
                widget_to_fill.insert('end', i)
    
    def __set_current_column_name(self):
        serie_temp = self.df_backup[self.current_column_name].drop_duplicates()
        if self.wid_value in serie_temp.values: 
            self.previous_column_name = self.current_column_name
            self.current_column_name = self.list_header[self.list_header.index(self.previous_column_name)+1]
            self.__filter_dataframe(self.previous_column_name)
        else:
            while self.wid_value not in self.df_backup[self.previous_column_name].values:
                self.current_column_name = self.previous_column_name
                self.previous_column_name = self.list_header[self.list_header.index(self.current_column_name)-1]
            self.__filter_dataframe(self.previous_column_name, reverse=True)
        
        return self.current_column_name
    
    def __filter_dataframe(self, previous_column, reverse=False):
        if reverse:
            headers_needs = self.list_header[self.list_header.index(previous_column): len(self.list_header)]
            self.df_filtered = self.df_backup.copy()
            if headers_needs[0] != self.list_header[0] and len(self.list_header) == 4:
                for k in self.used_filters.keys():
                    if k not in headers_needs:
                        idx = np.where(self.df_filtered[k]==self.used_filters[k])
                        self.df_filtered = self.df_filtered.iloc[idx].copy()
            idx = np.where(self.df_filtered[previous_column]==self.wid_value)
            self.df_filtered = self.df_filtered.iloc[idx].copy()
            self.df_filtered.drop(previous_column, axis='columns', inplace=True)
        else:
            idx = np.where(self.df_filtered[previous_column]==self.wid_value)
            self.df_filtered = self.df_filtered.iloc[idx].copy()
            self.df_filtered.drop(previous_column, axis='columns', inplace=True)
    
    def __update_used_filter(self):
        self.used_filters[self.current_column_name] = self.wid_value


class SubmitHability:
    
    file_path = None
    def __init__(self, file_path) -> None:
        self.file_path = file_path

    def write(self, text):
        self.file = open(self.file_path, 'a') 
        full_text = f"{text}\n"
        self.file.write(full_text)
        showinfo('HABILIDADE ADICIONADA',  'Habilidade selecionada.')
    
    def close(self):
        self.file.close()
        self.file = open(self.file_path, 'r')
        text = self.file.read()
        pc.clear()
        pc.copy(text)
        self._delete_content()
        showinfo('HABILIDADE ADICIONADA',  'Habilidade(s) adicionada(s) na área de transferência!\nJá pode utilizar o Ctrl + V')
    
    def _delete_content(self):
        self.file.close()
        self.file = open(self.file_path, 'w')
        self.file.close()
