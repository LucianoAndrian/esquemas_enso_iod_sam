"""
Funciones para plotear esquemas
"""
# ---------------------------------------------------------------------------- #
import matplotlib.pyplot as plt
import cartopy.feature
import cartopy.crs as ccrs

from scipy.signal import convolve2d

# ---------------------------------------------------------------------------- #
def plot_esquema_circ_hs(data_shd=None, levels_shd=None,
                         data_sld_ln=None, levels_sld_ln=None,
                         data_dtd_ln=None, levels_dtd_ln=None,
                         title='title', name_fig = 'name',
                         out_dir='out_dir', save = False,
                         step = 1, high=3.5,
                         color_shd=['dodgerblue', 'white', 'white', 'firebrick'],
                         color_sld=['Blue', 'Red'],
                         color_dtd=['#00B0CC', '#D00038']):
    width = 7

    if save:
        dpi = 300
    else:
        dpi = 100

    crs_latlon = ccrs.PlateCarree()

    fig = plt.figure(figsize=(width, high), dpi=dpi)
    ax = plt.axes(projection=ccrs.PlateCarree(central_longitude=180))
    ax.set_extent([0, 359, -80, 20], crs=crs_latlon)

    try:
        data_shd_name_var = list(data_shd.data_vars)[0]
        data_var = data_shd[data_shd_name_var]
        ax.contourf(data_shd.lon[::step], data_shd.lat[::step],
                    data_var[::step, ::step],
                    linewidths=1, alpha=.4, levels=levels_shd,
                    transform=crs_latlon,
                    colors=color_shd)
    except:
        pass

    try:
        data_sld_ln_name_var = list(data_sld_ln.data_vars)[0]
        data_sld_ln_var = data_sld_ln[data_sld_ln_name_var]
        ax.contour(data_sld_ln.lon[::step], data_sld_ln.lat[::step],
                   data_sld_ln_var[::step, ::step],
                   linewidths=1.5, alpha=.7, levels=levels_sld_ln,
                   transform=crs_latlon, colors=color_sld)
    except:
        pass

    try:
        data_dtd_ln_name_var = list(data_dtd_ln.data_vars)[0]
        data_dtd_ln_var = data_dtd_ln[data_dtd_ln_name_var]
        ax.contour(data_dtd_ln.lon[::step], data_dtd_ln.lat[::step],
                   data_dtd_ln_var[::step, ::step],
                   linewidths=1.2, alpha=0.8, levels=levels_dtd_ln,
                   linestyles='dashed',
                   transform=crs_latlon, colors=color_dtd)
    except:
        pass

    ax.add_feature(cartopy.feature.LAND, facecolor='white', edgecolor='grey')
    ax.add_feature(cartopy.feature.COASTLINE, linewidth=0.5)
    ax.coastlines(color='grey', linestyle='-', alpha=1)

    fig.text(0.5, 0.025, title, ha='center', fontsize=8)

    for spine in ax.spines.values():
        spine.set_linewidth(0.5)

    fig.subplots_adjust(bottom=0.1, wspace=0, hspace=0.25, left=0.01,
                        right=0.99, top=0.975)
    if save:
        print(f'save: {out_dir}{name_fig}' )
        plt.savefig(f'{out_dir}{name_fig}', dpi=dpi)
        plt.close()

    else:
        plt.show()

# ---------------------------------------------------------------------------- #
def plot_esquema_pp_t_sa(data_shd=None, levels_shd=None,
                         data_sld_ln=None, levels_sld_ln=None,
                         data_dtd_ln=None, levels_dtd_ln=None,
                         title='title', name_fig = 'name',
                         out_dir='out_dir', save = False,
                         step = 1, high=3.5,
                         color_shd=['dodgerblue', 'white', 'white', 'firebrick'],
                         color_sld=['Blue', 'Red'],
                         color_dtd=['#00B0CC', '#D00038']):

    width = 3

    if save:
        dpi = 300
    else:
        dpi = 100

    crs_latlon = ccrs.PlateCarree()

    fig = plt.figure(figsize=(width, high), dpi=dpi)
    ax = plt.axes(projection=ccrs.PlateCarree(central_longitude=180))
    ax.set_extent([275, 330, -60, 20], crs=crs_latlon)

    try:
        try:
            data_shd_name_var = list(data_shd.data_vars)[0]
            data_var = data_shd[data_shd_name_var]
        except:
            data_var = data_shd

        ax.contourf(data_shd.lon[::step], data_shd.lat[::step],
                    data_var[::step, ::step],
                    linewidths=0, alpha=1, levels=levels_shd,
                    transform=crs_latlon,
                    colors=color_shd)
    except:
        pass

    try:
        try:
            data_sld_ln_var = list(data_sld_ln.data_vars)[0]
            data_sld_ln_var = data_sld_ln[data_sld_ln_var]
        except:
            data_sld_ln_var = data_sld_ln

        ax.contour(data_sld_ln.lon[::step], data_sld_ln.lat[::step],
                   data_sld_ln_var[::step, ::step],
                   linewidths=1, alpha=1, levels=levels_sld_ln,
                   transform=crs_latlon, colors=color_sld)
    except:
        pass

    try:
        try:
            data_dtd_ln_var = list(data_dtd_ln.data_vars)[0]
            data_dtd_ln_var = data_dtd_ln[data_dtd_ln_var]
        except:
            data_dtd_ln_var = data_dtd_ln

        ax.contour(data_dtd_ln.lon[::step], data_dtd_ln.lat[::step],
                   data_dtd_ln_var[::step, ::step],
                   linewidths=1.2, alpha=0.8, levels=levels_dtd_ln,
                   linestyles='dashed',
                   transform=crs_latlon, colors=color_dtd)
    except:
        pass

    ax.add_feature(cartopy.feature.LAND, facecolor='white', edgecolor='grey')
    ax.add_feature(cartopy.feature.COASTLINE, linewidth=0.5)
    ax.coastlines(color='grey', linestyle='-', alpha=1)

    fig.text(0.5, 0.025, title, ha='center', fontsize=8)

    for spine in ax.spines.values():
        spine.set_linewidth(0.5)

    fig.subplots_adjust(bottom=0.1, wspace=0, hspace=0.25, left=0.01,
                        right=0.99, top=0.975)
    if save:
        print(f'save: {out_dir}{name_fig}' )
        plt.savefig(f'{out_dir}{name_fig}', dpi=dpi)
        plt.close()

    else:
        plt.show()

# ---------------------------------------------------------------------------- #