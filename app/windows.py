import tkinter as tk
import tkinter.ttk as ttk
from config.config import *
from data import get_sheet_names
from app.functions import FilterWidgetValues, SubmitHability

class App:

    root = tk.Tk()    

    def __init__(self):
        self.root
        self.root.title('Seletor de Habilidades')
             
        WidgetsApp()
        
        center(self.root, height=500)
        self.root.mainloop()

class WidgetsApp:
    
    def __init__(self):
        self.root = App.root
        
        self.filter = FilterWidgetValues()
        self.submit_hability = SubmitHability(r"data\habilitys.txt")

        
        self.class_label = ttk.Label(self.root, 
                                     text='MATÉRIA',
                                     width=25)
        self.class_combobox = ttk.Combobox(self.root,
                                           values=get_sheet_names(),
                                           width=50)
        self.knowlegde_objects_label = ttk.Label(self.root,
                                                 text='OBJETOS DE CONHECIMENTO')
        self.knowlegde_objects_combobox = ttk.Combobox(self.root)
        self.hability_labelframe = ttk.LabelFrame(self.root,
                                             text='HABILIDADES')
        self.hability_listbox = tk.Listbox(self.hability_labelframe,
                                           selectmode=tk.SINGLE)
        self.hability_label = tk.Label(self.hability_labelframe,
                                           justify=tk.LEFT)
        self.submit_button = ttk.Button(self.hability_labelframe,
                                         text='SELECIONAR HABILIDADE',
                                         width=30,
                                         command=lambda: self.select_hability())
        self.save_button = ttk.Button(self.hability_labelframe,
                                      text='COPIAR PARA A ÁREA DE TRANSFERÊNCIA',
                                      width=30,
                                      command=lambda: self.copy_to_clipboard())
        
        self.class_combobox.bind('<<ComboboxSelected>>', lambda evt: self._widgets_to_portuguese_class(evt))
        self.knowlegde_objects_combobox.bind('<<ComboboxSelected>>', lambda evt: self.filter.fill_widget(evt, self.hability_listbox))
        self.hability_listbox.bind('<<ListboxSelect>>', lambda evt: self.__show_hability(evt))
        
        self.class_label.grid(row=0, column=0, padx=(20, 0), pady=(20, 0), sticky=tk.EW)
        self.class_combobox.grid(row=0, column=1, padx=(10, 20), pady=(20, 0), sticky=tk.EW)
        self.knowlegde_objects_label.grid(row=3, column=0, padx=(20, 0), pady=(10, 0), sticky=tk.EW)
        self.knowlegde_objects_combobox.grid(row=3, column=1, padx=(10, 20), pady=(10, 0), sticky=tk.EW)
        
        self.hability_labelframe.grid(row=4, column=0, columnspan=2, padx=(20,20), pady=(10, 10), sticky=tk.EW)
        self.hability_listbox.pack(fill=tk.X, side=tk.TOP, expand=True, padx=(20, 0), pady=(0,10))
        self.hability_label.pack(fill=tk.X, side=tk.TOP, expand=False, padx=(20, 10), pady=(0, 10))
        self.save_button.pack(fill=tk.BOTH, side=tk.BOTTOM, expand=False, padx=(20, 20), pady=(0, 10))
        self.submit_button.pack(fill=tk.BOTH, side=tk.BOTTOM, expand=False, padx=(20, 20), pady=(0, 20))
    
    def copy_to_clipboard(self):
        self.submit_hability.close()
    
    def select_hability(self):
        self.submit_hability.write(self.hability_label.cget('text'))
    
    def __show_hability(self, evt):
        try:
            text = self.hability_listbox.get(evt.widget.curselection())
        except tk.TclError:
            self.hability_label.config(text='')
            return          
        multine_text = str()
        broken_in = 60
        idx=0
        while idx < len(text):
            if broken_in <= len(text):
                if idx <= broken_in:
                    multine_text += text[idx]
                    idx += 1
                else:
                    while text[idx] != ' ':
                        multine_text += text[idx]
                        idx += 1
                        if idx >= len(text):
                            break
                    multine_text += '\n'
                    broken_in += 60
                    idx += 1
            else:
                multine_text += text[len(multine_text):]
                break
     
        self.hability_label.config(text=multine_text)
        
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
            if k != 1:
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
        
        

       