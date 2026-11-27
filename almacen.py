# -*- coding: utf-8 -*-
"""Almacenamiento: Google Drive (si hay secretos configurados) o disco local (respaldo).
Guarda en una carpeta de Drive: alumno_<ID>.json (respuestas) y foto_<ID>_<ITEM>.<ext> (cuadernos)."""
import os, io, json, pathlib

DATA = pathlib.Path(os.getenv("EVAL_DATOS", "datos_evaluacion"))

def _cfg():
    try:
        import streamlit as st
        if "gcp_service_account" in st.secrets and "DRIVE_FOLDER_ID" in st.secrets:
            return dict(st.secrets["gcp_service_account"]), str(st.secrets["DRIVE_FOLDER_ID"])
    except Exception:
        pass
    return None

def modo(): return "Google Drive" if _cfg() else "disco local"

_svc_cache = {}
def _svc():
    if "s" not in _svc_cache:
        from google.oauth2 import service_account
        from googleapiclient.discovery import build
        info, _ = _cfg()
        cred = service_account.Credentials.from_service_account_info(info, scopes=["https://www.googleapis.com/auth/drive"])
        _svc_cache["s"] = build("drive", "v3", credentials=cred, cache_discovery=False)
    return _svc_cache["s"]

_ID = {}   # nombre -> fileId (evita buscar de nuevo)
def _buscar(nombre):
    if nombre in _ID: return _ID[nombre]
    folder = _cfg()[1]
    r = _svc().files().list(q=f"name='{nombre}' and '{folder}' in parents and trashed=false", fields="files(id)",
                            supportsAllDrives=True, includeItemsFromAllDrives=True, corpora="allDrives").execute()
    fid = r["files"][0]["id"] if r["files"] else None
    if fid: _ID[nombre] = fid
    return fid

def _subir(nombre, datos, mime):
    from googleapiclient.http import MediaIoBaseUpload
    media = MediaIoBaseUpload(io.BytesIO(datos), mimetype=mime, resumable=False); fid = _buscar(nombre)
    if fid: _svc().files().update(fileId=fid, media_body=media, supportsAllDrives=True).execute()
    else:
        f = _svc().files().create(body={"name": nombre, "parents": [_cfg()[1]]}, media_body=media, fields="id", supportsAllDrives=True).execute()
        _ID[nombre] = f["id"]

def _bajar(nombre):
    fid = _buscar(nombre)
    return _svc().files().get_media(fileId=fid, supportsAllDrives=True).execute() if fid else None

# ───── API pública ─────
def leer(dni):
    if _cfg():
        b = _bajar(f"alumno_{dni}.json"); return json.loads(b.decode("utf-8")) if b else None
    p = DATA / "alumnos" / f"{dni}.json"
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else None

def escribir(al):
    datos = json.dumps(al, ensure_ascii=False, indent=1).encode("utf-8")
    if _cfg(): _subir(f"alumno_{al['dni']}.json", datos, "application/json"); return
    (DATA / "alumnos").mkdir(parents=True, exist_ok=True); (DATA / "alumnos" / f"{al['dni']}.json").write_bytes(datos)

def guardar_foto(dni, iid, ext, datos):
    nombre = f"foto_{dni}_{iid}{ext}"; mime = "image/png" if ext == ".png" else "image/jpeg"
    if _cfg(): _subir(nombre, datos, mime); return nombre
    d = DATA / "fotos" / dni; d.mkdir(parents=True, exist_ok=True); (d / f"{iid}{ext}").write_bytes(datos)
    return str(d / f"{iid}{ext}")

def leer_foto(ref):
    if _cfg(): return _bajar(ref)
    p = pathlib.Path(ref); return p.read_bytes() if p.exists() else None

def ids():
    if _cfg():
        out, tok = [], None
        while True:
            r = _svc().files().list(q=f"'{_cfg()[1]}' in parents and name contains 'alumno_' and trashed=false", fields="nextPageToken, files(id,name)",
                                    pageSize=200, pageToken=tok, supportsAllDrives=True, includeItemsFromAllDrives=True, corpora="allDrives").execute()
            for f in r["files"]: _ID[f["name"]] = f["id"]; out.append(f["name"][7:-5])
            tok = r.get("nextPageToken")
            if not tok: return sorted(out)
    return sorted(p.stem for p in (DATA / "alumnos").glob("*.json"))
