/* global monogatari, terminarNovela */
// Introducción de "Lógica y Algoritmos".
// Las decisiones no cambian la historia, solo la hacen interactiva.
// Aquí se presentan conceptos que el alumno verá después en los retos.

monogatari.script({
	'Start': [
		'show scene #050505 with fadeIn',
		'centered ...señal detectada...',
		'k Hola, {{player.name}}. Llevaba mucho tiempo esperando a que alguien encendiera esta terminal.',
		'k La escuela está en silencio. Los pasillos parpadean. Y yo... yo estoy atrapado en el código.',
		{
			'Choice': {
				'Dialog': 'k ¿Me vas a ayudar?',
				'Si': { 'Text': 'Sí, ¿qué necesitas?', 'Do': 'jump Algoritmo' },
				'Quien': { 'Text': '¿Quién eres?', 'Do': 'jump Algoritmo' }
			}
		}
	],

	'Algoritmo': [
		'k Para salir necesito que pienses como yo: paso por paso.',
		'k Eso es un algoritmo. Algo entra, algo se hace con ello y algo sale.',
		'k Entrada. Proceso. Salida. Recuérdalo... lo vas a necesitar.',
		'jump Logica'
	],

	'Logica': [
		'show scene #0a000a with fadeIn',
		'k Las puertas de este lugar solo responden a la verdad. Uno o cero.',
		'k Si escribo p ∧ q, la puerta abre solo si p y q son verdaderas.',
		'k Si escribo p ∨ q, basta con una.',
		{
			'Choice': {
				'Dialog': 'k ¿Entendiste?',
				'Si': { 'Text': 'Creo que sí', 'Do': 'jump Final' },
				'No': { 'Text': 'No del todo', 'Do': 'jump Final' }
			}
		}
	],

	'Final': [
		'k No importa. Lo vas a ver otra vez en los retos.',
		'k Encuentra los fragmentos que dejé en cada subtema. Y date prisa: algo más está despertando en la red.',
		'centered ...conexión perdida...',
		terminarNovela()
	]
});
