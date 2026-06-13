% ============================================================
% Doctor Byte - Base de Conocimiento
% Hechos: sintoma/1, causa/2, recomendacion/2
% ============================================================

% ----------------------------------------------------------
% Declaraciones dinamicas: permiten que el backend agregue,
% modifique o elimine hechos en tiempo de ejecucion (CRUD).
% Estos hechos sirven como semilla inicial; la fuente de
% verdad tras el primer arranque es app/data/conocimiento.json.
% ----------------------------------------------------------
:- dynamic sintoma/1.
:- dynamic causa/2.
:- dynamic recomendacion/2.

% ----------------------------------------------------------
% Hechos - Sintomas disponibles (sintoma/1)
% ----------------------------------------------------------
sintoma(pantalla_negra).
sintoma(reinicio_inesperado).
sintoma(lentitud_sistema).
sintoma(no_enciende).
sintoma(ruido_ventilador).
sintoma(sobrecalentamiento).
sintoma(pantalla_azul).
sintoma(error_arranque).
sintoma(no_reconoce_disco).
sintoma(internet_lento_o_nulo).
sintoma(programas_se_cuelgan).
sintoma(no_detecta_usb).
sintoma(sin_sonido).
sintoma(imagen_distorsionada).
sintoma(memoria_insuficiente).
sintoma(virus_detectado).
sintoma(bateria_no_carga).
sintoma(teclado_no_responde).

% ----------------------------------------------------------
% Hechos - Mapeo sintoma -> falla (causa/2)
% Un sintoma puede apuntar a multiples fallas y una falla
% puede tener multiples sintomas causantes.
% ----------------------------------------------------------
causa(pantalla_negra,        falla_ram).
causa(pantalla_negra,        falla_fuente_poder).
causa(pantalla_negra,        falla_tarjeta_grafica).
causa(reinicio_inesperado,   sobrecalentamiento_cpu).
causa(reinicio_inesperado,   falla_ram).
causa(reinicio_inesperado,   falla_fuente_poder).
causa(lentitud_sistema,      falla_ram).
causa(lentitud_sistema,      infeccion_malware).
causa(lentitud_sistema,      falla_disco_duro).
causa(no_enciende,           falla_fuente_poder).
causa(no_enciende,           falla_placa_madre).
causa(ruido_ventilador,      sobrecalentamiento_cpu).
causa(sobrecalentamiento,    sobrecalentamiento_cpu).
causa(pantalla_azul,         falla_ram).
causa(pantalla_azul,         falla_sistema_operativo).
causa(error_arranque,        falla_disco_duro).
causa(error_arranque,        falla_sistema_operativo).
causa(no_reconoce_disco,     falla_disco_duro).
causa(internet_lento_o_nulo, falla_adaptador_red).
causa(programas_se_cuelgan,  falla_ram).
causa(programas_se_cuelgan,  infeccion_malware).
causa(no_detecta_usb,        falla_controlador_usb).
causa(sin_sonido,            falla_audio).
causa(imagen_distorsionada,  falla_tarjeta_grafica).
causa(memoria_insuficiente,  falla_ram).
causa(virus_detectado,       infeccion_malware).
causa(bateria_no_carga,      falla_bateria).
causa(teclado_no_responde,   falla_placa_madre).

% ----------------------------------------------------------
% Hechos - Recomendaciones por falla (recomendacion/2)
% ----------------------------------------------------------
recomendacion(falla_ram,               rec_verificar_ram).
recomendacion(falla_disco_duro,        rec_diagnostico_disco).
recomendacion(sobrecalentamiento_cpu,  rec_limpieza_termica).
recomendacion(falla_fuente_poder,      rec_revisar_fuente).
recomendacion(infeccion_malware,       rec_escaneo_antivirus).
recomendacion(falla_sistema_operativo, rec_reparar_so).
recomendacion(falla_tarjeta_grafica,   rec_drivers_grafica).
recomendacion(falla_placa_madre,       rec_servicio_tecnico).
recomendacion(falla_adaptador_red,     rec_drivers_red).
recomendacion(falla_controlador_usb,   rec_drivers_usb).
recomendacion(falla_audio,             rec_drivers_audio).
recomendacion(falla_bateria,           rec_reemplazar_bateria).
