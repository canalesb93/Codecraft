<?php 

if (isset($_POST["code"])) {
  $program = $_POST['code'];
  file_put_contents('input.craft', $program);
  $rel1 = dirname(__FILE__) . '/../compiler/parser.py ';
  $rel2 = dirname(__FILE__) . '/input.craft';
  $command = 'timeout 5s python ' . $rel1 . $rel2;
  $shellcmd = escapeshellcmd($command);
  exec($shellcmd, $out, $ret);

  if ($ret == 124) {
    echo implode("\n", $out);
    echo "\n Your program compilation timed out!";
  } else if ($ret == 1) {
    echo implode("\n", $out);
  } else {
    $rel1 = dirname(__FILE__) . '/../compiler/virtual_machine.py ';
    $rel2 = dirname(__FILE__) . '/input.crafted';
    $command = 'timeout 10s python ' . $rel1 . $rel2 . " 2>&1";
    $shellcmd = escapeshellcmd($command);
    exec($shellcmd, $output, $ret_var);
    echo implode("\n", $output);
    if ($ret_var == 124) {
      echo "\n Your program timed out!";
    }
  }



} else {
  echo "ERROR: CODE NOT FOUND! D:";
}

?>