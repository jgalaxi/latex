function tp2_01
    % Nucleación heterogénea con controles modernos (uifigure + uislider)

    % Crear la ventana
    fig = uifigure('Name','Probabilidad de nucleación');

    % Crear axes en la app
    ax = uiaxes(fig,'Position',[50 100 500 300]);
    title(ax, 'Probabilidad de nucleación heterogénea');
    xlabel(ax, '\DeltaT (subenfriamiento)');
    ylabel(ax, 'P(\DeltaT) (proporcional)');
    grid(ax, 'on');
    ylim(ax,[0 1.05]);

    % Parámetros iniciales
    B_init = 20;
    Tmax = 50;
    DeltaT = linspace(0.1, Tmax, 500);

    % Graficar curva inicial
    P = exp(-B_init ./ DeltaT);
    hLine = plot(ax, DeltaT, P, 'LineWidth', 2);

    % Slider para B
    sldB = uislider(fig,...
        'Position',[100 60 300 3],...
        'Limits',[0 100],...
        'Value',B_init,...
        'ValueChangedFcn',@(sld,evt) updatePlot(sld,DeltaT,hLine,ax));
    % Texto indicador
    lblB = uilabel(fig,'Position',[420 55 50 20],'Text','B');
end

function updatePlot(slider, DeltaT, hLine, ax)
    % Callback que actualiza la curva
    B = slider.Value;
    P = exp(-B ./ DeltaT);
    hLine.YData = P;
    legend(ax, sprintf('B = %.1f', B));
end
