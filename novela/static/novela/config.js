/* global monogatari, NOVELA */
// Configuración de Monogatari para Re:Code.
// Los datos de la página (urls de la API, etc.) vienen en window.NOVELA,
// que define el template novela/novela.html.

monogatari.settings({
	'Name': 'ReCode',
	'Version': '0.1.0',
	'Label': 'Start',
	'Slots': 3,
	'MultiLanguage': false,
	'LanguageSelectionScreen': false,
	'Language': 'Español',
	// Sin menú principal: la novela empieza directo al entrar a la materia.
	'ShowMainScreen': false,
	// No hay imágenes todavía; cuando agreguen, se puede activar.
	'Preload': false,
	'AutoSave': 0,
	// Django sirve los archivos, no hace falta el service worker de Monogatari.
	'ServiceWorkers': false,
	'AspectRatio': '16:9',
	'ForceAspectRatio': 'None',
	'TypeAnimation': true,
	'InstantText': true,
	'NVLTypeAnimation': true,
	'NarratorTypeAnimation': true,
	'CenteredTypeAnimation': true,
	'Orientation': 'any',
	'Skip': 0,
	// Las imágenes/sonidos irían en novela/static/novela/assets/<tipo>/
	'AssetsPath': {
		'root': NOVELA.assets,
		'characters': 'characters',
		'icons': 'icons',
		'images': 'images',
		'music': 'music',
		'scenes': 'scenes',
		'sounds': 'sounds',
		'ui': 'ui',
		'videos': 'videos',
		'voices': 'voices',
		'gallery': 'gallery'
	},
	'Storage': {
		'Adapter': 'LocalStorage',
		'Store': 'ReCode',
		'Endpoint': ''
	},
	'AllowRollback': true,
	'ExperimentalFeatures': false,
	'Screenshots': false
});

monogatari.preferences({
	'Language': 'Español',
	'Volume': { 'Music': 1, 'Voice': 1, 'Sound': 1, 'Video': 1 },
	'TextSpeed': 20,
	'AutoPlaySpeed': 5
});

monogatari.storage({
	player: { name: '' }
});

// Personaje compartido por todas las novelas: la entidad que guía al alumno.
monogatari.characters({
	'k': {
		name: 'K3RN3L',
		color: '#00ff00'
	}
});

// Paso final de cada historia: avisa a Django (progreso) y regresa a la materia.
window.terminarNovela = function () {
	return {
		'Function': {
			'Apply': async function () {
				await ReCode.postJSON(NOVELA.apiVista);
				window.location.href = NOVELA.alTerminar;
				return false;
			},
			'Revert': function () {}
		}
	};
};
