import standardatmosphere as statm
import isentropic as isen
from copy import copy


class Fluid:
    """
    An object that describes the working fluid.
    """

    def __init__(
        this,
        machNumber: float,
        gammaCold: float,
        gammaHot: float,
        cpCold: float,
        cpHot: float,
        altitude: float,
        massFlowRate: float,
    ) -> None:
        """
        machNumber -> unitless | gammaCold -> unitless | gammaHot -> unitless | cpCold -> J/(kg.K) | cpHot -> J/(kg.K) | altitude -> m | massFlowRate -> kg/s
        """
        this.machNumber = machNumber
        this.gammaCold = gammaCold
        this.gammaHot = gammaHot
        this.cpCold = cpCold
        this.cpHot = cpHot
        this.altitude = altitude
        atmosphere = statm.findStandardAtmosphere(altitude)
        this.isentropicRatios = isen.findIsentropicRatios(machNumber)
        this.atmosphericPressure = atmosphere[0]
        this.atmosphericTemperature = atmosphere[2]
        this.totalAtmosphericPressure = atmosphere[0] * this.isentropicRatios[0]
        this.totalAtmosphericTemperature = atmosphere[2] * this.isentropicRatios[2]
        this.totalPressure = this.totalAtmosphericPressure
        this.totalTemperature = this.totalAtmosphericTemperature
        this.massFlowRate = massFlowRate
        this.massFuelFlowRate = 0
        this.bypassMassFlowRate = 0
        this.work = {}
        this.initialVelocity = (
            this.machNumber
            * (this.gammaCold * this.rCold * this.atmosphericTemperature) ** 0.5
        )
        this.finalVelocity = 0
        this.bypassFinalVelocity = 0

    def get_rCold(this):
        return this.cpCold * (this.gammaCold - 1) / this.gammaCold

    rCold = property(get_rCold)

    def get_rHot(this):
        return this.cpHot * (this.gammaHot - 1) / this.gammaHot

    rHot = property(get_rHot)

    def get_pressure(this):
        return this.totalPressure / this.isentropicRatios[0]

    pressure = property(get_pressure)

    def GetPressure(this, totalPressure: float, mach: float, hot=True):
        if hot:
            k = this.gammaHot
        else:
            k = this.gammaCold
        return totalPressure / ((1 + (k - 1) / 2 * mach ** 2) ** (k / (k - 1)))

    def GetTemperature(this, totalTemperature: float, mach: float, hot=True):
        if hot:
            k = this.gammaHot
        else:
            k = this.gammaCold
        return totalTemperature / (1 + (k - 1) / 2 * mach ** 2)

    def GetDensity(
        this, totalPressure: float, totalTemperature: float, mach: float, hot=True
    ):
        if hot:
            r = this.rHot
        else:
            r = this.rCold
        return this.GetPressure(totalPressure, mach, hot) / (
            r * this.GetTemperature(totalTemperature, mach, hot)
        )


class Intake:
    """
    An object that models an intake.
    """

    def __init__(this) -> None:
        pass

    def simulate(this, fluid: Fluid) -> Fluid:
        """
        Updates the fluid properties by simulating the intake. The intake does not change any of the fluid's properties.
        """
        this.fluid = copy(fluid)
        return fluid


class NonMixingFan:
    """
    An object that models a non-mixing fan.
    """

    def __init__(
        this,
        efficiency: float,
        pressureRatio: float,
        bypassRatio: float,
        bypassDuctTotalPressureLoss: float,
    ) -> None:
        """
        efficiency -> unitless | pressureRatio -> unitless | bypassRatio -> unitless | bypassDuctTotalPressureLoss -> unitless
        """
        this.efficiency = efficiency
        this.pressureRatio = pressureRatio
        this.bypassRatio = bypassRatio
        this.bypassDuctTotalPressureLoss = bypassDuctTotalPressureLoss

    def simulate(this, fluid: Fluid) -> Fluid:
        """
        Updates the fluid properties by simulating the fan. Work is done on the fluid increasing pressure and temperature. Some of the fluid mass is bypassed.
        """
        pOut = fluid.totalPressure * this.pressureRatio
        tOutIdeal = fluid.totalTemperature * (this.pressureRatio) ** (
            (fluid.gammaCold - 1) / fluid.gammaCold
        )
        wIdeal = (
            fluid.massFlowRate * fluid.cpCold * (tOutIdeal - fluid.totalTemperature)
        )
        this.work = wIdeal / this.efficiency
        fluid.work[id(this)] = this.work
        tOut = fluid.totalTemperature + this.work / (fluid.massFlowRate * fluid.cpCold)
        fluid.totalPressure = pOut
        fluid.totalTemperature = tOut
        fluid.massFlowRate = fluid.massFlowRate / (1 + this.bypassRatio)
        fluid.bypassMassFlowRate = fluid.massFlowRate * this.bypassRatio
        # Handle the bypass
        this.totalPressureBypass = fluid.totalPressure * (
            1 - this.bypassDuctTotalPressureLoss
        )
        pRatioCritical = (1 + (fluid.gammaCold - 1) / 2) ** (
            fluid.gammaCold / (fluid.gammaCold - 1)
        )
        mach = 1
        if this.totalPressureBypass / fluid.atmosphericPressure <= pRatioCritical:
            # Not choked
            this.totalPressureBypass = fluid.totalAtmosphericPressure
            mach = (
                2
                / (fluid.gammaCold - 1)
                * (
                    (this.totalPressureBypass / fluid.atmosphericPressure)
                    ** ((fluid.gammaCold - 1) / fluid.gammaCold)
                    - 1
                )
            ) ** (1 / 2)
        this.pressureBypass = fluid.GetPressure(this.totalPressureBypass, mach, False)
        this.temperatureBypass = fluid.GetTemperature(
            fluid.totalTemperature, mach, False
        )
        fluid.bypassFinalVelocity = mach * (
            fluid.gammaCold * fluid.rCold * this.temperatureBypass
        ) ** (1 / 2)
        densityBypass = fluid.GetDensity(
            this.totalPressureBypass, fluid.totalTemperature, mach, False
        )
        this.area = fluid.bypassMassFlowRate / (
            densityBypass * fluid.bypassFinalVelocity
        )
        this.exitMach = mach
        this.fluid = copy(fluid)
        return fluid


