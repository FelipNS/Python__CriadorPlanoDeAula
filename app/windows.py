import tkinter as tk
from tkinter import *
import tkinter.ttk as ttk
from config.config import *
from data import get_names_sheet, get_class_df

class MainWindow:
    root = tk.Tk()

    def __init__(self):
        self.root
        
        Header()
        
        center(self.root)
        self.root.mainloop()


class Header:
    
    def __init__(self):
        self.root = MainWindow.root
        self.filter = FilterWidgetValues()
        
        self.class_label = ttk.Label(self.root, 
                                     text='MATÉRIA',
                                     width=25)
        self.class_combobox = ttk.Combobox(self.root, 
                                           values=get_names_sheet(),
                                           width=50)
        self.knowlegde_objects_label = ttk.Label(self.root,
                                                 text='OBJETOS DE CONHECIMENTO')
        self.knowlegde_objects_combobox = ttk.Combobox(self.root)       
        self.hability_labelf = ttk.LabelFrame(self.root,
                                             text='HABILIDADES')
        self.hability_listbox = Listbox(self.hability_labelf,
                                         selectmode=SINGLE)
        
        self.class_combobox.bind('<<ComboboxSelected>>', self._widgets_to_portuguese_class)
        
        self.class_label.grid(row=0, column=0, padx=(20, 0), pady=(20, 0), sticky=EW)
        self.class_combobox.grid(row=0, column=1, padx=(10, 20), pady=(20, 0), sticky=EW)
        self.knowlegde_objects_label.grid(row=2, column=0, padx=(20, 0), pady=(10, 20), sticky=EW)
        self.knowlegde_objects_combobox.grid(row=2, column=1, padx=(10, 20), pady=(10, 20), sticky=EW)
        
    def __is_portuguese(self) -> bool:
       value = self.class_combobox.get()
       if value == 'Português':
           return True
       else:
           return False
    
    def _widgets_to_portuguese_class(self, evt):
        self.filter._restore_attributes()
        self.filter.class_name = self.class_combobox.get()
        if self.__is_portuguese():
            self.atuation_field_label = ttk.Label(self.root,
                                                  text='CAMPO DE ATUAÇÃO')
            self.atuation_field_combobox = ttk.Combobox(self.root,
                                                        values=self.filter.filter(column='Campos de Atuação',
                                                                                  yourself=True))
            self.language_pratic_label = ttk.Label(self.root,
                                                   text='PRÁTICAS DE LINGUAGEM')
            self.language_pratic_combobox = ttk.Combobox(self.root)
            
            self.atuation_field_combobox.bind('<<ComboboxSelected>>', 
                                              lambda evt: self.filter.set_values_combo(self.language_pratic_combobox,
                                                                                       self.filter.filter('Campos de Atuação',
                                                                                                          self.atuation_field_combobox.get(),
                                                                                                          yourself=False)))
            self.language_pratic_combobox.bind('<<ComboboxSelected>>', 
                                               lambda evt: self.filter.set_values_combo(self.knowlegde_objects_combobox,
                                                                                        self.filter.filter('Práticas de Linguagem',
                                                                                                           self.language_pratic_combobox.get(),
                                                                                                           yourself=False)))
            self.knowlegde_objects_combobox.bind('<<ComboboxSelected>>', lambda evt: self.filter.fill_listbox(self.hability_listbox,
                                                                                                              self.knowlegde_objects_combobox))
            
            self.atuation_field_label.grid(row=1, column=0, padx=(20, 0), pady=(10, 0), sticky=EW)
            self.atuation_field_combobox.grid(row=1, column=1, padx=(10, 20), pady=(10, 0), sticky=EW)
            self.language_pratic_label.grid(row=2, column=0, padx=(20, 0), pady=(10, 0), sticky=EW)
            self.language_pratic_combobox.grid(row=2, column=1, padx=(10, 20), pady=(10, 0), sticky=EW)
            
            self.knowlegde_objects_label.grid_forget()
            self.knowlegde_objects_combobox.grid_forget()
            self.knowlegde_objects_label.grid(row=3, column=0, padx=(20, 0), pady=(10, 20), sticky=EW)
            self.knowlegde_objects_combobox.grid(row=3, column=1, padx=(10, 20), pady=(10, 20), sticky=EW)
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
            self.thematic_units_combobox = ttk.Combobox(self.root,
                                                        values=self.filter.filter(column='Unidades Temáticas',
                                                                                  yourself=True))
            
            self.thematic_units_combobox.bind('<<ComboboxSelected>>', 
                                               lambda evt: self.filter.set_values_combo(self.knowlegde_objects_combobox,
                                                                                        self.filter.filter('Unidades Temáticas',
                                                                                                           self.thematic_units_combobox.get(),
                                                                                                           yourself=False)))
            self.knowlegde_objects_combobox.bind('<<ComboboxSelected>>', lambda evt: self.filter.fill_listbox(self.hability_listbox,
                                                                                                              self.knowlegde_objects_combobox))
            
            self.thematic_units_label.grid(row=1, column=0, padx=(20, 0), pady=(10, 0), sticky=EW)
            self.thematic_units_combobox.grid(row=1, column=1, padx=(10, 20), pady=(10, 0), sticky=EW)
            

class FilterWidgetValues:
    
    class_name = None
    list_header = None
    df_filtered = None
    df_backup = None
    serie = None
    
    def select_class(self):
        match self.class_name:
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
        self.__uptade_list_header()
    
    def filter(self, column=None, target=None, yourself=False):
        if self.list_header == None:
            self.select_class()
        if yourself:
            self.serie  = self.df_filtered[column]
            self.__update_df_filtered(column, target)
        else:
            self.__update_df_filtered(column, target)
            self.__uptade_list_header()
            self.serie  = self.df_filtered[self.list_header[0]]
        self.serie = self.serie.drop_duplicates()
        values_list = [i for i in self.serie.values]
        return values_list
    
    def __uptade_list_header(self):
        self.list_header = [i for i in self.df_filtered.columns]
    
    def __update_df_filtered(self, column, target):
        if target != None:
            self.df_filtered = self.df_filtered[self.df_filtered[column]==target]
            self.df_filtered.drop(column, axis='columns', inplace=True)   
    
    def set_values_combo(self, combobox: ttk.Combobox, values):
        combobox['values'] = values
    
    def fill_listbox(self, listbox, combobox: ttk.Combobox):
        print(self.df_filtered[self.df_filtered['Objetos de Conhecimento']==combobox.get()]['Habilidades'])
        self._restore_attributes()
        
    def _restore_attributes(self):
        self.list_header = None
        try:
            self.df_filtered = self.df_backup.copy()
        except:
            pass