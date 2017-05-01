<?php 

$rel1 = dirname(__FILE__) . '/../compiler/parser.py ';
$rel2 = dirname(__FILE__) . '/../compiler/samples/factorial.craft';
$command = 'python ' . $rel1 . $rel2;

$shellcmd = escapeshellcmd($command);
$output = shell_exec($shellcmd);
// echo $output;

$rel1 = dirname(__FILE__) . '/../compiler/virtual_machine.py ';
$rel2 = dirname(__FILE__) . '/../compiler/samples/factorial.crafted';
$command = 'python ' . $rel1 . $rel2;
$shellcmd = escapeshellcmd($command);
$output = shell_exec($shellcmd);
echo $output;

?>