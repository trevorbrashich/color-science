import color
import numpy

"""
   title:: 
        xyz2srgb

   description::
         This method calls in the X, Y, Z tuple from the spectrum2xyz
         method and performs a linear transformation of the CIE matrix
         and the downscaled XYZ tristimulus values.It then computes
         where the RBG values are on the piecewise function which
         corrects for 2.4 gamma
   attributes::
      tristimulus
         A tuple returned from spectrum2xyz used to compute the 
         method xyz2sRGB.

   returns::
         tuple of X,Y,Z from spectrum2xyz and the sRGB factors
         in range [0,1]
   author::
      Trevor Brashich
"""



def xyz2srgb(tristimulus):
   matrix = numpy.matrix([[ 3.2404542, -1.5371385, -0.4985314],
                          [-0.9692660,  1.8760108,  0.0415560],
                          [ 0.0556434, -0.2040259,  1.0572252]])
   xyz = numpy.matrix(tristimulus).T
   XYZ = xyz / 100

   RGBLin = matrix * XYZ
   sRGB = RGBLin
    
   index = numpy.where(RGBLin <= 0.0031308)
   if len(index[0]) != 0:
      sRGB[index] = RGBLin[index] * 12.92

   index = numpy.where(RGBLin > 0.0031308)
   if len(index[0]) != 0:
      a = 0.055
      sRGB[index] = (1 + a) * numpy.array(RGBLin[index])**(1/2.4) - a

   sRGB = numpy.clip(sRGB, 0, 1)
   return sRGB[0,0], sRGB[1,0], sRGB[2,0]


if __name__ == '__main__':

   import color

   filename = 'real1.csv'

   array = numpy.loadtxt(filename, delimiter = ',', skiprows = 1)
   wavelengths = array[:,0]
   reflectances = array[:,1]

   tristimulus = color.spectrum2xyz(wavelengths,
                                    reflectances,
                                    illuminant='d65',
                                    observer='2deg')

   sRGB = color.xyz2srgb(tristimulus)

   print('X = {0}'.format(tristimulus[0]))
   print('Y = {0}'.format(tristimulus[1]))
   print('Z = {0}'.format(tristimulus[2]))
   print('')
   print('R = {0}'.format(sRGB[0]))
   print('G = {0}'.format(sRGB[1]))
   print('B = {0}'.format(sRGB[2]))

