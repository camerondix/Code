import math
from bisect import bisect
import matplotlib.pyplot as plt


def findStandardAtmosphere(h, usUnits=False):
    """
    Finds p, rho, and t of the US Standard Atmosphere at the h in metric or US units.
    """
    # Initialize constants
    heights = [0, 11000, 25000, 47000, 53000, 79000, 90000, 105000]  # m
    slopes = [-0.0065, 0.0, 0.003, 0.0, -0.0045, 0.0, 0.004, 0.004]  # K/m
    p_h = 101325  # Pa
    rho_h = 1.225  # kg/m^3
    t_0 = 288.16  # K
    g = 9.81  # m/s^2
    r = 287  # J/kg.K
    # Convert the units if US units
    if usUnits:
        heights = [x * 3.28084 for x in heights]  # ft
        slopes = [x / 3.28084 / 1.8 for x in slopes]  # R/ft
        p_h = 2116.2  # lb/ft^2
        rho_h = 0.002377  # slug/ft^3
        t_0 = 518.69  # R
        g = 32.2  # ft/s^2
        r = 1716  # ft.lb/slug.R

    # Loop through the each altitude range until it gets to h
    index = bisect(heights, h)
    for i in range(index):
        if slopes[i] != 0.0:
            if i == index - 1:
                t_h = t_0 + slopes[i] * (h - heights[i])
                p_h = p_h * (t_h / t_0) ** (-g / (slopes[i] * r))
                rho_h = rho_h * (t_h / t_0) ** (-g / (slopes[i] * r) - 1)
                return [p_h, rho_h, t_h]
            else:
                t_h = t_0 + slopes[i] * (heights[i + 1] - heights[i])
                p_h = p_h * (t_h / t_0) ** (-g / (slopes[i] * r))
                rho_h = rho_h * (t_h / t_0) ** (-g / (slopes[i] * r) - 1)
                t_0 = t_h
        else:
            if i == index - 1:
                p_h = p_h * math.exp((-g / (r * t_h)) * (h - heights[i]))
                rho_h = rho_h * math.exp((-g / (r * t_h)) * (h - heights[i]))
                return [p_h, rho_h, t_h]
            else:
                p_h = p_h * math.exp((-g / (r * t_h)) * (heights[i + 1] - heights[i]))
                rho_h = rho_h * math.exp(
                    (-g / (r * t_h)) * (heights[i + 1] - heights[i])
                )


def plotStandardAtmosphere(maxH, usUnits=False):
    """
    Plots p, rho, and t of the US Standard Atmosphere in metric or US units from 0 to maxH.
    """
    press = list()
    dens = list()
    temps = list()
    hUnit = "(m)"
    pUnit = "(Pa)"
    rhoUnit = r"($kg/m^3$)"
    tUnit = "(K)"
    if usUnits:
        hUnit = "(ft)"
        pUnit = r"($lbf/ft^2$)"
        rhoUnit = r"($slug/ft^3$)"
        tUnit = "(R)"
    for h in range(maxH):
        p, rho, t = findStandardAtmosphere(h, usUnits)
        press.append(p)
        dens.append(rho)
        temps.append(t)

    plt.subplot(111, ylabel=("h " + hUnit), xlabel=("P " + pUnit))
    plt.plot(press, range(maxH))
    plt.grid()
    plt.show()
    plt.subplot(111, ylabel=("h " + hUnit), xlabel=(r"$\rho$ " + rhoUnit))
    plt.plot(dens, range(maxH))
    plt.grid()
    plt.show()
    plt.subplot(111, ylabel=("h " + hUnit), xlabel=("T " + tUnit))
    plt.plot(temps, range(maxH))
    plt.grid()
    plt.show()
