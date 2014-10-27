function [x, obj] = solveLP (constraints, opening_costs, assignment_costs, C)

cvx_begin quiet
variable y(C)
variable x(C,C)

minimize sum(y(:).*opening_costs(:))+sum(x(:).*assignment_costs(:)); 
subject to 
    x >= 0;
    x <= 1;
    y >= 0;
    y <= 1;
    max(x,[],2) <= y; 
    sum(x,1) == 1; 
    x(constraints(:, 1)) == constraints(:, 2);
    
cvx_end 

obj = cvx_optval;
end