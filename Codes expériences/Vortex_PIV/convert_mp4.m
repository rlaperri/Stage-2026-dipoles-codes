%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%% Program to read avi and to write tif

clear

%% Load video

vid=VideoReader('E:\PIV_Robin\20260610\mov_11.mp4');

%% Save avi

writer = VideoWriter("E:\PIV_Robin\20260610\mov_11.avi","Uncompressed AVI");
writer.FrameRate = vid.FrameRate;
open(writer);

while hasFrame(vid)
    img = readFrame(vid);
    writeVideo(writer,img)
end

clear vid
close(writer)

% %% Save tiff
% k=1;
% while hasFrame(vid)
%     frame = readFrame(vid);
%     t = Tiff(['F:\stage_Nathan\data\essai51\image',num2str(k),'.tiff'],'w'); 
%     tagstruct.ImageLength = size(frame,1); 
%     tagstruct.ImageWidth = size(frame,2);
%     tagstruct.Photometric = Tiff.Photometric.RGB;
%     tagstruct.BitsPerSample = 8;
%     tagstruct.SamplesPerPixel = 3;
%     tagstruct.PlanarConfiguration = Tiff.PlanarConfiguration.Chunky; 
%     tagstruct.Software = 'MATLAB'; 
%     setTag(t,tagstruct)
%     
%     write(t,frame)
%     close(t)
% 
%     k=k+1;
% end