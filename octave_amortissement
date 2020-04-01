clear all; close all;clc;

% Build matrices of the system
M=4; m=4*0.05; 
K=4113.839026; k=186.568254;
C=1.55; 
copt=1.6325;
ci = copt%linspace(copt/4,copt,4); 
%changer copt par linespace(copt/4,copt,4) pour afficher plus de valeurs
acc = 1;

figure;set(gcf,'PaperUnits','centimeters','PaperPosition',[0 0 15 12],...
    'PaperSize',[15 12])
    
COL = lines(6); 


for i2= 1:length(ci);
  
  c = ci(i2)
  

K0=[K+k -k ; -k k];
M0=[M 0 ; 0 m ];
C0=[C+c -c ; -c c];

% Calcul de la réponse de manière directe (conseillé)
w=linspace(0,50,500); %(start,end, N= # de pointillés)
F=[-M*acc; -m*acc];

% Direct reference method
U=zeros(2,length(w)); %crée une matrice 2 lignes et length(w) colonnes avec que des zeros
for i=1:length(w) %Pour chaque i compris entre 1 et 50
  %F(1,1) = F(1,1) + C/1j/w(i)*acc - K/(w(i)^2)*acc;
  U(:,i)=(K0-w(i)^2*M0 + 1j*w(i)*C0)\F;  
end %pour chaque colonne,

%Amplitiude selon amortissement
semilogy(w,(abs(U(1,:))),'color',COL(i2,:),'linewidth',2); hold on ;set(gca,'fontsize',15)
xlabel('Freq (rad/s)'); ylabel('Ampl (m)')
hold on;

end

legend(num2str(ci'))
