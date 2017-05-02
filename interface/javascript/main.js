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
    blocklyDiv.style.left = '0px';
    blocklyDiv.style.width = blocklyArea.offsetWidth + 'px';
    blocklyDiv.style.height = blocklyArea.offsetHeight + 'px';
  };
  window.addEventListener('resize', onresize, false);
  onresize();
  Blockly.svgResize(workspace);

  // Sounds
  var playAudio = true;
  var chicken = new Audio('assets/chicken.mp3');
  var chickenhurt = new Audio('assets/chickenhurt.mp3');
  var chickenplop = new Audio('assets/chickenplop.mp3');

  // ==========================================================================
  // Python Execution
  // ==========================================================================

  $("#run-btn").click(function() {
    if (playAudio) chicken.play();
    swal({
      title: "Run program?",
      text: "Submit to execute your code",
      type: "info",
      showCancelButton: true,
      closeOnConfirm: false,
      confirmButtonText: "Run",
      confirmButtonClass: "btn-warning",
      showLoaderOnConfirm: true,
    }, function(){
      $.post('executer.php', { code: $('#textArea').text() }, function(data) {
        if (playAudio) chickenplop.play();
        swal({
          title: "Execution Complete!<br>",
          text: "<div id='output-result' class='text-left'>" + data + "</div><div class='text-center' style='font-size: small;'>There is a maximum execution time of 10 seconds</div>",
          confirmButtonClass: "btn-default",
          confirmButtonText: "Close",
          html: true
        });
      });
    });

    
  });  

  var clipboard = new Clipboard('#copy-btn');

  clipboard.on('success', function(e) {
    swal("Code copied!", "", "success")
  });

  $("#audio-btn").click(function() {
    playAudio = !playAudio;
    $("#audio-icon").toggleClass('fa-volume-up');
    $("#audio-icon").toggleClass('fa-volume-off');
  });  


  // ==========================================================================
  // Syntax Highlighting
  // ==========================================================================

  var contents = $('#textArea').html();
  var userModified = false;
  $('#textArea').keyup(function(e) {
    var key = (e.keyCode ? e.keyCode : e.which);
    text = $(this).text();
    html = $(this).html();
    if (key==13) {
      var position = getCaretCharacterOffsetWithin($(this).get(0));
      
      var lineheight = "";
      for (var i = position - 1; i >= 0; i--) {
        if (text[i] == '\n') {
          for (var j = i + 1; text[j] == ' '; j++) {
            lineheight += ' ';
          }
          break;
        }
      }

      if (text[position-1] == '{'){
        lineheight += "  ";
        html = html.replace("<div>","\n" + lineheight);
        html = html.replace("<br>","\n");
        html = html.replace("</div>","");
        $(this).html(html);
        setCaretPosition($(this).get(0), position + 1 + lineheight.length);
      } else {
        html = html.replace("<div>","\n" + lineheight);
        html = html.replace("<br>","\n");
        html = html.replace("</div>","");
        $(this).html(html);
        setCaretPosition($(this).get(0), position + 1 + lineheight.length);
      }
    } else if (contents!=$(this).html()){
      var position = getCaretCharacterOffsetWithin($(this).get(0));
      updateCode(text);
      userModified = true;
      setCaretPosition($(this).get(0), position);
    }
    contents = $(this).html();
  });

  function workspaceCodeUpdate() {
    if (userModified) {
      if (playAudio) chickenhurt.play();
      swal({
        title: "Your code will be overwritten!",
        text: "Careful, you are modifying code through blockly, this will erase any change you made to the code directly.",
        type: "warning",
        showCancelButton: true,
        confirmButtonColor: "#DD6B55",
        confirmButtonText: "Do it",
        cancelButtonText: "Cancel",
        closeOnConfirm: false,
        closeOnCancel: true
      },
      function(isConfirm){
        if (isConfirm) {
          userModified = false;
          var code = Blockly.JavaScript.workspaceToCode(workspace);
          code = code.replace(/[()]/g,'');
          code = code.replace(/&\^¿/g,'(');
          code = code.replace(/\?\^&/g,')');
          code = '  ' + code.replace(/[\n]/g,"\n  ");
          code = "craft {\n" + code + "\n}\n"
          updateCode(code)
          swal("Done!", "Your code now matches the graphical input.", "success");
        }
      });
    } else {
      userModified = false;
      var code = Blockly.JavaScript.workspaceToCode(workspace);
      code = code.replace(/[()]/g,'');
      code = code.replace(/&\^¿/g,'(');
      code = code.replace(/\?\^&/g,')');
      code = '  ' + code.replace(/[\n]/g,"\n  ");
      code = "craft {\n" + code + "\n}\n";
      updateCode(code);
    }
  }

  workspace.addChangeListener(workspaceCodeUpdate);
  workspaceCodeUpdate();

  function updateCode(code) {
    code = highlight(code);
    $('#textArea').html(code);
  }

  function highlight(code) {
    code = code.replace(/[=+-/*<>!]/g, "<span style='color: #e24d24;'>$&</span>");
    // code = code.replace(/[0-9+]/g, "<span style='color: #8f41c6;'>$&</span>");
    code = code.replace(/ true /g, "<span style='color: #8f41c6;'> true </span>");
    code = code.replace(/ false /g, "<span style='color: #8f41c6;'> false </span>");
    code = code.replace(/ and /g, "<span style='color: #e24d24;'> and </span>");
    code = code.replace(/ or /g, "<span style='color: #e24d24;'> or </span>");
    code = code.replace(/craft/g, "<span style='color: #5c84c4; font-style: italic;'>craft</span>");
    code = code.replace(/function/g, "<span style='color: #5c84c4; font-style: italic;'>function</span>");
    code = code.replace(/while/g, "<span style='color: #e24d24;'>while</span>");
    code = code.replace(/if/g, "<span style='color: #e24d24;'>if</span>");
    code = code.replace(/else/g, "<span style='color: #e24d24;'>else</span>");
    code = code.replace(/var/g, "<span style='color: #5c84c4; font-style: italic;'>var</span>");
    code = code.replace(/int/g, "<span style='color: #e28f24;'>int</span>");
    code = code.replace(/bool/g, "<span style='color: #e28f24;'>bool</span>");
    code = code.replace(/float/g, "<span style='color: #e28f24;'>float</span>");
    code = code.replace(/string/g, "<span style='color: #e28f24;'>string</span>");
    code = code.replace(/void/g, "<span style='color: #e28f24;'>void</span>");
    code = code.replace(/char/g, "<span style='color: #e28f24;'>char</span>");
    code = code.replace(/\"((?:\\.|[^"\\])*)\"/g, "<span style='color: #f4e842 !important;'>$&</span>");
    return code
  }

  function getCaretCharacterOffsetWithin(element) {
    var caretOffset = 0;
    var doc = element.ownerDocument || element.document;
    var win = doc.defaultView || doc.parentWindow;
    var sel;
    if (typeof win.getSelection != "undefined") {
      sel = win.getSelection();
      if (sel.rangeCount > 0) {
        var range = win.getSelection().getRangeAt(0);
        var preCaretRange = range.cloneRange();
        preCaretRange.selectNodeContents(element);
        preCaretRange.setEnd(range.endContainer, range.endOffset);
        caretOffset = preCaretRange.toString().length;
      }
    } else if ((sel = doc.selection) && sel.type != "Control") {
      var textRange = sel.createRange();
      var preCaretTextRange = doc.body.createTextRange();
      preCaretTextRange.moveToElementText(element);
      preCaretTextRange.setEndPoint("EndToEnd", textRange);
      caretOffset = preCaretTextRange.text.length;
    }
    return caretOffset;
  }

  function setCaretPosition(element, offset) {
    var range = document.createRange();
    var sel = window.getSelection();

    //select appropriate node
    var currentNode = null;
    var previousNode = null;
    for (var i = 0; i < element.childNodes.length; i++) {
      //save previous node
      previousNode = currentNode;
      //get current node
      currentNode = element.childNodes[i];
      //if we get span or something else then we should get child node
     while(currentNode.childNodes.length > 0){
        currentNode = currentNode.childNodes[0];
     }

      //calc offset in current node
      if (previousNode != null) {
          offset -= previousNode.length;
      }
      //check whether current node has enough length
      if (offset <= currentNode.length) {
          break;
      }
    }
    //move caret to specified offset
    if (currentNode != null) {
      range.setStart(currentNode, offset);
      range.collapse(true);
      sel.removeAllRanges();
      sel.addRange(range);
    }
  }


});