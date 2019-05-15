import numpy
import color
"""
   title:: 
      spectrum2xyz

   description::
         This method take an array of wavelengths and reflectances
         that were provided and imported and calculates the expected
         xbars, ybars, and zbars at each wavelength based on a reference
         CIE observer. It the uses the illuminant powers from another
         CIE reference illuminant array and calculates the XYZ coordinates

   attributes::
      wavelengths
         An numpy array of wavelengths provided from an outside file
         that is provide, which is real1.csv.
      reflectances
         A numpy array of reflectances of the provided
         wavelengths from the real1.csv
      illuminant
         Array  composed of illuminant powers and wavelengths
         from the CIE Reference Illuminant 

      observer
         A array  of chromatic responses from a CIE Standard Observer 
         at certain wavelengths. The default is 2 degrees.

   returns::
         Returns the converted X, Y, Z tristimulus values as a tuple based on the 
         wavelengths and reflectances provided.
 
   author::
      Trevor Brashich
"""


def spectrum2xyz(wavelengths, reflectances, illuminant = 'd65', observer = '2deg'):
   obs = color.CIEStandardObserver(observerType='2deg')
   ill = color.CIEReferenceIlluminant(illuminantType = illuminant)
   Xbar = color.interp1(obs.wavelengths, obs.xbars, wavelengths)  
   Ybar =  color.interp1(obs.wavelengths, obs.ybars, wavelengths) 
   Zbar = color.interp1(obs.wavelengths, obs.zbars, wavelengths)

   power = color.interp1(ill.wavelengths, ill.powers, wavelengths)
   N = numpy.sum(power*Ybar) 
   X = numpy.sum(Xbar*reflectances*power) / N
   Y = numpy.sum(Ybar*reflectances*power) / N
   Z = numpy.sum(Zbar*reflectances*power) / N
   return X, Y, Z
   
if __name__ == '__main__':

   import color

   filename = 'real1.csv'

   numpy.array = numpy.loadtxt(filename, delimiter = ',', skiprows = 1)
   wavelengths = numpy.array[:,0]
   reflectances = numpy.array[:,1]
  
   X, Y, Z = color.spectrum2xyz(wavelengths, 
                                reflectances,
                                illuminant='d65',
                                observer='2deg')

   print('X = {0}'.format(X))
   print('Y = {0}'.format(Y))
   print('Z = {0}'.format(Z))

