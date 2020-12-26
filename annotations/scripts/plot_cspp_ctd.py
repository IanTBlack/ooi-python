import math
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
from ooi.archived import ARCHIVED
import ooi.helpers as oh
import ooi.immutables as oi
import os

data_dir = 'C:/Users/Ian/Documents/GitHub/ooi-python/annotations/data'
fig_dir = 'C:/Users/Ian/Documents/GitHub/ooi-python/annotations/figures'
ims = [oi.CE01ISSP_CTDPF,oi.CE02SHSP_CTDPF,oi.CE06ISSP_CTDPF,oi.CE07SHSP_CTDPF]
  
def main():
    for im in ims:
        ddir = os.path.join(data_dir,im[0],im[2])
        fdir = os.path.join(fig_dir,im[0],im[2])
        os.makedirs(ddir,exist_ok=True)
        os.makedirs(fdir,exist_ok=True)
        m2m = ARCHIVED()
        if m2m.check_for_downloads(im,ddir) is True:
            files = m2m.get_filepaths(im,ddir)
        else:
            m2m = ARCHIVED()
            m2m.set_request_times()    
            r = m2m.submit_request(im)
            i = m2m.get_thredds(r)
            files = m2m.download_data(i,ddir)
        files = [os.path.join(ddir,f) for f in files]
        for file in files:
            deployment = oh.get_deployment(file)
            dataset = m2m.import_data(file)
            variables = ['time',
                         'obs',
                         'pressure',
                         'conductivity',
                         'temperature',
                         'salinity']
            df = oh.ds2df(dataset,variables,close=True)
            df = oh.sort_df(df)   
            ptest = oh.df_drop_range(df,'pressure',0,89)
            if math.isnan(ptest.pressure.mean()): #Skip CE06ISSP-0004 because the pressure data is bad.
                continue
            figname = '_'.join((im[0],im[2],deployment))
            plot_data(df,variables,fdir,figname)

def plot_data(df,variables,fdir,figname):
    df2 = df
    if 'ISSP' in figname:
        pmax = 30
    elif 'SHSP' in figname:
        pmax = 90
    df2 = oh.df_drop_range(df2,'pressure',0,pmax)
    df2 = oh.df_drop_range(df2,'salinity',2,42)
    df2 = oh.df_drop_range(df2,'temperature',0,35)   
    drops = ['time','obs','pressure']
    vs = [v for v in variables if v not in drops]    
    fig,ax = plt.subplots(len(vs)+1,1,figsize=(14,8.5),sharex=True)
    fig.subplots_adjust(left = 0.075,right=0.9,top = 0.95,bottom = 0.125,hspace = 0.2)
    for i in range(len(vs)):            
        vmin = math.floor(df2[vs[i]].min())
        vmax = math.ceil(df2[vs[i]].max())
        if vs == 'salinity':
                vmin = 28    
        p = ax[i].scatter(df2.time,df2.pressure,10,df2[vs[i]],
              label = vs[i],
              cmap='inferno',
              vmin=vmin,
              vmax=vmax)
        ypos = ax[i].get_position().y0
        cax = fig.add_axes([0.91,ypos,0.01,0.175])
        fig.colorbar(p,cax=cax,label=vs[i])      
        ax[i].set_ylabel('Pressure (dbar)')
        ax[i].invert_yaxis()
        ax[i].xaxis.set_minor_locator(MultipleLocator(1))
        ax[i].tick_params(which='minor',length=5)
        ax[i].tick_params(which='major',length=10)
    ax[i+1].plot(df2.time,df2.obs,'k.')
    ax[i+1].set_ylabel('Observation')
    ax[i+1].set_xlabel('Datetime')    
    ax[i+1].xaxis.set_minor_locator(MultipleLocator(1))
    ax[i+1].tick_params(which='minor',length=5)
    ax[i+1].tick_params(which='major',length=10)    
    fig.suptitle(figname)
    plt.savefig(os.path.join(fdir,figname) + '.png',orientation = 'landscape')
    plt.close()

if __name__ == "__main__":
    main()