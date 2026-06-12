%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%% Par Christophe Brouzet, conversion de mp4 en avi pour Davis

clear

%% Load video

dossier = '/home/rlqperri/Desktop/Acquisitions/20260605/'; %Dossier
addpath(dossier);
nom = 'mov_13'; %nom vidéo en mp4 (sans l'extension)
vid=VideoReader([dossier, nom, '.mp4']); % Video en mp4

%% Conversion en avi

writer = VideoWriter("E:\PIV_Robin\20260610\mov_11.avi","Uncompressed AVI");
writer.FrameRate = vid.FrameRate;
open(writer);

while hasFrame(vid)
    img = readFrame(vid);
    writeVideo(writer,img)
end

clear vid
close(writer)