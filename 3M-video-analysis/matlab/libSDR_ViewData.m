function libSDR_ViewData( train_y,train_x,varargin )
if nargin == 2
elseif nargin == 4
    test_x = varargin{2};
    test_y = varargin{1};
else
    error('输入参数个数错误')
end
W=libSDR_LDA(train_y,train_x,3,1,0);
clsnum=length(unique(train_y));
ID=unique(train_y);
vy=train_x*W;
label_colors = {'r','g','b','m','k','c','w','y'};
label_shapes = {'.','*','o','h','^'};
n = 0;
for j = 1:length(label_shapes)
    for i = 1:length(label_colors)
        n=n+1;
        draw{n}=[label_colors{i},label_shapes{j}];
    end
end
legend_label = {};
n = 0;
for c=1:clsnum
    n=n+1;
    lst=find(train_y==ID(c));
    plot3((vy(lst,1)),(vy(lst,2)),(vy(lst,3)),draw{mod(n,length(draw))})
    hold on
    legend_label{n} = [num2str(ID(c)),'(train)'];
end
if nargin == 4
    vy=test_x*W;
    for c=1:clsnum
        n=n+1;
        lst=find(test_y==ID(c));
        plot3((vy(lst,1)),(vy(lst,2)),(vy(lst,3)),draw{mod(n,length(draw))})
        hold on
        legend_label{n} = [num2str(ID(c)),'(test)'];
    end
end
legend(legend_label)
hold off
end

