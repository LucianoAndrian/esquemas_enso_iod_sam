"""
Esquema de prec y temp en SA - ENSO-IOD
"""
# ---------------------------------------------------------------------------- #
save = False
out_dir = '/home/luciano.andrian/doc/esquemas/salidas_plots/'

data_dir = '/home/luciano.andrian/doc/esquemas/salidas/'

# ---------------------------------------------------------------------------- #
import numpy as np
import xarray as xr
from scipy.ndimage import gaussian_filter

from utils.funciones_esquema import plot_esquema_pp_t_sa

import warnings
from shapely.errors import ShapelyDeprecationWarning
warnings.filterwarnings("ignore", category=ShapelyDeprecationWarning)

# Funciones aux -------------------------------------------------------------- #
def normalize_field(data):

    dims = ('lon', 'lat')
    skipna = True

    max_abs = abs(data).max(dim=dims, skipna=skipna)
    max_abs = max_abs.where(max_abs != 0)

    normalized = data / max_abs

    return normalized

def interp_to_grid(source_ds, target_ds):

    target_ds_var_name = list(target_ds.data_vars)[0]

    da = target_ds[target_ds_var_name]

    da_interp = da.interp(
        lat=source_ds.lat.values,
        lon=source_ds.lon.values,
        method='linear'
    )

    return da_interp


def smooth_precip_xr(da, sigma=1):
    """
    Suaviza un xarray.DataArray 2D manejando NaNs.
    Conserva coordenadas y metadatos.
    """

    try:
        da = da[list(da.data_vars)[0]]
    except:
        pass

    # 1. Extraemos los valores y creamos una máscara de NaNs
    v = da.values.copy()
    nan_mask = np.isnan(v)

    # 2. Reemplazamos NaNs por 0 para el cálculo del filtro
    v_zeroed = np.where(nan_mask, 0, v)

    # 3. Aplicamos el filtro al campo y a la máscara de presencia de datos
    v_smoothed = gaussian_filter(v_zeroed, sigma=sigma)
    w_smoothed = gaussian_filter((~nan_mask).astype(float), sigma=sigma)

    # 4. Normalizamos (esto evita que los bordes con NaNs se "desinflen")
    # Usamos np.where para evitar dividir por cero en zonas de puro NaN
    with np.errstate(divide='ignore', invalid='ignore'):
        result_array = v_smoothed / w_smoothed
        # Re-insertamos NaNs originales si prefieres mantener el recorte original
        result_array = np.where(nan_mask, np.nan, result_array)

    # 5. Devolvemos un nuevo DataArray con la misma estructura
    da_smooth = da.copy(data=result_array)
    da_smooth.attrs['processing'] = f'Gaussian filter applied (sigma={sigma})'

    return da_smooth


# Precipitacion -------------------------------------------------------------- #
comp_obs = xr.open_dataset(f'{data_dir}comp_pp_t_obs.nc').sel(level=0)
comp_mod = xr.open_dataset(f'{data_dir}comp_prec_cfsv2.nc')
# Fase positiva -------------------------------------------------------------- #
# Simultaneos
sim = comp_obs.sel(case='DMI_sim_pos')
sim_mod = comp_mod.sel(case='sim_pos')
sim = interp_to_grid(sim_mod, sim)

sim_hibrid = sim_mod + sim
sim_hibrid = normalize_field(sim_hibrid)

sim = normalize_field(sim)
sim_mod = normalize_field(sim_mod)

# Ninio
ninio_obs = comp_obs.sel(case='N34_un_pos')
ninio_mod = comp_mod.sel(case='n34_puros_pos')
ninio_obs = interp_to_grid(ninio_mod, ninio_obs)

ninio_hibrid = 2*ninio_obs + 0.4*ninio_mod
ninio_hibrid = normalize_field(ninio_hibrid)

ninio_obs = normalize_field(ninio_obs)
ninio_mod = normalize_field(ninio_mod)

# IOD
dmi = comp_obs.sel(case='DMI_un_pos')
dmi_mod = comp_mod.sel(case='dmi_puros_pos')
dmi_regre = xr.open_dataset(f'{data_dir}prec_regre_dmi_won34.nc')
regre_name = list(dmi_regre.data_vars)[0]
dmi_regre = dmi_regre.rename({regre_name: 'var'})

dmi = interp_to_grid(dmi_mod, dmi)
dmi_regre = interp_to_grid(dmi_mod, dmi_regre)

dmi_hibrid = dmi_mod*0 + dmi*1 + dmi_regre*1
dmi_hibrid = normalize_field(dmi_hibrid)
dmi = normalize_field(dmi)
dmi_mod = normalize_field(dmi_mod)
dmi_regre = normalize_field(dmi_regre)

plot_esquema_pp_t_sa(data_shd=smooth_precip_xr(sim, 2),
                     levels_shd=[-1, -0.3, -0.15, 0, 0.15, 0.3,  1],
                     data_sld_ln=smooth_precip_xr(ninio_obs, 3),
                     levels_sld_ln=[-0.3, -0.15,  0.15, 0.3],
                     data_dtd_ln=smooth_precip_xr(dmi_hibrid, 2),
                     levels_dtd_ln=[-0.3, -0.15,  0.15, 0.3],
                     title=f'El Niño (solid lines), Positive IOD (dotted lines), '
                           f'El Niño + positive IOD (shading)',
                     name_fig='esquema_positivo_pp_sa.png', save=save, step=1,
                     high=5,
                     color_shd=['#C3A569', '#D9C4A9', 'white', 'white', '#6FD1AB', '#66A79F'],
                     color_sld=['#744D20', '#A16B23', '#108EC8', '#09587A'],
                     color_dtd=['#460400', '#FF4031', '#1F00FF', '#10005C'])

