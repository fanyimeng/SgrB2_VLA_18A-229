"""
Script to create merged images of the masers and other lines
"""

from maserline_imaging import (myclean, tclean, makefits, siov1clean,
                               siov2clean, ch3ohmaserclean, ch3ohthermalclean,
                               csclean, so10clean, ch3ohKamaserclean,
                               h2oclean,
                              )
from ms_lists import Qmses, Kamses, Kmses


siov1clean(['../'+x for x in Qmses], name='18A-229_combined', threshold='25mJy')
siov2clean(['../'+x for x in Qmses], name='18A-229_combined', threshold='25mJy')
ch3ohmaserclean(['../'+x for x in Qmses], name='18A-229_combined', threshold='25mJy')
ch3ohthermalclean(['../'+x for x in Qmses], name='18A-229_combined', threshold='25mJy')
#csclean(['../'+x for x in Qmses], name='18A-229_combined', threshold='25mJy')

#ch3ohmaserclean(['../'+x for x in mses], name='18A-229_combined', threshold='25mJy',
#                fields=["Sgr B2 S Q", "Sgr B2 DS1 Q", "Sgr B2 DS2 Q", "Sgr B2 DS3 Q",])

#for ms in mses:
#
#    name = ms[:22]
#
#    siov1clean('../'+ms, name=name, threshold='50mJy',)



#ch3ohKamaserclean(['../'+x for x in Kamses], name='18A-229_combined', threshold='25mJy')
#so10clean(['../'+x for x in Kamses], name='18A-229_combined', threshold='25mJy')


#h2oclean(['../'+x for x in Kmses], name='18A-229_combined', threshold='25mJy')
