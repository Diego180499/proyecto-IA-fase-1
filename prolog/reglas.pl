% ============================================================
% Doctor Byte - Reglas de inferencia
% Reglas: posible_falla/2, posible_recomendacion/2,
%         diagnosticar/3, obtener_sintomas/1
% ============================================================

% ----------------------------------------------------------
% Regla: dado un sintoma S de la lista, inferir Falla
% Usa member/2 para iterar sobre la lista de sintomas.
% ----------------------------------------------------------
posible_falla(Sintomas, Falla) :-
    member(S, Sintomas),
    causa(S, Falla).

% ----------------------------------------------------------
% Regla: dada una falla, obtener su recomendacion
% ----------------------------------------------------------
posible_recomendacion(Falla, Rec) :-
    recomendacion(Falla, Rec).

% ----------------------------------------------------------
% Regla principal de diagnostico con corte (!) para evitar
% duplicados y la ejecucion del caso fallback cuando ya
% existe al menos una falla valida.
%   diagnosticar(Sintomas, Fallas, Recomendaciones)
% ----------------------------------------------------------
diagnosticar(Sintomas, Fallas, Recomendaciones) :-
    findall(F, posible_falla(Sintomas, F), FallasRaw),
    list_to_set(FallasRaw, Fallas),
    Fallas \= [],
    !,
    findall(R, (member(F, Fallas), posible_recomendacion(F, R)), RecsRaw),
    list_to_set(RecsRaw, Recomendaciones).

% Caso fallback: ningun sintoma reconocido o sin fallas asociadas
diagnosticar(_, [sin_diagnostico], [rec_servicio_tecnico]).

% ----------------------------------------------------------
% Regla: retorna la lista completa de sintomas disponibles
% ----------------------------------------------------------
obtener_sintomas(Sintomas) :-
    findall(S, sintoma(S), Sintomas).

% ----------------------------------------------------------
% Regla: retorna la lista completa de fallas diagnosticables
% (a partir del conjunto de fallas con recomendacion definida)
% ----------------------------------------------------------
obtener_fallas(Fallas) :-
    findall(F, recomendacion(F, _), FallasRaw),
    list_to_set(FallasRaw, Fallas).
