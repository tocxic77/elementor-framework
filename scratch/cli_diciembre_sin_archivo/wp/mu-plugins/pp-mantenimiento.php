<?php
/**
 * Plugin Name:  PP — Página de mantenimiento
 * Description:  Sirve una página de mantenimiento con HTTP 503 y ventana programada.
 * Version:      1.0.0
 * Author:       Hermes (para Mario Pennacchiotti)
 *
 * QUÉ HACE
 *   Con el modo activo, toda visita pública recibe la página de mantenimiento
 *   con estado 503 y cabecera Retry-After. El panel (/wp-admin), el login,
 *   wp-cron y la REST API siguen respondiendo: el sitio no se rompe por dentro
 *   y el administrador conectado ve el sitio normal.
 *
 * CÓMO SE PROGRAMA
 *   Se edita pp_mant_config() y se sube este archivo por FTP. El modo se activa
 *   si 'activo' es true, o si la hora de Chile cae dentro de [desde, hasta).
 *   'desde' sin 'hasta' = empieza y no termina solo (hay que desactivarlo).
 *
 * CÓMO SE COMPRUEBA SIN AFECTAR AL PÚBLICO
 *   ?pp_mant_preview=CLAVE  → la página, con HTTP 200 (vista previa)
 *   ?pp_mant_test=CLAVE     → la página, con HTTP 503 (prueba real)
 *   Funcionan aunque el modo esté inactivo.
 *
 * REVERSIBLE: borrar este archivo por FTP. No toca la base de datos.
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

/**
 * Configuración. Única parte que se edita.
 *
 * @return array
 */
function pp_mant_config() {
	return array(
		// Interruptor manual: true bloquea el sitio en este instante.
		'activo'   => false,
		// Ventana programada, hora de Chile, formato 'Y-m-d H:i'. Vacío = sin límite.
		'desde'    => '',
		'hasta'    => '',
		// Clave de vista previa y de prueba (no abre nada: solo muestra la página).
		'clave'    => 'pp-mant-2026',
		'titulo'   => 'Estamos en mantenimiento',
		'texto'    => 'Estamos actualizando el sitio. La dirección y el contenido siguen igual; no hay nada que hacer de tu parte.',
		// Línea de retorno, escrita por Mario. Vacía = no se muestra.
		'retorno'  => '',
		'contacto' => 'mariop@agroterramica.com',
		'logo'     => 'https://pennacchiotti.cl/wp-content/uploads/leroux-demo/pp-wordmark-claro.png',
		'logo_w'   => 977,
		'logo_h'   => 71,
	);
}

/**
 * Interpreta una fecha de configuración en la zona del sitio.
 *
 * @param string         $valor Valor 'Y-m-d H:i' o 'Y-m-d'.
 * @param DateTimeZone   $tz    Zona horaria.
 * @return DateTimeImmutable|null
 */
function pp_mant_fecha( $valor, $tz ) {
	$valor = trim( (string) $valor );
	if ( '' === $valor ) {
		return null;
	}
	foreach ( array( 'Y-m-d H:i', 'Y-m-d' ) as $formato ) {
		$fecha = DateTimeImmutable::createFromFormat( '!' . $formato, $valor, $tz );
		$errores = DateTimeImmutable::getLastErrors();
		if ( $fecha instanceof DateTimeImmutable && ( ! $errores || ( 0 === $errores['warning_count'] && 0 === $errores['error_count'] ) ) ) {
			return $fecha;
		}
	}
	return null;
}

/**
 * ¿Corresponde mostrar la página de mantenimiento ahora?
 *
 * @param array $c Configuración.
 * @return bool
 */
