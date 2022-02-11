import tkinter as tk
import tkinter.ttk as ttk
from tkinter.messagebox import showinfo
from config.config import *
from data import get_sheet_names, get_class_df
import pandas as pd
import numpy as np

class MainWindow:
    root = tk.Tk()

    def __init__(self):
        self.root
             
        Header()
        
        center(self.root, height=500)
        self.root.mainloop()


class Header:
    
    def __init__(self):
        self.root = MainWindow.root
        self.filter = FilterWidgetValues()
        
        self.class_label = ttk.Label(self.root, 
                                     text='MATÉRIA',
                                     width=25)
        self.class_combobox = ttk.Combobox(self.root,
                                           values=get_sheet_names(),
                                           width=50)
        self.knowlegde_objects_label = ttk.Label(self.root,
                                                 text='OBJETOS DE CONHECIMENTO')
        self.knowlegde_objects_combobox = ttk.Combobox(self.root)
        self.hability_labelfframe = ttk.LabelFrame(self.root,
                                             text='HABILIDADES')
        self.hability_listbox = tk.Listbox(self.hability_labelfframe,
                                           selectmode=tk.SINGLE)
        self.hability_label = tk.Label(self.hability_labelfframe,
                                           justify=tk.LEFT)
        self.submit_button = ttk.Button(self.hability_labelfframe,
                                         text='SELECIONAR HABILIDADE',
                                         command=lambda: self.submit_hability)
        
        self.class_combobox.bind('<<ComboboxSelected>>', lambda evt: self._widgets_to_portuguese_class(evt))
        self.knowlegde_objects_combobox.bind('<<ComboboxSelected>>', lambda evt: self.filter.fill_widget(evt, self.hability_listbox))
        self.hability_listbox.bind('<<ListboxSelect>>', lambda evt: self.__show_hability(evt))
        
        self.class_label.grid(row=0, column=0, padx=(20, 0), pady=(20, 0), sticky=tk.EW)
        self.class_combobox.grid(row=0, column=1, padx=(10, 20), pady=(20, 0), sticky=tk.EW)
        self.knowlegde_objects_label.grid(row=3, column=0, padx=(20, 0), pady=(10, 0), sticky=tk.EW)
        self.knowlegde_objects_combobox.grid(row=3, column=1, padx=(10, 20), pady=(10, 0), sticky=tk.EW)
        
        self.hability_labelfframe.grid(row=4, column=0, columnspan=2, padx=(20,20), pady=(10, 10), sticky=tk.EW)
        self.hability_listbox.grid(row=0, rowspan=5, column=0,columnspan=5, padx=(20, 20), pady=(20, 0), sticky=tk.EW)
        self.hability_label.grid(row=1, column=0, columnspan=3, padx=(20, 10), pady=(10, 0), sticky=tk.EW)
        self.submit_button.grid(row=1, column=3, columnspan=2, pady=(0, 20), pady=(10, 0), sticky=tk.EW)
    
    def submit_hability(self):
        hability = self.hability_label.cget('text')
        
        
    def __show_hability(self, evt):    
        self.hability_label.config(text=evt.widget.get(tk.ACTIVE))
        
    def __is_portuguese(self) -> bool:
       value = self.class_combobox.get()
       if value == 'Português':
           return True
       else:
           return False
    
    def _widgets_to_portuguese_class(self, evt):
        if self.__is_portuguese():
            self.atuation_field_label = ttk.Label(self.root,
                                                  text='CAMPOS DE ATUAÇÃO')
            self.atuation_field_combobox = ttk.Combobox(self.root)
            self.language_pratic_label = ttk.Label(self.root,
                                                   text='PRÁTICAS DE LINGUAGEM')
            self.language_pratic_combobox = ttk.Combobox(self.root)
            
            self.atuation_field_combobox.config(values=self.filter.fill_widget(evt))
            
            self.atuation_field_combobox.bind('<<ComboboxSelected>>', lambda evt: self.filter.fill_widget(evt, self.language_pratic_combobox))
            self.language_pratic_combobox.bind('<<ComboboxSelected>>', lambda evt: self.filter.fill_widget(evt, self.knowlegde_objects_combobox))
            
            self.atuation_field_label.grid(row=1, column=0, padx=(20, 0), pady=(10, 0), sticky=tk.EW)
            self.atuation_field_combobox.grid(row=1, column=1, padx=(10, 20), pady=(10, 0), sticky=tk.EW)
            self.language_pratic_label.grid(row=2, column=0, padx=(20, 0), pady=(10, 0), sticky=tk.EW)
            self.language_pratic_combobox.grid(row=2, column=1, padx=(10, 20), pady=(10, 0), sticky=tk.EW)
        else:
            try:
                self.atuation_field_label.grid_forget()
                self.atuation_field_combobox.grid_forget()
                self.language_pratic_label.grid_forget()
                self.language_pratic_combobox.grid_forget()
            except:
                pass
            self.thematic_units_label = ttk.Label(self.root,
                                                  text='UNIDADES TEMÁTICAS')
            self.thematic_units_combobox = ttk.Combobox(self.root)
            
            self.thematic_units_combobox.config(values=self.filter.fill_widget(evt))
            
            self.thematic_units_label.grid(row=1, column=0, padx=(20, 0), pady=(10, 0), sticky=tk.EW)
            self.thematic_units_combobox.grid(row=1, column=1, padx=(10, 20), pady=(10, 0), sticky=tk.EW)

            self.thematic_units_combobox.bind('<<ComboboxSelected>>', lambda evt: self.filter.fill_widget(evt, self.knowlegde_objects_combobox))
        
        self.__clear_combobox()
    
    def __clear_combobox(self):
        for k, widget in enumerate(self.root.children.values()):
            if k != 2:
                if widget.winfo_class() != 'TLabelframe':
                    if widget.winfo_class() == 'TCombobox':
                        widget.delete(0, tk.END)
                else:
                    for wid in widget.children.values():
                        try:
                            if wid.winfo_class() == 'Message':
                                wid.configure(text='')
                            else:
                                wid.delete(0, tk.END)
                        except:
                            pass
        

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
        
    def fill_widget(self, evt, widget_to_fill=ttk.Combobox()):
        self.wid_value = evt.widget.get()
        if widget_to_fill.winfo_class() != 'Listbox':
            if self.wid_value in get_sheet_names():
                self.__select_class_df(self.wid_value)
                self.current_column_name = self.list_header[0]
                serie = self.df_filtered[self.current_column_name]
                serie = serie.drop_duplicates()
                values = [i for i in serie.values]
                return values
            else:
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
            widget_to_fill.delete(0, tk.END)
            for i in values:
                widget_to_fill.insert(tk.END, i)
    
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

        

       