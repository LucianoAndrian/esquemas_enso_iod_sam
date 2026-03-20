"""
Computo de composites CFSv2 para esquemas - prec y temp en SA
"""
# ---------------------------------------------------------------------------- #
save = True
out_dir = '/home/luciano.andrian/doc/esquemas/salidas/'
# ---------------------------------------------------------------------------- #
cases_dir = "/pikachu/datos/luciano.andrian/cases_fields/"

# ---------------------------------------------------------------------------- #
import xarray as xr
from utils.funciones_generales import init_logger

# ---------------------------------------------------------------------------- #
logger = init_logger('esq_comp_pp_t_mod.log')

# ---------------------------------------------------------------------------- #
cases_cfsv2 = ['n34_puros_pos', 'n34_puros_neg',
               'dmi_puros_pos', 'dmi_puros_neg',
               'sim_pos', 'sim_neg']

end_name_file = '_detrend_05'

for v in ['prec', 'tref']:
    logger.info(f'Variable: {v}')

    if v == 'prec':
        fix = 30
        v_in_name = v

    elif v == 'tref':
        fix = 1
        v_in_name = v

    neutro = xr.open_dataset(f'{cases_dir}{v}_neutros_SON{end_name_file}.nc')
    neutro = neutro * fix
    name_var = list(neutro.data_vars)[0]
    neutro = neutro.rename({name_var:'var'})

    aux_var = []
    logger.info('cases')
    for c in cases_cfsv2:
        logger.debug(f'Case: {c}')

        case = xr.open_dataset(f'{cases_dir}{v}_{c}_SON{end_name_file}.nc').\
            rename({name_var:'var'})

        num_case = len(case.time)
        comp = case.mean('time')*fix - neutro.mean('time')

        aux_var.append(comp)

    comps = xr.concat(aux_var, dim='case')
    comps = comps.assign_coords(case=cases_cfsv2)  # nombres de los cases como coord

    if save:
        logger.info(f'Saving {out_dir}comp_{v}_cfsv2.nc')
        comps.to_netcdf(f'{out_dir}comp_{v}_cfsv2.nc')
        del comps

# ---------------------------------------------------------------------------- #
logger.info(f'Done')
# ---------------------------------------------------------------------------- #