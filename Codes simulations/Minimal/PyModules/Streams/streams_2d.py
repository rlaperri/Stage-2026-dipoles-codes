#!/home/rlqperri/miniconda3/envs/dedalus3/bin/python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 11 15:51:04 2022|
Library to represent 2d flows prescribed by potential and stream function
@author: sthalabard
"""

#% Startup File
import os, sys
import sympy
import  numpy as np
from sympy import besselj, jn
import mpmath, scipy

#%%
#SPECIFY FLOW as the sum
#of potential, irrotationnal and u, v contributions
class flow:
    def __init__(self,verbose=True,psi='0',phi='0',u='0',v='0',steady=True):
        import sympy
        from sympy import besselj, jn
        from sympy import re,im, I,E, symbols
        from sympy.utilities.lambdify import lambdify, implemented_function
        x,y,t=symbols('x y t', real=True)

        # Symbolic calculations
        self.sym={}
        local_dict={'x':x,'y':y,'t':t}
        psi_sym=sympy.parse_expr(psi,local_dict=local_dict)
        phi_sym=sympy.parse_expr(phi,local_dict=local_dict)
        u_sym=sympy.parse_expr(u,local_dict=local_dict)
        v_sym=sympy.parse_expr(v,local_dict=local_dict)
#        print(u_sym,u_sym.diff(x))

        self.sym['u'] =u_sym+sympy.diff(psi_sym,y)+sympy.diff(phi_sym,x)
        self.sym['v'] =v_sym+sympy.diff(-psi_sym,x)+sympy.diff(phi_sym,y)
        self.sym['psi'] =psi_sym
        self.sym['phi'] =phi_sym

        self.sym['om'] = self.sym['v'].diff(x)-self.sym['u'].diff(y)
        self.sym['div'] = self.sym['u'].diff(x)+self.sym['v'].diff(y)
        self.sym['flat'] = self.sym['u'].diff(y)+self.sym['v'].diff(x)


        self.sym['ux'] = self.sym['u'].diff(x)
        self.sym['uy'] = self.sym['u'].diff(y)
        self.sym['vx'] = self.sym['v'].diff(x)
        self.sym['vy'] = self.sym['v'].diff(y)

        # Turn the calculation into numpy functions
        self.steady=steady
        self.lambdify_fields()
        return None

    def lamb(self,field='u'):
        import sympy
        from sympy import besselj, jn
        from sympy import re,im, I,E, symbols
        from sympy.utilities.lambdify import lambdify, implemented_function
        x,y,t=symbols('x y t', real=True)
        bessel = {'besselj':scipy.special.jv,'besselk':scipy.special.kv,'besseli':scipy.special.iv,'bessely':scipy.special.yv}
        libraries = [bessel, "numpy"]     
        tmp= lambdify((x,y,t), self.sym[field],libraries)
        if self.steady:
            return lambda x,y: tmp(x,y,0) +0.*x*y
        else:
            return lambda x,y,t: tmp(x,y,t) +0.*x*y

    def lambdify_fields(self):
        for field in ['u','v','phi','psi','om','div','ux','uy','vx','vy']:
            self.__dict__[field]=self.lamb(field)
        return None

def add(f,g):
    import sympy
    from sympy import re,im, I,E, symbols
    from sympy.utilities.lambdify import lambdify, implemented_function
    x,y,t=symbols('x y t', real=True)
    h=flow()
    for k in ['u','v','psi','phi']:
        h.sym[k]=f.sym[k]+g.sym[k]
    h.lambdify_fields()
    return h

def add_list(fg):
    import sympy
    from sympy import re,im, I,E, symbols
    from sympy.utilities.lambdify import lambdify, implemented_function

    x,y,t=symbols('x y t', real=True)
    h=flow()
    for k in ['u','v','psi','phi']:
        for i,f in enumerate(fg):
            if i==0:
                h.sym[k]=f.sym[k]
            else:
                h.sym[k]=h.sym[k]+f.sym[k]
    h.lambdify_fields()
    return h

class lagrangian:
    def __init__(self,xy=(0,0),theta=0,V=1,t=0):
        self.x,self.y=xy
        self.theta=theta
        self.logV=0
        self.t=t

    def update(self,dt=0.01,flow=flow):
        k1x=self.x+flow.u(self.x,self.y,self.t)*dt*0.5
        k1y=self.y+flow.v(self.x,self.y,self.t)*dt*0.5
#        k1theta=self.theta+0.5*flow.om(self.x,self.y,self.t)*dt*0.5
#        k1V=self.logV+0.5*np.log(1+flow.div(self.x,self.y,self.t))*dt*0.5


        self.x=self.x+flow.u(k1x,k1y,0.5*dt+self.t)*dt
        self.y=self.y+flow.v(k1x,k1y,0.5*dt+self.t)*dt
        self.theta=self.theta+0.5*flow.om(k1x,k1y,0.5*dt+self.t)*dt
        self.logV=self.logV+ np.log(1+0.5*flow.div(k1x,k1y,0.5*dt+self.t))*dt

        self.t=self.t+dt
        return None
    
    def trajectory(self,trange=None,flow=flow):
        dt=trange[1]-trange[0]
        self.traj={}
        for field in ['x','y','u','v','t','theta','om','div']:
            self.traj[field]=np.zeros_like(trange)

        for i,t in enumerate(trange):
            self.update(flow=flow,dt=dt)
            self.traj['u'][i]=flow.u(self.x,self.y,self.t)
            self.traj['v'][i]=flow.v(self.x,self.y,self.t)
            self.traj['x'][i]=self.x
            self.traj['y'][i]=self.y
            self.traj['t'][i]=self.t
            self.traj['theta'][i]=self.theta
            self.traj['om'][i]=flow.om(self.x,self.y,self.t)
            self.traj['div'][i]=flow.div(self.x,self.y,self.t)

        return None
    
    def vorticity_meter(self,ell=0.1,xyt=None):
        if xyt is None:
            xyt=self.x,self.y,self.theta
        x,y,theta=xyt
        t1,t2=np.array([-np.cos(theta), np.cos(theta)]),np.array([-np.sin(theta),np.sin(theta)])
        t3,t4=np.array([-np.sin(theta), np.sin(theta)]),np.array([np.cos(theta), -np.cos(theta)])

        return x+ell*t1,y+ell*t2,x+ell*t3,y+ell*t4
#%% Quelques flots particuliers
def sink(xy=(0,0),chi=1,epsilon=1e-1,smooth=0):
    x0,y0=xy
    dr='((x-%0.2f)**2+(y-%0.2f)**2+%0.2f)**0.5' %(x0,y0,smooth)
    tmp_str='-%s *(1-exp(-(%0.5f/%0.5f)**6))/(2*pi*%s)' %(chi,dr,epsilon,dr)
    return flow(phi=tmp_str)

def vortex(xy=(0,0),chi=1,epsilon=1e-1,smooth=0):
    x0,y0=xy
    dr='((x-%0.2f)**2+(y-%0.2f)**2+%0.2f)**0.5' %(x0,y0,smooth)
    tmp_str='-%s *(1-exp(-(%0.5f/%0.5f)**6))/(2*pi*%s)' %(chi,dr,epsilon,dr)
    return flow(psi=tmp_str)
