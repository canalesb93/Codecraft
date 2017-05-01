<?php 

if (isset($_POST["code"])) {
  $program = $_POST['code'];
  file_put_contents('input.craft', $program);
  $rel1 = dirname(__FILE__) . '/../compiler/parser.py ';
  $rel2 = dirname(__FILE__) . '/input.craft';
  $command = 'python ' . $rel1 . $rel2;
  $shellcmd = escapeshellcmd($command);
  shell_exec($shellcmd);

  $rel1 = dirname(__FILE__) . '/../compiler/virtual_machine.py ';
  $rel2 = dirname(__FILE__) . '/input.crafted';
  $command = 'python ' . $rel1 . $rel2;
  $shellcmd = escapeshellcmd($command);
  $output = shell_exec($shellcmd);
  echo $output;
} else {
  echo "ERROR: CODE NOT FOUND! D:";
}

?>