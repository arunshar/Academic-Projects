%Level1 Pyramid
%Original Image (
I = imread('Lenna.png');
I = rgb2gray(I);
I = im2double(I);
I1 = im2double(I);

%Apply gaussian filter  
filter = [1/16, 1/8, 1/16;1/8, 1/4, 1/8;1/16, 1/8, 1/16];
dummy = zeros(3,3);
iter1 = zeros(size(I1,1),size(I1,2));
for ii=2:size(I1,1)-1
    for jj=2:size(I1,2)-1 
        image_segment = I1(ii-1:ii+1,jj-1:jj+1);
        for i=1:3
            for j=1:3
            dummy(i,j) = filter(i,j)*image_segment(i,j);
            end
        end
        iter1(ii,jj) = sum(sum((dummy)));
    end
end
imshow(iter1)

%Get Laplacian
Level1 = I1 - iter1;
imshow(Level1)

if (rem(length(iter1(:,1)),2)==0)
    rows = length(iter1(:,1));
else
    rows = length(iter1(:,1))-1;
end

if (rem(length(iter1(1,:)),2)==0)
    columns = length(iter1(1,:));
else
    columns = length(iter1(1,:))-1;
end

%Level2 Pyramid
%Downscaling 
New = double(zeros(rows/2,columns/2));
k = 1;
i = 1;
while k <= rows
    l = 1;
    j = 1;
    while l <= columns
        New(i,j) = iter1(k,l);
        l = l + 2;
        j = j + 1;
    end
    k = k + 2;
    i = i + 1;
end

%Blurring
I1 = im2double(New);
dummy = zeros(3,3);
iter2 = zeros(size(I1,1),size(I1,2));
for ii=2:size(I1,1)-1
    for jj=2:size(I1,2)-1 
        image_segment = I1(ii-1:ii+1,jj-1:jj+1);
        for i=1:3
            for j=1:3
            dummy(i,j) = filter(i,j)*image_segment(i,j);
            end
        end
        iter2(ii,jj) = sum(sum((dummy)));
    end
end

%Laplacian
Level2 = New - iter2;
imshow(Level2)

if (rem(length(iter2(:,1)),2)==0)
    rows = length(iter2(:,1));
else
    rows = length(iter2(:,1))-1;
end

if (rem(length(iter2(1,:)),2)==0)
    columns = length(iter2(1,:));
else
    columns = length(iter2(1,:))-1;
end

%Level 3 pyramid
New1 = double(zeros(rows/2,columns/2));
k = 2;
i = 1;
while k <= length(iter2)
    l = 2;
    j = 1;
    while l <= length(iter2)
        New1(i,j) = iter2(k,l);
        l = l + 2;
        j = j + 1;
    end
    k = k + 2;
    i = i + 1;
end

imshow(New1)

%Blurring
I1 = im2double(New1);
dummy = zeros(3,3);
iter3 = zeros(size(I1,1),size(I1,2));
for ii=2:size(I1,1)-1
    for jj=2:size(I1,2)-1 
        image_segment = I1(ii-1:ii+1,jj-1:jj+1);
        for i=1:3
            for j=1:3
            dummy(i,j) = filter(i,j)*image_segment(i,j);
            end
        end
        iter3(ii,jj) = sum(sum((dummy)));
    end
end

%Laplacian
Level3 = New1 - iter3;
imshow(Level3)

if (rem(length(iter3(:,1)),2)==0)
    rows = length(iter3(:,1));
else
    rows = length(iter3(:,1))-1;
end

if (rem(length(iter3(1,:)),2)==0)
    columns = length(iter3(1,:));
else
    columns = length(iter3(1,:))-1;
end

%Level 4 Pyramid
%Downscaling
New2 = double(zeros(rows/2,columns/2));
k = 1;
i = 1;
while k <= rows
    l = 1;
    j = 1;
    while l <= columns
        New2(i,j) = iter3(k,l);
        l = l + 2;
        j = j + 1;
    end
    k = k + 2;
    i = i + 1;
end

imshow(New2)

%Bluring
I1 = im2double(New2);
dummy = zeros(3,3);
iter4 = zeros(size(I1,1),size(I1,2));
for ii=2:size(I1,1)-1
    for jj=2:size(I1,2)-1 
        image_segment = I1(ii-1:ii+1,jj-1:jj+1);
        for i=1:3
            for j=1:3
            dummy(i,j) = filter(i,j)*image_segment(i,j);
            end
        end
        iter4(ii,jj) = sum(sum((dummy)));
    end
end

%Laplacian
Level4 = New2 - iter4;
imshow(Level4)

if (rem(length(iter4(:,1)),2)==0)
    rows = length(iter4(:,1));
else
    rows = length(iter4(:,1))-1;
end

if (rem(length(iter4(1,:)),2)==0)
    columns = length(iter4(1,:));
else
    columns = length(iter4(1,:))-1;
end

%Level 5 Pyramid
%Downscaling
New3 = double(zeros(rows/2,columns/2));
k = 1;
i = 1;
while k <= rows
    l = 1;
    j = 1;
    while l <= columns
        New3(i,j) = iter4(k,l);
        l = l + 2;
        j = j + 1;
    end
    k = k + 2;
    i = i + 1;
end

imshow(New3)

%Blurring
I1 = im2double(New3);
dummy = zeros(3,3);
iter5 = zeros(size(I1,1),size(I1,2));
for ii=2:size(I1,1)-1
    for jj=2:size(I1,2)-1 
        image_segment = I1(ii-1:ii+1,jj-1:jj+1);
        for i=1:3
            for j=1:3
            dummy(i,j) = filter(i,j)*image_segment(i,j);
            end
        end
        iter5(ii,jj) = sum(sum((dummy)));
    end
end

%Laplacian
Level5 = New3 - iter5;
imshow(Level5)

%reconstruction

rows = length(New3(:,1));
columns = length(New3(1,:));

final = New3 + Level5;
imshow(final)
%Upsampling
New4 = double(zeros(rows*2,columns*2));
k = 1;
i = 1;
while k < rows
    l = 1;
    j = 1;
    while l < columns
        New4(i,j) = final(k,l);
        New4(i,j+1) = (final(k,l) + final(k,l+1))/2;
        New4(i+1,j) = (final(k,l) + final(k+1,l))/2;
        New4(i+1,j+1) = (final(k,l) + final(k+1,l) + final(k,l+1) + final(k+1,l))/4;
        l = l + 1;
        j = j + 2;
    end
    k = k + 1;
    i = i + 2;
end

double(New4)
imshow(New4)

final2 = New4 + Level4;
imshow(final2)

rows = length(New4(:,1));
columns = length(New4(1,:));

New5 = double(zeros(rows*2,columns*2));
k = 1;
i = 1;
while k < rows
    l = 1;
    j = 1;
    while l < columns
        New5(i,j) = final2(k,l);
        New5(i,j+1) = (final2(k,l) + final2(k,l+1))/2;
        New5(i+1,j) = (final2(k,l) + final2(k+1,l))/2;
        New5(i+1,j+1) = (final2(k,l) + final2(k+1,l) + final2(k,l) + final2(k+1,l))/4;
        l = l + 1;
        j = j + 2;
    end
    k = k + 1;
    i = i + 2;
end

imshow(New5)

final3 = New5 + Level3;
imshow(final3)

rows = length(New5(:,1));
columns = length(New5(1,:));

New6 = double(zeros(rows*2,columns*2));
k = 1;
i = 1;
while k < rows
    l = 1;
    j = 1;
    while l < columns
        New6(i,j) = final3(k,l);
        New6(i,j+1) = (final3(k,l) + final3(k,l+1))/2;
        New6(i+1,j) = (final3(k,l) + final3(k+1,l))/2;
        New6(i+1,j+1) = (final3(k,l) + final3(k+1,l) + final3(k,l) + final3(k+1,l))/4;
        l = l + 1;
        j = j + 2;
    end
    k = k + 1;
    i = i + 2;
end

imshow(New6)

final4 = New6 + Level2;
imshow(final4)

rows = length(New6(:,1));
columns = length(New6(1,:));

New7 = double(zeros(rows*2,columns*2));
k = 1;
i = 1;
while k < rows
    l = 1;
    j = 1;
    while l < columns
        New7(i,j) = final4(k,l);
        New7(i,j+1) = (final4(k,l) + final4(k,l+1))/2;
        New7(i+1,j) = (final4(k,l) + final4(k+1,l))/2;
        New7(i+1,j+1) = (final4(k,l) + final4(k+1,l) + final4(k,l) + final4(k+1,l))/4;
        l = l + 1;
        j = j + 2;
    end
    k = k + 1;
    i = i + 2;
end

imshow(New7)

final5 = New7 + Level1;
imshow(final5)

rows = length(New7(:,1));
columns = length(New7(1,:));

minus = (I- New7);
sqr = power(minus,2);
mse = (sum(sum(sqr)))/(rows*columns);
