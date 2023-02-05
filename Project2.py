from turbineengine import *
import numpy as np
import matplotlib.pyplot as plt

#   Bypass Ratios
thrusts = list()
tsfcs = list()
parameters = np.arange(0, 10, 0.1)
for p in parameters:
    engine = TripleSpoolNonMixingHighBypassTurbofanEngine(bypassRatio=p)
    engine = engine.simulate()
    thrusts.append(engine.thrust / 1000)
    tsfcs.append(engine.thrustSpecificFuelConsumption * 10 ** 6)

plt.plot(parameters, thrusts)
plt.xlabel("Bypass Ratio")
plt.ylabel("Thrust (kN)")
plt.grid()
plt.show()

plt.plot(parameters, tsfcs)
plt.xlabel("Bypass Ratio")
plt.ylabel("TSFC (mg/(N.s)")
plt.grid()
plt.show()

#   Mach Number
thrusts = list()
tsfcs = list()
parameters = np.arange(0.7, 0.9, 0.01)
for p in parameters:
    engine = TripleSpoolNonMixingHighBypassTurbofanEngine(mach=p)
    engine = engine.simulate()
    thrusts.append(engine.thrust / 1000)
    tsfcs.append(engine.thrustSpecificFuelConsumption * 10 ** 6)

plt.plot(parameters, thrusts)
plt.xlabel("M")
plt.ylabel("Thrust (kN)")
plt.grid()
plt.show()

plt.plot(parameters, tsfcs)
plt.xlabel("M")
plt.ylabel("TSFC (mg/(N.s)")
plt.grid()
plt.show()

#   Altitude
thrusts = list()
tsfcs = list()
exitCorePRatios = list()
exitBypassPRatios = list()
momentumThrust = list()
pressureThrust = list()
bypassThrust = list()
parameters = np.arange(7000, 15000, 100)
for p in parameters:
    engine = TripleSpoolNonMixingHighBypassTurbofanEngine(altitude=p)
    engine = engine.simulate()
    thrusts.append(engine.thrust / 1000)
    tsfcs.append(engine.thrustSpecificFuelConsumption * 10 ** 6)
    exitCorePRatios.append(
        engine.fluid.totalPressure / engine.fluid.atmosphericPressure
    )
    exitBypassPRatios.append(
        engine.engineComponents[1].totalPressureBypass
        / engine.fluid.atmosphericPressure
    )
    momentumThrust.append(engine.coreMomentumThrust / 1000)
    pressureThrust.append(engine.corePressureThrust / 1000)
    bypassThrust.append(
        (engine.thrust - engine.coreMomentumThrust - engine.corePressureThrust) / 1000
    )

plt.plot(parameters, thrusts)
plt.xlabel("Altitude (m)")
plt.ylabel("Thrust (kN)")
plt.grid()
plt.show()

plt.plot(parameters, tsfcs)
plt.xlabel("Altitude (m)")
plt.ylabel("TSFC (mg/(N.s)")
plt.grid()
plt.show()

plt.plot(parameters, exitCorePRatios, label="Core")
plt.plot(parameters, exitBypassPRatios, label="Bypass")
plt.xlabel("Altitude (m)")
plt.ylabel("Pressure Ratio")
plt.legend()
plt.grid()
plt.show()

plt.plot(parameters, momentumThrust, label="Core Momentum")
plt.plot(parameters, pressureThrust, label="Core Pressure")
plt.plot(parameters, bypassThrust, label="Bypass")
plt.plot(parameters, thrusts, label="Total")
plt.legend()
plt.xlabel("Altitude (m)")
plt.ylabel("Thrust (kN)")
plt.grid()
plt.show()

#   Low-Pressure-Compressor Pressure Ratio
lthrusts = list()
ltsfcs = list()
lparameters = np.arange(1.1, 2.1, 0.01)
for p in lparameters:
    engine = TripleSpoolNonMixingHighBypassTurbofanEngine(lFanPressureRatio=p)
    engine = engine.simulate()
    lthrusts.append(engine.thrust / 1000)
    ltsfcs.append(engine.thrustSpecificFuelConsumption * 10 ** 6)

