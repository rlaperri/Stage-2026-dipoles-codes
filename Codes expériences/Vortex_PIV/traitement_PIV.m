%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%% Program pour utiliser les donnees PIV des vortex

clear

pix_per_mm=1;

%% Load data

path_data = ['E:\PIV_Robin\20260610\mov_1\TR_PIV_MPd(4x32x32_75%ov)\PostProc\SlidAvg L=10\'];
%v=loadvec([path_data,'B00021.vc7']); % raw velocity fields
v=loadvec([path_data,'*.vc7']); % raw velocity fields

X=v(1).x;
Y=v(1).y;
n_im=length(v);

U=v(15).vx;
V=v(15).vy;

%% Vorticity calculation from velocity fields

curl = vec2scal(filterf(v,3,'gauss','valid'),'rot'); % computes the vorticity of the phase-averaged velocity fields
%curl = vec2scal(v,'rot'); % computes the vorticity of the phase-averaged velocity fields
Xc=curl(1).x;
Yc=curl(1).y;

vort=curl(15).w;

%% PLot data

figure(1)
clf;
%imagesc(X,Y,sqrt(U'.^2+V'.^2)*1000)
imagesc(X,Y,U')
hold all
%quiver(X(1:pas:end),Y(1:pas:end),U(1:pas:end,1:pas:end)',V(1:pas:end,1:pas:end)','k','AutoScaleFactor',2)
axis image
axis xy
box on
colorbar
colormap('jet')
set(gca,'FontSize',15)
xlabel('$x$ [pix]','Interpreter','latex','FontSize',18)
ylabel('$y$ [pix]','Interpreter','latex','FontSize',18)
title('$v_y$ [pix/s]','Interpreter','latex','FontSize',18)

figure(2)
clf;
%imagesc(X,Y,sqrt(U'.^2+V'.^2)*1000)
imagesc(X,Y,V')
hold all
%quiver(X(1:pas:end),Y(1:pas:end),U(1:pas:end,1:pas:end)',V(1:pas:end,1:pas:end)','k','AutoScaleFactor',2)
axis image
axis xy
box on
colorbar
colormap('jet')
set(gca,'FontSize',15)
xlabel('$x$ [pix]','Interpreter','latex','FontSize',18)
ylabel('$y$ [pix]','Interpreter','latex','FontSize',18)
title('$v_y$ [pix/s]','Interpreter','latex','FontSize',18)

figure(3)
clf;
imagesc(X,Y,1/2.*(U'.^2+V'.^2))
%imagesc(X,Y,V')
hold all
%quiver(X(1:pas:end),Y(1:pas:end),U(1:pas:end,1:pas:end)',V(1:pas:end,1:pas:end)','k','AutoScaleFactor',2)
axis image
axis xy
box on
colorbar
colormap('jet')
set(gca,'FontSize',15)
xlabel('$x$ [pix]','Interpreter','latex','FontSize',18)
ylabel('$y$ [pix]','Interpreter','latex','FontSize',18)
title('$v_y$ [pix/s]','Interpreter','latex','FontSize',18)

figure(4)
clf;
imagesc(Xc,Yc,vort')
%imagesc(X,Y,V')
hold all
%quiver(X(1:pas:end),Y(1:pas:end),U(1:pas:end,1:pas:end)',V(1:pas:end,1:pas:end)','k','AutoScaleFactor',2)
axis image
axis xy
box on
colorbar
colormap('jet')
set(gca,'FontSize',15)
xlabel('$x$ [pix]','Interpreter','latex','FontSize',18)
ylabel('$y$ [pix]','Interpreter','latex','FontSize',18)
title('$v_y$ [/s]','Interpreter','latex','FontSize',18)
