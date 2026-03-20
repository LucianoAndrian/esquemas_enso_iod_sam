"""
Computo de composites CFSv2 para esquemas - prec y temp en SA
"""
# ---------------------------------------------------------------------------- #
save = True
out_dir = '/home/luciano.andrian/doc/esquemas/salidas/'

# ---------------------------------------------------------------------------- #
data_dir = '/pikachu/datos/luciano.andrian/observado/ncfiles/ERA5/1940_2020/'
#index_dir = '/pikachu/datos/luciano.andrian/DMI_N34_Leads_r/'

nc_date_dir = '/pikachu/datos/luciano.andrian/observado/ncfiles/' \
              'nc_composites_dates_no_ind_sst_anom/' #fechas

# ---------------------------------------------------------------------------- #
import xarray as xr
from utils.funciones import CaseComp
from utils.funciones_generales import init_logger, OpenObsDataSet

# ---------------------------------------------------------------------------- #
logger = init_logger('esq_comp_pp_t_obs.log')

# ---------------------------------------------------------------------------- #
cases = ['N34_un_pos', 'N34_un_neg', 'DMI_un_pos', 'DMI_un_neg',
         'DMI_sim_pos', 'DMI_sim_neg']

results = []
for v in ['prec', 'temp']:
    logger.info(f'Variable: {v}')
    if v == 'prec':
        v_name = 'ppgpcc_w_c_d_1'

    elif v == 'temp':
        v_name = 'tcru_w_c_d_0.25'

    logger.debug('using Opendataset')
    data = OpenObsDataSet(name=f'{v_name}_SON', sa=True)
    if v == 'prec':
        lon = data.lon.values
        lat = data.lat.values

    if v == 'prec':
        lon = data.lon.values
        lat = data.lat.values

    aux_var = []
    logger.info('cases')
    for c in cases:
        logger.debug(f'Cases {c}')

        comp1, num_case, neutro_comp = CaseComp(
            data, 'SON', mmonth=[9,11],
            c=c,
            two_variables=False,
            data2=None,
            return_neutro_comp=True,
            nc_date_dir=nc_date_dir
        )

        if v == 'temp':
            comp1 = comp1.sel(lat=slice(None, None, -1))
            comp1 = comp1.interp(lon=lon, lat=lat)

        aux_var.append(comp1)

    comps = xr.concat(aux_var, dim='case')
    comps = comps.assign_coords(case=cases)  # nombres de los cases como coord
    results.append(comps)

    ds_final = xr.concat(results, dim='level')


if save:
    logger.info(f'Saving {out_dir}comp_pp_t_obs.nc')
    ds_final.to_netcdf(f'{out_dir}comp_pp_t_obs.nc')

# ---------------------------------------------------------------------------- #
logger.info(f'Done')
# ---------------------------------------------------------------------------- #