#   Intermediate-Pressure-Compressor Pressure Ratio
thrusts = list()
tsfcs = list()
parameters = np.arange(1, 10, 0.1)
for p in parameters:
    engine = TripleSpoolNonMixingHighBypassTurbofanEngine(iCompPressureRatio=p)
    engine = engine.simulate()
    thrusts.append(engine.thrust / 1000)
    tsfcs.append(engine.thrustSpecificFuelConsumption * 10 ** 6)

plt.plot(lparameters, lthrusts, label="LPC")
plt.plot(parameters, thrusts, label="IPC")
plt.legend()
plt.xlabel("Pressure Ratio")
plt.ylabel("Thrust (kN)")
plt.grid()
plt.show()

plt.plot(lparameters, ltsfcs, label="LPC")
plt.plot(parameters, tsfcs, label="IPC")
plt.legend()
plt.xlabel("Pressure Ratio")
plt.ylabel("TSFC (mg/(N.s)")
plt.grid()
plt.show()

#   Low-Pressure-Compressor Efficiency
lthrusts = list()
ltsfcs = list()
lparameters = np.arange(0.7, 0.95, 0.01)
for p in lparameters:
    engine = TripleSpoolNonMixingHighBypassTurbofanEngine(lFanEfficiency=p)
    engine = engine.simulate()
    lthrusts.append(engine.thrust / 1000)
    ltsfcs.append(engine.thrustSpecificFuelConsumption * 10 ** 6)

#   High-Pressure-Compressor Efficiency
thrusts = list()
tsfcs = list()
parameters = np.arange(0.7, 0.95, 0.01)
for p in parameters:
    engine = TripleSpoolNonMixingHighBypassTurbofanEngine(hCompEfficiency=p)
    engine = engine.simulate()
    thrusts.append(engine.thrust / 1000)
    tsfcs.append(engine.thrustSpecificFuelConsumption * 10 ** 6)

plt.plot(lparameters, lthrusts, label="LPC")
plt.plot(parameters, thrusts, label="HPC")
plt.legend()
plt.xlabel("Efficiency")
plt.ylabel("Thrust (kN)")
plt.grid()
plt.show()

plt.plot(lparameters, ltsfcs, label="LPC")
plt.plot(parameters, tsfcs, label="HPC")
plt.legend()
plt.xlabel("Efficiency")
plt.ylabel("TSFC (mg/(N.s)")
plt.grid()
plt.show()

#   Low-Pressure-Turbine Efficiency
lthrusts = list()
ltsfcs = list()
lparameters = np.arange(0.8, 0.98, 0.01)
for p in lparameters:
    engine = TripleSpoolNonMixingHighBypassTurbofanEngine(lTurbineEfficiency=p)
    engine = engine.simulate()
    lthrusts.append(engine.thrust / 1000)
    ltsfcs.append(engine.thrustSpecificFuelConsumption * 10 ** 6)

#   High-Pressure-Turbine Efficiency
thrusts = list()
tsfcs = list()
parameters = np.arange(0.8, 0.98, 0.01)
for p in parameters:
    engine = TripleSpoolNonMixingHighBypassTurbofanEngine(hTurbineEfficiency=p)
    engine = engine.simulate()
    thrusts.append(engine.thrust / 1000)
    tsfcs.append(engine.thrustSpecificFuelConsumption * 10 ** 6)

plt.plot(lparameters, lthrusts, label="LPT")
plt.plot(parameters, thrusts, label="HPT")
plt.xlabel("Efficiency")
plt.ylabel("Thrust (kN)")
plt.legend()
plt.grid()
plt.show()

plt.plot(lparameters, ltsfcs, label="LPT")
plt.plot(parameters, tsfcs, label="HPT")
plt.xlabel("Efficiency")
plt.ylabel("TSFC (mg/(N.s)")
plt.legend()
plt.grid()
plt.show()
