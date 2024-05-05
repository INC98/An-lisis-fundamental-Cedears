# Análisis-fundamental-Cedears

Los analistas fundamentales analizan 5 partes de la empresa: capacidad de pagar deudas al corto plazo, capacidad de pagar deudas al largo plazo, la capacidad de generar dinero que tiene la empresa, la capacidad de generar ganancias y la valuación actual de la acción.
En base a los ratios se puede saber si la empresa es potable para invertir o no.

Para esto se creo un script con el objetivo de automatizar la obtención de los ratios de los cedears.

El output es un excel que presenta distintas columnas:
- Ticker: Nombre por el cual se encontrara la accion y el cedear.
- Liquidez: Es cuan capaz es la empresa de pagar sus deudas en el corto plazo, indica si la empresa va a quebrar en el corto plazo o no. Si el número da 0.5 para abajo se descarta, 1 resultado ok,  1.5 resultado bueno y de 2 para arriba excelente. Mientras mas lejos del 1 esta, mas liquida es.
- Solvencia: Es lo mismo que la liquidez pero en el largo plazo. Se ve si la empresa es viable a largo plazo y que no va a quebrar. Si el numero es menor de 0.5 se descarta, 1 resultado ok,  1.5 resultado bueno y 2 para arriba excelente. Mas lejos del 1 esta, mas solvente es. 
- Eficiencia: Capacidad de generar ingresos de la empresa. El número dice cuan buena es la empresa para rotar el dinero que tiene. Si da como resultado 1 estaria ok, 2 es un resultado decente, 4 o 5 para arriba excelente rotación de activos. Igualmente depende de la empresa ya que en las de servicios no hay tanta rotación de activos.
- Rentabilidad: Capacidad de generar ganancias de la empresa. El resultado depende mucho de la empresa. Para empresa tecnológicas >20% es el mínimo que se espera, >25% bueno, 30% para arriba excelente.
- Rentabilidad promedio 5a: Se ve la rentablididad promedio durante 5 años para ver si la empresa se mantuvo rentable a lo largo de los años.
Para empresas de bienes de consumo ver que esten entre 5% a 10%.
Para empresas mineras, bancos, etc. lo mas fácil es ver si se mantuvo en un promedio a lo largo de los años.
- P/E empresa: Se tienen en cuenta las ganancias. Dice cuantos años tardara la empresa en generar la cantidad de dólares que se invirtieron. Guarda con el P/E mayor a 50, para esto tienen que estar los ratios muy bien. Para empresa tecnológica que este arriba de 30 bien pero si no es tecnológica cuidado. Si es 10 o 15 estaria normal. Resultados de 5 o 2, cuidado con si la empresa es liquida y solvente porque sino puede estar por quebrar.
- P/E industria: Es el P/E promedio de la competencia. Comparar el P/E de la empresa para ver si es mayor, menor o igual al promedio de la industria. El objetivo es buscar que este correctamente valuada o subvaluada para poder invertir.
- P/S empresa: Se tienen en cuenta las ventas.
- P/S industria: Es el P/S promedio de la competencia. Comparar el P/S de la empresa para ver si es mayor, menor o igual al promedio de la industria. El objetivo es buscar que este correctamente valuada o subvaluada para poder invertir.
- P/B empresa: Se tiene en cuenta el patrimonio. 
- P/B industria: Es el P/B promedio de la competencia. Comparar el P/B de la empresa para ver si es mayor, menor o igual al promedio de la industria. El objetivo es buscar que este correctamente valuada o subvaluada para poder invertir.

El código esta hecho en Python y se utilizaron las librerias requests, BeautifulSoup, pandas, tqdm.

Para obtener el nombre de las acciones o mas conocido como Tickers, se utilizaron los publicados en https://www.invertironline.com/

Para obtener los resultados de Liquidez, Solvencia, Eficiencia y Rentabilidad se utilizo https://investing.com/

Para obtener las valuaciones de la empresa e industria, se utilizo https://wallmine.com/


