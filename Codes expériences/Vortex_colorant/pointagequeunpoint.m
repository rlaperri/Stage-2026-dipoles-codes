%% load video

folder = 'C:\Users\install\Videos\';
name = 'PIV1';

vid=VideoReader([folder,name,'.avi']);

%%
t0=17;

X=zeros(1,30);
Y=zeros(1,30);
k=1;
time=unique(floor(logspace(log10(t0),3,50)));
for i = 1:length(time)   
    t=time(i);
    im_rgb=(read(vid,t));
    im=double(rgb2gray(im_rgb));
    
    figure(1)
    clf;
    imagesc(im)
    hold all
    %imagesc(im_rgb(:,:,3))
    colormap('gray')
    axis image
    
    % pointer
    
    [x,y]=ginput(1); %tete
    
    plot(x,y,'ko')
    X(:,k)=x;
    Y(:,k)=y;

    k=k+1;

end

% %%
% load(['pointage51mano.mat']);
% D1=D1/0.02338*0.02258;

%%
T=(time-t0)./8.3;
X1=X(1,:)-ones(size(X(1,:)))*X(1,1);
Y1=Y(1,:)-ones(size(Y(1,:)))*Y(1,1);
D1=(X1.^2+Y1.^2).^(1/2)*0.02338;

figure(19)
clf;
plot(T,D1,'ko-')
set(gca,'YScale','log')
set(gca,'XScale','log')
set(gca,'FontSize',15)
xlabel('$t$ [s]','Interpreter','latex','FontSize',18)
ylabel('Distance [cm]','Interpreter','latex','FontSize',18)
xlim([0.1 150])
ylim([0.1 50])
hold all
%plot(timevec,2.2.*timevec.^1,'k--')
plot(timevec,950.5.*timevec.^(0.10),'r--')
grid on
%%
save('pointage61.mat','X1','Y1','t0','T','D1')