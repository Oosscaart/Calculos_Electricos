import tkinter as tk
from tkinter import ttk, messagebox
import math
from datetime import datetime

class CalculadoraCaidaTension:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculadora de Caída de Tensión - Grupo Hertz Servicios Eléctricos")
        self.root.geometry("1200x800")
        self.root.configure(bg='#f0f0f0')
        
        # Lista para almacenar historial
        self.historial = []
        
        # Tablas de impedancia
        self.impedancia_cobre = {
            "PVC": {
                "1": 0.52, "2": 0.62, "3": 0.75, "4": 0.95, "6": 1.44,
                "8": 2.26, "10": 3.6, "12": 5.6, "14": 0.89,
                "250": 0.217, "300": 0.194, "350": 0.174, "400": 0.161,
                "500": 0.141, "600": 0.131, "750": 0.118, "1000": 0.105,
                "1/0": 0.43, "2/0": 0.36, "3/0": 0.289, "4/0": 0.243
            },
            "Aluminio": {
                "1": 0.52, "2": 0.62, "3": 0.79, "4": 0.95, "6": 1.48,
                "8": 2.26, "10": 3.6, "12": 5.6, "14": 0.89,
                "250": 0.230, "300": 0.207, "350": 0.190, "400": 0.174,
                "500": 0.157, "600": 0.144, "750": 0.131, "1000": 0.118,
                "1/0": 0.43, "2/0": 0.36, "3/0": 0.302, "4/0": 0.256
            },
            "Acero": {
                "1": 0.52, "2": 0.66, "3": 0.79, "4": 0.98, "6": 1.48,
                "8": 2.26, "10": 3.6, "12": 5.6, "14": 0.89,
                "250": 0.240, "300": 0.213, "350": 0.197, "400": 0.184,
                "500": 0.164, "600": 0.154, "750": 0.141, "1000": 0.131,
                "1/0": 0.43, "2/0": 0.36, "3/0": 0.308, "4/0": 0.262
            }
        }

        self.impedancia_aluminio = {
            "PVC": {
                "1": 0.79, "2": 0.98, "3": 1.21, "4": 1.51, "6": 2.33,
                "250": 0.308, "300": 0.269, "350": 0.240, "400": 0.217,
                "500": 0.187, "600": 0.167, "750": 0.148, "1000": 0.128,
                "1/0": 0.62, "2/0": 0.52, "3/0": 0.43, "4/0": 0.36
            },
            "Aluminio": {
                "1": 0.79, "2": 0.98, "3": 1.21, "4": 1.51, "6": 2.36,
                "250": 0.322, "300": 0.282, "350": 0.253, "400": 0.233,
                "500": 0.200, "600": 0.180, "750": 0.161, "1000": 0.138,
                "1/0": 0.62, "2/0": 0.52, "3/0": 0.43, "4/0": 0.36
            },
            "Acero": {
                "1": 0.82, "2": 0.98, "3": 1.21, "4": 1.51, "6": 2.36,
                "250": 0.33, "300": 0.289, "350": 0.262, "400": 0.24,
                "500": 0.21, "600": 0.19, "750": 0.171, "1000": 0.151,
                "1/0": 0.66, "2/0": 0.52, "3/0": 0.46, "4/0": 0.36
            }
        }
        
        self.setup_ui()
    
    def setup_ui(self):
        # Título
        title_frame = tk.Frame(self.root, bg='#2c3e50', pady=15)
        title_frame.pack(fill='x')
        
        title_label = tk.Label(title_frame, text="Grupo Hertz Servicios Eléctricos S.A. de C.V.", 
                              font=('Arial', 14, 'bold'), fg='white', bg='#2c3e50')
        title_label.pack()
        
        subtitle_label = tk.Label(title_frame, text="Creado por Ing. Arturo Cruz Morales", 
                                 font=('Arial', 10), fg='#ecf0f1', bg='#2c3e50')
        subtitle_label.pack()
        
        # Frame principal con dos columnas
        main_frame = tk.Frame(self.root, bg='#f0f0f0', padx=10, pady=10)
        main_frame.pack(fill='both', expand=True)
        
        # Columna izquierda - Entrada de datos
        left_frame = tk.Frame(main_frame, bg='#f0f0f0')
        left_frame.pack(side='left', fill='y', padx=(0, 10))
        
        # Descripción
        desc_label = tk.Label(left_frame, text="Calculadora de Caída de Tensión\nBasada en NOM-001-SEDE-2012\nCalculando corriente automáticamente", 
                             font=('Arial', 11), bg='#f0f0f0', fg='#2c3e50')
        desc_label.pack(pady=(0, 15))
        
        # Frame de entrada de datos
        input_frame = tk.LabelFrame(left_frame, text="Datos del Circuito", font=('Arial', 11, 'bold'), 
                                   bg='#f0f0f0', fg='#2c3e50', padx=15, pady=15)
        input_frame.pack(fill='both', expand=True)
        
        # Tipo de circuito
        tk.Label(input_frame, text="Tipo de circuito:", font=('Arial', 10), bg='#f0f0f0').grid(row=0, column=0, sticky='w', pady=5)
        self.tipo_circuito_var = tk.StringVar(value="monofasico")
        tipo_circuito_frame = tk.Frame(input_frame, bg='#f0f0f0')
        tipo_circuito_frame.grid(row=0, column=1, sticky='w', pady=5)
        tk.Radiobutton(tipo_circuito_frame, text="Monofásico", variable=self.tipo_circuito_var, 
                      value="monofasico", bg='#f0f0f0').pack(side='left')
        tk.Radiobutton(tipo_circuito_frame, text="Trifásico", variable=self.tipo_circuito_var, 
                      value="trifasico", bg='#f0f0f0').pack(side='left')
        
        # Tipo de carga
        tk.Label(input_frame, text="Tipo de carga:", font=('Arial', 10), bg='#f0f0f0').grid(row=1, column=0, sticky='w', pady=5)
        self.tipo_carga_var = tk.StringVar(value="derivado")
        tipo_carga_frame = tk.Frame(input_frame, bg='#f0f0f0')
        tipo_carga_frame.grid(row=1, column=1, sticky='w', pady=5)
        tk.Radiobutton(tipo_carga_frame, text="Circuito derivado", variable=self.tipo_carga_var, 
                      value="derivado", bg='#f0f0f0').pack(side='left')
        tk.Radiobutton(tipo_carga_frame, text="Alimentador", variable=self.tipo_carga_var, 
                      value="alimentador", bg='#f0f0f0').pack(side='left')
        
        # Potencia con unidades
        tk.Label(input_frame, text="Potencia:", font=('Arial', 10), bg='#f0f0f0').grid(row=2, column=0, sticky='w', pady=5)
        potencia_frame = tk.Frame(input_frame, bg='#f0f0f0')
        potencia_frame.grid(row=2, column=1, sticky='w', pady=5)
        
        self.potencia_var = tk.StringVar()
        tk.Entry(potencia_frame, textvariable=self.potencia_var, width=12).pack(side='left', padx=(0, 5))
        
        self.unidad_potencia_var = tk.StringVar(value="W")
        unidad_combo = ttk.Combobox(potencia_frame, textvariable=self.unidad_potencia_var, width=8)
        unidad_combo['values'] = ("W", "kW", "kVA", "A", "HP")
        unidad_combo.pack(side='left')
        unidad_combo.bind('<<ComboboxSelected>>', self.cambiar_unidad_potencia)
        
        # Voltaje
        tk.Label(input_frame, text="Tensión nominal (V):", font=('Arial', 10), bg='#f0f0f0').grid(row=3, column=0, sticky='w', pady=5)
        self.voltaje_var = tk.StringVar()
        tk.Entry(input_frame, textvariable=self.voltaje_var, width=20).grid(row=3, column=1, sticky='w', pady=5)
        
        # Tipo de equipo
        tk.Label(input_frame, text="Tipo de equipo:", font=('Arial', 10), bg='#f0f0f0').grid(row=4, column=0, sticky='w', pady=5)
        self.tipo_equipo_var = tk.StringVar(value="Motor mediano (1-10 HP)")
        self.tipo_equipo_combo = ttk.Combobox(input_frame, textvariable=self.tipo_equipo_var, width=17)
        self.tipo_equipo_combo['values'] = (
            "Personalizado",
            "Motor pequeño (<1 HP)",
            "Motor mediano (1-10 HP)", 
            "Motor grande (>10 HP)",
            "Iluminación incandescente",
            "Iluminación fluorescente",
            "Iluminación LED",
            "Cargas resistivas",
            "UPS/Rectificadores"
        )
        self.tipo_equipo_combo.grid(row=4, column=1, sticky='w', pady=5)
        self.tipo_equipo_combo.bind('<<ComboboxSelected>>', self.actualizar_factores)
        
        # Factor de potencia
        tk.Label(input_frame, text="Factor de potencia (cos φ):", font=('Arial', 10), bg='#f0f0f0').grid(row=5, column=0, sticky='w', pady=5)
        self.fp_var = tk.StringVar(value="0.87")
        tk.Entry(input_frame, textvariable=self.fp_var, width=20).grid(row=5, column=1, sticky='w', pady=5)
        
        # Eficiencia
        tk.Label(input_frame, text="Eficiencia (η):", font=('Arial', 10), bg='#f0f0f0').grid(row=6, column=0, sticky='w', pady=5)
        self.eficiencia_var = tk.StringVar(value="0.88")
        tk.Entry(input_frame, textvariable=self.eficiencia_var, width=20).grid(row=6, column=1, sticky='w', pady=5)
        
        # Calibre
        tk.Label(input_frame, text="Calibre del conductor:", font=('Arial', 10), bg='#f0f0f0').grid(row=7, column=0, sticky='w', pady=5)
        self.calibre_var = tk.StringVar()
        calibre_combo = ttk.Combobox(input_frame, textvariable=self.calibre_var, width=17)
        calibre_combo['values'] = ("1", "2", "3", "4", "6", "8", "10", "12", "14", "1/0", "2/0", "3/0", "4/0", 
                                  "250", "300", "350", "400", "500", "600", "750", "1000")
        calibre_combo.grid(row=7, column=1, sticky='w', pady=5)
        
        # Material
        tk.Label(input_frame, text="Material del conductor:", font=('Arial', 10), bg='#f0f0f0').grid(row=8, column=0, sticky='w', pady=5)
        self.material_var = tk.StringVar(value="cobre")
        material_frame = tk.Frame(input_frame, bg='#f0f0f0')
        material_frame.grid(row=8, column=1, sticky='w', pady=5)
        tk.Radiobutton(material_frame, text="Cobre", variable=self.material_var, 
                      value="cobre", bg='#f0f0f0').pack(side='left')
        tk.Radiobutton(material_frame, text="Aluminio", variable=self.material_var, 
                      value="aluminio", bg='#f0f0f0').pack(side='left')
        
        # Longitud
        tk.Label(input_frame, text="Longitud del circuito (m):", font=('Arial', 10), bg='#f0f0f0').grid(row=9, column=0, sticky='w', pady=5)
        self.longitud_var = tk.StringVar()
        tk.Entry(input_frame, textvariable=self.longitud_var, width=20).grid(row=9, column=1, sticky='w', pady=5)
        
        # Número de conductores
        tk.Label(input_frame, text="Conductores por fase:", font=('Arial', 10), bg='#f0f0f0').grid(row=10, column=0, sticky='w', pady=5)
        self.num_conductores_var = tk.StringVar(value="1")
        tk.Entry(input_frame, textvariable=self.num_conductores_var, width=20).grid(row=10, column=1, sticky='w', pady=5)
        
        # Canalización
        tk.Label(input_frame, text="Tipo de canalización:", font=('Arial', 10), bg='#f0f0f0').grid(row=11, column=0, sticky='w', pady=5)
        self.canalizacion_var = tk.StringVar(value="PVC")
        canalizacion_combo = ttk.Combobox(input_frame, textvariable=self.canalizacion_var, width=17)
        canalizacion_combo['values'] = ("PVC", "Aluminio", "Acero")
        canalizacion_combo.grid(row=11, column=1, sticky='w', pady=5)
        
        # Botones
        button_frame = tk.Frame(left_frame, bg='#f0f0f0')
        button_frame.pack(pady=20)
        
        calcular_btn = tk.Button(button_frame, text="Calcular Caída de Tensión", 
                               command=self.calcular, font=('Arial', 11, 'bold'),
                               bg='#3498db', fg='white', padx=20, pady=10,
                               cursor='hand2')
        calcular_btn.pack(pady=5)
        
        limpiar_btn = tk.Button(button_frame, text="Limpiar Campos", 
                              command=self.limpiar_campos, font=('Arial', 11),
                              bg='#95a5a6', fg='white', padx=20, pady=10,
                              cursor='hand2')
        limpiar_btn.pack(pady=5)
        
        # Columna derecha - Resultados e Historial
        right_frame = tk.Frame(main_frame, bg='#f0f0f0')
        right_frame.pack(side='right', fill='both', expand=True)
        
        # Frame de resultados (parte superior derecha)
        self.resultado_frame = tk.LabelFrame(right_frame, text="Resultados del Cálculo", font=('Arial', 12, 'bold'), 
                                           bg='#f0f0f0', fg='#2c3e50', padx=10, pady=10)
        self.resultado_frame.pack(fill='both', expand=True, pady=(0, 10))
        
        # Frame para el texto de resultados con scrollbar
        resultado_text_frame = tk.Frame(self.resultado_frame)
        resultado_text_frame.pack(fill='both', expand=True)
        
        self.resultado_text = tk.Text(resultado_text_frame, font=('Consolas', 10), 
                                    bg='white', wrap=tk.WORD, state='disabled')
        resultado_scrollbar = tk.Scrollbar(resultado_text_frame, command=self.resultado_text.yview)
        self.resultado_text.config(yscrollcommand=resultado_scrollbar.set)
        
        self.resultado_text.pack(side='left', fill='both', expand=True)
        resultado_scrollbar.pack(side='right', fill='y')
        
        # Frame de historial (parte inferior derecha)
        historial_frame = tk.LabelFrame(right_frame, text="Historial de Cálculos y Fórmulas", font=('Arial', 12, 'bold'), 
                                       bg='#f0f0f0', fg='#2c3e50', padx=10, pady=10)
        historial_frame.pack(fill='both', expand=True)
        
        # Frame para el texto de historial con scrollbar
        historial_text_frame = tk.Frame(historial_frame)
        historial_text_frame.pack(fill='both', expand=True)
        
        self.historial_text = tk.Text(historial_text_frame, font=('Consolas', 9), 
                                    bg='#f8f9fa', wrap=tk.WORD, state='disabled')
        historial_scrollbar = tk.Scrollbar(historial_text_frame, command=self.historial_text.yview)
        self.historial_text.config(yscrollcommand=historial_scrollbar.set)
        
        self.historial_text.pack(side='left', fill='both', expand=True)
        historial_scrollbar.pack(side='right', fill='y')
        
        # Botón para limpiar historial
        limpiar_historial_btn = tk.Button(historial_frame, text="Limpiar Historial", 
                                        command=self.limpiar_historial, font=('Arial', 9),
                                        bg='#e74c3c', fg='white', padx=10, pady=5,
                                        cursor='hand2')
        limpiar_historial_btn.pack(pady=(5, 0))

    def actualizar_factores(self, event=None):
        """Actualiza automáticamente factor de potencia y eficiencia según el tipo de equipo"""
        tipo = self.tipo_equipo_var.get()
        
        factores = {
            "Motor pequeño (<1 HP)": {"fp": "0.80", "eficiencia": "0.82"},
            "Motor mediano (1-10 HP)": {"fp": "0.87", "eficiencia": "0.88"},
            "Motor grande (>10 HP)": {"fp": "0.92", "eficiencia": "0.92"},
            "Iluminación incandescente": {"fp": "1.0", "eficiencia": "0.95"},
            "Iluminación fluorescente": {"fp": "0.90", "eficiencia": "0.85"},
            "Iluminación LED": {"fp": "0.95", "eficiencia": "0.90"},
            "Cargas resistivas": {"fp": "1.0", "eficiencia": "1.0"},
            "UPS/Rectificadores": {"fp": "0.85", "eficiencia": "0.88"}
        }
        
        if tipo in factores:
            self.fp_var.set(factores[tipo]["fp"])
            self.eficiencia_var.set(factores[tipo]["eficiencia"])

    def cambiar_unidad_potencia(self, event=None):
        """Maneja el cambio de unidad de potencia y ajusta la interfaz"""
        unidad = self.unidad_potencia_var.get()
        
        # Si selecciona Amperios, no necesita factor de potencia ni eficiencia para el cálculo de corriente
        if unidad == "A":
            # Ocultar campos de factor de potencia y eficiencia para corriente
            # pero mantenerlos para información
            pass
        else:
            # Mostrar todos los campos normalmente
            pass

    def convertir_a_watts(self, valor, unidad, voltaje, tipo_circuito, factor_potencia=None):
        """Convierte diferentes unidades a watts"""
        try:
            valor = float(valor)
            
            if unidad == "W":
                return valor
            elif unidad == "kW":
                return valor * 1000
            elif unidad == "HP":
                return valor * 746  # 1 HP = 746 W
            elif unidad == "kVA":
                # kVA a W: P = S × cos φ
                if factor_potencia is None:
                    factor_potencia = float(self.fp_var.get())
                return valor * 1000 * factor_potencia
            elif unidad == "A":
                # Amperios a W: P = V × I × cos φ (monofásico) o P = √3 × V × I × cos φ (trifásico)
                if factor_potencia is None:
                    factor_potencia = float(self.fp_var.get())
                if tipo_circuito == "monofasico":
                    return voltaje * valor * factor_potencia
                else:  # trifásico
                    return math.sqrt(3) * voltaje * valor * factor_potencia
            else:
                raise ValueError(f"Unidad {unidad} no reconocida")
                
        except ValueError as e:
            raise ValueError(f"Error en conversión de unidades: {str(e)}")

    def obtener_corriente_directa(self, valor, unidad):
        """Si la unidad es Amperios, devuelve directamente la corriente"""
        if unidad == "A":
            return float(valor)
        return None
        """Actualiza automáticamente factor de potencia y eficiencia según el tipo de equipo"""
        tipo = self.tipo_equipo_var.get()
        
        factores = {
            "Motor pequeño (<1 HP)": {"fp": "0.80", "eficiencia": "0.82"},
            "Motor mediano (1-10 HP)": {"fp": "0.87", "eficiencia": "0.88"},
            "Motor grande (>10 HP)": {"fp": "0.92", "eficiencia": "0.92"},
            "Iluminación incandescente": {"fp": "1.0", "eficiencia": "0.95"},
            "Iluminación fluorescente": {"fp": "0.90", "eficiencia": "0.85"},
            "Iluminación LED": {"fp": "0.95", "eficiencia": "0.90"},
            "Cargas resistivas": {"fp": "1.0", "eficiencia": "1.0"},
            "UPS/Rectificadores": {"fp": "0.85", "eficiencia": "0.88"}
        }
        
        if tipo in factores:
            self.fp_var.set(factores[tipo]["fp"])
            self.eficiencia_var.set(factores[tipo]["eficiencia"])

    def calcular_corriente(self, potencia, voltaje, tipo_circuito, factor_potencia, eficiencia):
        """Calcula la corriente basada en potencia y factores"""
        if tipo_circuito == "monofasico":
            corriente = potencia / (voltaje * factor_potencia * eficiencia)
        else:  # trifasico
            corriente = potencia / (math.sqrt(3) * voltaje * factor_potencia * eficiencia)
        
        return corriente
    
    def calcular(self):
        try:
            # Obtener valores básicos
            tipo_circuito = self.tipo_circuito_var.get()
            tipo_carga = self.tipo_carga_var.get()
            valor_potencia = self.potencia_var.get().strip()
            unidad_potencia = self.unidad_potencia_var.get()
            voltaje = float(self.voltaje_var.get())
            calibre = self.calibre_var.get()
            material = self.material_var.get()
            longitud = float(self.longitud_var.get())
            num_conductores = int(self.num_conductores_var.get())
            canalizacion = self.canalizacion_var.get()
            tipo_equipo = self.tipo_equipo_var.get()
            
            # Validar campos vacíos
            if not all([calibre, valor_potencia, self.voltaje_var.get(), 
                       self.longitud_var.get(), self.num_conductores_var.get()]):
                messagebox.showerror("Error", "Por favor, complete todos los campos.")
                return
            
            # Obtener factores
            factor_potencia = float(self.fp_var.get()) if self.fp_var.get() else 0.9
            eficiencia = float(self.eficiencia_var.get()) if self.eficiencia_var.get() else 0.9
            
            # Validar rangos de factores
            if not (0.1 <= factor_potencia <= 1.0):
                messagebox.showerror("Error", "Factor de potencia debe estar entre 0.1 y 1.0")
                return
            if not (0.1 <= eficiencia <= 1.0):
                messagebox.showerror("Error", "Eficiencia debe estar entre 0.1 y 1.0")
                return
            
            # Determinar cómo calcular la corriente
            corriente_directa = self.obtener_corriente_directa(valor_potencia, unidad_potencia)
            
            if corriente_directa is not None:
                # Si ingresó amperios directamente
                corriente = corriente_directa
                potencia_watts = self.convertir_a_watts(valor_potencia, "A", voltaje, tipo_circuito, factor_potencia)
                
                if tipo_circuito == "monofasico":
                    formula_corriente = f"Corriente ingresada directamente: I = {corriente} A"
                    calculo_corriente = f"Potencia calculada: P = V × I × cos φ = {voltaje} × {corriente} × {factor_potencia} = {potencia_watts:.0f} W"
                else:
                    formula_corriente = f"Corriente ingresada directamente: I = {corriente} A"
                    calculo_corriente = f"Potencia calculada: P = √3 × V × I × cos φ = √3 × {voltaje} × {corriente} × {factor_potencia} = {potencia_watts:.0f} W"
                    
                info_conversion = f"Entrada: {valor_potencia} A → Corriente: {corriente} A"
                
            else:
                # Convertir a watts y calcular corriente
                potencia_watts = self.convertir_a_watts(valor_potencia, unidad_potencia, voltaje, tipo_circuito, factor_potencia)
                corriente = self.calcular_corriente(potencia_watts, voltaje, tipo_circuito, factor_potencia, eficiencia)
                
                # Información de conversión
                if unidad_potencia == "W":
                    info_conversion = f"Entrada: {valor_potencia} W"
                elif unidad_potencia == "kW":
                    info_conversion = f"Entrada: {valor_potencia} kW → {potencia_watts:.0f} W"
                elif unidad_potencia == "HP":
                    info_conversion = f"Entrada: {valor_potencia} HP → {potencia_watts:.0f} W ({float(valor_potencia)} × 746)"
                elif unidad_potencia == "kVA":
                    info_conversion = f"Entrada: {valor_potencia} kVA → {potencia_watts:.0f} W ({float(valor_potencia)} × 1000 × {factor_potencia})"
                
                # Fórmulas de cálculo
                if tipo_circuito == "monofasico":
                    formula_corriente = f"Monofásico: I = P / (V × cos φ × η)"
                    calculo_corriente = f"I = {potencia_watts:.0f} / ({voltaje} × {factor_potencia} × {eficiencia}) = {corriente:.2f} A"
                else:
                    formula_corriente = f"Trifásico: I = P / (√3 × V × cos φ × η)"
                    calculo_corriente = f"I = {potencia_watts:.0f} / (√3 × {voltaje} × {factor_potencia} × {eficiencia}) = {corriente:.2f} A"
            
            # Determinar la tabla a usar
            tabla = self.impedancia_cobre if material == "cobre" else self.impedancia_aluminio
            
            # Validar calibre en tabla
            if calibre not in tabla[canalizacion]:
                messagebox.showerror("Error", f"Calibre {calibre} no encontrado para {material.capitalize()}.")
                return
            
            # Obtener impedancia
            z = tabla[canalizacion][calibre]
            
            # Cálculo de caída de tensión
            if tipo_circuito == "monofasico":
                caida_v = (2 * z * corriente * longitud / 1000) / num_conductores
                formula_caida = f"Monofásico: ΔV = (2 × Z × I × L / 1000) / n"
                calculo_caida = f"ΔV = (2 × {z} × {corriente:.2f} × {longitud} / 1000) / {num_conductores}"
            else:
                caida_v = (math.sqrt(3) * z * corriente * longitud / 1000) / num_conductores
                formula_caida = f"Trifásico: ΔV = (√3 × Z × I × L / 1000) / n"
                calculo_caida = f"ΔV = (√3 × {z} × {corriente:.2f} × {longitud} / 1000) / {num_conductores}"
            
            caida_p = (caida_v / voltaje) * 100
            
            # Agregar al historial
            self.agregar_historial(tipo_circuito, valor_potencia, unidad_potencia, potencia_watts, 
                                 corriente, voltaje, calibre, material, longitud, num_conductores, 
                                 canalizacion, z, factor_potencia, eficiencia, tipo_equipo, 
                                 info_conversion, formula_corriente, calculo_corriente,
                                 formula_caida, calculo_caida, caida_v, caida_p)
            
            # Mostrar resultados
            self.mostrar_resultados(caida_p, caida_v, tipo_carga, valor_potencia, unidad_potencia,
                                  potencia_watts, corriente, voltaje, calibre, material, longitud, 
                                  num_conductores, canalizacion, tipo_circuito, z, factor_potencia, 
                                  eficiencia, tipo_equipo, info_conversion, formula_corriente, 
                                  calculo_corriente, formula_caida, calculo_caida)
            
        except ValueError as e:
            messagebox.showerror("Error", f"Error en valores ingresados: {str(e)}")
        except Exception as e:
            messagebox.showerror("Error", f"Error en el cálculo: {str(e)}")
    
    def mostrar_resultados(self, caida_p, caida_v, tipo_carga, valor_potencia, unidad_potencia,
                          potencia_watts, corriente, voltaje, calibre, material, longitud, 
                          num_conductores, canalizacion, tipo_circuito, z, factor_potencia, 
                          eficiencia, tipo_equipo, info_conversion, formula_corriente, 
                          calculo_corriente, formula_caida, calculo_caida):
        # Limpiar texto anterior
        self.resultado_text.config(state='normal')
        self.resultado_text.delete('1.0', tk.END)
        
        # Formatear resultados
        resultado = f"RESULTADOS DEL CÁLCULO\n"
        resultado += "=" * 60 + "\n\n"
        
        resultado += f"CONVERSIÓN DE UNIDADES:\n"
        resultado += f"{info_conversion}\n"
        if unidad_potencia != "A":
            resultado += f"Potencia en watts: {potencia_watts:.0f} W\n"
        resultado += "\n"
        
        resultado += f"CÁLCULO DE CORRIENTE:\n"
        resultado += f"Equipo: {tipo_equipo}\n"
        resultado += f"Fórmula aplicada: {formula_corriente}\n"
        resultado += f"Cálculo: {calculo_corriente}\n\n"
        
        resultado += f"PARÁMETROS DE ENTRADA:\n"
        resultado += f"• Tipo de circuito: {tipo_circuito.capitalize()}\n"
        resultado += f"• Tipo de carga: {tipo_carga.capitalize()}\n"
        resultado += f"• Potencia ingresada: {valor_potencia} {unidad_potencia}\n"
        if unidad_potencia != "A":
            resultado += f"• Potencia en watts: {potencia_watts:.0f} W\n"
            resultado += f"• Factor de potencia: {factor_potencia}\n"
            resultado += f"• Eficiencia: {eficiencia}\n"
        resultado += f"• Corriente calculada: {corriente:.2f} A\n"
        resultado += f"• Tensión nominal: {voltaje} V\n"
        resultado += f"• Calibre: {calibre}\n"
        resultado += f"• Material: {material.capitalize()}\n"
        resultado += f"• Longitud: {longitud} m\n"
        resultado += f"• Conductores por fase: {num_conductores}\n"
        resultado += f"• Canalización: {canalizacion}\n"
        resultado += f"• Impedancia (Z): {z} Ω/km\n\n"
        
        resultado += f"CÁLCULO DE CAÍDA DE TENSIÓN:\n"
        resultado += f"Fórmula aplicada: {formula_caida}\n"
        resultado += f"Cálculo: {calculo_caida}\n"
        resultado += f"ΔV = {caida_v:.4f} volts\n\n"
        
        resultado += f"RESULTADO PRINCIPAL:\n"
        resultado += f"Caída de tensión: {caida_p:.2f}% ({caida_v:.2f} volts)\n\n"
        
        resultado += "EVALUACIÓN NORMATIVA:\n"
        if tipo_carga == "alimentador" and caida_p <= 2:
            resultado += "✓ CUMPLE: La caída de voltaje está por debajo del 2%\n"
            resultado += "Permitido según artículos 210-19 Nota 4 y 215-2 Nota 2\n"
            resultado += "de la NOM-001-SEDE-2012."
        elif tipo_carga == "derivado" and caida_p <= 3:
            resultado += "✓ CUMPLE: La caída de voltaje está por debajo del 3%\n"
            resultado += "Permitido según artículos 210-19 Nota 4 y 215-2 Nota 2\n"
            resultado += "de la NOM-001-SEDE-2012."
        else:
            resultado += "✗ NO CUMPLE: La caída de voltaje excede lo permitido\n"
            resultado += "según artículos 210-19 Nota 4 y 215-2 Nota 2\n"
            resultado += "de la NOM-001-SEDE-2012.\n\n"
            if tipo_carga == "alimentador":
                resultado += "REQUERIMIENTO: Máximo 2% para alimentadores.\n"
                resultado += f"EXCESO: {caida_p - 2:.2f}%"
            else:
                resultado += "REQUERIMIENTO: Máximo 3% para circuitos derivados.\n"
                resultado += f"EXCESO: {caida_p - 3:.2f}%"
        
        self.resultado_text.insert('1.0', resultado)
        self.resultado_text.config(state='disabled')
    
    def agregar_historial(self, tipo_circuito, valor_potencia, unidad_potencia, potencia_watts, 
                         corriente, voltaje, calibre, material, longitud, num_conductores, 
                         canalizacion, z, factor_potencia, eficiencia, tipo_equipo, 
                         info_conversion, formula_corriente, calculo_corriente,
                         formula_caida, calculo_caida, caida_v, caida_p):
        
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        entrada_historial = {
            'timestamp': timestamp,
            'tipo_circuito': tipo_circuito,
            'valor_potencia': valor_potencia,
            'unidad_potencia': unidad_potencia,
            'potencia_watts': potencia_watts,
            'corriente': corriente,
            'voltaje': voltaje,
            'calibre': calibre,
            'material': material,
            'longitud': longitud,
            'num_conductores': num_conductores,
            'canalizacion': canalizacion,
            'z': z,
            'factor_potencia': factor_potencia,
            'eficiencia': eficiencia,
            'tipo_equipo': tipo_equipo,
            'info_conversion': info_conversion,
            'formula_corriente': formula_corriente,
            'calculo_corriente': calculo_corriente,
            'formula_caida': formula_caida,
            'calculo_caida': calculo_caida,
            'caida_v': caida_v,
            'caida_p': caida_p
        }
        
        self.historial.append(entrada_historial)
        self.actualizar_historial()
    def actualizar_historial(self):
        self.historial_text.config(state='normal')
        self.historial_text.delete('1.0', tk.END)
        
        historial_texto = "HISTORIAL DE CÁLCULOS Y FÓRMULAS APLICADAS\n"
        historial_texto += "=" * 80 + "\n\n"
        
        for i, entrada in enumerate(reversed(self.historial[-10:]), 1):  # Mostrar últimos 10
            historial_texto += f"CÁLCULO #{len(self.historial) - i + 1} - {entrada['timestamp']}\n"
            historial_texto += "-" * 50 + "\n"
            
            historial_texto += f"EQUIPO: {entrada['tipo_equipo']}\n"
            historial_texto += f"ENTRADA: {entrada['valor_potencia']} {entrada['unidad_potencia']}\n"
            historial_texto += f"CONVERSIÓN: {entrada['info_conversion']}\n"
            historial_texto += f"DATOS: {entrada['tipo_circuito'].capitalize()}, "
            
            if entrada['unidad_potencia'] != "A":
                historial_texto += f"P={entrada['potencia_watts']:.0f}W, "
                historial_texto += f"cos φ={entrada['factor_potencia']}, η={entrada['eficiencia']}, "
            
            historial_texto += f"V={entrada['voltaje']}V, "
            historial_texto += f"Cal.{entrada['calibre']}, {entrada['material'].capitalize()}, "
            historial_texto += f"L={entrada['longitud']}m\n\n"
            
            historial_texto += f"CÁLCULO DE CORRIENTE:\n"
            historial_texto += f"FÓRMULA: {entrada['formula_corriente']}\n"
            historial_texto += f"SUSTITUCIÓN: {entrada['calculo_corriente']}\n"
            historial_texto += f"RESULTADO: I = {entrada['corriente']:.2f} A\n\n"
            
            historial_texto += f"IMPEDANCIA: Z = {entrada['z']} Ω/km ({entrada['material'].capitalize()}, {entrada['canalizacion']})\n\n"
            
            historial_texto += f"CÁLCULO DE CAÍDA DE TENSIÓN:\n"
            historial_texto += f"FÓRMULA: {entrada['formula_caida']}\n"
            historial_texto += f"Donde: Z=Impedancia, I=Corriente, L=Longitud, n=Conductores por fase\n"
            historial_texto += f"SUSTITUCIÓN: {entrada['calculo_caida']}\n"
            historial_texto += f"ΔV = {entrada['caida_v']:.4f} volts\n\n"
            
            historial_texto += f"PORCENTAJE: %ΔV = (ΔV / V_nominal) × 100\n"
            historial_texto += f"%ΔV = ({entrada['caida_v']:.4f} / {entrada['voltaje']}) × 100 = {entrada['caida_p']:.2f}%\n"
            
            historial_texto += "\n"
        
        if len(self.historial) > 10:
            historial_texto += f"... y {len(self.historial) - 10} cálculos anteriores\n"
        
        # Información adicional sobre las fórmulas
        historial_texto += "\n" + "=" * 80 + "\n"
        historial_texto += "INFORMACIÓN SOBRE LAS FÓRMULAS Y CONVERSIONES:\n\n"
        
        historial_texto += "CONVERSIONES DE UNIDADES:\n"
        historial_texto += "• W → W: Directo\n"
        historial_texto += "• kW → W: kW × 1000\n"
        historial_texto += "• HP → W: HP × 746\n"
        historial_texto += "• kVA → W: kVA × 1000 × cos φ\n"
        historial_texto += "• A → W: V × I × cos φ (monofásico) o √3 × V × I × cos φ (trifásico)\n\n"
        
        historial_texto += "CÁLCULO DE CORRIENTE:\n"
        historial_texto += "MONOFÁSICO: I = P / (V × cos φ × η)\n"
        historial_texto += "TRIFÁSICO: I = P / (√3 × V × cos φ × η)\n"
        historial_texto += "NOTA: Si ingresa amperios directamente, no se aplican estas fórmulas\n\n"
        
        historial_texto += "CAÍDA DE TENSIÓN:\n"
        historial_texto += "MONOFÁSICO: ΔV = (2 × Z × I × L / 1000) / n\n"
        historial_texto += "El factor 2 considera ida y vuelta de la corriente\n"
        historial_texto += "TRIFÁSICO: ΔV = (√3 × Z × I × L / 1000) / n\n"
        historial_texto += "√3 ≈ 1.732 (factor para sistemas trifásicos balanceados)\n\n"
        
        historial_texto += "VARIABLES:\n"
        historial_texto += "• P: Potencia del equipo (W)\n"
        historial_texto += "• V: Tensión nominal (V)\n"
        historial_texto += "• cos φ: Factor de potencia\n"
        historial_texto += "• η: Eficiencia del equipo\n"
        historial_texto += "• I: Corriente calculada (A)\n"
        historial_texto += "• Z: Impedancia del conductor (Ω/km)\n"
        historial_texto += "• L: Longitud del circuito (m)\n"
        historial_texto += "• n: Número de conductores en paralelo por fase\n"
        historial_texto += "• 1000: Factor de conversión de m a km\n\n"
        
        historial_texto += "FACTORES TÍPICOS SEGÚN NOM-001-SEDE-2012:\n"
        historial_texto += "• Motores pequeños (<1 HP): cos φ=0.80, η=0.82\n"
        historial_texto += "• Motores medianos (1-10 HP): cos φ=0.87, η=0.88\n"
        historial_texto += "• Motores grandes (>10 HP): cos φ=0.92, η=0.92\n"
        historial_texto += "• Iluminación LED: cos φ=0.95, η=0.90\n"
        historial_texto += "• Cargas resistivas: cos φ=1.0, η=1.0\n\n"
        
        historial_texto += "EQUIVALENCIAS ÚTILES:\n"
        historial_texto += "• 1 HP = 746 W\n"
        historial_texto += "• 1 kVA = 1000 VA\n"
        historial_texto += "• P (W) = S (VA) × cos φ\n"
        historial_texto += "• S (VA) = V × I (monofásico) o √3 × V × I (trifásico)\n"
        
        self.historial_text.insert('1.0', historial_texto)
        self.historial_text.config(state='disabled')
        # Scroll al inicio
        self.historial_text.see('1.0')
    
    def limpiar_campos(self):
        self.potencia_var.set("")
        self.unidad_potencia_var.set("W")
        self.voltaje_var.set("")
        self.fp_var.set("0.87")
        self.eficiencia_var.set("0.88")
        self.calibre_var.set("")
        self.longitud_var.set("")
        self.num_conductores_var.set("1")
        self.tipo_circuito_var.set("monofasico")
        self.tipo_carga_var.set("derivado")
        self.material_var.set("cobre")
        self.canalizacion_var.set("PVC")
        self.tipo_equipo_var.set("Motor mediano (1-10 HP)")
        
        self.resultado_text.config(state='normal')
        self.resultado_text.delete('1.0', tk.END)
        self.resultado_text.config(state='disabled')
    
    def limpiar_historial(self):
        self.historial.clear()
        self.historial_text.config(state='normal')
        self.historial_text.delete('1.0', tk.END)
        self.historial_text.insert('1.0', "Historial limpiado.\n\nRealice un cálculo para ver las fórmulas aplicadas.")
        self.historial_text.config(state='disabled')

if __name__ == "__main__":
    root = tk.Tk()
    app = CalculadoraCaidaTension(root)
    root.mainloop()