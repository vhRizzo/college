clc
clear
close all

PO = 0.15;
ts = 0.4;
te = 0.8;

ec = sqrt(log(PO)^2/(pi^2 + log(PO)^2));
wn = (pi-asin(sqrt(1-ec^2)))/(ts*sqrt(1-ec^2));

num = 1;
den = [1 0.4];

H = tf(wn^2, [1 2*wn*ec wn^2]);
Hdis = c2d(H, 0.01);

sys = tf(num, den);
sysdis = c2d(sys, 0.01);

sysdisma = feedback(sysdis, Hdis);
sysdismf = feedback(11.642*sysdisma, 1);
sysdisma = 11.642*sysdisma;

hold on
step(sysdisma)
impulse(sysdisma)
legend('Resposta ao degrau', 'Resposta ao impulso')
title('Malha Aberta')
xlim([0 4])
hold off

figure

hold on
step(sysdismf)
impulse(sysdismf)
legend('Resposta ao degrau', 'Resposta ao impulso')
title('Malha Fechada')
xlim([0 1])
hold off

figure

subplot(2, 1, 1)
hold on
step(sys)
impulse(sys)
title('Sistema Contínuo')
xlim([0 15])
hold off
subplot(2, 1, 2)
hold on
step(sysdismf)
impulse(sysdismf)
title('Sistema Digital')
xlim([0 0.6])
sgtitle('Comparação Sistema Contínuo Real e Digital Projetado')
hold off
