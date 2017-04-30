$( document ).ready( function() {
  // ==========================================================================
  // SETUP
  // ==========================================================================
  var blocklyArea = document.getElementById('blocklyArea');
  var blocklyDiv = document.getElementById('blocklyDiv');
  var workspace = Blockly.inject(blocklyDiv, {
    toolbox: document.getElementById('toolbox'),
    grid: {
      spacing: 20,
      length: 3,
      colour: '#ccc',
      snap: true
    },
    trashcan: true
  });
  var onresize = function(e) {
    // Compute the absolute coordinates and dimensions of blocklyArea.
    /* var element = blocklyArea;
      var x = 0;
      var y = 0;
      do {
        x += element.offsetLeft;
        y += element.offsetTop;
        element = element.offsetParent;
      } while (element);
      // Position blocklyDiv over blocklyArea.
      blocklyDiv.style.top = y + 'px';
    */
    blocklyDiv.style.left = '0px';
    blocklyDiv.style.width = blocklyArea.offsetWidth + 'px';
    blocklyDiv.style.height = blocklyArea.offsetHeight + 'px';
  };
  window.addEventListener('resize', onresize, false);
  onresize();
  Blockly.svgResize(workspace);


  // ==========================================================================
  // Other
  // ==========================================================================
  function myUpdateFunction(event) {
    var code = Blockly.JavaScript.workspaceToCode(workspace);
    code = code.replace(/[()]/g,'');
    code = code.replace(/[¿]/g,'(');
    code = code.replace(/[?]/g,')');
    code = '  ' + code.replace(/[\n]/g,"\n  ");
    code = "craft {\n" + code + "\n}\n"
    // console.log(code);
    code = highlighter(code);
    $('#textArea').html(code)

  }
  workspace.addChangeListener(myUpdateFunction);
  myUpdateFunction();

  var clipboard = new Clipboard('.copy-btn');

  clipboard.on('success', function(e) {
    alert('Copied!');
  });

  function highlighter(code) {
    code = code.replace(/=/g, "<span style='color: #e24d24;'>=</span>");
    code = code.replace(/craft/g, "<span style='color: #5c84c4;'>craft</span>");
    code = code.replace(/function/g, "<span style='color: #5c84c4;'>function</span>");
    code = code.replace(/while/g, "<span style='color: #e24d24;'>while</span>");
    code = code.replace(/if/g, "<span style='color: #e24d24;'>if</span>");
    code = code.replace(/else/g, "<span style='color: #e24d24;'>else</span>");
    code = code.replace(/var/g, "<span style='color: #5c84c4;'>var</span>");
    code = code.replace(/int/g, "<span style='color: #e28f24;'>int</span>");
    code = code.replace(/bool/g, "<span style='color: #e28f24;'>bool</span>");
    code = code.replace(/float/g, "<span style='color: #e28f24;'>float</span>");
    code = code.replace(/string/g, "<span style='color: #e28f24;'>string</span>");
    code = code.replace(/void/g, "<span style='color: #e28f24;'>void</span>");
    code = code.replace(/char/g, "<span style='color: #e28f24;'>char</span>");
    return code
  }

});