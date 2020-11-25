import matplotlib.pyplot as plt # For plotting the swing curve
import math as m # For performing mathematical operations

# Input the necessary inputs

G = 1 # pu
H = 2.5 # Inertia Constant
f = 50 # Frequency

M = (G * H)/(180 * f) # Moment of Inertia

E = 450 # Voltage Behind transient reactance
V = 400 # Generator voltage
MVA = 500 # MVA rating of generator
load = 460 # Load in kW

MVAb = MVA # MVA Base
kVAb = V # kVA Base

X1 = 0.5 # Prefault reactance
X2 = 1.0 # During fault reactance
X3 = 0.75 # Postfault reactance

pfactor = 1000

dt = 0.0002 * pfactor# Swing curve time interval
t1 = 0.066 * pfactor# Fault clearing time
T = 0.5 * pfactor# Total time for execution

Vpu = V / kVAb
Epu = E / kVAb

Pmax1 = (Vpu * Epu)/X1 # Prefault
Pmax2 = (Vpu * Epu)/X2 # During fault
Pmax3 = (Vpu * Epu)/X3 # Postfault

# Prefault power transfer
ppt = load/MVAb


sm = (dt/pfactor)**2/M # Power multiplying factor for estimating change in delta

t = 0 # Initial timestamp

# Output arrays for storing Pe and delta, which will be plotted later
EP = [] # Storing electrical power Pe
DEL = [] # Storing angle delta
TIME = []

# Taking the prefault condition
delta = m.asin(ppt/Pmax1) # Finding initial delta
Pe0 = Pmax1 * m.sin(delta) # Intial electrical power
Pa = ppt - Pe0
ddchange = sm * Pa
while(t <= T):
	TIME = TIME + [t]
	if t == 0:
		Pe = Pmax2 * m.sin(delta)
		Pa = ppt - Pe
		ddchange = (ddchange + (sm * Pa))/2
		EP = EP + [Pe]
		DEL = DEL + [delta * (180/m.pi)]
	elif t < t1:
		delta = ((delta * (180/m.pi)) + ddchange) * m.pi/180
		Pe = Pmax2 * m.sin(delta)
		Pa = ppt - Pe
		ddchange = ddchange + (sm * Pa)
		EP = EP + [Pe]
		DEL = DEL + [delta * (180/m.pi)]
	elif t == t1:
		# Before clearance
		delta = ((delta * (180/m.pi)) + ddchange) * m.pi/180
		Pe = Pmax2 * m.sin(delta)
		Pa = ppt - Pe
		#ddchange = ddchange + (sm * Pa)
		dd1 = (sm * Pa)
		# after clearance
		Pe = Pmax3 * m.sin(delta)
		Pa = ppt - Pe
		dd2 = (sm * Pa)
		ddchange = ddchange + (dd1 + dd2)/2
		#delta = ((delta * (180/m.pi)) + ddchange) * m.pi/180

		EP = EP + [Pe]
		DEL = DEL + [delta * (180/m.pi)]
	else:
		delta = ((delta * (180/m.pi)) + ddchange) * m.pi/180
		Pe = Pmax3 * m.sin(delta)
		Pa = ppt - Pe
		ddchange = ddchange + (sm * Pa)
		EP = EP + [Pe]
		DEL = DEL + [delta * (180/m.pi)]
	t = t + dt


# Plotting swing equation
plt.scatter(TIME, DEL, c = 'r')
#plt.scatter(DEL, EP, c = 'r')
plt.xlabel('time(ms)')
plt.ylabel('Rotor angle (delta)')
plt.show()

