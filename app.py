import streamlit as st
import pandas as pd
import json
from datetime import datetime

# ---------------------- CONFIGURACIÓN GENERAL ----------------------
st.set_page_config(page_title="Imagen Digital Studio", page_icon="📸", layout="wide")

# Colores personalizados
colores = {
    "Servicios": "#8e44ad",
    "Clientes": "#2980b9",
    "Ventas": "#27ae60",
    "Canjes de Puntos": "#f39c12",
    "Administración": "#e74c3c"
}

# ---------------------- ARCHIVO DE GUARDADO DE DATOS ----------------------
ARCHIVO_DATOS = "datos_estudio.json"

# Datos iniciales por si es la primera vez
datos_iniciales = {
    "servicios": [
        {"nombre": "Sesión Fotográfica Básica", "puntos": 10, "activo": True, "es_navidad": False},
        {"nombre": "Video de Evento", "puntos": 20, "activo": True, "es_navidad": False},
        {"nombre": "Fotografías Navideñas", "puntos": 15, "activo": True, "es_navidad": True}
    ],
    "clientes": {
        "Juan Pérez": {"puntos": 50, "activo": True},
        "María Gómez": {"puntos": 35, "activo": True}
    },
    "ventas": [],
    "reglas_canjes": [
        (20, "Sesión de fotos pequeña gratis"),
        (40, "Impresión de 5 fotos tamaño carta"),
        (60, "Sesión fotográfica completa")
    ],
    "usuarios": {
        "Dimerson": {"clave": "admin123", "rol": "administrador"},
        "Usuario": {"clave": "1234", "rol": "consulta"}
    }
}

