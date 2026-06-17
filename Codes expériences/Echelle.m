% Par Robin LAPERRIÈRE le 9/06/2026

%{
À partir d'une image de référence, permet d'avoir l'échelle
de cette dernière et le rapport distance/pixel
%}

%% Chargement image

dossier = '/home/rlqperri/Desktop/Acquisitions/20260610/'; %Dossier
addpath(dossier);
nom = 'Echelle'; % nom de l'image

D_reel = 0.04 ; %taille de l'échelle, connue (en m)

image_rgb = imread([dossier, nom, '.png']);
image = im2gray(image_rgb);

figure(1)
clf;
imagesc(image)
hold all
colormap('gray')
axis image

[x,y]=ginput(2);

close all

D_px = ((x(2)-x(1)).^2 + (y(2)-y(1)).^2).^(1/2);

r = D_reel/D_px; % Rapport m/px

disp(r);
