function x = mincut(W, maxSize)

n = size(W, 1);
k = 1;

cvx_solver Gurobi
cvx_begin

variable x(n, 1) binary
expression f1(n, n)
for i = 1:n
    for j = 1:n
        f1(i, j) = W(i, j)*pos(x(i)-x(j));
    end
end
expression f2(n, n)
for i = 1:n
    for j = 1:n
        f2(i, j) = W(i, j)*pos(x(j)-x(i));
    end
end
expression f0(n, n)
for i = 1:n
    for j = 1:n
        f0(i, j) = W(i, j)*min(x(i), x(j));
    end
end

minimize (sum(f1(:)) + sum(f2(:)))
subject to
%     x >= 0;
%     x <= 1;
    x(k) == 1;
    sum(x) <= maxSize;
cvx_end

end