class Compressor:
    """
    An object that models a compressor.
    """

    def __init__(this, efficiency: float, pressureRatio: float) -> None:
        """
        efficiency -> unitless | pressureRatio -> unitless
        """
        this.efficiency = efficiency
        this.pressureRatio = pressureRatio

    def simulate(this, fluid: Fluid) -> Fluid:
        """
        Updates the fluid properties by simulating the compressor. Work is done on the fluid increasing pressure and temperature.
        """
        pOut = fluid.totalPressure * this.pressureRatio
        tOutIdeal = fluid.totalTemperature * (this.pressureRatio) ** (
            (fluid.gammaCold - 1) / fluid.gammaCold
        )
        wIdeal = (
            fluid.massFlowRate * fluid.cpCold * (tOutIdeal - fluid.totalTemperature)
        )
        this.work = wIdeal / this.efficiency
        fluid.work[id(this)] = this.work
        tOut = fluid.totalTemperature + this.work / (fluid.massFlowRate * fluid.cpCold)
        fluid.totalPressure = pOut
        fluid.totalTemperature = tOut
        this.fluid = copy(fluid)
        return fluid


class CombustionChamber:
    """
    An object that models a combustion chamber.
    """

    def __init__(
        this,
        efficiency: float,
        totalPressureLoss: float,
        totalExitTemperature: float,
        fuelLowerHeatingValue: float,
    ) -> None:
        """
        efficiency -> unitless | totalPressureLoss -> unitless | totalExitTemperature -> K | fuelLowerHeatingValue -> J/kg
        """
        this.efficiency = efficiency
        this.totalPressureLoss = totalPressureLoss
        this.totalExitTemperature = totalExitTemperature
        this.fuelLowerHeatingValue = fuelLowerHeatingValue

    def simulate(this, fluid: Fluid) -> Fluid:
        """
        Updates the fluid properties by simulating the combustion chamber. Heat is added to the fluid and total pressure is lost. Additional mass flow is added to the fluid from the fuel.
        """
        mFuel = (
            fluid.massFlowRate
            * fluid.cpHot
            * (this.totalExitTemperature - fluid.totalTemperature)
            / (
                this.efficiency * this.fuelLowerHeatingValue
                + fluid.cpHot * (this.totalExitTemperature - fluid.totalTemperature)
            )
        )
        fluid.massFlowRate += mFuel
        fluid.massFuelFlowRate = mFuel
        fluid.totalTemperature = this.totalExitTemperature
        fluid.totalPressure = fluid.totalPressure * (1 - this.totalPressureLoss)
        this.fluid = copy(fluid)
        return fluid


class Turbine:
    """
    An object that models a turbine.
    """

    def __init__(this, efficiency: float, poweredComponent) -> None:
        """
        efficiency -> unitless
        """
        this.efficiency = efficiency
        this.poweredComponentID = id(poweredComponent)

    def simulate(this, fluid: Fluid) -> Fluid:
        """
        Updates the fluid properties by simulating the turbine. The fluid does work decreasing the total temperature and pressure.
        """
        tOut = fluid.totalTemperature - fluid.work[this.poweredComponentID] / (
            fluid.massFlowRate * fluid.cpHot
        )
        tSOut = (
            fluid.totalTemperature - (fluid.totalTemperature - tOut) / this.efficiency
        )
        fluid.totalPressure = fluid.totalPressure * (
            tSOut / fluid.totalTemperature
        ) ** (fluid.gammaHot / (fluid.gammaHot - 1))
        fluid.totalTemperature = tOut
        this.fluid = copy(fluid)
        return fluid


