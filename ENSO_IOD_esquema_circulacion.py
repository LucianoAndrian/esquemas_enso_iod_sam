"""
Esquema de circulacion - ENSO-IOD
"""
# ---------------------------------------------------------------------------- #
save = False
out_dir = '/home/luciano.andrian/doc/esquemas/salidas_plots/'

data_dir = '/home/luciano.andrian/doc/esquemas/salidas/'

# ---------------------------------------------------------------------------- #
import xarray as xr

from utils.funciones_esquema import plot_esquema_circ_hs

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

# Fase positiva -------------------------------------------------------------- #
comp_obs = xr.open_dataset(f'{data_dir}comp_cir_obs.nc')
comp_mod = xr.open_dataset(f'{data_dir}comp_cir_cfsv2.nc')

# Simultaneos
sim = comp_obs.sel(case='DMI_sim_pos', level=200)
sim_mod = comp_mod.sel(case='sim_pos')
sim_hibrid = sim_mod + sim
sim_hibrid = normalize_field(sim_hibrid)

sim = normalize_field(sim)
sim_mod = normalize_field(sim_mod)

# Ninio
ninio_obs = comp_obs.sel(case='N34_un_pos', level=200)
ninio_mod = comp_mod.sel(case='n34_puros_pos')

ninio_hibrid = 2*ninio_obs + 0.4*ninio_mod
ninio_hibrid = normalize_field(ninio_hibrid)

# IOD
dmi = comp_obs.sel(case='DMI_un_pos', level=200)
dmi_mod = comp_mod.sel(case='dmi_puros_pos')
dmi_regre = xr.open_dataset(f'{data_dir}hgt200_regre_dmi_won34_HS.nc')
regre_name = list(dmi_regre.data_vars)[0]
dmi_regre = dmi_regre.rename({regre_name: 'var'})


dmi_hibrid = dmi_mod*0.3 + dmi*0.5 + dmi_regre*1
dmi_hibrid = normalize_field(dmi_hibrid)


plot_esquema_circ_hs(data_shd=sim, levels_shd=[-1, -0.2, 0, 0.2, 1],
                     data_sld_ln=ninio_hibrid, levels_sld_ln=[-0.35, 0.3],
                     data_dtd_ln=dmi_hibrid, levels_dtd_ln=[-0.35, 0.35],
                     title=f'El Niño (solid lines), Positive IOD (dotted lines), '
                           f'El Niño + positive IOD (shading)',
                     name_fig='esquema_positivo_hs_circ.png', save=save, step=1,
                     high=2.3,
                     color_dtd=['#007E72', '#B2000D'])

# Fase negativa -------------------------------------------------------------- #
# Simultaneos
sim = comp_obs.sel(case='DMI_sim_neg', level=200)
sim_mod = comp_mod.sel(case='sim_neg')
sim_hibrid = sim_mod*0.5 + sim
sim_hibrid = normalize_field(sim_hibrid)

sim = normalize_field(sim)
sim_mod = normalize_field(sim_mod)

# Ninia
ninia_obs = comp_obs.sel(case='N34_un_neg', level=200)
ninia_mod = comp_mod.sel(case='n34_puros_neg')

ninia_hibrid = 1*ninia_obs + 0*ninia_mod
ninia_hibrid = normalize_field(ninia_hibrid)

# IOD
dmi = comp_obs.sel(case='DMI_un_neg', level=200)
dmi_mod = comp_mod.sel(case='dmi_puros_neg')
dmi_regre = xr.open_dataset(f'{data_dir}hgt200_regre_dmi_won34_HS.nc')*-1
regre_name = list(dmi_regre.data_vars)[0]
dmi_regre = dmi_regre.rename({regre_name: 'var'})


dmi_hibrid = dmi_mod*0.5 + dmi*1 + dmi_regre*0
dmi_hibrid = normalize_field(dmi_hibrid)


plot_esquema_circ_hs(data_shd=sim, levels_shd=[-1, -0.2, 0, 0.2, 1],
                     data_sld_ln=ninia_hibrid, levels_sld_ln=[-0.3, 0.3],
                     data_dtd_ln=dmi_hibrid, levels_dtd_ln=[-0.3, 0.3],
                     title=f'La Niña (solid lines), Negative IOD (dotted lines), '
                           f'La Niña + negative IOD (shading)',
                     name_fig='esquema_negativo_hs_circ.png', save=save, step=1,
                     high=2.3,
                     color_dtd=['#007E72', '#B2000D'])

# ---------------------------------------------------------------------------- #