"""
Computo de composites obs para esquemas
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
from utils.funciones_generales import init_logger

# ---------------------------------------------------------------------------- #
logger = init_logger('esq_comp_circ_obs.log')

# ---------------------------------------------------------------------------- #
cases = ['N34_un_pos', 'N34_un_neg', 'DMI_un_pos', 'DMI_un_neg',
         'DMI_sim_pos', 'DMI_sim_neg']

results = []

for v, hpalevel in zip(['HGT200_SON_mer_d_w', 'HGT750_SON_mer_d_w'], [200,750]):
    logger.info(f'Variables {v}')

    data = xr.open_dataset(data_dir + v + '.nc')

    comps = []
    logger.info('cases')
    for c in cases:
        logger.debug(f'Case {c}')

        comp1, num_case, neutro_comp = CaseComp(
            data, 'SON', mmonth=[9,11],
            c=c,
            two_variables=False,
            data2=None,
            return_neutro_comp=True,
            nc_date_dir=nc_date_dir
        )

        comps.append(comp1)

    comps = xr.concat(comps, dim='case')
    comps = comps.assign_coords(case=cases) # nombres de los cases como coord
    comps = comps.expand_dims(level=[hpalevel]) #  dim adiconal hpa level
    results.append(comps)

ds_final = xr.concat(results, dim='level')

if save:
    logger.info(f'Saving {out_dir}comp_cir_obs.nc')
    ds_final.to_netcdf(f'{out_dir}comp_cir_obs.nc')
# ---------------------------------------------------------------------------- #