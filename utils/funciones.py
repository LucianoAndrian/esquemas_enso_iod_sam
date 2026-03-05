"""
Funciones para composite
(from https://github.com/LucianoAndrian/ENSO_IOD/)
"""
# ---------------------------------------------------------------------------- #
import numpy as np
import xarray as xr

# ---------------------------------------------------------------------------- #
def CompositeSimple(original_data, index, mmin, mmax):
    def is_months(month, mmin, mmax):
        return (month >= mmin) & (month <= mmax)

    if len(index) != 0:
        comp_field = original_data.sel(
            time=original_data.time.dt.year.isin([index]))
        comp_field = comp_field.sel(
            time=is_months(month=comp_field['time.month'], mmin=mmin, mmax=mmax))
        if len(comp_field.time) != 0:
            comp_field = comp_field.mean(['time'], skipna=True)
        else:  # si sólo hay un año
            comp_field = comp_field.drop_dims(['time'])

        return comp_field
    else:
        print(' len index = 0')

def CaseComp(data, s, mmonth, c, two_variables=False, data2=None,
             return_neutro_comp=False, nc_date_dir='None'):
    """
    Las fechas se toman del periodo 1920-2020 basados en el DMI y N34 con ERSSTv5
    Cuando se toman los periodos 1920-1949 y 1950_2020 las fechas que no pertencen
    se excluyen de los composites en CompositeSimple()
    """
    mmin = mmonth[0]
    mmax = mmonth[-1]

    aux = xr.open_dataset(nc_date_dir + '1920_2020' + '_' + s + '.nc')
    neutro = aux.Neutral

    try:
        case = aux[c]
        case = case.where(case >= 1940)
        aux.close()

        case_num = len(case.values[np.where(~np.isnan(case.values))])
        case_num2 = case.values[np.where(~np.isnan(case.values))]

        neutro_comp = CompositeSimple(original_data=data, index=neutro,
                                      mmin=mmin, mmax=mmax)
        data_comp = CompositeSimple(original_data=data, index=case,
                                    mmin=mmin, mmax=mmax)

        comp = data_comp - neutro_comp

        if two_variables:
            neutro_comp2 = CompositeSimple(original_data=data2, index=neutro,
                                           mmin=mmin, mmax=mmax)
            data_comp2 = CompositeSimple(original_data=data2, index=case,
                                         mmin=mmin, mmax=mmax)

            comp2 = data_comp2 - neutro_comp2
        else:
            comp2 = None
    except:
        print('Error en ' + s + c)

    if two_variables:
        if return_neutro_comp:
            return comp, case_num, comp2, neutro_comp, neutro_comp2
        else:
            return comp, case_num, comp2
    else:
        if return_neutro_comp:
            return comp, case_num, neutro_comp
        else:
            return comp, case_num
