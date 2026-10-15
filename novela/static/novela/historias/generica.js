/* global monogatari, terminarNovela, NOVELA */
// Historia de relleno para las materias que todavía no tienen la suya.
// Para escribir la de una materia, crear historias/<slug>.js (ej. linux.js).

monogatari.script({
	'Start': [
		'show scene #050505 with fadeIn',
		'k {{player.name}}... esta parte de la red todavía está en silencio.',
		'k Aún no recupero mis recuerdos sobre ' + NOVELA.materia + '.',
		'k Ve a los retos. Tal vez ahí encuentres algo.',
		terminarNovela()
	]
});
