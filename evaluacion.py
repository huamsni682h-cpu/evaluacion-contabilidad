# -*- coding: utf-8 -*-
"""
Evaluación EPT 3.° – HT 70 % · HE 20 % · HD 10 %   (15 días, un bloque por día)
Ejecutar:   pip install streamlit pandas      →      streamlit run evaluacion.py
Variables opcionales: EVAL_INICIO=2026-11-30  EVAL_CLAVE=tu_clave  EVAL_DATOS=carpeta
"""
import os, json, pathlib, datetime as dt
import pandas as pd
import streamlit as st
import banco as B
import almacen as A

DATA = pathlib.Path(os.getenv("EVAL_DATOS", "datos_evaluacion"))
(DATA / "alumnos").mkdir(parents=True, exist_ok=True); (DATA / "fotos").mkdir(exist_ok=True)
LISTA = pathlib.Path("lista.csv")
INICIO = dt.date.fromisoformat(os.getenv("EVAL_INICIO", "2026-11-30"))
CLAVE = os.getenv("EVAL_CLAVE", "docente2026")
AREA = {"HT": "Habilidades técnicas (Contabilidad)", "HE": "Habilidades de emprendimiento", "HD": "Habilidades digitales"}

st.set_page_config(page_title="Evaluación EPT 3.°", page_icon="📒", layout="centered")

def lista():
    return pd.read_csv(LISTA, dtype=str).fillna("") if LISTA.exists() else pd.DataFrame()
def ruta(dni): return DATA / "alumnos" / f"{dni}.json"
def cargar(dni):
    a = A.leer(dni)
    if a is None: return None
    g = lista().set_index("id")["grupo"].to_dict().get(dni) if LISTA.exists() else None; a.setdefault("grupo", g or B.grupo_de(dni)); return a
def guardar(al): A.escribir(al)
def dia_actual(): return max(1, min(B.DIAS, (dt.date.today() - INICIO).days + 1))

# ───────────────────────── ITEM ─────────────────────────
def mostrar(item, al):
    caso = B.construir(item, al["dni"], al["grupo"]); iid = item["id"]; ans = al["resp"].get(iid)
    with st.container(border=True):
        st.markdown(f"**{iid}** · {AREA[item['area']]} · _{item['pts']} pt_")
        st.write(caso["texto"])
        t = caso["tipo"]; bloqueado = ans is not None and not (t == "foto" and ans.get("rev") is None)
        valor = None
        if t == "mc":
            valor = st.radio("Elige:", caso["opciones"], index=None, key=iid, disabled=bloqueado)
        elif t == "num":
            valor = st.number_input(caso["etiqueta"], step=0.01, format="%.2f", key=iid, disabled=bloqueado)
        elif t == "formula":
            valor = st.text_input("Fórmula (empieza con =)", key=iid, disabled=bloqueado)
        elif t == "match":
            valor = {k: st.selectbox(k, ["—"] + caso["opciones"], key=f"{iid}-{k}", disabled=bloqueado) for k in caso["izq"]}
        elif t == "fill":
            valor = [st.selectbox(f, ["—"] + caso["opciones"], key=f"{iid}-{n}", disabled=bloqueado) for n, f in enumerate(caso["frases"])]
        elif t == "foto":
            st.info("📓 **En tu cuaderno:** " + caso["tarea"])
            st.caption("En CADA hoja escribe: nombres y apellidos, grado y sección, fecha y N.° de día. " + B.RUBRICA)
            valor = st.number_input("Dato de control – " + caso["etiqueta"], step=0.01, format="%.2f", key=iid + "c", disabled=bloqueado)
            foto = st.file_uploader("Sube la FOTO de tu cuaderno (JPG/PNG)", type=["jpg", "jpeg", "png"], key=iid + "f", disabled=bloqueado)
        if ans:
            if t == "foto":
                rev = ans.get("rev")
                st.success("Enviado. Dato de control " + ("✔ correcto" if B.fraccion(caso, ans["resp"]) else "✘ incorrecto")
                           + (" · Cuaderno: pendiente de revisión del docente" if rev is None else f" · Cuaderno revisado: {rev*100:.0f} %"))
            else:
                ok = B.fraccion(caso, ans["resp"])
                st.success(f"Respondida · {ok*100:.0f} % correcto ({B.puntaje_item(item, caso, ans):.2f} pt)")
        if not bloqueado:
            if st.button("Enviar respuesta", key=iid + "b"):
                if t in ("mc",) and valor is None: st.warning("Elige una opción."); return
                if t == "formula" and not valor.strip(): st.warning("Escribe la fórmula."); return
                if t == "foto":
                    if foto is None: st.warning("Debes subir la foto del cuaderno."); return
                    p = A.guardar_foto(al["dni"], iid, pathlib.Path(foto.name).suffix.lower(), bytes(foto.getbuffer()))
                    al["resp"][iid] = {"resp": valor, "foto": str(p), "rev": None, "t": dt.datetime.now().isoformat(timespec="seconds")}
                else:
                    if t in ("match", "fill") and "—" in (valor.values() if t == "match" else valor):
                        st.warning("Completa todas las opciones."); return
                    al["resp"][iid] = {"resp": valor, "t": dt.datetime.now().isoformat(timespec="seconds")}
                guardar(al); st.rerun()

