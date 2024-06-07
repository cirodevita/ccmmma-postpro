from netCDF4 import Dataset


class ROMS:
    def __init__(self, filename, time, depths, lons, lats):
        self.lons = lons
        self.lats = lats
        self.depths = depths
        self.time = time

        self.temp = None
        self.salt = None
        self.zeta = None
        self.U = None
        self.V = None
        self.vbar = None
        self.ubar = None

        self.ncdstfile = Dataset(filename, "w", format="NETCDF4")

        self.ncdstfile.createDimension("time", size=1)
        self.ncdstfile.createDimension("depth", size=len(depths))
        self.ncdstfile.createDimension("latitude", size=len(lats))
        self.ncdstfile.createDimension("longitude", size=len(lons))

        self.timeVar = self.ncdstfile.createVariable("time", "i4", "time")
        self.timeVar.description = "Time since initialization"
        self.timeVar.long_name = "time since initialization"
        self.timeVar.units = "seconds since 1968-05-23 00:00:00"
        self.timeVar.calendar = "gregorian"
        self.timeVar.field = "time, scalar, series"
        self.timeVar.standard_name = "time"
        self.timeVar.axis = "T"

        self.depthVar = self.ncdstfile.createVariable("depth", "f4", "depth")
        self.depthVar.description = "depth"
        self.depthVar.long_name = "depth"
        self.depthVar.units = "meters"
        self.depthVar.standard_name = "depth"
        self.depthVar.axis = "Z"

        self.lonVar = self.ncdstfile.createVariable("longitude", "f4", "longitude")
        self.lonVar.description = "Longitude"
        self.lonVar.long_name = "longitude"
        self.lonVar.units = "degrees_east"
        self.lonVar.standard_name = "longitude"
        self.lonVar.axis = "X"

        self.latVar = self.ncdstfile.createVariable("latitude", "f4", "latitude")
        self.latVar.description = "Latitude"
        self.lonVar.long_name = "latitude"
        self.latVar.units = "degrees_north"
        self.latVar.standard_name = "latitude"
        self.latVar.axis = "Y"

        self.zetaVar = self.ncdstfile.createVariable("zeta", "f4", ("time", "latitude", "longitude"), fill_value=1.e+37)
        self.zetaVar.description = "Free surface height"
        self.zetaVar.units = "meter"
        self.zetaVar.long_name = "free-surface"

        self.uVar = self.ncdstfile.createVariable("u", "f4", ("time", "depth", "latitude", "longitude"), fill_value=1.e+37)
        self.uVar.description = "U-momentum component"
        self.uVar.units = "meter second-1"
        self.uVar.long_name = "u-momentum component"
        self.uVar.field = "u-velocity, scalar, series"

        self.vVar = self.ncdstfile.createVariable("v", "f4", ("time", "depth", "latitude", "longitude"), fill_value=1.e+37)
        self.vVar.description = "V-momentum component"
        self.vVar.units = "meter second-1"
        self.vVar.long_name = "v-momentum component"
        self.vVar.field = "v-velocity, scalar, series"

        self.ubarVar = self.ncdstfile.createVariable("ubar", "f4", ("time", "latitude", "longitude"), fill_value=1.e+37)
        self.ubarVar.description = "Vertically integrated u-momentum component"
        self.ubarVar.units = "meter second-1"
        self.ubarVar.long_name = "vertically integrated u-momentum component"

        self.vbarVar = self.ncdstfile.createVariable("vbar", "f4", ("time", "latitude", "longitude"), fill_value=1.e+37)
        self.vbarVar.description = "Vertically integrated v-momentum component"
        self.vbarVar.units = "meter second-1"
        self.vbarVar.long_name = "vertically integrated v-momentum component"

        self.saltVar = self.ncdstfile.createVariable("salt", "f4", ("time", "depth", "latitude", "longitude"), fill_value=1.e+37)
        self.saltVar.description = "Salinity"
        self.saltVar.long_name = "salinity"
        self.saltVar.field = "salinity, scalar, series"

        self.tempVar = self.ncdstfile.createVariable("temp", "f4", ("time", "depth", "latitude", "longitude"), fill_value=1.e+37)
        self.tempVar.description = "Potential temperature"
        self.tempVar.units = "Celsius"
        self.tempVar.long_name = "potential temperature"
        self.tempVar.field = "temperature, scalar, series"

    def write(self):
        self.timeVar[:] = self.time
        self.lonVar[:] = self.lons
        self.latVar[:] = self.lats
        self.depthVar[:] = self.depths

        self.zetaVar[:] = self.zeta
        self.saltVar[:] = self.temp
        self.tempVar[:] = self.temp
        self.uVar[:] = self.U
        self.vVar[:] = self.V
        self.ubarVar[:] = self.ubar
        self.vbarVar[:] = self.vbar

    def close(self):
        if self.ncdstfile:
            self.ncdstfile.close()
