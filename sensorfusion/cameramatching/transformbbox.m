close all;
folder = 'lab';

orig  = rgb2gray(imread(strcat('zedcam',folder,'.png')));
I = rgb2gray(imread(strcat('ircam',folder,'.png')));

bboxA = [   
            520 265 205 330
            205 140 340 300
        ];

labelsA = ["vivi","window"];

tform = affine2d(out.tform_affine);

rout = affineOutputView(size(orig),tform);
J = imwarp(I,tform,'OutputView',rout);

[bboxB,indices] = bboxwarp(bboxA,tform,rout);
labelsB = labelsA(indices);

annotatedI = insertObjectAnnotation(I,'Rectangle',bboxA,labelsA);
annotatedJ = insertObjectAnnotation(orig,'Rectangle',bboxB,labelsB);
figure
montage({annotatedI, annotatedJ})