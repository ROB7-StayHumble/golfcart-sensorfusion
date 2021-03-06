close all

folder = 'lab';

original  = rgb2gray(imread(strcat('zedcam',folder,'.png')));
distorted = rgb2gray(imread(strcat('ircam',folder,'.png')));

subplot(2,2,1);
imshow(original);

subplot(2,2,2);
imshow(distorted);

run(strcat('points/',folder,'/points'));

subplot(2,2,3);
showMatchedFeatures(original,distorted,...
    matchedPtsOriginal,matchedPtsDistorted);
title('Matched points');

subplot(2,2,4);
outputView = imref2d(size(original));
Ir_affine = imwarp(distorted,affine2d(out.tform_affine),'OutputView',outputView);
Ir_project = imwarp(distorted,projective2d(out.tform_project),'OutputView',outputView);
imshow(Ir_affine); 
title('Recovered image');