"""
Funciones generales
"""
# ---------------------------------------------------------------------------- #
import xarray as xr
import numpy as np
import logging
import os

# ---------------------------------------------------------------------------- #
def xrFieldTimeDetrend(xrda, dim, deg=1):
    # detrend along a single dimension
    aux = xrda.polyfit(dim=dim, deg=deg)
    try:
        trend = xr.polyval(xrda[dim], aux.var_polyfit_coefficients[0])
    except:
        trend = xr.polyval(xrda[dim], aux.polyfit_coefficients[0])

    dt = xrda - trend
    return dt

# ---------------------------------------------------------------------------- #
def open_and_load(path):
    ds = xr.open_dataset(path, engine='netcdf4')  # backend explícito
    ds_loaded = ds.load()  # carga a memoria
    ds.close()             # cierra archivo en disco
    return ds_loaded

# ---------------------------------------------------------------------------- #
def MakeMask(DataArray, dataname='mask'):
    import regionmask
    mask=regionmask.defined_regions.natural_earth_v5_0_0.countries_110.mask(DataArray)
    mask = xr.where(np.isnan(mask), mask, 1)
    mask = mask.to_dataset(name=dataname)
    return mask

# ---------------------------------------------------------------------------- #
def SameDateAs(data, datadate):
    """
    En data selecciona las mismas fechas que datadate
    :param data:
    :param datadate:
    :return:
    """
    return data.sel(time=datadate.time.values)
# ---------------------------------------------------------------------------- #
def MakerMaskSig(data, r_crit):
    mask_sig = data.where((data < -1 * r_crit) | (data > r_crit))
    mask_sig = mask_sig.where(np.isnan(mask_sig), 1)

    return mask_sig

# ---------------------------------------------------------------------------- #
def Weights(data):
    weights = np.transpose(np.tile(np.cos(data.lat * np.pi / 180),
                                   (len(data.lon), 1)))
    data_w = data * weights
    return data_w

# ---------------------------------------------------------------------------- #
def init_logger(log_name="app.log", level=logging.INFO):
    """
    Inicializa un logger que guarda el log en una carpeta 'logs'
    ubicada en el mismo directorio del script que lo llama.
    """
    # directorio donde está ESTE archivo
    # y subir un nivel -> directorio raíz del proyecto
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)

    log_dir = os.path.join(project_root, "logs")
    os.makedirs(log_dir, exist_ok=True)
    log_path = os.path.join(log_dir, log_name)

    if os.path.exists(log_path):
        os.remove(log_path)

    logging.basicConfig(
        level=level,
        format='%(asctime)s [%(levelname)s] %(message)s',
        handlers=[
            logging.FileHandler(log_path),
            logging.StreamHandler()
        ]
    )

    return logging.getLogger(__name__)

# ---------------------------------------------------------------------------- #