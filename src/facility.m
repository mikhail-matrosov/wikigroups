load('../data/test/W.mat', 'W');
C = size(W, 1);

opening_costs = 0.5*ones(C, 1);
for i=1:C
    W(i, :) = W(i, :)/sum(W(i, :));
end
assignment_costs = 1 - (1/2*W + 1/3*W^2 + 1/6*W^3);

%cvx_solver Gurobi;
cvx_begin 
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
    
cvx_end 

incVal = Inf;
inc = x;

actList = [1];
nodeSets = {x, []};
valArray = [incVal];


while ~isempty(actList)
    z = find(valArray == min(valArray), 1, 'first');
    node = actList(z);
    actList(z) = [];
    valArray(z) = [];
    x = nodeSets{node, 1};
    varBranch = find(10^(-3) < x & x < 1 - 10^(-3), 1, 'first');
    
    %setting branch variable to 0
    constraints = vertcat(nodeSets{node, 2}, [varBranch, 0]);
    [x1, val] = solveLP (constraints, opening_costs, assignment_costs, C);
    
    if val <= incVal
        if isempty(find(10^(-3) < x1 & x1 < 1 - 10^(-3), 1, 'first'))
            inc = x1;
            incVal = val;
        else
            nodeNum = size(nodeSets, 1) + 1;
            actList = [actList nodeNum];
            valArray = [valArray val];
            nodeSets{nodeNum, 1} = x1;
            nodeSets{nodeNum, 2} = constraints;
        end
    end
    
    %setting branch variable to 1
    constraints = vertcat(nodeSets{node, 2}, [varBranch, 1]);
    [x2, val] = solveLP (constraints, opening_costs, assignment_costs, C);
    
    if val <= incVal
        if isempty(find(10^(-3) < x2 & x2 < 1 - 10^(-3), 1, 'first'))
            inc = x2;
            incVal = val;
        else
            nodeNum = size(nodeSets, 1) + 1;
            actList = [actList nodeNum];
            valArray = [valArray val];
            nodeSets{nodeNum, 1} = x2;
            nodeSets{nodeNum, 2} = constraints;
        end
    end
    
    disp(numel(actList));
    
end
