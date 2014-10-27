function clusterILP = ILP_fun(maxSize, cluster1, cluster2)

% Finds smaller cluster inside provided clusters
% cluster1, cluster 2 - cluster indices 

load('../data/A_6800.mat', 'A');
A = double(logical(A));
% load('../data/correct_clusters.mat');
% cluster1 = cluster_cole + 1;
% cluster2 = cluster_tom + 1;
W = A([cluster1; cluster2], [cluster1; cluster2]);

[r, c] = find(W);

n = size(W, 1);
m = size(r, 1);

%cvx_solver Gurobi;
cvx_begin
variable x(n, 1) 
expressions y(m, 1) 
for i = 1:m
    y(i) = min([x(r(i)), x(c(i))]);
end

maximize sum(y(:))
subject to
    sum(x) <= maxSize;
    x >= 0;
    x <= 1;
cvx_end

x = x>0.5;

z = find(x(1:numel(cluster1)));
clusterILP = cluster1(z);
z = find(x(numel(cluster1)+1:end));
clusterILP = [clusterILP; cluster2(z)];
clusterILP = clusterILP-1;

end