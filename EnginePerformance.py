from turbineengine import *
from copy import copy

#   Small, Single-Spool Turbojet Engine
# Define the working fluid
fluid = Fluid(0.85, 1.4, 1.333, 1005, 1150, 0, 5.8)

# Build the engine components
intake = Intake()
compressor = Compressor(0.78, 5)
combustionChamber = CombustionChamber(0.98, 5.5 / 100, 1300, 43.1 * 10 ** 6)
turbine = Turbine(0.86, compressor)
jetPipe = JetPipe()
nozzle = ConvergentNozzle(3.5 / 100)

# Put the components together
engineComponents = list(
    [intake, compressor, combustionChamber, turbine, jetPipe, nozzle]
)

# Build the engine
turboJetEngine = TurbineEngine(fluid, engineComponents)
turboJetEngine.simulate()

turboJetEngine = copy(turboJetEngine)


#   Triple-Spool, Non-Mixing, High-Bypass Turbofan Engine

# Define the working fluid
fluid = Fluid(0.84, 1.4, 1.333, 1005, 1150, 10 * 1000, 780)

# Build the engine components
intake = Intake()
lFan = NonMixingFan(0.78, 1.5, 6, 0.05)
iCompressor = Compressor(0.8, 6.5)
hCompressor = Compressor(0.82, 4.2)
combustionChamber = CombustionChamber(0.97, 0.05, 1750, 42.5 * 10 ** 6)
hTurbine = Turbine(0.92, hCompressor)
iTurbine = Turbine(0.9, iCompressor)
lTurbine = Turbine(0.88, lFan)
jetPipe = JetPipe()
nozzle = ConvergentNozzle(0.02)

# Put the components together
engineComponents = list(
    [
        intake,
        lFan,
        iCompressor,
        hCompressor,
        combustionChamber,
        hTurbine,
        iTurbine,
        lTurbine,
        jetPipe,
        nozzle,
    ]
)

# Build the engine
turboFanEngine = TurbineEngine(fluid, engineComponents)
turboFanEngine.simulate()

turboFanEngine = copy(turboFanEngine)
