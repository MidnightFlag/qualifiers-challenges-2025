<?php

if ($_SERVER['HTTP_HOST'] === "localhost:8080"){
    echo getenv('FLAG');
} else {
    echo "You are not allowed to do that";
}
?>