# Fase negativa -------------------------------------------------------------- #
# Simultaneos
sim = comp_obs.sel(case='DMI_sim_neg')
sim_mod = comp_mod.sel(case='sim_neg')
sim = interp_to_grid(sim_mod, sim)

sim_hibrid = sim_mod + sim
sim_hibrid = normalize_field(sim_hibrid)

sim = normalize_field(sim)
sim_mod = normalize_field(sim_mod)

# Ninia
ninia_obs = comp_obs.sel(case='N34_un_neg')
ninia_mod = comp_mod.sel(case='n34_puros_neg')
ninia_obs = interp_to_grid(ninia_mod, ninia_obs)

ninia_hibrid = 2*ninia_obs + 0.4*ninia_mod
ninia_hibrid = normalize_field(ninia_hibrid)

ninia_obs = normalize_field(ninia_obs)
ninia_mod = normalize_field(ninia_mod)

# IOD
dmi = comp_obs.sel(case='DMI_un_neg')
dmi_mod = comp_mod.sel(case='dmi_puros_neg')
dmi_regre = xr.open_dataset(f'{data_dir}prec_regre_dmi_won34.nc')*-1
regre_name = list(dmi_regre.data_vars)[0]
dmi_regre = dmi_regre.rename({regre_name: 'var'})

dmi = interp_to_grid(dmi_mod, dmi)
dmi_regre = interp_to_grid(dmi_mod, dmi_regre)

dmi_hibrid = dmi_mod*0.5 + dmi*1 + dmi_regre*0
dmi_hibrid = normalize_field(dmi_hibrid)
dmi = normalize_field(dmi)
dmi_mod = normalize_field(dmi_mod)
dmi_regre = normalize_field(dmi_regre)

plot_esquema_pp_t_sa(data_shd=smooth_precip_xr(sim, 2),
                     levels_shd=[-1, -0.3, -0.15, 0, 0.15, 0.3,  1],
                     data_sld_ln=smooth_precip_xr(ninia_obs, 2),
                     levels_sld_ln=[-0.3, -0.15,  0.15, 0.3],
                     data_dtd_ln=smooth_precip_xr(dmi_hibrid, 2),
                     levels_dtd_ln=[-0.3, -0.15,  0.15, 0.3],
                     title=f'El Niño (solid lines), Positive IOD (dotted lines), '
                           f'El Niño + positive IOD (shading)',
                     name_fig='esquema_negativo_hs_circ.png', save=save, step=1,
                     high=5,
                     color_shd=['#C3A569', '#D9C4A9', 'white', 'white', '#6FD1AB', '#66A79F'],
                     color_sld=['#744D20', '#A16B23', '#108EC8', '#09587A'],
                     color_dtd=['#460400', '#FF4031', '#1F00FF', '#10005C'])

# Fase positiva -------------------------------------------------------------- #
# Simultaneos
sim = comp_obs.sel(case='DMI_sim_neg')
sim_mod = comp_mod.sel(case='sim_neg')
sim = interp_to_grid(sim_mod, sim)

sim_hibrid = sim_mod + sim
sim_hibrid = normalize_field(sim_hibrid)

sim = normalize_field(sim)
sim_mod = normalize_field(sim_mod)

# Ninia
ninia_obs = comp_obs.sel(case='N34_un_neg')
ninia_mod = comp_mod.sel(case='n34_puros_neg')
ninia_obs = interp_to_grid(ninia_mod, ninia_obs)

ninia_hibrid = ninia_obs + ninia_mod*2
ninia_hibrid = normalize_field(ninia_hibrid)

ninia_obs = normalize_field(ninia_obs)
ninia_mod = normalize_field(ninia_mod)

# IOD
dmi = comp_obs.sel(case='DMI_un_neg')
dmi_mod = comp_mod.sel(case='dmi_puros_neg')
dmi_regre = xr.open_dataset(f'{data_dir}temp_regre_dmi_won34.nc')
regre_name = list(dmi_regre.data_vars)[0]
dmi_regre = dmi_regre.rename({regre_name: 'var'})

dmi = interp_to_grid(dmi_mod, dmi)
dmi_regre = interp_to_grid(dmi_mod, dmi_regre)

dmi_hibrid = dmi_mod*0 + dmi*1 + dmi_regre*1
dmi_hibrid = normalize_field(dmi_hibrid)
dmi = normalize_field(dmi)
dmi_mod = normalize_field(dmi_mod)
dmi_regre = normalize_field(dmi_regre)

plot_esquema_pp_t_sa(data_shd=smooth_precip_xr(sim, 2),
                     levels_shd=[-1, -0.3, -0.15, 0, 0.15, 0.3,  1],
                     data_sld_ln=smooth_precip_xr(ninia_obs, 3),
                     levels_sld_ln=[-0.5, -0.2,  0.2, 0.5],
                     data_dtd_ln=smooth_precip_xr(dmi_hibrid, 2),
                     levels_dtd_ln=[-0.3, -0.15,  0.15, 0.3],
                     title=f'El Niño (solid lines), Positive IOD (dotted lines), '
                           f'El Niño + positive IOD (shading)',
                     name_fig='esquema_negativo_pp_sa.png', save=save, step=1,
                     high=5,
                     color_shd=['#6B6FC3', '#7BC3BB', 'white', 'white', '#FFAD7E', '#FF6962'],
                     color_sld=['#001574', '#0026E1', '#CB0003', '#7A0003'],
                     color_dtd=['#005D20', '#00E946', '#CE00C1', '#6D0067'])
#