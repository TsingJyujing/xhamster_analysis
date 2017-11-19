DRDim = 64;
K = 127;
load('sp_mat_mat.mat')
[u,s,v] = svds(spmat,DRDim);
ds = diag(s);
ru = bsxfun(@times,u,ds(:)');
res = kmeans(ru,K);
[W] = libSDR_LDA(res,ru,3);
Dru = ru*W;
figure(1);
hold on;
for i = 1:K
    plot3(Dru(res==i,1),Dru(res==i,2),Dru(res==i,3),'.')
end
hold off;