function libSDR_TryClassification( y,x,test_ratio,isrand )
if isrand == 1 %Random Mode
    [~,I] = sort(rand(length(y),1));
    x=x(I,:);
    y=y(I);
end
ClsID = unique(y);
ClsNum= length(ClsID);
train_x=[];
test_x=[];
train_y=[];
test_y=[];
for i = 1:ClsNum
    sub_id = find(y==ClsID(i));
    sub_x = x(sub_id,:);
    sub_y = y(sub_id);
    num_test = round(length(sub_y)*test_ratio);
    sub_test_x = sub_x(1:num_test,:);
    sub_train_x = sub_x((1+num_test):end,:);
    sub_test_y = sub_y(1:num_test);
    sub_train_y = sub_y((1+num_test):end);
    train_x=[train_x;sub_train_x];
    train_y=[train_y;sub_train_y];
    test_x=[test_x;sub_test_x];
    test_y=[test_y;sub_test_y];
end
libSDR_ViewData( train_y,train_x,test_y,test_x )
end

