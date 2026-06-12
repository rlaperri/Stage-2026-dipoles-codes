% D'après un code écrit probablement par Christophe BROUZET et/ou Nathan BAGSHAW
% Par Robin LAPERRIÈRE le 9/06/2026

%{
DESCRIPTION:
A partir d'une certaine video de dipôle, permet de relever la vitesse
de ce dernier ainsi que sa taille caractéristitque en fonction du temps
pour en déduire le nombre de Reynolds

Deux pointages : 
- Un à la tête du dipôle (ou l'une de ses têtes lors de la collision)
- Un aux deux extrémités du dipôles afin de quantifier sa largeur
%}

r = 0.0002; % En m/px, conversion en cm (d'après le code Echelle.m)
nu = 10.^-6; % Viscosité cinématique de l'eau (en m2/s)

%% Chargement vidéo

dossier = '/home/rlqperri/Desktop/Acquisitions/20260605/'; %Dossier
addpath(dossier);
nom = 'mov_13'; %nom vidéo (sans l'extension)
vid=VideoReader([dossier, nom, '.mp4']); %changer l'extension si besoin

%{
Sur Ubuntu,la fonction VideoReader peut donner des problèmes, vérifier 
que le module gstreamer est bien mis à jour, updater apt et redémarrer
la machine : https://stackoverflow.com/questions/33486233/unable-to-initialize-the-video-obtain-properties-videoreader-in-matlab
%}

%% Scan vidéo
t0= 1; % Indice de début du scan
tf = 80; %Indice de fin de scan
N = 5; % Nombre de pointages

%{
Si l'analyse se fait sur un intervalle de temps logarithmique
time=unique(floor(logspace(log10(t0),3,50)));
%}

time = unique(floor(linspace(t0, tf, N)));

framerate = 22.30; %En fps

% Listes des coordonnées x et y de la tête aux différents instants
X = zeros(1,N); Y = zeros(1,N);

% Liste de la largeur du dipôle aux différents instants
L_dipole = zeros(1,N);

k=1; % indice de la boucle
for i = 1:length(time)  
    %{
    Cette boucle permet de pointer un objet de la vidéo
    sur l'intervalle de temps choisi
    %}

    % ouverture vidéo
    disp(i);
    t=time(i);
    im_rgb=(read(vid,t));
    im=double(rgb2gray(im_rgb));
    
    % représentation de la frame
    figure(1)
    clf;
    imagesc(im)
    hold all
    colormap('gray')
    axis image
    
    % pointage de la tête du dipôle pour le calcul de la vitesse
    [x,y]=ginput(1);
    plot(x,y,'ko')
    X(:,k)=x;
    Y(:,k)=y;

    % pointage de la largeur du dipôle 
    [x,y]=ginput(2);
    plot(x,y,'ko')
    L_dipole(:,k) = ((x(2)-x(1)).^2 + (y(2)-y(1)).^2).^(1/2);

    k=k+1;

end

disp(L_dipole);

%% Calculs des grandeurs pertinentes

% Calcul de la distance de la tête au point initial

T=(time-t0)./framerate; % Intervalle de temps en s

X1=X(1,:)-ones(size(X(1,:)))*X(1,1); 
Y1=Y(1,:)-ones(size(Y(1,:)))*Y(1,1);
D1=r*(X1.^2+Y1.^2).^(1/2); %m

% Calcul des vitesses de la tête

V = r*(D1(2:N) - D1(1:N-1))./(T(2:N) - T(1:N-1)); %m/s

% Calcul du nombre de Reynolds du dipôle

Re = V.*U(1:N-1)/nu;

%% Graphiques 

% Graphique D1 = f(T)

figure(2)
clf;
plot(T,D1,'ko-')

% Si on souhaite passer en échelle log
%set(gca,'YScale','log')
%set(gca,'XScale','log')

set(gca,'FontSize',15)
xlabel('$t$ [s]','Interpreter','latex','FontSize',18)
ylabel('Distance [m]','Interpreter','latex','FontSize',18)

hold all

grid on

% Graphique V = f(T)

figure(3)
clf;
plot(T(1:N-1),V,'ko-')

% Si on souhaite passer en échelle log
%set(gca,'YScale','log')
%set(gca,'XScale','log')

set(gca,'FontSize',15)
xlabel('$t$ [s]','Interpreter','latex','FontSize',18)
ylabel('Vitesse [m/s]','Interpreter','latex','FontSize',18)

hold all
grid on

% Graphique L_dipole = f(T)

figure(4)
clf;
plot(T,r*L_dipole,'ko-')

% Si on souhaite passer en échelle log
%set(gca,'YScale','log')
%set(gca,'XScale','log')

set(gca,'FontSize',15)
xlabel('$t$ [s]','Interpreter','latex','FontSize',18)
ylabel('Longeur dipôle[m]','Interpreter','latex','FontSize',18)

hold all
grid on

figure(5)
clf;
plot(T(1:N-1),Re,'ko-')

% Si on souhaite passer en échelle log
%set(gca,'YScale','log')
%set(gca,'XScale','log')

set(gca,'FontSize',15)
xlabel('$t$ [s]','Interpreter','latex','FontSize',18)
ylabel('Re','Interpreter','latex','FontSize',18)

hold all
grid on

