"""
Tools (functions) for continuum imaging.
Not a standalone script; meant to be imported.
"""

import datetime
import shutil
import os
import glob
import re

from immath_cli import immath_cli as immath
from tclean_cli import tclean_cli as tclean
from impbcor_cli import impbcor_cli as impbcor
from exportfits_cli import exportfits_cli as exportfits
from gaincal_cli import gaincal_cli as gaincal
from applycal_cli import applycal_cli as applycal
from taskinit import casalog



def makefits(myimagebase, cleanup=True):
    if os.path.exists(myimagebase+'.image.tt0'):
        try:
            impbcor(imagename=myimagebase+'.image.tt0', pbimage=myimagebase+'.pb.tt0', outfile=myimagebase+'.image.tt0.pbcor', overwrite=True) # perform PBcorr
            exportfits(imagename=myimagebase+'.image.tt0.pbcor', fitsimage=myimagebase+'.image.tt0.pbcor.fits', dropdeg=False, overwrite=True) # export the corrected image
        except AttributeError as ex:
            print(ex)
        exportfits(imagename=myimagebase+'.image.tt1', fitsimage=myimagebase+'.image.tt1.fits', dropdeg=False, overwrite=True) # export the corrected image
        exportfits(imagename=myimagebase+'.pb.tt0', fitsimage=myimagebase+'.pb.tt0.fits', dropdeg=False, overwrite=True) # export the PB image
        exportfits(imagename=myimagebase+'.model.tt0', fitsimage=myimagebase+'.model.tt0.fits', dropdeg=False, overwrite=True) # export the PB image
        exportfits(imagename=myimagebase+'.model.tt1', fitsimage=myimagebase+'.model.tt1.fits', dropdeg=False, overwrite=True) # export the PB image
        exportfits(imagename=myimagebase+'.residual.tt0', fitsimage=myimagebase+'.residual.tt0.fits', dropdeg=False, overwrite=True) # export the PB image
        exportfits(imagename=myimagebase+'.alpha', fitsimage=myimagebase+'.alpha.fits', dropdeg=False, overwrite=True)
        exportfits(imagename=myimagebase+'.alpha.error', fitsimage=myimagebase+'.alpha.error.fits', dropdeg=False, overwrite=True)

        if cleanup:
            for ttsuffix in ('.tt0', '.tt1', '.tt2'):
                for suffix in ('pb{tt}', 'weight', 'sumwt{tt}', 'psf{tt}',
                               'model{tt}', 'mask', 'image{tt}', 'residual{tt}',
                               'alpha', 'alpha.error'):
                    # keep the model around
                    if not suffix.format(tt=ttsuffix) == 'model.tt0':
                        os.system('rm -rf {0}.{1}'.format(myimagebase, suffix).format(tt=ttsuffix))
    elif os.path.exists(myimagebase+'.image'):
        try:
            impbcor(imagename=myimagebase+'.image', pbimage=myimagebase+'.pb', outfile=myimagebase+'.image.pbcor', overwrite=True) # perform PBcorr
            exportfits(imagename=myimagebase+'.image.pbcor', fitsimage=myimagebase+'.image.pbcor.fits', dropdeg=False, overwrite=True) # export the corrected image
        except AttributeError as ex:
            print(ex)
        exportfits(imagename=myimagebase+'.pb', fitsimage=myimagebase+'.pb.fits', dropdeg=False, overwrite=True) # export the PB image
        exportfits(imagename=myimagebase+'.model', fitsimage=myimagebase+'.model.fits', dropdeg=False, overwrite=True) # export the PB image
        exportfits(imagename=myimagebase+'.residual', fitsimage=myimagebase+'.residual.fits', dropdeg=False, overwrite=True) # export the PB image

        if cleanup:
            ttsuffix=''
            for suffix in ('pb{tt}', 'weight', 'sumwt{tt}', 'psf{tt}',
                           'model{tt}', 'mask', 'image{tt}', 'residual{tt}',
                           'alpha', 'alpha.error'):
                os.system('rm -rf {0}.{1}'.format(myimagebase, suffix).format(tt=ttsuffix))
    else:
        raise IOError("No image file found matching {0}".format(myimagebase))


