% ============================================================
% Doctor Byte - Archivo raiz del motor de inferencia
% Consulta (include) los demas archivos de la base de
% conocimiento. Este es el archivo que carga prolog_service.py
% ============================================================

:- consult('base_conocimiento.pl').
:- consult('descripciones.pl').
:- consult('reglas.pl').
:- consult('persistencia.pl').
