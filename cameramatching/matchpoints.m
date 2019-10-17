close all

original  = rgb2gray(imread('zedcam.png'));
distorted = rgb2gray(imread('ircam.png'));

subplot(2,2,1);
imshow(original);

subplot(2,2,2);
imshow(distorted);

matchedPtsOriginal  = [ [810.7,115.3],
                        [819.7,145.3],
                        [797.2,178.3],
                        [917.2,262.3],
                        [480.7,274.3],
                        [486.7,160.3],
                        [476.2,68.75],
                        [474.8,109.3],
                        [473.2,313.3],
                        [495.7,433.2],
                        [489.8,335.8],
                        [486.7,335.8],
                        [309.7,506.8],
                        [294.8,497.8],
                        [885.7,449.7],
                        [788.2,385.3],
                        [964.2,607.2],
                        [805,499.7],
                        [785.5,436.3],
                        [874.9,273.1],
                        [916.3,381.9],
                        [872.3,388.3],
                        [846.4,363.7],
                        [841.2,357.3],
                        [517.5,458.3],
                        [638.2,95.75],
                        [639.7,154.3],
                        [635.2,170.8],
                        [641.2,415.3]];
                    
matchedPtsDistorted = [ [550.2,93.45],
                        [569.1,124.6],
                        [541.3,159.1],
                        [661.5,268.2],
                        [198.5,274.9],
                        [210.7,155.8],
                        [204,72.3],
                        [200.7,110.1],
                        [192.9,319.4],
                        [219.6,473.4],
                        [209.6,345],
                        [202.9,348.4],
                        [62.65,509.8],
                        [41.5,492],
                        [628.1,461.9],
                        [542.4,380.6],
                        [694.5,590.8],
                        [544.5,511.3],
                        [529.5,440.8],
                        [630,271.2],
                        [661.5,394.3],
                        [618,401.8],
                        [594,373.3],
                        [591,364.3],
                        [243,466.3],
                        [374.2,76.25],
                        [374.2,137.8],
                        [372.8,157.2],
                        [375.8,413.8]];

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