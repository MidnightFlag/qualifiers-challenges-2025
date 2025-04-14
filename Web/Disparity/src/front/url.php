<?php

ini_set("default_socket_timeout", 5);

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    die("/url.php is only accessible with POST");
}

if (!isset($_POST['url']) || strlen($_POST['url']) === 0) {
    die("Parameter 'url' is mandatory");
}

$url = $_POST['url'];

try {
    $parsed = parse_url($url);
} catch (Exception $e){
    die("Failed to parse URL");
}

if (strlen($parsed['host']) === 0){
    die("Host can not be empty");
}

if ($parsed['scheme'] !== "http"){
    die("HTTP is the only option");
}

// Prevent DNS rebinding
try {
    $ip = gethostbyname($parsed['host']);
} catch(Exception $e) {
    die("Failed to resolve IP");
}

// Prevent from fetching localhost
if (preg_match("/^127\..*/",$ip) || $ip === "0.0.0.0"){
    die("Can't fetch localhost");
}

$url =  str_replace($parsed['host'],$ip,$url);

// Fetch url
try {
    ob_start();
    $len_content = readfile($url);
    $content = ob_get_clean();
} catch (Exception $e) {
    die("Failed to request URL");
}

if ($len_content > 0) {
    echo $content;
} else {
    die("Empty reply from server");
}

?>