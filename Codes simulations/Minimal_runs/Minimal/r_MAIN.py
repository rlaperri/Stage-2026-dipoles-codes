#!/home/sthalabard/miniforge3/envs/dedalus3/bin/python3
#!/home/sthalabard/Software/anaconda3/envs/dedalus3/bin/python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun  2 12:13:38 2024
Gluing Script to launch parallel dedalus runs
@author: sthalabard
"""
#%%
startup_file='r_init.py'
Dedalus_file='r_dedalus.py'
NPROC=4

exec(open(startup_file).read())
print('initialization done!')

#%%
print('Copying into %s' %p.IOtmpOut)
#MAIN=os.path.join(p.IOtmpOut,'main.py')
MAIN='main%02d.py' %i
cmd='cp %s %s; chmod +x %s' %(Dedalus_file, MAIN, MAIN)
os.system(cmd)
paramfile='param%02d.dill' %i
newline='paramfile = "%s"'%paramfile
cmd="sed -i '26c%s' '%s'"%(newline,MAIN)
os.system(cmd)

#%%
if NPROC>1:
    print('Launching mpirun on %d processors....' %NPROC)
    cmd='mpiexec -n %d python3  %s' %(NPROC,MAIN) 
    os.system(cmd)
else:
    print('Launching serial run (no parallelization)')
    cmd='python3  %s' %(MAIN,) 
    os.system(cmd)

#%% CLEA
#OutFolder='/home/sthalabard/DATA/DATA_Arnaud/'
OutFolder='TESTRUN/'
Serie="%s_%s/R%0.3f/%d_nu%0.2e_eta%0.2e" %(p.VORTEXTYPE,p.WALL,p.R,p.N,p.nu,p.eta) 
IO=os.path.join(OutFolder,Serie)
if not os.path.exists(IO):
   print('cleaning into %s' %IO)
   shutil.move(MAIN,os.path.join(p.IOtmpOut,MAIN))
   shutil.move(paramfile,os.path.join(p.IOtmpOut,paramfile))
   shutil.move(p.IOtmpOut,IO)
   os.removedirs(p.IOtmp)
else:
   print('%s already existing: please rename manually' %IO)
