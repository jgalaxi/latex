R = 8.314;    
Q = 240e3;    
n = 4.0;

hoop_stress_MPa = @(p_bar, r_mm, t_mm) (p_bar*0.1) .* (r_mm ./ t_mm);
calibrate_A = @(tr_minutes, T_C, sigma_MPa) ...
    (tr_minutes*60) ./ ((sigma_MPa.^(-n)) .* exp(Q./(R*(T_C+273.15))));

A = calibrate_A(15.0, 900.0, 50.0);
rupture_time_minutes = @(T_C, sigma_MPa) ...
    (A .* (sigma_MPa.^(-n)) .* exp(Q./(R*(T_C+273.15)))) / 60.0;

temps_C = linspace(700, 1100, 300);

% Valores iniciales
p0 = 50;   % bar
r0 = 50;   % mm
t0 = 5;    % mm
sigma0 = hoop_stress_MPa(p0, r0, t0);

fig = uifigure('Name','t_r vs T con sliders');
ax = uiaxes(fig,'Position',[50 200 500 300]);
semilogy(ax, temps_C, rupture_time_minutes(temps_C, sigma0), 'LineWidth',2);
xlabel(ax,'Temperatura (°C)');
ylabel(ax,'Tiempo a rotura (min, log)');
title(ax,'Tiempo a rotura vs T');
grid(ax,"on");

% --- Sliders ---
uilabel(fig,'Position',[50 150 100 22],'Text','Presión (bar)');
sld_p = uislider(fig,'Position',[160 160 300 3], ...
    'Limits',[10 100],'Value',p0);

uilabel(fig,'Position',[50 110 100 22],'Text','Radio (mm)');
sld_r = uislider(fig,'Position',[160 120 300 3], ...
    'Limits',[10 100],'Value',r0);

uilabel(fig,'Position',[50 70 100 22],'Text','Espesor (mm)');
sld_t = uislider(fig,'Position',[160 80 300 3], ...
    'Limits',[2 15],'Value',t0);


% --- Callback para actualizar ---
function updatePlot(~,~,ax,temps_C,rupture_time_minutes,hoop_stress_MPa,sld_p,sld_r,sld_t)
    sigma = hoop_stress_MPa(sld_p.Value, sld_r.Value, sld_t.Value);
    semilogy(ax, temps_C, rupture_time_minutes(temps_C, sigma), 'LineWidth',2);
    xlabel(ax,'Temperatura (°C)');
    ylabel(ax,'Tiempo a rotura (min, log)');
    title(ax,sprintf('t_r vs T (σ=%.1f MPa)',sigma));
    grid(ax,"on");
end

% Asociar callbacks
sld_p.ValueChangedFcn = @(src,event) updatePlot(src,event,ax,temps_C,rupture_time_minutes,hoop_stress_MPa,sld_p,sld_r,sld_t);
sld_r.ValueChangedFcn = @(src,event) updatePlot(src,event,ax,temps_C,rupture_time_minutes,hoop_stress_MPa,sld_p,sld_r,sld_t);
sld_t.ValueChangedFcn = @(src,event) updatePlot(src,event,ax,temps_C,rupture_time_minutes,hoop_stress_MPa,sld_p,sld_r,sld_t);