function pp_mant_esta_activo( $c ) {
	if ( ! empty( $c['activo'] ) ) {
		return true;
	}
	$tz    = function_exists( 'wp_timezone' ) ? wp_timezone() : new DateTimeZone( 'America/Santiago' );
	$desde = pp_mant_fecha( $c['desde'], $tz );
	$hasta = pp_mant_fecha( $c['hasta'], $tz );
	if ( ! $desde && ! $hasta ) {
		return false;
	}
	$ahora = new DateTimeImmutable( 'now', $tz );
	if ( $desde && $ahora < $desde ) {
		return false;
	}
	if ( $hasta && $ahora >= $hasta ) {
		return false;
	}
	return true;
}

/**
 * Segundos de Retry-After: hasta el fin de la ventana, o una hora.
 *
 * @param array $c Configuración.
 * @return int
 */
function pp_mant_retry( $c ) {
	$tz    = function_exists( 'wp_timezone' ) ? wp_timezone() : new DateTimeZone( 'America/Santiago' );
	$hasta = pp_mant_fecha( $c['hasta'], $tz );
	if ( ! $hasta ) {
		return 3600;
	}
	$segundos = $hasta->getTimestamp() - time();
	if ( $segundos < 60 ) {
		return 60;
	}
	return $segundos > 86400 ? 86400 : $segundos;
}

/**
 * Envía cabeceras, imprime la página y termina la petición.
 *
 * @param array $c      Configuración.
 * @param int   $status Código HTTP: 503 en producción, 200 en vista previa.
 * @return void
 */
function pp_mant_render( $c, $status ) {
	if ( ! headers_sent() ) {
		status_header( $status );
		nocache_headers();
		header( 'Content-Type: text/html; charset=utf-8' );
		header( 'Cache-Control: no-store, no-cache, must-revalidate, max-age=0' );
		header( 'X-Robots-Tag: noindex, nofollow', true );
		if ( 503 === $status ) {
			header( 'Retry-After: ' . pp_mant_retry( $c ) );
		}
	}
	echo pp_mant_html( $c ); // phpcs:ignore WordPress.Security.EscapeOutput -- el HTML se arma escapado.
	exit;
}

/**
 * HTML de la página. Todo valor de configuración se escapa aquí.
 *
 * @param array $c Configuración.
 * @return string
 */
