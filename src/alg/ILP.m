function z = ILP(W)
n = size(W, 1);

% cvx_solver Gurobi;
cvx_begin
variable x(n, 1) binary
variable y(n, n) binary

maximize sum(sum(W'*y))
subject to
    for i = 1:n
        for j = 1:n
            y(i, j) <= x(i);
            y(i, j) <= x(j);
        end
    end
    sum(x) <= 500;

cvx_end

z = find(x);
end