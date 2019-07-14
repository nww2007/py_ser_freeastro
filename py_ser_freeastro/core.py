#!/usr/bin/env python3
# vim:fileencoding=UTF-8
# -*- coding: UTF-8 -*-

"""
Created on 15 juny 2019 y.

@author: Vlsdimir Nekrasov nww2007@mail.ru
"""


import sys
import struct
import numpy as np
from progress.bar import Bar
import logging
logging.basicConfig(format = u'%(filename)s:%(lineno)d: %(levelname)-8s [%(asctime)s] %(message)s', level = logging.DEBUG, stream=sys.stdout)


# class ser(np.array):
class ser(object):
    """
    A set of methods for working with a set of images in the SER format.
    """
    def __init__(self, fname):
        """
        Download information from file.
        """
#         super.__init__()

        # luids 
        self.MONO       = 0
        self.BAYER_RGGB = 8
        self.BAYER_GRBG = 9
        self.BAYER_GBRG = 10
        self.BAYER_BGGR = 11
        self.BAYER_CYYM = 16
        self.BAYER_YCMY = 17
        self.BAYER_YMCY = 18
        self.BAYER_MYYC = 19
        self.RGB        = 100
        self.BGR        = 101

        self.fname = fname

        with open(self.fname, 'rb') as fd:
            # Download information from the header.
            self.header = fd.read(178)
            self.parse_header()

            # Download images.
            self.frames = np.zeros((self.framecount, self.imageheight, self.imagewidth))
            bar = Bar('Downloading', max=self.framecount)
            for frame in range(self.framecount):
#             for frame in range(1):
                bar.next()
                t_frame = fd.read(self.imageheight * self.imagewidth * self.pixeldepthperplane//8)
                for line in range(self.imageheight):
                    for pixel in range(self.imagewidth):
                        index = (line * self.imagewidth + pixel) * 2
                        self.frames[frame][line][pixel] = struct.unpack('<H', t_frame[index:index+2])[0]
            bar.finish()

            # Download the trailer
            self.trailer = fd.read(self.framecount * 8)
            self.parse_trailer()


    def parse_header(self):
        """
        Parse the title.
        """
        self.fileid             = self.header[0:14]
        self.luid               = struct.unpack('<i', self.header[14:18])[0]
        self.colorid            = struct.unpack('<i', self.header[18:22])[0]
        self.littleendian_FALSE = 0
        self.littleendian_TRUE  = 1
        self.littleendian       = struct.unpack('<i', self.header[22:26])[0]
        self.imagewidth         = struct.unpack('<i', self.header[26:30])[0]
        self.imageheight        = struct.unpack('<i', self.header[30:34])[0]
        self.pixeldepthperplane = struct.unpack('<i', self.header[34:38])[0]
        self.framecount         = struct.unpack('<i', self.header[38:42])[0]
        self.observer           = self.header[42:82]
        self.telescope          = self.header[82:122]
        self.datetime           = struct.unpack('<q', self.header[122:130])[0]
        self.datetime_utc       = struct.unpack('<q', self.header[130:138])[0]
#         logging.info('{0}x{1}'.format(self.imagewidth, self.imageheight))


    def parse_trailer(self):
        """
        Parse the trailer
        """
        for i in range(0, self.framecount*8, 8):
            tuli = (struct.unpack('<Q', self.trailer[i:i+8])[0])


def main(argv):
    logging.info('%s started.\n' % argv[0])

    fn  = './images/ASICAP_2019-05-10_01_43_36_523.SER'

    frames = ser(fn)
#     logging.debug(type(frames))
#     logging.debug(type(object))

# #     darks_fn   = './images/ASICAP_2019-05-10_02_12_00_621.SER'
# #     offsets_fn = './images/ASICAP_2019-05-10_02_30_47_294.SER'
# 
# #     frames = ser.ser()
# #     frames.read(darks_fn)
# #     frames.read(lights_fn)
# #     ser_fr = serialise_frames(frames)
# #     logging.debug('std1={}'.format(ser_fr.std()))
# #     hist_fr = get_hist(ser_fr)
# #     plt.plot(hist_fr)
# #     plt.grid()
# #     plt.show()
# 
#     fnames = [
#             '/home/nww/ASICAP/tmp/ASICAP_2019-05-25_15_34_52_584.SER',
#             '/home/nww/ASICAP/tmp/ASICAP_2019-05-25_15_36_05_343.SER',
#             '/home/nww/ASICAP/tmp/ASICAP_2019-05-25_15_37_34_373.SER',
#             '/home/nww/ASICAP/tmp/ASICAP_2019-05-25_15_37_47_276.SER',
#             '/home/nww/ASICAP/tmp/ASICAP_2019-05-25_15_37_58_784.SER',
#             '/home/nww/ASICAP/tmp/ASICAP_2019-05-25_15_39_06_703.SER',
#             '/home/nww/ASICAP/tmp/ASICAP_2019-05-25_15_39_17_476.SER',
#             '/home/nww/ASICAP/tmp/ASICAP_2019-05-25_15_39_27_330.SER',
#             '/home/nww/ASICAP/tmp/ASICAP_2019-05-25_15_39_36_623.SER',
#             '/home/nww/ASICAP/tmp/ASICAP_2019-05-25_15_39_48_239.SER',
#             '/home/nww/ASICAP/tmp/ASICAP_2019-05-25_15_40_20_816.SER',
#             '/home/nww/ASICAP/tmp/ASICAP_2019-05-25_15_40_32_118.SER',
#             '/home/nww/ASICAP/tmp/ASICAP_2019-05-25_15_40_47_796.SER',
#             '/home/nww/ASICAP/tmp/ASICAP_2019-05-25_15_40_59_999.SER',
#             '/home/nww/ASICAP/tmp/ASICAP_2019-05-25_15_41_10_321.SER',
#             '/home/nww/ASICAP/tmp/ASICAP_2019-05-25_15_41_41_276.SER',
#             '/home/nww/ASICAP/tmp/ASICAP_2019-05-25_15_42_07_956.SER',
#             '/home/nww/ASICAP/tmp/ASICAP_2019-05-25_15_42_19_287.SER',
#             '/home/nww/ASICAP/tmp/ASICAP_2019-05-25_15_42_31_180.SER',
#             '/home/nww/ASICAP/tmp/ASICAP_2019-05-25_15_42_43_981.SER',
#             '/home/nww/ASICAP/tmp/ASICAP_2019-05-25_15_43_07_152.SER',
#             '/home/nww/ASICAP/tmp/ASICAP_2019-05-25_15_43_36_180.SER',
#             '/home/nww/ASICAP/tmp/ASICAP_2019-05-25_15_44_01_167.SER',
#             '/home/nww/ASICAP/tmp/ASICAP_2019-05-25_15_44_33_214.SER',
#             '/home/nww/ASICAP/tmp/ASICAP_2019-05-25_15_44_58_952.SER',
#     ]
# 
#     print('{};{};{};{};{}'.format('File', 'Temperature', 'Exposure', 'Gain', 'std'))
#     for fn in fnames:
#         print('{}'.format(fn), flush=True, file=sys.stderr)
#         frames = ser.ser()
#         frames.read(fn)
#         ser_fr = serialise_frames(frames)
# 
#         config = configparser.ConfigParser()
#         config.read(fn + '.txt')
# 
#         print('{};{};{};{};{}'.format(fn, config['ZWO ASI120MC']['temperature'], config['ZWO ASI120MC']['exposure'], config['ZWO ASI120MC']['gain'], ser_fr.std()))

    logging.info('%s finished.\n' % argv[0])
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))

