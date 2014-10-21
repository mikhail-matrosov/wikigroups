clusterSizes = [30 10 5];
pInside = 0.3;
pOutside = 0.05;

W = zeros(sum(clusterSizes));
k = 0;
names = cell(sum(clusterSizes), 1);

for i = 1:numel(clusterSizes)
    W(k + 1:k + clusterSizes(i), :) = ...
        binornd(1, pOutside, [clusterSizes(i), sum(clusterSizes)]);
    W(k + 1:k + clusterSizes(i), k + 1:k + clusterSizes(i)) = ...
        binornd(1, pInside, [clusterSizes(i), clusterSizes(i)]);
    for j = 1:clusterSizes(i)
        names{k+j} = strcat(num2str(i), '_');
        names{k+j} = strcat(names{k+j}, num2str(j));
    end
    k = k + clusterSizes(i);
end

if ~exist('../../data/test', 'dir')
    mkdir('../../data/', 'test');
end

save('../../data/test/W.mat', 'W');
save('../../data/test/names.mat', 'names');