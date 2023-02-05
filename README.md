# Jet Engine Simulation

## Triple-Spool Non-Mixing High-Bypass Turbofan Engine ([Simulation.py](https://github.com/camerondix/jet_engine_simulation/blob/main/Simulation.py))

### Thrust v Bypass Ratio
The thrust should decrease as the bypass ratio decreases because the bypass ratio controls how much of the fluid goes through the bypass. More fluid going through the bypass means less thrust.

![Figure_1](https://user-images.githubusercontent.com/97497313/216799874-f4822023-6c37-40cc-8fe2-807c723d6fcb.png)

### Fuel Consumption v Bypass Ratio
The TSFC should decrease as the bypass ratio decreases because the bypass ratio controls how much of the fluid goes through the bypass. More fluid going through the bypass means less thrust and lower TSFC.

![Figure_2](https://user-images.githubusercontent.com/97497313/216799876-5f59ae04-aec1-4401-95ea-6f67f21fe26a.png)

### Thrust v Mach Number
Thrust decreases as speed increases because thrust is related to the change in velocity of the exit to the entrance.

![Figure_3](https://user-images.githubusercontent.com/97497313/216799877-9d5b9602-226a-44eb-ad7e-2f79fbb462b6.png)

### Fuel Consumption v Mach Number
The faster you want to fly, the more it costs in fuel. Generally, we want to fly faster to get to the destination faster.

![Figure_4](https://user-images.githubusercontent.com/97497313/216799879-73d9d36a-abe5-4ebc-a8a6-2e301a5dd890.png)

### Thrust v Altitude
This plot looks correct up until 11000 m, thrust should increase as altitude increases. At 11000 m the temperature is constant and in this plot the thrust is constant. The thrust should continue to increase because pressure will still exponentially decrease. For these reasons the model is not correct as it assumes a varying exit area when in reality the area would be fixed.

![Figure_5](https://user-images.githubusercontent.com/97497313/216799882-00a95ff3-ba54-4b1a-adf3-215acd244abf.png)

### Fuel Consumption v Altitude
This plot looks correct up until 11000 m, TSFC should increase as altitude increases. At 11000 m the temperature is constant and, in this plot, the TSFC is constant. The TSFC should continue to increase because pressure will still exponentially decrease. For these reasons the model is not correct as it assumes a varying exit area when in reality the area would be fixed.

![Figure_6](https://user-images.githubusercontent.com/97497313/216799883-f6027207-020f-4c9b-a2ea-b44dc6b1e63e.png)

### Pressure Ratio v Altitude
Core pressure ratio should increase as altitude goes up because at higher altitudes the exit total atmospheric pressure is lower. At 11000 m the pressure ratio is constant which is not correct, it should continue to increase.

![Figure_7](https://user-images.githubusercontent.com/97497313/216799884-54b0ae9c-48ed-4807-9cae-c862637f3de5.png)

### Momentum Thrust v Altitude
As altitude increases the core thrust increases and bypass thrust decreases. This makes sense except after 11000 m.

![Figure_8](https://user-images.githubusercontent.com/97497313/216799885-d26f85b4-ab73-4cf3-96ff-b2c78a3aa192.png)

### Thrust v Pressure Ratio
This makes sense for the IPC because you only want to compress the fluid to a certain point before the combustor is basically doing nothing. As pressure increases temperature also increases. The LPC is similar except we are still getting good thrust out of it before that happens.

![Figure_9](https://user-images.githubusercontent.com/97497313/216799886-360dd0f3-055e-43b7-9db9-189fccbc936f.png)

### Fuel Consumption v Pressure Ratio
This makes sense because it requires more fuel to increase the turbine outputs and in turn increase exit pressure.

![Figure_10](https://user-images.githubusercontent.com/97497313/216799887-524f57b3-754b-4427-831c-da949e854e48.png)

### Thrust v Efficiency
This makes sense because if we get more efficient then we get more thrust.

![Figure_11](https://user-images.githubusercontent.com/97497313/216799889-98cb114f-96a4-43e0-9142-1f0661214a18.png)

### Fuel Consumption v Efficiency
This makes sense because if we get more efficient then we burn less fuel.

![Figure_12](https://user-images.githubusercontent.com/97497313/216799890-a7d44168-3ba4-4901-a2f2-29f5d4784a20.png)

### Fuel Consumption v Efficiency
This makes sense because if we get more efficient then we burn less fuel.

![Figure_13](https://user-images.githubusercontent.com/97497313/216799891-1105355e-8bad-4503-b555-b27dfb9374ab.png)

### Fuel Consumption v Efficiency
This makes sense because if we get more efficient then we burn less fuel.

![Figure_14](https://user-images.githubusercontent.com/97497313/216799893-89515c9d-4665-40e7-b6c5-90eccbb186a4.png)
