import tkinter as tk
from tkinter import ttk, messagebox
import math
from exportador import exportar_resultado_pdf

class VentanaCalculos:
    def __init__(self, master):
        self.ventana = tk.Toplevel(master)
        self.ventana.title("Sistema de Cálculo Eléctrico - NOM-001-SEDE-2012")
        self.ventana.geometry("1100x700")
        self.ventana.configure(bg="#f0f0f0")
        self.tipo_var = tk.StringVar(value="motor")
        self.entradas = {}
        self.resultados = {}

        self.panel_entrada = tk.LabelFrame(self.ventana, text="📋 Entrada de datos", font=("Century Gothic", 10, "bold"), padx=10, pady=10)
        self.panel_entrada.place(x=10, y=10, width=300, height=670)

        self.panel_resultados = tk.LabelFrame(self.ventana, text="📊 Resultados", font=("Century Gothic", 10, "bold"))
        self.panel_resultados.place(x=320, y=10, width=400, height=500)

        self.panel_historial = tk.LabelFrame(self.ventana, text="📁 Historial de cálculos", font=("Century Gothic", 10, "bold"))
        self.panel_historial.place(x=320, y=520, width=400, height=160)

        self.resultado_text = tk.Text(self.panel_resultados, height=30, width=50, state="disabled")
        self.resultado_text.pack(pady=10)

        self.frame_validaciones = ttk.Frame(self.panel_entrada)
        self.frame_validaciones.pack(pady=10, fill="x")

        self._crear_contenido()


    def actualizar_material(self, event=None):
        seleccion = self.canalizacion_var.get()
        if "PVC" in seleccion:
            self.material = "PVC"
        elif "PGG" in seleccion:
            self.material = "ACERO"
        elif "Charola" in seleccion:
            self.material = "ALUMINIO"
        else:
            self.material = "PVC"

    def _crear_contenido(self):
        ttk.Label(self.panel_entrada, text="Tipo de carga:").pack()
        opciones = ["motor", "transformador", "potencia_kw", "interruptor"]
        tk.OptionMenu(self.panel_entrada, self.tipo_var, *opciones, command=self.mostrar_campos).pack()

        self.frame_campos = ttk.Frame(self.panel_entrada)
        self.frame_campos.pack(pady=5, fill="x")

        ttk.Button(self.panel_entrada, text="Calcular", command=self.calcular_corriente).pack(pady=10)
        ttk.Button(self.panel_historial, text="Exportar PDF", command=self.exportar_pdf).pack(pady=5)

        self.mostrar_campos(self.tipo_var.get())

    def mostrar_campos(self, tipo):
        for widget in self.frame_campos.winfo_children():
            widget.destroy()
        self.entradas.clear()

        campos = {
            "motor": [("HP", "hp"), ("Voltaje (V)", "voltaje"), ("Eficiencia (0-1)", "eficiencia"), ("Factor de potencia", "fp")],
            "transformador": [("Potencia (kVA)", "potencia"), ("Voltaje (V)", "voltaje")],
            "potencia_kw": [("Potencia (kW)", "potencia"), ("Voltaje (V)", "voltaje"), ("Factor de potencia", "fp")],
            "interruptor": [("Corriente (A)", "corriente")],
        }

        for texto, clave in campos[tipo]:
            ttk.Label(self.frame_campos, text=texto).pack(anchor="w")
            entry = ttk.Entry(self.frame_campos)
            entry.pack(fill="x")
            self.entradas[clave] = entry

        adicionales = [("Longitud (m)", "longitud")]
        for texto, clave in adicionales:
            ttk.Label(self.frame_campos, text=texto).pack(anchor="w")
            entry = ttk.Entry(self.frame_campos)
            entry.pack(fill="x")
            self.entradas[clave] = entry

        ttk.Label(self.frame_campos, text="Canalización").pack(anchor="w")
        self.canalizacion_var = tk.StringVar(value="Tubería PVC tipo pesado")
        canal_menu = ttk.Combobox(self.frame_campos, textvariable=self.canalizacion_var, values=["Tubería PVC tipo pesado", "Tubería Conduit PGG", "Charola Tipo Escalera"], state="readonly")
        canal_menu.pack(fill="x")
        canal_menu.bind("<<ComboboxSelected>>", self.actualizar_material)
        self.entradas["canalizacion"] = self.canalizacion_var

        ttk.Label(self.frame_campos, text="Circuito (monofásico/trifásico)").pack(anchor="w")
        self.circuito_var = tk.StringVar(value="trifasico")
        circuito_menu = ttk.Combobox(self.frame_campos, textvariable=self.circuito_var, values=["monofasico", "trifasico"], state="readonly")
        circuito_menu.pack(fill="x")
        self.entradas["circuito"] = self.circuito_var

    def calcular_caida_tension(self, corriente, longitud, calibre, voltaje, factor_correccion=1.0):
        resistencias = {
            "14": 0.0059, "12": 0.0039, "10": 0.00328, "8": 0.00208, "6": 0.00131,
            "4": 0.00082, "3": 0.00065, "2": 0.00052, "1": 0.00041,
            "1/0": 0.00033, "2/0": 0.00026, "3/0": 0.00021, "4/0": 0.00017,
            "250": 0.00014, "300": 0.00012, "350": 0.00011, "400": 0.00010,
            "500": 0.00008, "600": 0.00007
        }
        r = resistencias.get(calibre, 0.00328)
        distancia_total = longitud * 2
        caida_v = math.sqrt(3) * corriente * r * distancia_total * factor_correccion
        porcentaje = (caida_v / voltaje) * 100
        return caida_v, porcentaje
    def calcular_corriente(self):
        try:
            for widget in self.frame_validaciones.winfo_children():
                widget.destroy()

            self.actualizar_material()

            tipo = self.tipo_var.get()
            valores = {k: e.get().strip() for k, e in self.entradas.items()}
            if any(v == '' for v in valores.values()):
                raise ValueError("Faltan datos obligatorios.")

            voltaje = float(valores.get("voltaje", 220))
            longitud = float(valores["longitud"])
            corriente = 0

            if tipo == "motor":
                hp = float(valores["hp"])
                eficiencia = float(valores["eficiencia"])
                fp = float(valores["fp"])
                kw = hp * 0.746
                corriente = (kw * 1000) / (math.sqrt(3) * voltaje * eficiencia * fp)
                corriente_corregida = corriente * (1.1 if fp == 0.9 else 1.25)
            elif tipo == "transformador":
                kva = float(valores["potencia"])
                circuito = valores["circuito"].lower()
                corriente = (kva * 1000) / (voltaje if circuito == "monofasico" else math.sqrt(3) * voltaje)
                corriente_corregida = corriente * 1.25
            elif tipo == "potencia_kw":
                kw = float(valores["potencia"])
                fp = float(valores["fp"])
                corriente = (kw * 1000) / (math.sqrt(3) * voltaje * fp)
                corriente_corregida = corriente
            elif tipo == "interruptor":
                corriente = float(valores["corriente"])
                corriente_corregida = corriente

            interruptor = self.seleccionar_interruptor(corriente_corregida)
            calibre_sugerido = self.seleccionar_calibre(corriente_corregida, voltaje, longitud)

            caida_v, caida_pct = self.calcular_caida_tension(corriente_corregida, longitud, calibre_sugerido, voltaje)

            self.resultados = {
                "Tipo carga": tipo,
                "Voltaje": voltaje,
                "Corriente": f"{corriente:.2f} A",
                "Corriente corregida": f"{corriente_corregida:.2f} A",
                "Interruptor": f"{interruptor} A",
                "Calibre recomendado": calibre_sugerido,
                "Canalización": self.material,
                "Caída de tensión": f"{caida_v:.2f} V ({caida_pct:.2f}%)"
            }
            self.mostrar_resultados()

            if self.material == "ALUMINIO":
                self.mostrar_validaciones(tipo="charola")
            else:
                self.mostrar_validaciones(tipo="tuberia")

        except Exception as e:
            messagebox.showerror("Error", f"Verifica los datos ingresados.\n{e}")

    def seleccionar_calibre(self, corriente, voltaje, longitud):
        tabla = {
            "14": 15, "12": 20, "10": 30, "8": 40, "6": 55, "4": 70,
            "3": 85, "2": 95, "1": 110, "1/0": 125, "2/0": 145, "3/0": 165,
            "4/0": 195, "250": 215, "300": 240, "350": 260, "400": 280,
            "500": 320, "600": 355
        }
        factor_ajuste = 0.88  # Ejemplo por temperatura/agrupamiento
        for cal, amp in tabla.items():
            if corriente <= amp * factor_ajuste:
                caida_v, caida_pct = self.calcular_caida_tension(corriente, longitud, cal, voltaje)
                if caida_pct <= 5:
                    return cal
        return max(tabla.keys(), key=lambda x: tabla[x])


    def seleccionar_interruptor(self, corriente):
        valores = [15, 20, 30, 40, 50, 60, 70, 80, 90, 100, 125, 150, 175, 200]
        for val in valores:
            if corriente <= val:
                return val
        return valores[-1]
    
    def mostrar_resultados(self):
        self.resultado_text.configure(state="normal")
        self.resultado_text.delete("1.0", tk.END)
        for k, v in self.resultados.items():
            self.resultado_text.insert(tk.END, f"{k}: {v}\n")

        self.resultado_text.insert(tk.END, "\n📌 Observaciones según NOM-001-SEDE-2012:\n")
        if "Caída de tensión" in self.resultados:
            caida_pct = float(self.resultados["Caída de tensión"].split("(")[1].replace("%)", "").replace("%", "").strip())
            if caida_pct > 5:
                self.resultado_text.insert(tk.END, f"❌ Caída de tensión superior al 5% permitido ({caida_pct:.2f}%)\n")
            else:
                self.resultado_text.insert(tk.END, f"✅ Caída de tensión dentro del límite permitido ({caida_pct:.2f}%)\n")
        self.resultado_text.insert(tk.END, "🔎 Verifica la caída de tensión: < 5% según Art. 215 y 220.\n")
        self.resultado_text.configure(state="disabled")


    def mostrar_validaciones(self, tipo="tuberia"):
        for widget in self.frame_validaciones.winfo_children():
            widget.destroy()

        ttk.Label(self.frame_validaciones, text="Número de hilos por fase:").pack()
        self.entry_hilos = ttk.Entry(self.frame_validaciones)
        self.entry_hilos.pack()

        if tipo == "charola":
            ttk.Label(self.frame_validaciones, text="Ancho de charola (mm):").pack()
            self.ancho_charola_entry = ttk.Entry(self.frame_validaciones)
            self.ancho_charola_entry.pack()
        elif tipo == "tuberia":
            ttk.Label(self.frame_validaciones, text="Diámetro de la tubería (pulgadas):").pack()
            self.diametro_tuberia_entry = ttk.Entry(self.frame_validaciones)
            self.diametro_tuberia_entry.pack()

        self.boton_validar = ttk.Button(self.frame_validaciones, text="Validar Charola o Tubería", command=lambda: self.validar_espacios(tipo))
        self.boton_validar.pack(pady=10)

       
    def obtener_area_conductor(self, calibre):
        tabla_areas = {
            "12": 3.31, "10": 5.26, "8": 8.37, "6": 13.3, "4": 21.2, "2": 33.6,
            "1/0": 55.3, "2/0": 64.8, "3/0": 73.9, "4/0": 84.7,
            "250": 95.0, "300": 109.0, "350": 122.6, "400": 133.4,
            "500": 158.0, "600": 185.0, "750": 221.0, "1000": 253.0
        }
        return tabla_areas.get(str(calibre), 0)

    def validar_espacios(self, tipo="tuberia"):
        try:
            calibre = str(self.resultados["Calibre recomendado"]).strip()
            hilos = int(self.entry_hilos.get())
            mensaje = ""

            if tipo == "charola":
                ancho_charola = float(self.ancho_charola_entry.get())
                requerido = hilos * 10
                mensaje += "\u2705 Charola adecuada\n" if ancho_charola >= requerido else f"❌ Charola insuficiente: requiere {requerido} mm\n"

            elif tipo == "tuberia":
                diametro_pulgadas = float(self.diametro_tuberia_entry.get())
                diametro_mm = diametro_pulgadas * 25.4
                area_total = math.pi * (diametro_mm / 2) ** 2
                limite_ocupacion = area_total * 0.40

                area_conductor = self.obtener_area_conductor(calibre)
                area_ocupada = area_conductor * hilos

                mensaje += f"\nÁrea de la tubería (100%): {area_total:.1f} mm²\n"
                mensaje += f"Ocupación permitida (40%): {limite_ocupacion:.1f} mm²\n"
                mensaje += f"Área ocupada por conductores: {area_ocupada:.1f} mm²\n"

                if area_ocupada <= limite_ocupacion:
                    mensaje += "✅ Tubería adecuada\n"
                else:
                    area_necesaria = (area_ocupada * 100) / 40
                    diametro_necesario = 2 * math.sqrt(area_necesaria / math.pi)
                    pulgadas_necesarias = diametro_necesario / 25.4
                    mensaje += "❌ Tubería insuficiente\n"
                    mensaje += f"Área requerida al 100%: {area_necesaria:.1f} mm²\n"
                    mensaje += f"Diámetro mínimo requerido: {diametro_necesario:.1f} mm ({pulgadas_necesarias:.2f} pulgadas)\n"

            self.resultado_text.configure(state="normal")
            self.resultado_text.insert(tk.END, "\n" + mensaje)
            self.resultado_text.configure(state="disabled")

        except Exception as e:
            messagebox.showerror("Error", f"Error en validaciones: {e}")

    def exportar_pdf(self):
        if not self.resultados:
            messagebox.showwarning("Advertencia", "Realiza primero un cálculo.")
            return
        try:
            exportar_resultado_pdf(self.resultados, nombre_archivo="memoria_calculo.pdf", usuario="Usuario Demo", proyecto="Proyecto Residencia")
            messagebox.showinfo("Éxito", "PDF generado correctamente.")
        except Exception as e:
            messagebox.showerror("Error al exportar", str(e))