# ───────────────────────── ALUMNO ─────────────────────────
def vista_alumno():
    st.title("📒 Evaluación de Educación para el Trabajo")
    st.caption("3.° de secundaria · HT 70 % · HE 20 % · HD 10 % · Nota sobre 20")
    al = st.session_state.get("al")
    if not al:
        L = lista()
        if L.empty: st.error("Falta lista.csv: ejecuta primero  python generar_lista.py"); return
        with st.form("login"):
            sal = st.selectbox("Salón", sorted(L["salon"].unique()), format_func=lambda x: f"3.° {x}")
            fila = st.selectbox("Tu nombre", L.sort_values(["salon", "apellidos"]).to_dict("records"),
                                format_func=lambda x: f"{x['salon']} · {x['apellidos']} {x['nombres']}")
            cod = st.text_input("Tu código personal (4 dígitos)", type="password", max_chars=4)
            if st.form_submit_button("Ingresar"):
                if fila["salon"] != sal: st.error("Ese nombre no es del salón elegido.")
                elif cod != fila["codigo"]: st.error("Código incorrecto.")
                else:
                    al = cargar(fila["id"]) or dict(dni=fila["id"], nombre=f"{fila['apellidos']} {fila['nombres']}".upper(),
                         grado="3.°", seccion=fila["salon"], grupo=fila["grupo"], resp={})
                    guardar(al); st.session_state.al = al; st.rerun()
        return
    c1, c2 = st.columns([4, 1]); c1.markdown(f"**{al['nombre']}** · Código {al['dni']} · {al['grado']} “{al['seccion']}” · **Grupo {al['grupo']}**")
    if c2.button("Salir"): st.session_state.pop("al"); st.rerun()
    tot = B.totales(al["dni"], al["resp"], al["grupo"]); hoy = dia_actual()
    st.progress(min(1.0, len(al["resp"]) / len(B.ITEMS)), text=f"Avance: {len(al['resp'])}/{len(B.ITEMS)} actividades · Día {hoy} de {B.DIAS}")
    m = st.columns(4); m[0].metric("HT /14", f"{tot['HT']:.2f}"); m[1].metric("HE /4", f"{tot['HE']:.2f}")
    m[2].metric("HD /2", f"{tot['HD']:.2f}"); m[3].metric("Nota /20", f"{tot['TOTAL']:.2f}")
    st.caption("La nota se completa cuando el docente revise tus cuadernos (60 % de cada caso con foto).")
    dia = st.select_slider("Día de trabajo", options=list(range(1, hoy + 1)), value=hoy)
    pend = [i for i in B.ITEMS if i["dia"] < hoy and i["id"] not in al["resp"]]
    if pend: st.warning(f"Tienes {len(pend)} actividad(es) atrasada(s): " + ", ".join(i["id"] for i in pend))
    for it in [i for i in B.ITEMS if i["dia"] == dia]: mostrar(it, al)

# ───────────────────────── DOCENTE ─────────────────────────
def vista_docente():
    st.title("👩‍🏫 Panel del docente")
    if st.text_input("Clave", type="password") != CLAVE: st.stop()
    al_list = [cargar(i) for i in A.ids()]
    if not al_list: st.info("Aún no hay alumnos registrados."); return
    filas = []
    for a in al_list:
        t = B.totales(a["dni"], a["resp"], a["grupo"])
        pend = sum(1 for k, v in a["resp"].items() if k.startswith("HT-F") and v.get("rev") is None)
        filas.append({"Alumno": a["nombre"], "DNI": a["dni"], "Grado": a["grado"], "Sección": a["seccion"], "Grupo": a["grupo"],
                      "Actividades": len(a["resp"]), "HT/14": round(t["HT"], 2), "HE/4": round(t["HE"], 2),
                      "HD/2": round(t["HD"], 2), "NOTA/20": t["TOTAL"], "Cuadernos por revisar": pend})
    df = pd.DataFrame(filas).sort_values(["Sección", "Alumno"]); st.dataframe(df, use_container_width=True, hide_index=True)
    st.download_button("⬇ Descargar notas (CSV)", df.to_csv(index=False).encode("utf-8-sig"), "notas_EPT.csv", "text/csv")
    st.subheader("Asignar grupo (A, B, C, D)")
    c1, c2 = st.columns([3, 1]); s0 = c1.selectbox("Alumno", al_list, format_func=lambda a: f"{a['nombre']} · grupo {a['grupo']}", key="sg")
    ng = c2.selectbox("Grupo", list(B.GRUPOS), index=B.GRUPOS.index(s0["grupo"]), key="ng")
    if s0["resp"]: st.caption("Ya respondió: el grupo no se puede cambiar.")
    elif st.button("Cambiar grupo") and ng != s0["grupo"]: s0["grupo"] = ng; guardar(s0); st.rerun()
    st.subheader("Revisar cuadernos")
    sel = st.selectbox("Alumno", al_list, format_func=lambda a: f"{a['nombre']} ({a['dni']})")
    for it in [i for i in B.ITEMS if i["foto"] and i["id"] in sel["resp"]]:
        a = sel["resp"][it["id"]]; caso = B.construir(it, sel["dni"], sel["grupo"])
        with st.container(border=True):
            st.markdown(f"**{it['id']}** · control del alumno: {a['resp']} · correcto: {caso['control']} "
                        f"{'✔' if B.fraccion(caso, a['resp']) else '✘'}")
            st.caption(caso["texto"])
            b = A.leer_foto(a["foto"])
            if b: st.image(b)
            rev = st.slider("Calidad del cuaderno (rúbrica)", 0, 100, int((a.get("rev") or 0) * 100), 5, key=f"r{sel['dni']}{it['id']}")
            if st.button("Guardar revisión", key=f"g{sel['dni']}{it['id']}"):
                a["rev"] = rev / 100; guardar(sel); st.success("Guardado"); st.rerun()

modo = st.sidebar.radio("Ingresar como", ["Alumno", "Docente"])
st.sidebar.caption(f"Almacenamiento: {A.modo()}")
st.sidebar.caption(f"Inicio de la evaluación: {INICIO:%d/%m/%Y} · Hoy: día {dia_actual()}")
vista_alumno() if modo == "Alumno" else vista_docente()
