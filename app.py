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

# Datos iniciales completos
datos_iniciales = {
    "servicios": [
        {"nombre": "Sesión Fotográfica Básica", "puntos": 10, "activo": True, "es_navidad": False},
        {"nombre": "Video de Evento", "puntos": 20, "activo": True, "es_navidad": False},
        {"nombre": "Fotografías Navideñas", "puntos": 15, "activo": True, "es_navidad": True},
        {"nombre": "Sesión Exterior", "puntos": 25, "activo": True, "es_navidad": False},
        {"nombre": "Álbum Digital Completo", "puntos": 30, "activo": True, "es_navidad": False}
    ],
    "clientes": {
        "Juan Pérez": {"puntos": 50, "activo": True},
        "María Gómez": {"puntos": 35, "activo": True},
        "Carlos Ruiz": {"puntos": 70, "activo": True},
        "Ana Mora": {"puntos": 20, "activo": True}
    },
    "ventas": [],
    "reglas_canjes": [
        (20, "Sesión de fotos pequeña gratis"),
        (40, "Impresión de 5 fotos tamaño carta"),
        (60, "Sesión fotográfica completa"),
        (80, "Video corto promocional"),
        (100, "Álbum impreso de lujo")
    ],
    "usuarios": {
        "Dimerson": {"clave": "admin123", "rol": "administrador"},
        "Usuario": {"clave": "1234", "rol": "consulta"}
    }
}