function pp_mant_html( $c ) {
	$titulo   = esc_html( $c['titulo'] );
	$texto    = esc_html( $c['texto'] );
	$logo     = esc_url( $c['logo'] );
	$logo_w   = (int) $c['logo_w'];
	$logo_h   = (int) $c['logo_h'];
	$correo   = antispambot( (string) $c['contacto'] );
	$retorno  = trim( (string) $c['retorno'] );
	$bloque_r = '' === $retorno ? '' : '<p class="pp-mant__retorno">' . esc_html( $retorno ) . '</p>';

	$css = <<<'CSS'
*,*::before,*::after{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{
	margin:0;min-height:100vh;display:flex;flex-direction:column;
	background:#223035;color:#EFEFEF;
	font-family:"DM Sans",system-ui,-apple-system,"Segoe UI",sans-serif;
	font-size:15px;line-height:1.65;-webkit-font-smoothing:antialiased;
}
::selection{background:#D5DEDE;color:#20282D}
a{color:#FBFAF9;text-decoration:underline;text-underline-offset:3px;text-decoration-thickness:1px}
a:hover{text-decoration-thickness:2px}
a:focus-visible{outline:2px solid #D5DEDE;outline-offset:4px;border-radius:2px}
.pp-mant{flex:1 1 auto;display:flex;align-items:center;padding:112px 28px 64px}
.pp-mant__inner{width:100%;max-width:760px;margin:0 auto}
.pp-mant__logo{display:block;width:220px;max-width:72%;height:auto;margin:0 0 40px}
.pp-mant__titulo{
	margin:0 0 24px;max-width:22ch;color:#FBFAF9;
	font-family:"Newsreader",Georgia,"Times New Roman",serif;
	font-weight:300;font-size:56px;line-height:1.1;letter-spacing:-.01em;
}
.pp-mant__texto{margin:0;max-width:60ch;font-size:18px;line-height:1.6;color:#D9DEDE}
.pp-mant__retorno{
	margin:0;padding-top:20px;max-width:60ch;font-size:16px;line-height:1.6;color:#EFEFEF;
	border-top:1px solid rgba(251,250,249,.14);
}
.pp-mant__texto+.pp-mant__retorno{margin-top:40px}
.pp-mant__contacto{margin:48px 0 0;font-size:16px}
.pp-mant__contacto a{display:inline-block;padding:10px 0}
.pp-mant__pie{
	padding:24px 28px;border-top:1px solid rgba(251,250,249,.14);
	font-size:13px;line-height:1.5;color:#D9DEDE;
}
.pp-mant__pie span{display:block;width:100%;max-width:760px;margin:0 auto}
@media (max-width:1023px){
	.pp-mant{padding:80px 32px 48px}
	.pp-mant__titulo{font-size:48px}
}
@media (max-width:767px){
	.pp-mant{padding:64px 28px 40px}
	.pp-mant__logo{width:180px;margin-bottom:32px}
	.pp-mant__titulo{font-size:40px}
	.pp-mant__texto{font-size:17px}
	.pp-mant__contacto{margin-top:40px}
}
@media (max-width:389px){
	.pp-mant{padding:48px 20px 32px}
	.pp-mant__logo{width:160px}
	.pp-mant__titulo{font-size:32px}
}
CSS;

	return <<<HTML
<!doctype html>
<html lang="es-CL">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>Mantenimiento — PENNACCHIOTTI</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500&family=Newsreader:wght@300;400&display=swap" rel="stylesheet">
<style>
{$css}
</style>
</head>
<body>
<main class="pp-mant" id="contenido">
	<div class="pp-mant__inner">
		<img class="pp-mant__logo" src="{$logo}" width="{$logo_w}" height="{$logo_h}" alt="PENNACCHIOTTI">
		<h1 class="pp-mant__titulo">{$titulo}</h1>
		<p class="pp-mant__texto">{$texto}</p>
		{$bloque_r}
		<p class="pp-mant__contacto">Escríbenos a <a href="mailto:{$correo}">{$correo}</a>.</p>
	</div>
</main>
<footer class="pp-mant__pie"><span>PENNACCHIOTTI · Control, estandarización y desarrollo de capacidades operacionales</span></footer>
</body>
</html>
HTML;
}

/**
 * Intercepta la petición pública mientras el modo está activo.
 */
add_action(
	'template_redirect',
	function () {
		$c = pp_mant_config();

		$pedida = static function ( $nombre ) {
			return isset( $_GET[ $nombre ] ) ? sanitize_text_field( wp_unslash( $_GET[ $nombre ] ) ) : '';
		};

		$previa = '' !== $pedida( 'pp_mant_preview' ) && hash_equals( (string) $c['clave'], $pedida( 'pp_mant_preview' ) );
		$prueba = '' !== $pedida( 'pp_mant_test' ) && hash_equals( (string) $c['clave'], $pedida( 'pp_mant_test' ) );

		if ( ! $previa && ! $prueba ) {
			if ( is_admin() || wp_doing_ajax() || wp_doing_cron() ) {
				return;
			}
			if ( defined( 'REST_REQUEST' ) && REST_REQUEST ) {
				return;
			}
			$ruta = isset( $_SERVER['REQUEST_URI'] ) ? (string) wp_unslash( $_SERVER['REQUEST_URI'] ) : '';
			if ( false !== strpos( $ruta, 'wp-login.php' ) || false !== strpos( $ruta, '/wp-admin' ) ) {
				return;
			}
			if ( false !== strpos( $ruta, 'robots.txt' ) ) {
				return;
			}
			if ( current_user_can( 'manage_options' ) ) {
				return;
			}
			if ( ! pp_mant_esta_activo( $c ) ) {
				return;
			}
			pp_mant_render( $c, 503 );
		}

		pp_mant_render( $c, $prueba ? 503 : 200 );
	},
	0
);
