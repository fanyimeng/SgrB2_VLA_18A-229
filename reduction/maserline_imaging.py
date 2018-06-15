"""
Functions for imaging the masers and other lines
"""
import datetime
import os
import glob

from utilities import id_spws, id_spw

from tclean_cli import tclean_cli as tclean
from impbcor_cli import impbcor_cli as impbcor
from exportfits_cli import exportfits_cli as exportfits


def makefits(myimagebase, cleanup=True):
    impbcor(imagename=myimagebase+'.image', pbimage=myimagebase+'.pb', outfile=myimagebase+'.image.pbcor', overwrite=True) # perform PBcorr
    exportfits(imagename=myimagebase+'.image.pbcor', fitsimage=myimagebase+'.image.pbcor.fits', dropdeg=True, overwrite=True) # export the corrected image
    exportfits(imagename=myimagebase+'.image', fitsimage=myimagebase+'.image.fits', dropdeg=True, overwrite=True) # export the corrected image
    exportfits(imagename=myimagebase+'.pb', fitsimage=myimagebase+'.pb.fits', dropdeg=True, overwrite=True) # export the PB image
    exportfits(imagename=myimagebase+'.model', fitsimage=myimagebase+'.model.fits', dropdeg=True, overwrite=True) # export the PB image
    exportfits(imagename=myimagebase+'.residual', fitsimage=myimagebase+'.residual.fits', dropdeg=True, overwrite=True) # export the PB image

    if cleanup:
        for suffix in ('pb', 'weight', 'sumwt', 'psf',
                       'model', 'mask', 'image', 'residual',
                       'alpha', 'alpha.error'):
            os.system('rm -rf {0}.{1}'.format(myimagebase, suffix))


def myclean(
    vis,
    name,
    linename,
    spws,
    imsize=2000,
    cell='0.04arcsec',
    fields=["Sgr B2 N Q", "Sgr B2 NM Q", "Sgr B2 MS Q"],
    niter=1000,
    threshold='25mJy',
    robust=0.5,
    savemodel='none',
    **kwargs
):
    if hasattr(spws, 'items'):
        assert not isinstance(vis, str)
        spws = [spws[k] for k in vis]

    for field in fields:
        imagename = ("{name}_{field}_r{robust}_{linename}_clean1e4_{threshold}"
                     .format(name=name, field=field.replace(" ","_"),
                             robust=robust, threshold=threshold,
                             linename=linename,
                            )
                    )
        tclean(vis=vis,
               field=field,
               spw=spws,
               imsize=[imsize, imsize],
               cell=cell,
               imagename=imagename,
               niter=niter,
               threshold=threshold,
               robust=robust,
               gridder='standard',
               deconvolver='hogbom',
               specmode='cube',
               weighting='briggs',
               pblimit=0.2,
               interactive=False,
               outframe='LSRK',
               datacolumn='corrected',
               savemodel=savemodel,
               **kwargs
              )
        makefits(imagename)


# Q-band
def siov1clean(vis, name, **kwargs):
    if isinstance(vis, list):
        spws = id_spws(vis, freq=43.12203e9)
    else:
        spws = "42"
    return myclean(vis=vis, name=name, linename='SiOv=1', spws=spws, **kwargs)

def siov2clean(vis, name, **kwargs):
    if isinstance(vis, list):
        spws = id_spws(vis, freq=42.82048e9)
    else:
        spws = "39"
    return myclean(vis=vis, name=name, linename='SiOv=2', spws=spws, **kwargs)

def ch3ohmaserclean(vis, name, **kwargs):
    if isinstance(vis, list):
        spws = id_spws(vis, freq=44.06949e9)
    else:
        spws = "50"
    return myclean(vis=vis, name=name, linename='CH3OH44.1', spws=spws, **kwargs)

def ch3ohthermalclean(vis, name, **kwargs):
    if isinstance(vis, list):
        spws = id_spws(vis, freq=48.372456e9)
    else:
        spws = "20"
    return myclean(vis=vis, name=name, linename='CH3OH48.4', spws=spws, **kwargs)

