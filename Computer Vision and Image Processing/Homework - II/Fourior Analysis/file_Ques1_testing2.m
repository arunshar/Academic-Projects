I = imread('lena.jpg');
I = rgb2gray(I);
I1 =  im2double(I);
input = imresize(I1, [100 100]); % Resize function is used for the purpose of reducing the complexity
[x1,y1] = size(input);

temp_mat = zeros(x1,y1);
temp_mat = complex(temp_mat);
output_mat = zeros(x1,y1);
output_mat = complex(output_mat);
output_mat3 = zeros(x1,y1);
output_mat3 = double(output_mat3);
%output_mat = im2double(output_mat);
l1 = double(length(input(:,1)));
l2 = double(length(input(1,:)));

k = 1;
k = double(k);
while k <= l1
    l = 1;
    l = double(l);
    while l <= l2
        m = 1;
        m = double(m);
        while m <= l1
            n = 1;
            n = double(n);
            while n <= l2
                temp_mat(m,n) = (input(m,n))*(exp((-1i)*(2*pi)*(((k*m)/l1) + ((l*n)/l2))));
             n = n + 1;
            end
            m = m + 1;
        end
        output_mat(k,l) = sum(sum(temp_mat));
        output_mat2(k,l) = abs(sum(sum(temp_mat)));
        l = l + 1;
    end
    k = k + 1;
end
imshow(output_mat)
output_3 = (1/sqrt(m*n)).*(output_mat2);
output_mat4 = zeros(x1,y1);
row = length(output_mat3(1,:))/2;
column = length(output_mat3(1,:))/2;
output_mat4(row,column) = 255;

%Inverse

temp_mat1 = zeros(x1,y1);
temp_mat1 = complex(temp_mat1);
output_mat5 = zeros(x1,y1);
output_mat5 = complex(output_mat);
%output_mat = im2double(output_mat);
l1 = double(length(input(:,1)));
l2 = double(length(input(1,:)));

k = 1;
k = double(k);
while k <= l1
    l = 1;
    l = double(l);
    while l <= l2
        m = 1;
        m = double(m);
        while m <= l1
            n = 1;
            n = double(n);
            while n <= l2
                temp_mat1(m,n) = (output_mat(m,n))*(exp((1i)*(2*pi)*(((k*m)/l1) + ((l*n)/l2))));
             n = n + 1;
            end
            m = m + 1;
        end
        output_mat5(k,l) = sum(sum(temp_mat1));
        output_mat3(k,l) = abs(sum(sum(temp_mat1)));
        l = l + 1;
    end
    k = k + 1;
end
final_output = (1/(m*n)).*(output_mat5);
imshow(output_mat5)
imshow(final_output)

%Mean Square Error 
a1 = abs(final_output);
minus = (input - a1);
sqr = power(minus,2);
mse = (sum(sum(sqr)));