class JetPipe:
    """
    An object that models a jet pipe.
    """

    def __init__(this) -> None:
        pass

    def simulate(this, fluid: Fluid) -> Fluid:
        """
        Updates the fluid properties by simulating the jet pipe. The jet pipe does not change any of the fluid's properties.
        """
        this.fluid = copy(fluid)
        return fluid


class ConvergentNozzle:
    """
    An object that models a convergent nozzle.
    """

    def __init__(this, totalPressureLoss: float) -> None:
        """
        totalPressureLoss -> unitless
        """
        this.totalPressureLoss = totalPressureLoss

    def simulate(this, fluid: Fluid) -> Fluid:
        """
        Updates the fluid properties by simulating the convergent nozzle.
        """
        pRatioCritical = (1 + (fluid.gammaHot - 1) / 2) ** (
            fluid.gammaHot / (fluid.gammaHot - 1)
        )
        pOut = fluid.totalPressure * (1 - this.totalPressureLoss)
        mach = 1
        if pOut / fluid.atmosphericPressure <= pRatioCritical:
            # Not choked
            pOut = fluid.totalAtmosphericPressure
            mach = (
                2
                / (fluid.gammaHot - 1)
                * (
                    (pOut / fluid.atmosphericPressure)
                    ** ((fluid.gammaHot - 1) / fluid.gammaHot)
                    - 1
                )
            ) ** (1 / 2)
        fluid.totalTemperature = fluid.totalTemperature * (
            pOut / fluid.totalPressure
        ) ** ((fluid.gammaHot - 1) / fluid.gammaHot)
        fluid.totalPressure = pOut
        fluid.finalVelocity = mach * (
            fluid.gammaHot
            * fluid.rHot
            * fluid.GetTemperature(fluid.totalTemperature, mach)
        ) ** (0.5)
        this.area = fluid.massFlowRate / (
            fluid.GetDensity(fluid.totalPressure, fluid.totalTemperature, mach)
            * fluid.finalVelocity
        )
        this.exitMach = mach
        this.fluid = copy(fluid)
        return fluid


class TurbineEngine:
    """
    An object that models a turbine engine made up of any variety of components.
    """

    def __init__(
        this,
        fluid: Fluid,
        engineComponents: list,
    ) -> None:
        """
        The parameter engineComponents must be in the order that the fluid flows.
        """
        this.fluid = fluid
        this.engineComponents = engineComponents
        this.thrust = 0

    def simulate(this):
        for component in this.engineComponents:
            this.fluid = component.simulate(this.fluid)
            if type(component) is ConvergentNozzle:
                this.coreMomentumThrust = (
                    this.fluid.massFlowRate * this.fluid.finalVelocity
                    - (this.fluid.massFlowRate - this.fluid.massFuelFlowRate)
                    * this.fluid.initialVelocity
                )
                this.corePressureThrust = component.area * (
                    this.fluid.GetPressure(this.fluid.totalPressure, component.exitMach)
                    - this.fluid.atmosphericPressure
                )
                this.thrust += this.coreMomentumThrust + this.corePressureThrust
            elif type(component) is NonMixingFan:
                this.thrust += this.fluid.bypassMassFlowRate * (
                    this.fluid.bypassFinalVelocity - this.fluid.initialVelocity
                ) + component.area * (
                    component.pressureBypass - this.fluid.atmosphericPressure
                )
        this.thrustSpecificFuelConsumption = this.fluid.massFuelFlowRate / this.thrust
        return copy(this)


class TripleSpoolNonMixingHighBypassTurbofanEngine:
    """
    Models a specific Triple-Spool, Non-Mixing, High-Bypass Turbofan Engine
    """

    def __init__(
        this,
        bypassRatio=6,
        mach=0.84,
        altitude=10000,
        lFanPressureRatio=1.5,
        iCompPressureRatio=6.5,
        lFanEfficiency=0.78,
        hCompEfficiency=0.82,
        hTurbineEfficiency=0.92,
        lTurbineEfficiency=0.88,
    ) -> None:
        # Define the working fluid
        fluid = Fluid(mach, 1.4, 1.333, 1005, 1150, altitude, 780)

        # Build the engine components
        intake = Intake()
        lFan = NonMixingFan(lFanEfficiency, lFanPressureRatio, bypassRatio, 0.05)
        iCompressor = Compressor(0.8, iCompPressureRatio)
        hCompressor = Compressor(hCompEfficiency, 4.2)
        combustionChamber = CombustionChamber(0.97, 0.05, 1750, 42.5 * 10 ** 6)
        hTurbine = Turbine(hTurbineEfficiency, hCompressor)
        iTurbine = Turbine(0.9, iCompressor)
        lTurbine = Turbine(lTurbineEfficiency, lFan)
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
        this.turboFanEngine = TurbineEngine(fluid, engineComponents)

    def simulate(this) -> TurbineEngine:
        return this.turboFanEngine.simulate()
