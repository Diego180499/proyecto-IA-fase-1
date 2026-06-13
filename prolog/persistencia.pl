% ============================================================
% Doctor Byte - Persistencia (predicados dinamicos)
% Mecanismo 1 (opcional): hechos dinamicos del historial.
%
% NOTA: Para la Fase 1 la persistencia del historial se
% gestiona desde Python (historial_service.py) en formato
% JSON. Este archivo se incluye como soporte del Mecanismo 1
% descrito en el analisis y para mantener a Prolog extensible.
% ============================================================

:- dynamic historial_diagnostico/4.
% historial_diagnostico(ID, Sintomas, Fallas, Timestamp)

% ----------------------------------------------------------
% Regla dinamica: registra un diagnostico en memoria.
%   registrar_diagnostico(ID, Sintomas, Fallas)
% ----------------------------------------------------------
registrar_diagnostico(ID, Sintomas, Fallas) :-
    get_time(T),
    assertz(historial_diagnostico(ID, Sintomas, Fallas, T)).

% ----------------------------------------------------------
% Regla: persiste todos los hechos del historial a un archivo
% usando tell/1 + portray_clause/1 + told/0.
%   save_historial(+RutaArchivo)
% ----------------------------------------------------------
save_historial(Ruta) :-
    tell(Ruta),
    ( historial_diagnostico(ID, S, F, T),
      portray_clause(historial_diagnostico(ID, S, F, T)),
      fail
    ; true
    ),
    told.
