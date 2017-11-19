function [W] = libSDR_SCMF(y,x,Wdim,beta)
%去看libSDR函数的说明
size_y=size(y);
size_x=size(x);
if size_y(1)==1
    size_y=size_y';
    data_x=data_x';
end
size_y=size(y);
size_x=size(x);
W=zeros(Wdim,size_x(2));
for j=1:(Wdim-1)
    w=libSDR_SCSF(y,x,beta);
    w=w./norm(w);
    W(j,:)=w(:)';
    [len,dim] = size(x);
    w = w(:)';
    mw=repmat(w,len,1);
    x=x-repmat(sum(mw.*x,2),1,dim).*mw;
end
w=libSDR_SCSF(y,x,beta);
w=w./norm(w);
W(Wdim,:)=w(:)';
W=W';
end