def myclean(
    vis,
    name,
    spws="2,4,5,6,7,8,9,11,12,13,14,15,16,17,18,21,22,23,24,25,27,28,29,30,31,33,34,35,36,38,41,43,44,46,47,48,49,51,52,53,54,55,56,57,58,59,60,62,63,64",
    imsize=8000,
    cell='0.01arcsec',
    fields=["Sgr B2 N Q", "Sgr B2 NM Q", "Sgr B2 MS Q", "Sgr B2 S Q", "Sgr B2 DS1 Q", "Sgr B2 DS2 Q", "Sgr B2 DS3 Q",],
    niter=10000,
    threshold='0.75mJy',
    robust=0.5,
    savemodel='none',
    gridder='standard',
    phasecenters=None,
    mask='',
    scales=[],
    datacolumn='corrected',
    noneg=True,
    cleanup=True,
    **kwargs
):
    for field in fields:
        imagename = ("{name}_{field}_r{robust}_allcont_clean1e4_{threshold}"
                     .format(name=name, field=field.replace(" ","_"),
                             robust=robust, threshold=threshold)
                    )
        if phasecenters is not None:
            phasecenter = phasecenters[field]
        else:
            phasecenter = ''

        if not os.path.exists(imagename+".image.tt0.pbcor.fits"):
            rslt = tclean(vis=vis,
                          field=field,
                          spw=spws,
                          imsize=[imsize, imsize],
                          cell=cell,
                          imagename=imagename,
                          niter=niter,
                          threshold=threshold,
                          phasecenter=phasecenter,
                          robust=robust,
                          gridder=gridder,
                          deconvolver='mtmfs',
                          specmode='mfs',
                          nterms=2,
                          weighting='briggs',
                          pblimit=0.1,
                          interactive=False,
                          outframe='LSRK',
                          datacolumn=datacolumn,
                          savemodel=savemodel,
                          scales=scales,
                          mask=mask,
                          **kwargs
                         )
            makefits(imagename, cleanup=cleanup)
        else:
            casalog.post("Skipping {0}".format(imagename), origin='myclean')

        if noneg and os.path.exists(imagename+".model.tt0"):
            noneg_model(modelname=imagename+".model.tt0",
                        ms=vis,
                        imagename=imagename,
                        imsize=[imsize, imsize],
                        cell=cell,
                        phasecenter=phasecenter,
                        gridder=gridder,
                        robust=robust,
                        scales=scales,
                        **kwargs
                       )


def noneg_model(modelname, ms, imagename, **kwargs):
    """
    Given a model image, set all model components positive, then ft them into
    the ms's model column
    """
    if os.path.exists(modelname+".positive"):
        shutil.rmtree(modelname+".positive")

    immath(imagename=modelname,
           expr='iif(IM0<0, 0.0, IM0)',
           outfile=modelname+".positive",
          )

    if os.path.exists(modelname):
        if os.path.exists(modelname+".old"):
            shutil.rmtree(modelname+".old")
        os.rename(modelname, modelname+".old")

    tclean(vis=ms,
           imagename=imagename,
           startmodel=modelname+".positive",
           niter=0,
           deconvolver='mtmfs',
           specmode='mfs',
           nterms=1,
           calcpsf=False,
           calcres=False,
           interactive=False,
           savemodel='modelcolumn',
           **kwargs
          )

name_regex = re.compile('18A-229_2018_([0-9][0-9])_([0-9][0-9])_T([0-9][0-9])_[0-9][0-9]_[0-9][0-9].[0-9][0-9][0-9]')

def mygaincal(vis, name_regex=name_regex, caltable=None, **kwargs):
    if isinstance(vis, list) or isinstance(vis, tuple):
        for onems in vis:
            matches = name_regex.search(onems)
            assert matches.groups() is not None
            mon,day,hr = matches.groups()
            caltable_ = "{0}_{1}_T{2}_{3}".format(mon,day,hr,caltable)
            if not os.path.exists(caltable_):
                gaincal(vis=onems, caltable=caltable_, **kwargs)
    else:
        casalog.post("FAILURE: bad vis input {0}".format(vis),
                     origin='mygaincal', priority='SEVERE')
        raise ValueError

def myapplycal(vis, name_regex=name_regex, gaintable=None, **kwargs):
    assert len(gaintable) == 1
    if isinstance(vis, list) or isinstance(vis, tuple):
        for onems in vis:
            matches = name_regex.search(onems)
            assert matches.groups() is not None
            mon,day,hr = matches.groups()
            caltable = gaintable[0]
            caltable_ = "{0}_{1}_T{2}_{3}".format(mon,day,hr,caltable)
            if os.path.exists(caltable_):
                applycal(vis=onems, gaintable=[caltable_], **kwargs)
            else:
                casalog.post("FAILURE: table {0} not found".format(caltable_),
                             origin='myapplycal', priority='SEVERE')
                raise IOError("No such table {0}".format(caltable_))
    else:
        casalog.post("FAILURE: bad vis input {0}".format(vis),
                     origin='myapplycal', priority='SEVERE')
        raise ValueError
