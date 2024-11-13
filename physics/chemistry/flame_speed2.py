import cantera as ct
import matplotlib.pyplot as plt
import numpy as np

fig, ax = plt.subplots()
file = 'mechanisms/marinov_ethanol/ethanol-marinov.yaml'
# models = {'Original': 'baseline', 'LMR-R': 'linear-Burke'}
# colours = ["xkcd:grey",'xkcd:purple']
Tin = 293  # unburned gas temperature [K]
p=760  # pressure [torr]
n=2 # number of points to simulate
phi_list = np.linspace(0.5,1,n) # equivalence ratios to simulate across
# for k, m in enumerate(models):
vel_list = []
P_e = []
gas = ct.Solution(file)
for j, phi in enumerate(phi_list):
    print("NNNNNNNNNNNNNNNNNNN  ", j)
    gas.set_equivalence_ratio(phi, 'c2h5oh', {'o2':1, 'n2': 3.76})
    gas.TP = Tin, (p/760)*ct.one_atm
    print(gas())
    P_e.append(gas.concentrations[gas.species_index("c2h5oh")]*1000*8.31*gas.T/1e5)
    f = ct.FreeFlame(gas, grid=np.linspace(0, 0.05, 30))
    f.set_refine_criteria(ratio=3, slope=0.06, curve=0.10)
    # f.transport_model = 'multicomponent' # optionally enable
    # f.soret_enabled = True  # optionally enable
    f.solve(loglevel=1, auto=True)
    vel_list.append(f.velocity[0] * 100) # cm/s
ax.plot(P_e, vel_list)
# ax.set_xticklabels([f"{phi:.1f} {p/(10**5):.3f}" for p, phi in zip(P_e, phi_list)])
# expData = {
#    'X_NH3': [16.3,16.4,17.0,18.0,19.0,20.0,21.9,24.0,26.0,28.5,29.0,30.0,31.0,31.5],
#    'vel': [1.35,1.48,2.30,3.36,4.01,5.88,6.80,8.14,6.73,5.00,4.78,3.3,2.9,3.0]
# }
# X_NH3 = np.divide(expData['X_NH3'],100)
# X_O2 = np.multiply(np.subtract(1,X_NH3), 0.21)
# phi_data = np.divide(np.divide(X_NH3,X_O2),np.divide(4,3))
# ax.plot(phi_data, expData['vel'], 'o', fillstyle='none', color='k', label='Ronney')
ax.legend(frameon=False, loc='upper right')
ax.set_ylabel(r'Burning velocity [cm $\rm s^{-1}$]')
ax.set_xlabel(r'Equivalence Ratio')

# fig, ax = plt.subplots()
fig, ax1 = plt.subplots()

color = 'tab:green'
ax1.set_xlabel('z, m')
ax1.set_ylabel('T, K', color=color)
ax1.plot(f.grid, f.T, color=color)
# ax1.plot(t_D, tvec6[:, 0], color="tab:orange")
ax1.tick_params(axis='y', labelcolor=color)

ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

color = 'tab:blue'
ax2.set_ylabel('sync', color=color)  # we already handled the x-label with ax1
# for 
ax2.plot(f.grid, sync_D, color=color)
ax2.tick_params(axis='y', labelcolor=color)


ax.plot(f.grid, f.T)
ax.plot(f.grid, f.T)

plt.show()


