function [W] = libSDR_MCEP(label_y,data_x,Wdim,beta)
%去看libSDR函数的说明
size_y=size(label_y);
size_x=size(data_x);

if size_y(1)==1
    size_y=size_y';
    data_x=data_x';
end
size_y=size(label_y);
size_x=size(data_x);

W=zeros(Wdim,size_x(2));

ClsID=unique(label_y);
ClsNum=length(ClsID);
Sb=zeros(size_x(2));
m=sum(data_x)./length(data_x);
Sw = zeros(size_x(2));
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
W = real(EigVec(:,1:Wdim));
end
