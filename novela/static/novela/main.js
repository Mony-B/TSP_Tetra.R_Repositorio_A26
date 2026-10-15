/* global Monogatari, monogatari, NOVELA */
'use strict';

const { $_ready } = Monogatari;

$_ready(async () => {
	// Antes de arrancar, pedimos a Django el nombre del alumno (JSON) para
	// que la historia pueda usar {{player.name}}.
	try {
		const alumno = await ReCode.getJSON(NOVELA.apiAvance);
		monogatari.storage({ player: { name: alumno.nombre || 'alumno' } });
	} catch (e) {
		monogatari.storage({ player: { name: 'alumno' } });
	}

	await monogatari.init('#monogatari');
});
