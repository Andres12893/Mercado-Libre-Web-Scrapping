# Mercado-Libre-Web-Scraping

El objetivo de este proyecto es aprender Web Scraping a traves de la pagina de Mercado Libre, voy a scrapear algunas secciones de items de mi interes para luego calcular un promedio de precio y condiciones (en caso de que estas existan, como por ejemplo cupones o cuotas), para identificar cuando algo esta en "barato" utilizando un promedio de precio de los ultimos 30 dias (en dolares), para la segunda parte vamos a usar una API de tipo de cambio para siempre cauntificarlo en dolares (problemas del tercer mundo)

Futuros Updates:
1) Darle dinamismo a las url en lugar de estar copiando la url a mano
2) ~~Solucionar problemas de contendores de elementos de atributos de autos~~
3) ~~Agregar estos archivos a bases de datos~~
4) Realizar analisis de datos + envio de notificaciones
5) Agregar componentes nube
6) Dashboard en tableau

---
Update 1:
Se agregaron las columnas year y kilometraje que poseen informacion para el caso de los autos, de que año es el modelo y cuantos kilometros tiene recorridos, estos seran transformados a otros tipos de datos en futuras actualizaciones (probablemente cuando se guarden en bases de datos), como los legos no tienen este tema, no se agrego en el bloque if.

Update 2:
Refactorizacion de codigo en funciones mas chicas, se agrego tambien el upload a un bucket de AWS S3, donde sera tomado por Athena en un futuro
