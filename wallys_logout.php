<?php
session_start();
session_destroy();
header("Location: wallys_login.php");
exit();
?>