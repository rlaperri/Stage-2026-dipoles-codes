% Written by Christophe BROUZET
% Additional comments by Robin LAPERRIÈRE the 29/05/2026

function y = density_bacs(N , H , L , W , V_lost , position)

%{
DESCRIPTION:
Given the parameters of the tank where we want to create a vertical
and stable stratification using salt, this function returns the two 
densities that one should use in order to fill the tank using the two
buckets methods.
%} 

% ARGUMENTS
% N is the Brunt-Vaisala pulsation that we want
% H (cm) is the height of fluid in the tank
% L (cm) is the length of the tank
% W (cm) is the width of the tank
% V_lost is the volume that remains below the propeller (cm3)
% position : describe how we fill the tank: 'bottom' or 'top'

% RETURNS
% h = height of water that we need in each water bucket
% rho_tank = density in the saltwater bucket
% rho_min = minimum density in the tank
% rho_max = maximum density in the tank


l_bucket = 53; % lenght of the bucket 
w_bucket = 33; % width of the bucket 
rho_water = 998;
%V_lost = y.h_lost*60*60;  % volume that remains below the propeller
V_tot = H*L*W;
r=V_lost/(V_tot/2+V_lost); 
g=9.81;                   % pesanteur
s=1/(g/(N*N*H*0.01)+0.5); % coefficient used to calculate the variation in 
t=1/(g/(N*N*H*0.01)-0.5); % the tank knowing N and H
y.h = V_tot/(2*l_bucket*w_bucket) ; % height of water that we need in each water tank


%y.h = V_tot/(2*1000) ;   % height of water that we need in each water tank

switch position

    case 'bottom' 
        y.rho_tank = rho_water*(1+t/(1-r)); % density in the saltwater tank 
        y.rho_min= rho_water;
        y.rho_max= y.rho_tank*(1-r)+rho_water*r;
    
    
    case 'top'
        y.rho_tank=rho_water*(1-r)/(1-r-s); 
        y.rho_min= rho_water*(1-r)+y.rho_tank*r;
        y.rho_max= y.rho_tank;
     
end

V_lost = 53*33*9;
W = 33; L = 78.5; H = 28;
N_exp = 1.7;
