function [ varargout ] = libSDR_PCA(train_x,test_x,dim)
if nargout == 0
    error('没有输出变量程序不工作 n(-_-)n zzZZ')
end
varargout = cell(1,nargout);
W = pca(train_x);
[~,max_dim]=size(W);
if dim > max_dim
    error('维度大于数据个数，请重设维度。')
end
W = W(:,1:dim);
varargout{1} = W;
[~,dim_train] = size(train_x);
[~,dim_test] = size(test_x);
if nargout>=2
    varargout{2} = train_x*W;
end
if nargout>=3
    if dim_train == dim_test
        varargout{3} = test_x*W;
    else
        varargout{3} = [];
    end
end
end

