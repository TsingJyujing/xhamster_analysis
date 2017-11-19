function [W] = libSDR_MCPP(label_y,data_x,Wdim,beta)
%去看libSDR函数的说明
size_y=size(label_y);
size_x=size(data_x);

if size_y(1)==1
    size_y=size_y';
    data_x=data_x';
end

size_y=size(label_y);
size_x=size(data_x);

ClsID=unique(label_y);
ClsNum=length(ClsID);

if(Wdim>ClsNum)
    error('本方法使用预先降维，降维后维度不得大于类数。')
end

Wp = zeros(ClsNum,size_x(2));

for i=1:ClsNum
    disp(['区分类号：',num2str(ClsID(i))])
    flabel_y=label_y;
    flabel_y(find(label_y==ClsID(i)))=0;
    flabel_y(find(label_y~=ClsID(i)))=1;
    Wp(i,:)=libSDR_SCSF(flabel_y,data_x,beta);
end

if (Wdim==ClsNum)
    W=Wp';
else
    data_x=data_x*Wp';
    
    size_y=size(label_y);
    size_x=size(data_x);
    
    Sw=beta.*eye(size_x(2));
    
    Sb=zeros(size_x(2));
    m=sum(data_x)./length(data_x);
    
    
    disp('正在构造多类分类矩阵...')
    for k=1:ClsNum
        NowLable=ClsID(k);
        lst=find(label_y==NowLable);
        Nk=length(lst);
        if Nk<=2
            disp(['类别:',num2str(NowLable),'的样本太少！']);
        end
        Ck=data_x(lst,:);
        mk=sum(Ck)./Nk;
        Dk=Ck-repmat(mk,Nk,1);
        Sk=Dk'*Dk;
        Sw=Sw+Sk;
        Sb=Sb+Nk.*((mk-m)'*(mk-m));
    end
    for i=1:100
        if rank(Sw)<size_x(2)
            Sw=Sw+eye(size_x(2)).*(beta/100);
        else
            break;
        end
    end
    disp(['辅助矩阵系数：',num2str(beta*(i-1))])
    D=Sw\Sb;
    [EigVec,EigVal]=eig(D);
    [~,I] = sort(diag(EigVal),'descend');EigVec = EigVec(:,I);
    W = EigVec(:,1:Wdim)';
    W = real(Wp'*W');
end
end
