close all

original  = rgb2gray(imread('zedcam.png'));
distorted = rgb2gray(imread('ircam.png'));

subplot(2,2,1);
imshow(original);

subplot(2,2,2);
imshow(distorted);

points;

subplot(2,2,3);
showMatchedFeatures(original,distorted,...
    matchedPtsOriginal,matchedPtsDistorted);
title('Matched points');

tform_poly = fitgeotrans(matchedPtsDistorted,matchedPtsOriginal,'polynomial',2);

subplot(2,2,4);
outputView = imref2d(size(original));
Jr = imwarp(distorted,tform_poly,'OutputView',outputView);
imshow(Jr); 
title('Recovered image');