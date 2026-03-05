"""
Computo de composites CFSv2 para esquemas
"""
# ---------------------------------------------------------------------------- #
save = True
out_dir = '/home/luciano.andrian/doc/esquemas/salidas/'
# ---------------------------------------------------------------------------- #
cases_dir = "/pikachu/datos/luciano.andrian/cases_fields/"

# ---------------------------------------------------------------------------- #
import xarray as xr
from utils.funciones_generales import Weights
from utils.funciones_generales import init_logger

# ---------------------------------------------------------------------------- #
logger = init_logger('esq_comp_circ_mod.log')

# ---------------------------------------------------------------------------- #
cases_cfsv2 = ['n34_puros_pos', 'n34_puros_neg',
               'dmi_puros_pos', 'dmi_puros_neg',
               'sim_pos', 'sim_neg']

neutro = xr.open_dataset(cases_dir + 'hgt_neutros_SON_05.nc') \
    .rename({'hgt': 'var'})
neutro = Weights(neutro.__mul__(9.80665))

aux_hgt = []
logger.info('cases')
for c in cases_cfsv2:
    logger.debug(f'Case {c}')
    case = xr.open_dataset(cases_dir + 'hgt_' + c + '_SON_05.nc'). \
        rename({'hgt': 'var'})
    case = Weights(case.__mul__(9.80665))
    num_case = len(case.time)
    comp = case.mean('time') - neutro.mean('time')

    spread = case - comp
    spread = spread.std('time')

    aux_hgt.append(comp)

comps = xr.concat(aux_hgt, dim='case')
comps = comps.assign_coords(case=cases_cfsv2)  # nombres de los cases como coord

if save:
    logger.info(f'Saving {out_dir}comp_cir_cfsv2.nc')
    comps.to_netcdf(f'{out_dir}comp_cir_cfsv2.nc')
# ---------------------------------------------------------------------------- #
