import streamlit as st
import pandas as pd
from datetime import datetime
# ---------------------- CONFIGURACIÓN DE LA PÁGINA ----------------------
st.set_page_config(
     page_title="Sistema de Fidelización - Imagen Digital",
     page_icon="💳",
     layout="wide",
     initial_sidebar_state="expanded"
)
# ---------------------- TUS DATOS ORIGINALES (TAL CUAL LOS ESCRIBISTE) ----------------------
clientes_puntos = {
      "Juan Perez": 150,
      "Maria Lopez": 230,
      "Carlos Ruiz": 80,
      "Ana Gonzalez": 450,
      "Luis Martinez": 120,
      "Sofia Ramirez": 320,
      "Jorge Castro": 90,
      "Diana Morales": 500,
      "Kevin Flores": 200,
      "Laura Mendez": 180,
      "Pedro Jimenez": 75,
      "Carmen Rojas": 410,
      "Mario Torres": 290,
      "Paula Vega": 350,
      "Ricardo Soto": 60
}
clientes_datos = {
      "Juan Perez": {"tel": "8888-1111", "correo": "juan.p@email.com"},
      "Maria Lopez": {"tel": "8888-2222", "correo": "maria.l@email.com"},
      "Carlos Ruiz": {"tel": "8888-3333", "correo": "carlos.r@email.com"},
      "Ana Gonzalez": {"tel": "8888-4444", "correo": "ana.g@email.com"},
      "Luis Martinez": {"tel": "8888-5555", "correo": "luis.m@email.com"},
      "Sofia Ramirez": {"tel": "8888-6666", "correo": "sofia.r@email.com"},
      "Jorge Castro": {"tel": "8888-7777", "correo": "jorge.c@email.com"},
      "Diana Morales": {"tel": "8888-8888", "correo": "diana.m@email.com"},
      "Kevin Flores": {"tel": "8888-9999", "correo": "kevin.f@email.com"},
      "Laura Mendez": {"tel": "8877-1010", "correo": "laura.m@email.com"},
      "Pedro Jimenez": {"tel": "8877-2020", "correo": "pedro.j@email.com"},
      "Carmen Rojas": {"tel": "8877-3030", "correo": "carmen.r@email.com"},
      "Mario Torres": {"tel": "8877-4040", "correo": "mario.t@email.com"},
      "Paula Vega": {"tel": "8877-5050", "correo": "paula.v@email.com"},
      "Ricardo Soto": {"tel": "8877-6060", "correo": "ricardo.s@email.com"}
}
reglas_canjes = [
      (100, "Sesión Fotográfica Básica"),
      (200, "Álbum Digital Pequeño"),
      (300, "Sesión Familiar + Impresión")
]
lista_servicios = [
      "📸 Sesión Fotográfica Individual",
      "👨‍👩‍👧‍👦 Sesión Fotográfica Familiar",
      "🎓 Sesión de Graduación",
      "💍 Sesión Pre-Boda / Boda",
      "🎁 Artículos Personalizados (Tazas, Llaveros)",
      "👕 Uniformes Deportivos / Corporativos",
      "🖼️ Retablos y Cuadros Decorativos",
      "🖨️ Impresión de Fotos Alta Calidad",
      "📔 Elaboración de Álbumes Físicos",
      "🎞️ Edición y Retoque Digital"
]
historial_ventas = [
      ("Maria Lopez", "Sesión Familiar", "15/04/2026", "¢ 25,000"),
      ("Juan Perez", "Impresión 20 fotos", "18/04/2026", "¢ 8,500"),
      ("Ana Gonzalez", "Uniformes x 5", "20/04/2026", "¢ 12,000"),
      ("Sofia Ramirez", "Retablo Mediano", "22/04/2026", "¢ 15,000"),
      ("Carlos Ruiz", "Sesión Individual", "25/04/2026", "¢ 10,000"),
      ("Diana Morales", "Álbum Digital + Impreso", "26/04/2026", "¢ 35,000"),
      ("Luis Martinez", "Tazas Personalizadas x 6", "28/04/2026", "¢ 7,200"),
      ("Mario Torres", "Sesión Graduación", "29/04/2026", "¢ 18,000"),
      ("Paula Vega", "Cuadros Canvas", "30/04/2026", "¢ 9,500"),
      ("Kevin Flores", "Paquete Fiestas", "01/05/2026", "¢ 22,000")
]
def guardar_puntos():
      pass
# ---------------------- MENÚ LATERAL (IGUAL A TU DISEÑO) ----------------------
st.sidebar.markdown("""
     <div style="background-color:#2c3e50; padding:15px; border-radius:5px; text-align:center; margin-bottom:20px;">
         <h2 style="color:white; margin:0; font-size:18px;">MENÚ PRINCIPAL</h2>
     </div>
""", unsafe_allow_html=True)
opcion = st.sidebar.radio(
     label="",
     options=["Servicios", "Clientes", "Ventas", "Canjes de Puntos"],
     index=3,
     label_visibility="collapsed"
)
# Colores exactos de tus botones
colores = {
     "Servicios": "#3498db",
     "Clientes": "#2ecc71",
     "Ventas": "#e74c3c",
     "Canjes de Puntos": "#f39c12"
}
# ---------------------- PANTALLA SERVICIOS ----------------------
if opcion == "Servicios":
     st.markdown(f"""
         <div style="background-color:{colores['Servicios']}; padding:12px; border-radius:5px; margin-bottom:20px;">
             <h1 style="color:white; margin:0; font-size:22px; text-align:center;">📸 CATÁLOGO DE SERVICIOS</h1>
         </div>
     """, unsafe_allow_html=True)
     for servicio in lista_servicios:
         st.markdown(f"""
             <div style="background-color:#f8f9fa; color:#34495e; padding:12px 20px; margin:5px 50px; border-radius:3px; font-size:16px;">
                 {servicio}
             </div>
         """, unsafe_allow_html=True)