# ---------------------- FUNCIONES ----------------------
def cargar_datos():
    try:
        with open(ARCHIVO_DATOS, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return datos_iniciales

def guardar_datos(datos):
    with open(ARCHIVO_DATOS, "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=4, ensure_ascii=False)

datos = cargar_datos()

# ---------------------- INICIO DE SESIÓN ----------------------
if "sesion_iniciada" not in st.session_state:
    st.session_state.sesion_iniciada = False
    st.session_state.usuario_actual = ""
    st.session_state.rol_actual = ""

if not st.session_state.sesion_iniciada:
    st.markdown("""
    <div style="text-align:center; padding:30px; background-color: #f8f9fa; border-radius:10px; margin: 20px;">
        <h1>📸 INICIO DE SESIÓN</h1>
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
    st.stop()

# ---------------------- CABECERA ----------------------
st.markdown("""
<div style="text-align:center; margin-bottom:20px; padding:15px; background-color: #ffffff; border-radius:8px; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">
    <h1 style="margin:5px 0; color:#333;">IMAGEN DIGITAL STUDIO</h1>
    <p style="color:#666; font-size:15px;">Fotografía & Video | Calidad y profesionalismo</p>
    <div style="margin-top:15px; padding:10px; background-color:#f8f9fa; border-radius:5px;">
        <p>📍 <strong>Dirección:</strong> Limón Centro, diagonal a la MUCAP</p>
        <p>📞 <strong>Teléfono:</strong> 2695-1234</p>
        <p>💬 <strong>WhatsApp:</strong> 8888-7777</p>
        <p>📧 <strong>Correo:</strong> informacion@imagenstudiocr.com</p>
    </div>
    <hr>
</div>
""", unsafe_allow_html=True)

# ---------------------- MENÚ ----------------------
opcion = st.sidebar.selectbox(
    "📋 MENÚ PRINCIPAL",
    ["Servicios", "Clientes", "Ventas", "Canjes de Puntos"] + (["Administración"] if st.session_state.rol_actual == "administrador" else [])
)

if st.sidebar.button("🚪 Cerrar Sesión", use_container_width=True):
    st.session_state.sesion_iniciada = False
    st.rerun()
# ---------------------- PANTALLA SERVICIOS ----------------------
if opcion == "Servicios":
    st.markdown(f"""
        <div style="background-color:{colores['Servicios']}; padding:12px; border-radius:5px; margin-bottom:20px;">
            <h1 style="color:white; margin:0; font-size:22px; text-align:center;">🛠️ NUESTROS SERVICIOS</h1>
        </div>
    """, unsafe_allow_html=True)

    if st.session_state.rol_actual == "administrador":
        with st.expander("➕ Agregar Nuevo Servicio"):
            nombre_serv = st.text_input("Nombre del Servicio")
            puntos_serv = st.number_input("Valor en Puntos", min_value=1)
            es_navidad = st.checkbox("¿Es Navideño?")
            if st.button("Guardar Servicio"):
                if nombre_serv:
                    datos["servicios"].append({"nombre": nombre_serv, "puntos": puntos_serv, "activo": True, "es_navidad": es_navidad})
                    guardar_datos(datos)
                    st.success("✅ Guardado")
                    st.rerun()

    st.subheader("📋 Lista Completa")
    df_serv = pd.DataFrame(datos["servicios"])
    df_serv = df_serv.rename(columns={"nombre":"Servicio", "puntos":"Puntos", "activo":"Activo", "es_navidad":"Navidad"})
    st.dataframe(df_serv, use_container_width=True)

    if st.session_state.rol_actual == "administrador":
        st.subheader("⚙️ Acciones")
        if datos["servicios"]:
            sel_serv = st.selectbox("Seleccionar", [s["nombre"] for s in datos["servicios"]])
            accion = st.radio("Opción", ["Activar/Desactivar", "Eliminar"])
            if st.button("Ejecutar"):
                for s in datos["servicios"]:
                    if s["nombre"] == sel_serv:
                        if accion == "Activar/Desactivar":
                            s["activo"] = not s["activo"]
                        else:
                            datos["servicios"].remove(s)
                        guardar_datos(datos)
                        st.rerun()

# ---------------------- PANTALLA CLIENTES ----------------------
elif opcion == "Clientes":
    st.markdown(f"""
        <div style="background-color:{colores['Clientes']}; padding:12px; border-radius:5px; margin-bottom:20px;">
            <h1 style="color:white; margin:0; font-size:22px; text-align:center;">👥 GESTIÓN DE CLIENTES</h1>
        </div>
    """, unsafe_allow_html=True)

    if st.session_state.rol_actual == "administrador":
        with st.expander("➕ Nuevo Cliente"):
            nombre_cli = st.text_input("Nombre Completo")
            puntos_cli = st.number_input("Puntos Iniciales", min_value=0)
            if st.button("Guardar Cliente"):
                if nombre_cli and nombre_cli not in datos["clientes"]:
                    datos["clientes"][nombre_cli] = {"puntos": puntos_cli, "activo": True}
                    guardar_datos(datos)
                    st.success("✅ Cliente creado")
                    st.rerun()

    st.subheader("📋 Lista de Clientes")
    lista_cli = []
    for nom, info in datos["clientes"].items():
        lista_cli.append({"Nombre": nom, "Puntos": info["puntos"], "Estado": "ACTIVO" if info["activo"] else "INACTIVO"})
    st.dataframe(pd.DataFrame(lista_cli), use_container_width=True)

    if st.session_state.rol_actual == "administrador":
        st.subheader("🔄 Cambiar Estado")
        if datos["clientes"]:
            sel_cli = st.selectbox("Cliente", list(datos["clientes"].keys()))
            if st.button("Cambiar Estado"):
                datos["clientes"][sel_cli]["activo"] = not datos["clientes"][sel_cli]["activo"]
                guardar_datos(datos)
                st.rerun()
# ---------------------- PANTALLA VENTAS ----------------------
elif opcion == "Ventas":
    st.markdown(f"""
        <div style="background-color:{colores['Ventas']}; padding:12px; border-radius:5px; margin-bottom:20px;">
            <h1 style="color:white; margin:0; font-size:22px; text-align:center;">💳 HISTORIAL DE VENTAS</h1>
        </div>
    """, unsafe_allow_html=True)

    if st.session_state.rol_actual == "administrador":
        with st.expander("➕ Registrar Nueva Venta"):
            activos = [c for c, v in datos["clientes"].items() if v["activo"]]
            cliente_v = st.selectbox("Cliente", activos)
            serv_activos = [s["nombre"] for s in datos["servicios"] if s["activo"]]
            serv_v = st.selectbox("Servicio", serv_activos)
            monto_v = st.number_input("Monto ₡", min_value=0.0)
           
            if st.button("Guardar Venta"):
                datos["ventas"].append([
                    cliente_v, serv_v, datetime.now().strftime("%d/%m/%Y %H:%M"), f"¢ {monto_v:,.2f}"
                ])
                puntos_ganar = next((s["puntos"] for s in datos["servicios"] if s["nombre"] == serv_v), 0)
                datos["clientes"][cliente_v]["puntos"] += puntos_ganar
                guardar_datos(datos)
                st.success(f"✅ Venta registrada. +{puntos_ganar} puntos")
                st.rerun()

    if datos["ventas"]:
        df_ventas = pd.DataFrame(datos["ventas"], columns=["Cliente", "Servicio", "Fecha", "Monto"])
        st.dataframe(df_ventas, use_container_width=True)
        total = sum(float(v[3].replace("¢ ","").replace(",","")) for v in datos["ventas"])
        st.info(f"**TOTAL DEL MES: ₡ {total:,.2f}**")

        if st.session_state.rol_actual == "administrador":
            fila = st.number_input("Número de fila a borrar", min_value=0, max_value=len(datos["ventas"])-1)
            if st.button("Anular Venta"):
                datos["ventas"].pop(fila)
                guardar_datos(datos)
                st.rerun()
    else:
        st.info("Sin ventas registradas")

# ---------------------- PANTALLA CANJES ----------------------
elif opcion == "Canjes de Puntos":
    st.markdown(f"""
        <div style="background-color:{colores['Canjes de Puntos']}; padding:12px; border-radius:5px; margin-bottom:20px;">
            <h1 style="color:white; margin:0; font-size:22px; text-align:center;">🎁 CANJES DE PUNTOS</h1>
        </div>
    """, unsafe_allow_html=True)

    st.markdown('<div style="background:#e8f5e9; padding:20px; border-radius:8px;">', unsafe_allow_html=True)

    nombre_canje = st.text_input("Nombre del Cliente")
    if st.button("🔍 Consultar Puntos"):
        if nombre_canje in datos["clientes"] and datos["clientes"][nombre_canje]["activo"]:
            st.success(f"✅ Puntos disponibles: {datos['clientes'][nombre_canje]['puntos']}")
        else:
            st.error("❌ Cliente no válido o inactivo")

    st.subheader("📋 Premios Disponibles")
    premios_texto = [f"🔸 {p} puntos: {d}" for p,d in datos["reglas_canjes"]]
    for p in premios_texto:
        st.write(p)

    if premios_texto:
        sel_premio = st.radio("Seleccione premio", premios_texto)
        if st.button("✅ Realizar Canje"):
            if not nombre_canje or nombre_canje not in datos["clientes"]:
                st.error("Primero consulte el nombre del cliente")
            elif not sel_premio:
                st.error("Seleccione un premio")
            else:
                puntos_neces = int(sel_premio.split()[0])
                puntos_act = datos["clientes"][nombre_canje]["puntos"]
                if puntos_act >= puntos_neces:
                    datos["clientes"][nombre_canje]["puntos"] -= puntos_neces
                    guardar_datos(datos)
                    st.success("🎉 ¡Canje exitoso! Puntos descontados.")
                    st.rerun()
                else:
                    st.error("❌ Puntos insuficientes")

    st.markdown('</div>', unsafe_allow_html=True)
# ---------------------- PANTALLA ADMINISTRACIÓN ----------------------
elif opcion == "Administración":
    st.markdown(f"""
        <div style="background-color:{colores['Administración']}; padding:12px; border-radius:5px; margin-bottom:20px;">
            <h1 style="color:white; margin:0; font-size:22px; text-align:center;">⚙️ PANEL DE ADMINISTRACIÓN</h1>
        </div>
    """, unsafe_allow_html=True)

    st.warning("⚠️ **Solo para personal autorizado** - Aquí se modifica todo el sistema")

    # Gestión de Usuarios
    st.subheader("👤 Gestionar Usuarios")
    df_usuarios = []
    for usuario, info in datos["usuarios"].items():
        df_usuarios.append({
            "Usuario": usuario,
            "Rol": info["rol"]
        })
    st.dataframe(pd.DataFrame(df_usuarios), use_container_width=True)

    # Crear nuevo usuario
    with st.expander("➕ Crear Nuevo Usuario"):
        nuevo_user = st.text_input("Nombre de Usuario")
        nueva_clave = st.text_input("Contraseña", type="password")
        rol_nuevo = st.selectbox("Rol", ["administrador", "consulta"])
        if st.button("Guardar Usuario"):
            if nuevo_user and nuevo_user not in datos["usuarios"]:
                datos["usuarios"][nuevo_user] = {"clave": nueva_clave, "rol": rol_nuevo}
                guardar_datos(datos)
                st.success("✅ Usuario creado correctamente")
                st.rerun()

    # Modificar Reglas de Canje
    st.subheader("🎁 Modificar Reglas de Premios")
    nueva_puntos = st.number_input("Puntos necesarios", min_value=10, step=10)
    nueva_desc = st.text_input("Descripción del premio")
    if st.button("Agregar Nueva Regla"):
        if nueva_desc:
            datos["reglas_canjes"].append((nueva_puntos, nueva_desc))
            guardar_datos(datos)
            st.success("✅ Regla agregada")
            st.rerun()

    # Resumen del sistema
    st.subheader("📊 Resumen General del Sistema")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Servicios", len(datos["servicios"]))
    with col2:
        st.metric("Total Clientes", len(datos["clientes"]))
    with col3:
        st.metric("Total Ventas", len(datos["ventas"]))

    # Reiniciar sistema
    if st.button("🔄 Reiniciar Datos a Estado Original", type="secondary"):
        if st.checkbox("Estoy seguro, borrar todo y empezar de nuevo"):
            datos = datos_iniciales
            guardar_datos(datos)
            st.success("✅ Sistema reiniciado por completo")
            st.rerun()
