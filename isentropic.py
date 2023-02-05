import matplotlib.pyplot as plt
import numpy as np


def findIsentropicRatios(m, k=1.4):
    """
    Finds the isentropic stagnation to static ratio of p, rho, and t at m.
    """
    temp = 1.0 + ((k - 1.0) / 2.0) * m ** 2.0
    press = temp ** (k / (k - 1.0))
    dens = temp ** (1.0 / (k - 1.0))
    return [press, dens, temp]


def plotMachVsIsentropicRatios():
    """
    Plots the mach number vs isentropic ratios for mach numbers 0 to 10.
    """
    # Create the mach arrays and initial ratio arrays
    machs1 = np.arange(0.0, 5.0, 0.01)
    machs2 = np.arange(5.0, 10.1, 0.1)
    machs =  np.concatenate((machs1, machs2), axis = 0)
    p_ratios = list()
    rho_ratios = list()
    t_ratios = list()

    # Calculate the ratios for each mach number
    for mach in machs:
        ratios = findIsentropicRatios(mach)
        p_ratios.append(ratios[0])
        rho_ratios.append(ratios[1])
        t_ratios.append(ratios[2])

    # Plot the ratios
    plt.plot(machs, p_ratios, label = "Pressure")
    plt.plot(machs, rho_ratios, label = "Density")
    plt.plot(machs, t_ratios, label = "Temperature")
    plt.yscale("log")
    plt.xlabel("Mach Number")
    plt.title("Isentropic Ratios")
    plt.legend(loc = 'upper left')
    plt.grid()
    plt.show()
    return
    
def findIsentropicConditions(m_1, p_1, rho_1, t_1, m_2, k=1.4):
    """
    Finds the isentropic conditions at m_2 given conditions at m_1: p_1, rho_1, and t_1.
    """
    # Find ratios at 1
    ratios_1 = findIsentropicRatios(m_1, k)
    # Find the stagnation conditions
    p_0 = ratios_1[0] * p_1
    rho_0 = ratios_1[1] * rho_1
    t_0 = ratios_1[2] * t_1
    # Find the ratios at 2
    ratios_2 = findIsentropicRatios(m_2, k)
    # Find the conditions at 2
    p_2 = p_0 / ratios_2[0]
    rho_2 = rho_0 / ratios_2[1]
    t_2 = t_0 / ratios_2[2]
    return [p_2, rho_2, t_2]