# ---------------------- PANTALLA CLIENTES ----------------------
elif opcion == "Clientes":
     st.markdown(f"""
         <div style="background-color:{colores['Clientes']}; padding:12px; border-radius:5px; margin-bottom:20px;">
             <h1 style="color:white; margin:0; font-size:22px; text-align:center;">👤 LISTADO DE CLIENTES</h1>
         </div>
     """, unsafe_allow_html=True)
     # Preparar datos para tabla
     datos_tabla = []
     for nombre, datos in clientes_datos.items():
         puntos = clientes_puntos.get(nombre, 0)
         datos_tabla.append({
             "Nombre Completo": nombre,
             "Teléfono": datos['tel'],
             "Correo Electrónico": datos['correo'],
             "Puntos Acumulados": puntos
         })
    
     df_clientes = pd.DataFrame(datos_tabla)
     st.dataframe(df_clientes, use_container_width=True, hide_index=True, height=400)
# ---------------------- PANTALLA VENTAS ----------------------
elif opcion == "Ventas":
     st.markdown(f"""
         <div style="background-color:{colores['Ventas']}; padding:12px; border-radius:5px; margin-bottom:20px;">
             <h1 style="color:white; margin:0; font-size:20px; text-align:center;">💳 HISTORIAL DE VENTAS - ABRIL 2026</h1>
         </div>
     """, unsafe_allow_html=True)
     # Tabla de ventas
     df_ventas = pd.DataFrame(
         historial_ventas,
         columns=["Cliente", "Descripción del Servicio", "Fecha", "Monto"]
     )
     st.dataframe(df_ventas, use_container_width=True, hide_index=True, height=400)
     # Cálculo total del mes (igual que tu código)
     total = sum([float(v[3].replace("¢ ","").replace(",","")) for v in historial_ventas])
     st.markdown(f"""
         <div style="text-align:center; font-size:18px; font-weight:bold; color:#27ae60; margin-top:15px;">
             📊 TOTAL DEL MES: ¢ {total:,.2f}
         </div>
     """, unsafe_allow_html=True)
# ---------------------- PANTALLA CANJES DE PUNTOS ----------------------
elif opcion == "Canjes de Puntos":
     st.markdown(f"""
         <div style="background-color:{colores['Canjes de Puntos']}; padding:12px; border-radius:5px; margin-bottom:20px;">
             <h1 style="color:white; margin:0; font-size:22px; text-align:center;">🎁 CANJES DE PUNTOS</h1>
         </div>
     """, unsafe_allow_html=True)
     # Sección consultar puntos
     st.markdown('<div style="background-color:#e8f5e9; padding:20px; border-radius:5px; margin:10px 30px;">', unsafe_allow_html=True)
    
     nombre_cliente = st.text_input("Nombre del Cliente:")
     puntos_mostrados = st.empty()
     if st.button("🔍 Consultar Puntos"):
         if nombre_cliente.strip() in clientes_puntos:
             pts = clientes_puntos[nombre_cliente.strip()]
             puntos_mostrados.success(f"✅ Tienes acumulados: {pts} puntos")
         else:
             puntos_mostrados.warning("⚠️ Atención: Cliente no encontrado")
     # Selección de premio
     st.markdown("<br><b>Selecciona el premio:</b>", unsafe_allow_html=True)
     premio_opciones = [f"{cantidad} puntos - {descripcion}" for cantidad, descripcion in reglas_canjes]
     premio_seleccionado_texto = st.radio("", premio_opciones, label_visibility="collapsed")
     # Botón canjear
     if st.button("✅ Canjear Premio", type="primary"):
         nombre = nombre_cliente.strip()
         if not nombre or nombre not in clientes_puntos:
             st.error("⚠️ Primero consulta un cliente válido")
         elif not premio_seleccionado_texto:
             st.error("⚠️ Selecciona un premio para canjear")
         else:
             puntos_necesarios = int(premio_seleccionado_texto.split(" ")[0])
             descripcion_premio = premio_seleccionado_texto.split(" - ",1)[1]
             puntos_actuales = clientes_puntos[nombre]
             if puntos_actuales >= puntos_necesarios:
                 clientes_puntos[nombre] -= puntos_necesarios
                 guardar_puntos()
                 st.success(f"""
                     🎉 ¡Canje Exitoso! 
                     Felicidades {nombre}! 
                     Has canjeado: {descripcion_premio} 
                     Se descontaron {puntos_necesarios} puntos. 
                     Te quedan: {clientes_puntos[nombre]} puntos.
                 """)
             else:
                 st.error(f"""
                     ❌ Puntos insuficientes 
                     Lo sentimos {nombre}, 
                     Necesitas {puntos_necesarios} puntos y solo tienes {puntos_actuales}. 
                     ¡Sigue acumulando!
                 """)
     st.markdown('</div>', unsafe_allow_html=True)
     # Reglas de premios
     st.markdown("""
         <div style="background-color:#eaf2f8; padding:15px; border-radius:5px; margin:20px 30px;">
             <h3 style="color:#2980b9; margin-top:0;">📋 Premios disponibles</h3>
     """, unsafe_allow_html=True)
     for i, (cantidad, premio) in enumerate(reglas_canjes):
         color = "#d6eaf8" if i % 2 == 0 else "#aed6f1"
         st.markdown(f"""
             <div style="background-color:{color}; color:#1a5276; padding:10px; border-radius:3px; margin:5px 0;">
                 {cantidad} puntos → {premio}
             </div>
         """, unsafe_allow_html=True)
    
     st.markdown("</div>", unsafe_allow_html=True) 
