import sys
import numpy as np
from netCDF4 import Dataset
from util.Interpolator import Interp2D, Interp3D, depths
from util.Wacomm import Wacomm


if __name__ == '__main__':
    if len(sys.argv) != 5:
        print("Usage: python " + str(sys.argv[0]) + " initialization_date source_file history_dir destination_file")
        sys.exit(-1)

    iDate = sys.argv[1]
    src = sys.argv[2]
    history_dir = sys.argv[3]
    dst = sys.argv[4]

    print("iDate:" + iDate + " src: " + src + " history: " + history_dir + " dst: " + dst)

    # Open the NetCDF file
    ncsrcfile = Dataset(src)

    # Read variables
    time = ncsrcfile.variables["ocean_time"][:]
    Xlat = ncsrcfile["lat_rho"][:]
    Xlon = ncsrcfile["lon_rho"][:]
    s_rho = ncsrcfile["s_rho"][:]
    mask_rho = ncsrcfile["mask_rho"][:]
    H = ncsrcfile["h"][:]

    dstLon = np.linspace(Xlon.min(), Xlon.max(), len(Xlon[0]))
    dstLat = np.linspace(Xlat.min(), Xlat.max(), len(Xlat))

    # Instantiate a Wacomm archive file
    wacomm = Wacomm(dst, time, depths, dstLon, dstLat)

    # Create a 2D biliniear interpolator on Rho points
    interpolator2DRho = Interp2D(Xlon, Xlat, dstLon, dstLat)

    # Create a 3D biliniear interpolator on Rho points
    interpolator3DRho = Interp3D(Xlon, Xlat, dstLon, dstLat, s_rho, mask_rho, H)

    # print("sfconc...")
    # conc = ncsrcfile.variables["conc"][:]
    # sfconc = interpolator2DRho.interp(conc[0, -1])
    # print("...sfconc")

    print("conc...")
    conc = ncsrcfile.variables["conc"][:]
    conc = interpolator3DRho.interp(conc)
    print("...conc")

    print("Saving archive file...")
    wacomm.mask = interpolator3DRho.mask
    wacomm.conc = conc
    wacomm.sfconc = conc[0, 0]
    wacomm.write()

    # Close the NetCDF file
    ncsrcfile.close()
    wacomm.close()
