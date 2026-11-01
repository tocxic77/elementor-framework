<?php
/**
 * Plugin Name: PP · identidad
 * Description: Favicon, apple-touch-icon y tarjeta social. Sólo añade cabeceras; no toca contenido ni consultas.
 * Version: 1.0
 */

add_action( 'wp_head', function () {
	$base = get_stylesheet_directory_uri() . '/assets';

	printf( '<link rel="icon" type="image/png" sizes="512x512" href="%s/pp-favicon-512.png">' . "\n", esc_url( $base ) );
	printf( '<link rel="apple-touch-icon" sizes="180x180" href="%s/pp-favicon-180.png">' . "\n", esc_url( $base ) );
	printf( '<meta property="og:image" content="%s/pp-og-1200x630.jpg">' . "\n", esc_url( $base ) );
	echo '<meta property="og:image:width" content="1200">' . "\n";
	echo '<meta property="og:image:height" content="630">' . "\n";
	printf( '<meta property="og:image:alt" content="%s">' . "\n", esc_attr( get_bloginfo( 'name' ) ) );
	echo '<meta name="twitter:card" content="summary_large_image">' . "\n";
}, 5 );
