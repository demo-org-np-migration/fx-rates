# fx-rates

Esto trae las tasas de cambio de OpenFX cada 15 minutos y las guarda en la base `rates`. Lo armé
un viernes a la tarde porque risk necesitaba algo ya para no seguir pegando las tasas a mano en un
Excel, así que no esperen nada elegante: es un CronJob con un solo script adentro. Si el día de
mañana alguien quiere hacerlo bien, que lo separe en el `fetch` y el `save` y le agregue tests, pero
por ahora anda y con eso alcanza.

Para correrlo local: `pip install -r requirements.txt` y después `DRY_RUN=1 python3 fetch_rates.py`,
que imprime las tasas por consola sin tocar la base (útil para probar que el fetch a OpenFX
funciona sin romper nada). Sin `DRY_RUN` inserta una fila por moneda en `fx_rates` de la base
`rates`, que se crea sola si no existe.

Para deployar: `./deploy.sh staging`. No hay pipeline de CI/CD para esto, lo subo yo a mano cuando
toca. Un detalle: la key de OpenFX está en el script, pedirle a Vale si vence.