# ---------------------- FUNCIONES PARA GUARDAR Y CARGAR DATOS ----------------------
def cargar_datos():
    try:
        with open(ARCHIVO_DATOS, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return datos_iniciales

def guardar_datos(datos):
    with open(ARCHIVO_DATOS, "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=4, ensure_ascii=False)

# Cargamos los datos
datos = cargar_datos()

# ---------------------- SISTEMA DE INICIO DE SESIÓN Y SEGURIDAD ----------------------
if "sesion_iniciada" not in st.session_state:
    st.session_state.sesion_iniciada = False
    st.session_state.usuario_actual = ""
    st.session_state.rol_actual = ""

# Si no ha iniciado sesión, mostramos la pantalla de login
if not st.session_state.sesion_iniciada:
    st.markdown("""
    <div style="text-align:center; padding:30px; background-color: #f8f9fa; border-radius:10px; margin: 20px;">
        <img src="https://i.imgur.com/7Z8X8yY.png" width="200" style="margin-bottom:20px;">
        <h1>🔒 INICIO DE SESIÓN</h1>
        <p style="color:#666;">Sistema de Gestión - Imagen Digital Studio</p>
    </div>
    """, unsafe_allow_html=True)
   
    usuario = st.text_input("Usuario")
    clave = st.text_input("Contraseña", type="password")
   
    if st.button("Ingresar", type="primary", use_container_width=True):
        if usuario in datos["usuarios"] and datos["usuarios"][usuario]["clave"] == clave:
            st.session_state.sesion_iniciada = True
            st.session_state.usuario_actual = usuario
            st.session_state.rol_actual = datos["usuarios"][usuario]["rol"]
            st.rerun()
        else:
            st.error("❌ Usuario o contraseña incorrectos")
   
    # Detenemos el código aquí hasta que inicie sesión
    st.stop()

# ---------------------- CABECERA CON LOGO E INFORMACIÓN DE CONTACTO ----------------------
st.markdown("""
<div style="text-align:center; margin-bottom:20px; padding:15px; background-color: #ffffff; border-radius:8px; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">
    <img src="https://i.imgur.com/7Z8X8yY.png" width="100" style="margin-bottom:10px;">
    <h1 style="margin:5px 0; color:#333;">IMAGEN DIGITAL STUDIO</h1>
    <p style="color:#666; font-size:15px;">Fotografía & Video | Calidad y profesionalismo</p>
   
    <!-- INFORMACIÓN DE CONTACTO COMPLETA -->
    <div style="margin-top:15px; padding:10px; background-color:#f8f9fa; border-radius:5px;">
        <p style="margin:5px 0; font-size:14px; color:#444;">
            📍 <strong>Dirección:</strong> Limón Centro, diagonal a la MUCAP
        </p>
        <p style="margin:5px 0; font-size:14px; color:#444;">
            📞 <strong>Teléfono:</strong> 2695-1234
        </p>
        <p style="margin:5px 0; font-size:14px; color:#444;">
            💬 <strong>WhatsApp:</strong> 8888-7777
        </p>
        <p style="margin:5px 0; font-size:14px; color:#444;">
            📧 <strong>Correo:</strong> informacion@imagenstudiocr.com
        </p>
    </div>
    <hr style="border: 1px solid #eee; margin-top:15px;">
</div>
""", unsafe_allow_html=True)

# ---------------------- MENÚ PRINCIPAL ----------------------
opcion = st.sidebar.selectbox(
    "📋 MENÚ PRINCIPAL",
    ["Servicios", "Clientes", "Ventas", "Canjes de Puntos"] + (["Administración"] if st.session_state.rol_actual == "administrador" else [])
)

# Botón para cerrar sesión
if st.sidebar.button("🚪 Cerrar Sesión", use_container_width=True):
    st.session_state.sesion_iniciada = False
    st.rerun()
# ---------------------- PANTALLA DE SERVICIOS ----------------------
if opcion == "Servicios":
    st.markdown(f"""
        <div style="background-color:{colores['Servicios']}; padding:12px; border-radius:5px; margin-bottom:20px;">
            <h1 style="color:white; margin:0; font-size:22px; text-align:center;">🛠️ GESTIÓN DE SERVICIOS</h1>
        </div>
    """, unsafe_allow_html=True)

    # Solo el administrador puede agregar, modificar o eliminar
    if st.session_state.rol_actual == "administrador":
        with st.expander("➕ Agregar Nuevo Servicio"):
            nombre_serv = st.text_input("Nombre del Servicio")
            puntos_serv = st.number_input("Valor en Puntos", min_value=1, step=1)
            es_navidad = st.checkbox("¿Es Fotografía Navideña?")
           
            if st.button("Guardar Servicio"):
                if nombre_serv.strip() != "":
                    datos["servicios"].append({
                        "nombre": nombre_serv,
                        "puntos": puntos_serv,
                        "activo": True,
                        "es_navidad": es_navidad
                    })
                    guardar_datos(datos)
                    st.success("✅ Servicio guardado correctamente")
                    st.rerun()
                else:
                    st.warning("⚠️ Escribe un nombre para el servicio")

    # Mostrar lista de servicios
    st.subheader("📋 Lista de Servicios")
    df_servicios = pd.DataFrame(datos["servicios"])
    df_servicios = df_servicios.rename(columns={
        "nombre": "Nombre del Servicio",
        "puntos": "Puntos",
        "activo": "¿Activo?",
        "es_navidad": "🎄 Navideño"
    })
    st.dataframe(df_servicios, use_container_width=True, hide_index=True, height=350)

    # Acciones: Activar/Desactivar o Eliminar
    if st.session_state.rol_actual == "administrador":
        st.subheader("⚙️ Acciones")
        if len(datos["servicios"]) > 0:
            nombres_servicios = [s["nombre"] for s in datos["servicios"]]
            seleccion_servicio = st.selectbox("Seleccionar Servicio", nombres_servicios)
            accion = st.radio("Selecciona qué hacer", ["Activar / Desactivar", "Eliminar Servicio"])
           
            if st.button("Ejecutar Acción"):
                for servicio in datos["servicios"]:
                    if servicio["nombre"] == seleccion_servicio:
                        if accion == "Activar / Desactivar":
                            servicio["activo"] = not servicio["activo"]
                            estado = "ACTIVADO" if servicio["activo"] else "DESACTIVADO"
                            st.success(f"✅ Servicio {estado} correctamente")
                        else:
                            datos["servicios"].remove(servicio)
                            st.success("🗑️ Servicio eliminado")
                       
                        guardar_datos(datos)
                        st.rerun()
        else:
            st.info("No hay servicios registrados aún")

# ---------------------- PANTALLA DE CLIENTES ----------------------
elif opcion == "Clientes":
    st.markdown(f"""
        <div style="background-color:{colores['Clientes']}; padding:12px; border-radius:5px; margin-bottom:20px;">
            <h1 style="color:white; margin:0; font-size:22px; text-align:center;">👥 GESTIÓN DE CLIENTES</h1>
        </div>
    """, unsafe_allow_html=True)

    # Crear nuevo cliente
    if st.session_state.rol_actual == "administrador":
        with st.expander("➕ Crear Nuevo Cliente"):
            nombre_cliente = st.text_input("Nombre Completo")
            puntos_iniciales = st.number_input("Puntos Iniciales", min_value=0, step=1)
           
            if st.button("Guardar Cliente"):
                if nombre_cliente.strip() != "" and nombre_cliente not in datos["clientes"]:
                    datos["clientes"][nombre_cliente] = {"puntos": puntos_iniciales, "activo": True}
                    guardar_datos(datos)
                    st.success("✅ Cliente creado correctamente")
                    st.rerun()
                else:
                    st.warning("⚠️ El nombre está vacío o el cliente ya existe")

    # Mostrar lista de clientes
    st.subheader("📋 Lista de Clientes")
    lista_clientes = []
    for nombre, info in datos["clientes"].items():
        lista_clientes.append({
            "Cliente": nombre,
            "Puntos Acumulados": info["puntos"],
            "Estado": "ACTIVO" if info["activo"] else "INACTIVO"
        })
   
    df_clientes = pd.DataFrame(lista_clientes)
    st.dataframe(df_clientes, use_container_width=True, hide_index=True, height=400)

    # Activar o desactivar clientes
    if st.session_state.rol_actual == "administrador":
        st.subheader("🔄 Cambiar Estado de Cliente")
        if len(datos["clientes"]) > 0:
            cliente_seleccionado = st.selectbox("Seleccionar Cliente", list(datos["clientes"].keys()))
           
            if st.button("Cambiar Estado"):
                datos["clientes"][cliente_seleccionado]["activo"] = not datos["clientes"][cliente_seleccionado]["activo"]
                guardar_datos(datos)
                st.success("✅ Estado actualizado correctamente")
                st.rerun()
# ---------------------- PANTALLA DE VENTAS ----------------------
elif opcion == "Ventas":
    st.markdown(f"""
        <div style="background-color:{colores['Ventas']}; padding:12px; border-radius:5px; margin-bottom:20px;">
            <h1 style="color:white; margin:0; font-size:22px; text-align:center;">💳 HISTORIAL DE VENTAS - {datetime.now().strftime('%B %Y').upper()}</h1>
        </div>
    """, unsafe_allow_html=True)

    # Registrar nueva venta
    if st.session_state.rol_actual == "administrador":
        with st.expander("➕ Registrar Nueva Venta"):
            lista_clientes_activos = [c for c, info in datos["clientes"].items() if info["activo"]]
            cliente_venta = st.selectbox("Cliente", lista_clientes_activos)
            lista_servicios_activos = [s["nombre"] for s in datos["servicios"] if s["activo"]]
            servicio_venta = st.selectbox("Servicio Realizado", lista_servicios_activos)
            monto_venta = st.number_input("Monto (₡)", min_value=0.0, step=100.0)
           
            if st.button("Guardar Venta"):
                # Agregamos la venta al historial
                datos["ventas"].append([
                    cliente_venta,
                    servicio_venta,
                    datetime.now().strftime("%d/%m/%Y %H:%M"),
                    f"¢ {monto_venta:,.2f}"
                ])
                # Sumamos los puntos al cliente
                puntos_ganados = next((s["puntos"] for s in datos["servicios"] if s["nombre"] == servicio_venta), 0)
                datos["clientes"][cliente_venta]["puntos"] += puntos_ganados
                guardar_datos(datos)
                st.success(f"✅ Venta registrada. Se sumaron {puntos_ganados} puntos a {cliente_venta}")
                st.rerun()

    # Mostrar tabla de ventas
    if len(datos["ventas"]) > 0:
        df_ventas = pd.DataFrame(
            datos["ventas"],
            columns=["Cliente", "Descripción del Servicio", "Fecha", "Monto"]
        )
        st.dataframe(df_ventas, use_container_width=True, hide_index=True, height=400)

        # Calcular total del mes
        total_mes = sum([float(v[3].replace("¢ ","").replace(",","")) for v in datos["ventas"]])
        st.markdown(f"""
            <div style="text-align:center; font-size:18px; font-weight:bold; color:#27ae60; margin-top:15px;">
                📊 TOTAL DEL MES: ¢ {total_mes:,.2f}
            </div>
        """, unsafe_allow_html=True)

        # Opción para anular venta
        if st.session_state.rol_actual == "administrador":
            st.subheader("❌ Anular Venta")
            numero_fila = st.number_input("Número de fila a anular (empieza en 0)", min_value=0, max_value=len(datos["ventas"])-1, step=1)
           
            if st.button("Anular esta venta"):
                datos["ventas"].pop(numero_fila)
                guardar_datos(datos)
                st.success("✅ Venta anulada y eliminada del historial")
                st.rerun()
    else:
        st.info("No hay ventas registradas aún")
# ---------------------- PANTALLA DE CANJES DE PUNTOS ----------------------
elif opcion == "Canjes de Puntos":
    st.markdown(f"""
        <div style="background-color:{colores['Canjes de Puntos']}; padding:12px; border-radius:5px; margin-bottom:20px;">
            <h1 style="color:white; margin:0; font-size:22px; text-align:center;">🎁 CANJES DE PUNTOS</h1>
        </div>
    """, unsafe_allow_html=True)

    st.markdown('<div style="background-color:#e8f5e9; padding:20px; border-radius:5px; margin:10px 30px;">', unsafe_allow_html=True)

    # Consultar puntos
    nombre_cliente = st.text_input("Nombre del Cliente:")
    resultado_busqueda = st.empty()
   
    if st.button("🔍 Consultar Puntos"):
        nombre_buscar = nombre_cliente.strip()
        if nombre_buscar in datos["clientes"] and datos["clientes"][nombre_buscar]["activo"]:
            puntos = datos["clientes"][nombre_buscar]["puntos"]
            resultado_busqueda.success(f"✅ Tienes acumulados: {puntos} puntos")
        else:
            resultado_busqueda.warning("⚠️ Cliente no encontrado o está inactivo")

    # Seleccionar premio
    st.markdown("<br><b>Selecciona el premio a canjear:</b>", unsafe_allow_html=True)
    premio_opciones = [f"{cantidad} puntos - {descripcion}" for cantidad, descripcion in datos["reglas_canjes"]]
    premio_seleccionado_texto = st.radio("", premio_opciones, label_visibility="collapsed")

    # Canjear puntos
    if st.button("✅ Canjear Premio", type="primary"):
        nombre = nombre_cliente.strip()
        if not nombre or nombre not in datos["clientes"] or not datos["clientes"][nombre]["activo"]:
            st.error("⚠️ Primero consulta un cliente válido y activo")
        elif not premio_seleccionado_texto:
            st.error("⚠️ Selecciona un premio para canjear")
        else:
            puntos_necesarios = int(premio_seleccionado_texto.split(" ")[0])
            descripcion_premio = premio_seleccionado_texto.split(" - ", 1)[1]
            puntos_actuales = datos["clientes"][nombre]["puntos"]

            if puntos_actuales >= puntos_necesarios:
                # Guardamos los cambios para que no se pierdan nunca
                datos["clientes"][nombre]["puntos"] -= puntos_necesarios
                guardar_datos(datos)
                st.success(f"""
                    🎉 ¡Canje Exitoso!
                    Felicidades {nombre}!
                    Has canjeado por: {descripcion_premio}
                    Se descontaron {puntos_necesarios} puntos.
                    Te quedan: {datos["clientes"][nombre]["puntos"]} puntos.
                    ✅ Los cambios quedaron guardados correctamente.
                """)
            else:
                st.error(f"""
                    ❌ Puntos insuficientes
                    Lo sentimos {nombre},
                    Necesitas {puntos_necesarios} puntos para este premio.
                    Actualmente tienes {puntos_actuales} puntos.
                """)

    st.markdown('</div>', unsafe_allow_html=True)
