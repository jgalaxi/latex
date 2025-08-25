% creep_model_full.m - Modelo simple de rotura por fluencia en aceros de caldera
% t_r = A * sigma^(-n) * exp(Q/(R*T))

R = 8.314;    % J/mol-K
Q = 240e3;    % J/mol
n = 4.0;

% -------- Funciones anónimas --------
hoop_stress_MPa = @(p_bar, r_mm, t_mm) (p_bar*0.1) .* (r_mm ./ t_mm);
calibrate_A = @(tr_minutes, T_C, sigma_MPa) ...
    (tr_minutes*60) ./ ( (sigma_MPa.^(-n)) .* exp(Q./(R*(T_C+273.15))) );

% Calibración con dato del caso: 900 °C, 50 MPa → 15 min
A = calibrate_A(15.0, 900.0, 50.0);

rupture_time_seconds = @(T_C, sigma_MPa) ...
    A .* (sigma_MPa.^(-n)) .* exp(Q./(R*(T_C+273.15)));

% -------- Ejemplo numérico --------
r = 50; t = 5; p = 50; T = 900;
sigma = hoop_stress_MPa(p, r, t);
tr_s = rupture_time_seconds(T, sigma);
fprintf('Sigma=%.1f MPa, Tiempo a rotura=%.1f min\n', sigma, tr_s/60);

% -------- Gráficos --------
% 1) Tiempo a rotura vs Temperatura
temps_C = linspace(800, 1000, 81);
stresses = [30, 40, 50, 60];
figure; hold on;
for s = stresses
    tr = rupture_time_seconds(temps_C, s);
    semilogy(temps_C, tr/60, 'DisplayName', sprintf('%.0f MPa', s));
end
xlabel('Temperatura (°C)');
ylabel('Tiempo a rotura (min, log)');
title('t_r vs T para distintas tensiones');
legend show; grid on;

% 2) Tiempo a rotura vs Tensión
sigmas = linspace(20, 80, 200);
temps2 = [850, 900, 950];
figure; hold on;
for T = temps2
    tr = rupture_time_seconds(T, sigmas);
    semilogy(sigmas, tr/60, 'DisplayName', sprintf('%d °C', T));
end
xlabel('Tensión circunferencial (MPa)');
ylabel('Tiempo a rotura (min, log)');
title('t_r vs σ para distintas temperaturas');
legend show; grid on;

% 3) Sensibilidad a espesor
t_vals = linspace(3, 8, 100);
trs = zeros(size(t_vals));
for i=1:length(t_vals)
    sigma = hoop_stress_MPa(50, r, t_vals(i));
    trs(i) = rupture_time_seconds(900, sigma)/60;
end
figure;
semilogy(t_vals, trs, 'r');
xlabel('Espesor (mm)');
ylabel('Tiempo a rotura (min, log)');
title('Sensibilidad a espesor (p=50 bar, T=900 °C)');
grid on;

% 4) Sensibilidad a presión
p_vals = linspace(30, 70, 100);
trs = zeros(size(p_vals));
for i=1:length(p_vals)
    sigma = hoop_stress_MPa(p_vals(i), r, 5);
    trs(i) = rupture_time_seconds(900, sigma)/60;
end
figure;
semilogy(p_vals, trs, 'b');
xlabel('Presión (bar)');
ylabel('Tiempo a rotura (min, log)');
title('Sensibilidad a presión (t=5 mm, T=900 °C)');
grid on;
