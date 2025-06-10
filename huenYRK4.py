import numpy as np
import matplotlib.pyplot as plt

# Método de Heun (RK2)
def heun(f, t, y0):
    y = np.zeros(len(t))
    y[0] = y0
    h = t[1] - t[0]
    for i in range(len(t) - 1):
        k1 = f(t[i], y[i])
        k2 = f(t[i+1], y[i] + h * k1)
        y[i+1] = y[i] + (h / 2) * (k1 + k2)
    return y

# Método de Runge-Kutta 4to orden
def rk4(f, t, y0):
    y = np.zeros(len(t))
    y[0] = y0
    h = t[1] - t[0]
    for i in range(len(t) - 1):
        k1 = f(t[i], y[i])
        k2 = f(t[i] + h/2, y[i] + h * k1 / 2)
        k3 = f(t[i] + h/2, y[i] + h * k2 / 2)
        k4 = f(t[i] + h, y[i] + h * k3)
        y[i+1] = y[i] + (h / 6) * (k1 + 2*k2 + 2*k3 + k4)
    return y

# --- Ejercicio 37: Población ---

# Parámetros del problema
k = 0.000095
NM = 5000
N0 = 100
t0 = 0
tf = 20
n = int((tf - t0) / h) + 1
t_37 = np.linspace(0, 20, n)
h = 0.1

# Función diferencial
def f37(t, N):
    return k * N * (NM - N)

# Soluciones
N_heun = heun(f37, t_37, N0)
N_rk4 = rk4(f37, t_37, N0)

# --- Ejercicio 39: Crecimiento de tumor ---

# Parámetros
alpha = 0.8
k_39 = 60
nu = 0.25
A0 = 1
t_39 = np.linspace(0, 30, 31)  # paso de 1 día

# Función diferencial
def f39(t, A):
    return alpha * A * (1 - (A / k_39)**nu)
# Soluciones
A_heun = heun(f39, t_39, A0)
A_rk4 = rk4(f39, t_39, A0)

# --- Ejercicio 40: Caída libre con fricción cuadrática ---

# Parámetros
m = 5
g = 9.81
k_40 = 0.05
v0 = 0
t_40 = np.linspace(0, 15, 151)  # paso de 0.1 s

# Función diferencial
def f40(t, v):
    return -g + (k_40 / m) * v**2

# Soluciones
v_heun = heun(f40, t_40, v0)
v_rk4 = rk4(f40, t_40, v0)

# iteraciones
def print_table(title, t, heun_vals, rk4_vals):
    print(f"\n--- {title} ---")
    print(f"{'t':>6} {'Heun':>15} {'RK4':>15}")
    print("-" * 40)
    for i in range(len(t)):
        print(f"{t[i]:6.2f} {heun_vals[i]:15.6f} {rk4_vals[i]:15.6f}")

print_table("POBLACIÓN", t_37, N_heun, N_rk4)
print_table("CRECIMIENTO TUMORAL", t_39, A_heun, A_rk4)
print_table("CAÍDA LIBRE", t_40, v_heun, v_rk4)

# --- Gráficas ---

# Población
plt.figure(figsize=(10,6))
plt.plot(t, N_heun, 'o-', label='Heun (RK2)', color='blue')
plt.plot(t, N_rk4, 's-', label='Runge-Kutta 4to orden', color='green')
plt.xlabel('Tiempo (años)')
plt.ylabel('Población N(t)')
plt.title('Crecimiento Poblacional con Capacidad Limitada')
plt.legend()
plt.grid(True)
plt.show()

# Tumor
plt.figure(figsize=(10,5))
plt.plot(t_39, A_heun, 'o-', label='Heun (RK2)', color='blue')
plt.plot(t_39, A_rk4, 's-', label='Runge-Kutta 4to orden', color='green')
plt.title('Crecimiento del área del tumor')
plt.xlabel('Tiempo (días)')
plt.ylabel('Área A(t) [mm²]')
plt.legend()
plt.grid(True)

# Caída libre
plt.figure(figsize=(10,5))
plt.plot(t_40, v_heun, 'o-', label='Heun (RK2)', color='blue')
plt.plot(t_40, v_rk4, 's-', label='Runge-Kutta 4to orden', color='green')
plt.title('Velocidad de objeto en caída libre con fricción cuadrática')
plt.xlabel('Tiempo (s)')
plt.ylabel('Velocidad v(t) [m/s]')
plt.legend()
plt.grid(True)

plt.show()
