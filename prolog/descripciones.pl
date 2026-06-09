% ============================================================
% Doctor Byte - Descripciones legibles
% Hechos: descripcion_sintoma/2, descripcion_falla/2,
%         descripcion_recomendacion/2
% ============================================================

% ----------------------------------------------------------
% Descripciones legibles de sintomas (descripcion_sintoma/2)
% ----------------------------------------------------------
descripcion_sintoma(pantalla_negra,        "Pantalla en negro al encender el equipo").
descripcion_sintoma(reinicio_inesperado,   "El equipo se reinicia solo sin previo aviso").
descripcion_sintoma(lentitud_sistema,      "El sistema operativo responde muy lento").
descripcion_sintoma(no_enciende,           "El equipo no enciende al presionar el boton de encendido").
descripcion_sintoma(ruido_ventilador,      "Ruido excesivo o inusual proveniente del ventilador").
descripcion_sintoma(sobrecalentamiento,    "El equipo se calienta en exceso durante el uso").
descripcion_sintoma(pantalla_azul,         "Aparece pantalla azul de la muerte (BSOD)").
descripcion_sintoma(error_arranque,        "Error al arrancar o cargar el sistema operativo").
descripcion_sintoma(no_reconoce_disco,     "El sistema no detecta el disco duro").
descripcion_sintoma(internet_lento_o_nulo, "Conexion a internet lenta o sin conectividad").
descripcion_sintoma(programas_se_cuelgan,  "Los programas se congelan o cierran inesperadamente").
descripcion_sintoma(no_detecta_usb,        "El equipo no detecta dispositivos USB conectados").
descripcion_sintoma(sin_sonido,            "El audio no funciona en el equipo").
descripcion_sintoma(imagen_distorsionada,  "La imagen en pantalla presenta artefactos o distorsion").
descripcion_sintoma(memoria_insuficiente,  "Mensajes frecuentes de memoria RAM insuficiente").
descripcion_sintoma(virus_detectado,       "El antivirus reporta amenazas o comportamiento sospechoso").
descripcion_sintoma(bateria_no_carga,      "La bateria del equipo no carga (aplica a laptops)").
descripcion_sintoma(teclado_no_responde,   "El teclado no responde o registra pulsaciones incorrectas").

% ----------------------------------------------------------
% Descripciones legibles de fallas (descripcion_falla/2)
% ----------------------------------------------------------
descripcion_falla(falla_ram,               "Falla en modulo(s) de memoria RAM").
descripcion_falla(falla_disco_duro,        "Falla o dano en el disco duro / SSD").
descripcion_falla(sobrecalentamiento_cpu,  "Sobrecalentamiento del procesador (CPU)").
descripcion_falla(falla_fuente_poder,      "Falla en la fuente de poder / adaptador").
descripcion_falla(infeccion_malware,       "Infeccion por malware, virus o ransomware").
descripcion_falla(falla_sistema_operativo, "Corrupcion o falla en el sistema operativo").
descripcion_falla(falla_tarjeta_grafica,   "Falla en la tarjeta grafica (GPU)").
descripcion_falla(falla_placa_madre,       "Falla en la placa madre (motherboard)").
descripcion_falla(falla_adaptador_red,     "Falla en el adaptador de red (WiFi/Ethernet)").
descripcion_falla(falla_controlador_usb,   "Falla en controladores o puertos USB").
descripcion_falla(falla_audio,             "Falla en tarjeta de audio o drivers de sonido").
descripcion_falla(falla_bateria,           "Bateria danada o al final de su vida util").
descripcion_falla(sin_diagnostico,         "No se pudo determinar una falla a partir de los sintomas").

% ----------------------------------------------------------
% Descripciones legibles de recomendaciones (descripcion_recomendacion/2)
% ----------------------------------------------------------
descripcion_recomendacion(rec_verificar_ram,      "Verificar, re-insertar o reemplazar los modulos de RAM").
descripcion_recomendacion(rec_diagnostico_disco,  "Ejecutar diagnostico SMART del disco y considerar reemplazo").
descripcion_recomendacion(rec_limpieza_termica,   "Limpiar ventiladores y aplicar pasta termica nueva al CPU").
descripcion_recomendacion(rec_revisar_fuente,     "Revisar la fuente de poder con multimetro o reemplazarla").
descripcion_recomendacion(rec_escaneo_antivirus,  "Ejecutar escaneo completo con antivirus actualizado").
descripcion_recomendacion(rec_reparar_so,         "Ejecutar reparacion o reinstalacion del sistema operativo").
descripcion_recomendacion(rec_drivers_grafica,    "Desinstalar y reinstalar drivers de tarjeta grafica").
descripcion_recomendacion(rec_servicio_tecnico,   "Llevar el equipo a servicio tecnico especializado").
descripcion_recomendacion(rec_drivers_red,        "Actualizar o reinstalar drivers del adaptador de red").
descripcion_recomendacion(rec_drivers_usb,        "Reinstalar controladores USB desde el administrador de dispositivos").
descripcion_recomendacion(rec_drivers_audio,      "Actualizar o reinstalar drivers de audio").
descripcion_recomendacion(rec_reemplazar_bateria, "Reemplazar la bateria por una compatible con el modelo del equipo").
