## 25/03/2025

## Lamb dipole colliding into a wall

The setting is inspired from the one considered by Marie Farge et al in [1,2] except that we use a Lamb dipole rather than a Mexican hat vortex.



## Setting
Spatial domain is $[-\pi/2,\pi/2] \times [-\pi,\pi]$.

We wish to integrate the vorticity transport

$\partial_t \omega + {\bf u }\cdot \nabla \omega= \nu \Delta \omega$ ; $\quad {\bf u} = -\nabla^\perp \psi,\quad \psi= -\Delta^{-1} \omega$

subject to no-slip BC at the walls.

The initial condition is a Lamb vortex prescribed by

$
 \omega_0({\bf x}) =
\begin{cases}
    &  -\frac{2Ub}{J_0(b)} J_1(b\frac{r}R) \frac{y}{r} \quad r<R\\
    &   0 \quad r>R
\end{cases}, \quad \psi_0({\bf x}) = \Delta^{-1} \omega_0 
$


Here, $J_0$, $J_1$ are bessel functions of the first kind and $b$ is the first zero of  $J_1$.
$\psi_0$ is periodic in the $y$ direction and has vanishing gradient at $x = \pm \pi/2$, ensuring no-slip and impermeability BC on the wall. In practice,though. the combinations of  finite-resolutions, low viscosity and high porosity coefficient lead to Gibbs-phenomena.


## Method

Our simulations use a penalization method, which consists in integrating the vorticity transport in 
a fully doubly periodic domain $[-\pi,\pi] \times [-\pi,\pi]$, only with the added forcing term in the rhs $f_\eta= -\eta \omega {\mathbf 1}_{|{\bf x}|>\pi/2}$.

$\eta$ is a porosity parameter, which in principle we want to take as large as possible.

## Results

### 1. Free evolution
When setting $\eta=0$, the dipole evolves only under the action of viscosity.

The evolution is most easily analized in the reference frame of the center of mass.
In the presence of viscosity, the Lamb dipole quickly destabilizes.
At each time, we characterize the dipolar structure in terms of a cubic fit 
\begin{equation}
    \omega = a \psi' +b \psi'^3,\quad \psi' = \psi+Uy
\end{equation} 
with $\psi$ the stream function with doubly periodic boundary conditions.  $U$ is determined to minimize scatter in the functionnal relationship between vorticity and stream function. 

The figures reveal show four different stages

- $t \lesssim1$ : transient

- $1\lesssim t\lesssim 20$ :  Stationnary stage, determined by maximal mixing under macroscopic constraints

- $20\lesssim t\lesssim 200$: Diffusive stage

- $200\lesssim t$: Finite-size effects

![Temporal evolution of the vortex velocity (left) and the $a,b$ profile parameters (right)](0-evo.png)

![Temporal evolution of the vortex radius (left) and vorticity norms (rights) ](data/1-evo.png)


![Representative states of each of the stages
](data/2-examples.pdf)


### 2. Collison with the $\eta$-wall

Collision with the wall is signaled by production of vorticity $Z=\int \omega^2$. Convergence as $\alpha$ increases in unclear.

![3 evolutions from a Lamb dipole with $R_0=\pi/16$ and various viscosity and porosity with resolution $N^2=512^2$](data/3-evo.pdf)

![Temporal evolution of Energy and enstrophy at $\nu=2 \times 10^{-3}$ for $N=512$ (dash) and $1024$ (solid)](data/bounce.png)


## How To

The compressed folder minimal contains minimal config

to launch

- Change line 1 of r_MAIN.py to specify python path:

``` #!/xxx/dedalus3/bin/python3```

- Run
```
conda activate dedalus3
chmod +x r_MAIN.py
./r_MAIN.py 
```

- The file r_init.py specifies physical and numerical parameters (including number of procs)

- The file SHOW.py provides minimal example of outputs.

## Biblio

1. [Energy dissipating structures produced by walls in
two-dimensional flows at vanishing viscosity](https://hal.science/hal-01022604/document), Nguyen vab Yen et al, 2011

2. [Production of dissipative vortice by solid bodies in incompressible flows](https://www.umr-lops.fr/content/download/78679/file/M_Farge.pdf), Presentation by M. Farge