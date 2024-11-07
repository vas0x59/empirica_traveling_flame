import cantera as ct
import matplotlib.pyplot as plt
import numpy as np

fig, ax = plt.subplots()
file = 'mechanisms/marinov_ethanol/ethanol-marinov.yaml'
# models = {'Original': 'baseline', 'LMR-R': 'linear-Burke'}
# colours = ["xkcd:grey",'xkcd:purple']
Tin = 453  # unburned gas temperature [K]
p=760  # pressure [torr]
n=10 # number of points to simulate
phi_list = np.linspace(0.5,1.8,n) # equivalence ratios to simulate across
# for k, m in enumerate(models):
vel_list = []
gas = ct.Solution(file)
for j, phi in enumerate(phi_list):
    print("NNNNNNNNNNNNNNNNNNN  ", j)
    gas.set_equivalence_ratio(phi, 'c2h5oh', {'O2':1, 'N2': 3.76})
    gas.TP = Tin, (p/760)*ct.one_atm
    f = ct.FreeFlame(gas, grid=np.linspace(0, 0.05, 30))
    f.set_refine_criteria(ratio=3, slope=0.06, curve=0.10)
    # f.transport_model = 'multicomponent' # optionally enable
    # f.soret_enabled = True  # optionally enable
    f.solve(loglevel=1, auto=True)
    vel_list.append(f.velocity[0] * 100) # cm/s
ax.plot(phi_list, vel_list)
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
plt.show()