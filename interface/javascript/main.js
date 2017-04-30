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
    console.log(code);
    $('#textarea').html(code)
  }
  workspace.addChangeListener(myUpdateFunction);


});