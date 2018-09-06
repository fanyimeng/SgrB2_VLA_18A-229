"""
Script to create merged images of the masers and other lines
"""
import sys
sys.path.append('.')
assert os.getenv('SCRIPT_DIR') is not None
sys.path.append(os.getenv('SCRIPT_DIR'))

from maserline_imaging import (myclean, tclean, makefits, siov1clean,
                               siov2clean, ch3ohmaserclean, ch3ohthermalclean,
                               csclean, so10clean, ch3ohKamaserclean,
                               h2oclean, nh311clean, nh322clean, nh321clean,
                               nh332clean, nh31918clean, nh31212clean,
                               nh31313clean, nh31414clean, nh31817clean,
                               nh31716clean, nh31615clean, nh344clean,
                               nh355clean, nh377clean, nh353clean, nh354clean,
                               nh365clean,
                              )
from ms_lists import Qmses, Kamses, Kmses


#siov1clean(['../'+x for x in Qmses], name='18A-229_combined', threshold='25mJy')
#siov2clean(['../'+x for x in Qmses], name='18A-229_combined', threshold='25mJy')
#ch3ohmaserclean(['../'+x for x in Qmses], name='18A-229_combined', threshold='25mJy')
#ch3ohthermalclean(['../'+x for x in Qmses], name='18A-229_combined', threshold='25mJy')
#csclean(['../'+x for x in Qmses], name='18A-229_combined', threshold='25mJy')

#ch3ohmaserclean(['../'+x for x in mses], name='18A-229_combined', threshold='25mJy',
#                fields=["Sgr B2 S Q", "Sgr B2 DS1 Q", "Sgr B2 DS2 Q", "Sgr B2 DS3 Q",])

#for ms in Qmses:
#
#    name = ms[:22]
#
#    ch3ohmaserclean('../'+ms, name=name, threshold='50mJy',)



#ch3ohKamaserclean(['../'+x for x in Kamses], name='18A-229_combined', threshold='25mJy')
#so10clean(['../'+x for x in Kamses], name='18A-229_combined', threshold='25mJy')
#nh31918clean(['../'+x for x in Kamses], name='18A-229_combined', threshold='25mJy')
#nh31212clean(['../'+x for x in Kamses], name='18A-229_combined', threshold='25mJy')
#nh31313clean(['../'+x for x in Kamses], name='18A-229_combined', threshold='25mJy')
#nh31414clean(['../'+x for x in Kamses], name='18A-229_combined', threshold='25mJy')
#nh31817clean(['../'+x for x in Kamses], name='18A-229_combined', threshold='25mJy')
#nh31716clean(['../'+x for x in Kamses], name='18A-229_combined', threshold='25mJy')
#nh31615clean(['../'+x for x in Kamses], name='18A-229_combined', threshold='25mJy')


#h2oclean(['../'+x for x in Kmses], name='18A-229_combined', threshold='25mJy')
nh322clean(['../'+x for x in Kmses], name='18A-229_combined', threshold='25mJy')
nh311clean(['../'+x for x in Kmses], name='18A-229_combined', threshold='25mJy')
nh321clean(['../'+x for x in Kmses], name='18A-229_combined', threshold='25mJy')
nh332clean(['../'+x for x in Kmses], name='18A-229_combined', threshold='25mJy')
nh344clean(['../'+x for x in Kmses], name='18A-229_combined', threshold='25mJy')
nh355clean(['../'+x for x in Kmses], name='18A-229_combined', threshold='25mJy')
nh377clean(['../'+x for x in Kmses], name='18A-229_combined', threshold='25mJy')
nh353clean(['../'+x for x in Kmses], name='18A-229_combined', threshold='25mJy')
nh354clean(['../'+x for x in Kmses], name='18A-229_combined', threshold='25mJy')
nh365clean(['../'+x for x in Kmses], name='18A-229_combined', threshold='25mJy')
