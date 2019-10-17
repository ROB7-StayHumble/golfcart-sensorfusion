figure(1)
imshow('zedcam.png')
[x3,y3] = ginput;
hold on
scatter(x3,y3,'filled','b')
hold on
scatter(x2,y2,'filled','b')