def csclean(vis, name, **kwargs):
    return myclean(vis=vis, name=name, linename='CS1-0', spws="26", **kwargs)


# Ka-band
def ch3ohKamaserclean(vis, name, **kwargs):
    return myclean(vis=vis, name=name, linename='CH3OH36.1', spws="11",
                   fields=['Sgr B2 MN Ka', 'Sgr B2 MS Ka'], **kwargs)

def so10clean(vis, name, **kwargs):
    return myclean(vis=vis, name=name, linename='SO10_01', spws="56",
                   fields=['Sgr B2 MN Ka', 'Sgr B2 MS Ka'], **kwargs)

# K-band
def h2oclean(vis, name, **kwargs):
    return myclean(vis=vis, name=name, linename='H2O', spws={'../18A-229_2018_03_29_T13_19_55.276/18A-229.sb35069722.eb35251855.58206.45698415509.ms': '55',
                                                             '../18A-229_2018_03_28_T17_09_22.432/18A-229.sb35069722.eb35251150.58205.383514664354.ms': '53',
                                                            },
                   cell='0.1arcsec',
                   imsize=1000, 
                   chanchunks=16,
                   fields=['Sgr B2 MN K', 'Sgr B2 SDS K'], **kwargs)

#  3      EVLA_Q#A1C1#3     128   TOPO   46111.536        62.500      8000.0  46115.5046       10  RR  LL NH3 18-18
#  10     EVLA_Q#A1C1#10    128   TOPO   46982.796        62.500      8000.0  46986.7650       10  RR  LL PN 1-0
#  19     EVLA_Q#A2C2#19    256   TOPO   48269.070        62.500     16000.0  48277.0387       11  RR  LL H2CO 413-414
#  20     EVLA_Q#A2C2#20    512   TOPO   48351.181        62.500     32000.0  48367.1502       11  RR  LL CH3OH 101-000
#  26     EVLA_Q#A2C2#26    128   TOPO   48999.378       125.000     16000.0  49007.3158       11  RR  LL CS 1-0
#  32     EVLA_Q#A2C2#32    128   TOPO   49821.915       125.000     16000.0  49829.8525       11  RR  LL NH3 19-19
#  37     EVLA_Q#B1D1#37    128   TOPO   42504.779       125.000     16000.0  42512.7170       13  RR  LL SiO v=3
#  39     EVLA_Q#B1D1#39    512   TOPO   42805.924        31.250     16000.0  42813.9086       13  RR  LL SiO v=2
#  40     EVLA_Q#B1D1#40    128   TOPO   42825.271       125.000     16000.0  42833.2082       13  RR  LL NH3 17-17
#  42     EVLA_Q#B1D1#42    512   TOPO   43107.389        31.250     16000.0  43115.3733       13  RR  LL SiO v=1
#  45     EVLA_Q#B1D1#45    256   TOPO   43401.088       125.000     32000.0  43417.0256       13  RR  LL SiO v=0
#  50     EVLA_Q#B2D2#50    256   TOPO   44049.752       125.000     32000.0  44065.6892       14  RR  LL CH3OH maser
#  61     EVLA_Q#B2D2#61    512   TOPO   45395.577       125.000     64000.0  45427.5143       14  RR  LL H52a
#
#  2      EVLA_KA#A1C1#2     256   TOPO   35120.882        62.500     16000.0  35128.8504       10  RR  LL NH3 14-14
#  11     EVLA_KA#A1C1#11    512   TOPO   36155.702        31.250     16000.0  36163.6861       10  RR  LL CH3OH 4(-1,4)-3(0,3)
#  12     EVLA_KA#A1C1#12    512   TOPO   36259.894        62.500     32000.0  36275.8624       10  RR  LL NH3 19(18) + CH3CN 2-1
#  18     EVLA_KA#A2C2#18    256   TOPO   33143.717        62.500     16000.0  33151.6859       11  RR  LL NH3 13-13
#  26     EVLA_KA#A2C2#26    256   TOPO   34114.159        62.500     16000.0  34122.1279       11  RR  LL NH3 18(17)
#  36     EVLA_KA#B1D1#36    256   TOPO   31412.085        62.500     16000.0  31420.0535       13  RR  LL NH3 12-12
#  42     EVLA_KA#B1D1#42    256   TOPO   32206.209        62.500     16000.0  32214.1778       13  RR  LL NH3 17(16)
#  56     EVLA_KA#B2D2#56    256   TOPO   29988.912        62.500     16000.0  29996.8804       14  RR  LL SO 10-01
#  61     EVLA_KA#B2D2#61    256   TOPO   30524.706        62.500     16000.0  30532.6751       14  RR  LL NH3 16(15)
#
# 18A-229_2018_03_29_T13_19_55.276/18A-229.sb35069722.eb35251855.58206.45698415509.ms
#  2      EVLA_K#A1C1#2     256   TOPO   22776.698        31.250      8000.0  22780.6827       10  RR  LL
#  3      EVLA_K#A1C1#3     256   TOPO   22824.698        31.250      8000.0  22828.6827       10  RR  LL
#  4      EVLA_K#A1C1#4     256   TOPO   23092.810        31.250      8000.0  23096.7945       10  RR  LL
#  5      EVLA_K#A1C1#5     128   TOPO   23651.365        62.500      8000.0  23655.3336       10  RR  LL
#  6      EVLA_K#A1C1#6     256   TOPO   23684.359        62.500     16000.0  23692.3282       10  RR  LL
#  7      EVLA_K#A1C1#7     256   TOPO   23712.486        62.500     16000.0  23720.4549       10  RR  LL
#  12     EVLA_K#A1C1#12    128   TOPO   24129.187       125.000     16000.0  24137.1242       10  RR  LL
#  16     EVLA_K#A1C1#16    256   TOPO   24522.710        62.500     16000.0  24530.6788       10  RR  LL
#  26     EVLA_K#A2C2#26    256   TOPO   25704.857        62.500     16000.0  25712.8254       11  RR  LL
#  48     EVLA_K#B2D2#48    128   TOPO   21279.407        62.500      8000.0  21283.3758       14  RR  LL
#  55     EVLA_K#B2D2#55   3072   TOPO   22225.099         5.208     16000.0  22233.0969       14  RR  LL H2O, presumably....
#  58     EVLA_K#B2D2#58    128   TOPO   22646.992        62.500      8000.0  22650.9607       14  RR  LL
#
# 18A-229_2018_03_28_T17_09_22.432/18A-229.sb35069722.eb35251150.58205.383514664354.ms
#  2      EVLA_K#A1C1#2     256   TOPO   22824.717        31.250      8000.0  22828.7011       10  RR  LL
#  3      EVLA_K#A1C1#3     256   TOPO   23092.828        31.250      8000.0  23096.8128       10  RR  LL
#  4      EVLA_K#A1C1#4     256   TOPO   23684.378        62.500     16000.0  23692.3466       10  RR  LL
#  5      EVLA_K#A1C1#5     256   TOPO   23712.504        62.500     16000.0  23720.4732       10  RR  LL
#  10     EVLA_K#A1C1#10    128   TOPO   24129.205       125.000     16000.0  24137.1426       10  RR  LL
#  14     EVLA_K#A1C1#14    256   TOPO   24522.728        62.500     16000.0  24530.6972       10  RR  LL
#  24     EVLA_K#A2C2#24    256   TOPO   25704.876        62.500     16000.0  25712.8444       11  RR  LL
#  46     EVLA_K#B2D2#46    128   TOPO   21279.424        62.500      8000.0  21283.3930       14  RR  LL
#  53     EVLA_K#B2D2#53   3072   TOPO   22225.117         5.208     16000.0  22233.1141       14  RR  LL # h2o
#  56     EVLA_K#B2D2#56    128   TOPO   22647.009        62.500      8000.0  22650.9779       14  RR  LL
