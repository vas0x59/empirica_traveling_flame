*empirica_traveling_flame*

> ### Странствующий огонек 
> При некоторых условиях пламя может двигаться по открытому каналу (см. ссылку). 
> Объясните это явление.  https://www.youtube.com/watch?v=SqhXQUzVMlQ
>
> Исследуйте **время жизни** (2) и **скорость** (1) такого пламени.
>
> При каких **условиях** оно демонстрирует **периодическое поведение**?  (3)
>
> Получите **максимальное время жизни** странствующего огонька для **заданного количества топлива**.  (4)
>

# Теория

## Cкорость пламени (1)
### Модель 1:


Тут схема


#### 0. огонек набигает на смесь fuel + o2 + n2
#### 1. Рассматривается передний фронт горения, считаем, что это premixed combustion.
#### 2. Скорость огонька опредляется максимальной нормальной скоростью горения, которая достижима при концентрациях над каналом. 
> *(**для н. у. и этилового спирта** (см. график из п. 3) это по идее сразу над поверхностью, и соответсвует концентрации удовл. $P_{fuel} = P_{sat}$)*
>
> *(но у поверности есть жидкость (отводит тепло ?) )*
>
> *(в любов случаи можно определеить порядок скоретей для диапозона концентраций)* 
#### 3. Решаем в системе отсчета закрепленной за пламенем в 1D
Используем Cantera  https://cantera.org/science/flames.html
##### Equations:
Continuity:

$$
\frac{\partial \rho u}{\partial x} = 0
$$

Energy: 

$$
\rho c_p u \frac{\partial T}{\partial z} =
    \frac{\partial}{\partial z}\left(\lambda \frac{\partial T}{\partial z}\right)
    - \sum_k j_k \frac{\partial h_k}{\partial z}
    - \sum_k h_k W_k \dot{\omega}_k
$$

Species:

$$
\rho u \frac{\partial Y_k}{\partial z} = - \frac{\partial j_k}{\partial z}
    + W_k \dot{\omega}_k
$$

Diffusive Fluxes:

$$
j_k = \frac{\rho W_k}{\overline{W}^2} \sum_i W_i D_{ki} \frac{\partial X_i}{\partial z}
      - \frac{D_k^T}{T} \frac{\partial T}{\partial z}
$$


##### BC:

Inlet boundary:

$$
T(z_0) = T_0
\\
\dot{m}_0 Y_{k,0} - j_k(z_0) - \rho(z_0) u(z_0) Y_k(z_0) = 0
$$

Outlet boundary:

$$
\left.\frac{\partial T}{\partial z}\right|_{z_0} = 0
\\
\left.\frac{\partial Y_k}{\partial z}\right|_{z_0} = 0
$$

Понятно, что решение, когда ничего не прореагировало тоже подходит под ур. 
Решение с пламянем получаем т к начально предположение = состоянию равновесия смеси исходной (на inlet) .

$\dot{\omega}_k$ Получаем из мехнизма реакции.

см. [Мехнизмы химической реакции](physics/chemistry/MECHs.md)
