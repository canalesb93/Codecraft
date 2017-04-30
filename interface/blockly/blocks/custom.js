goog.require('Blockly.Blocks');

// \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
// =============================================================================
// BLOCKS
// =============================================================================
// /////////////////////////////////////////////////////////////////////////////

Blockly.Blocks['while'] = {
  init: function() {
    this.appendValueInput("CONDITION")
        .setCheck(null)
        .appendField("while");
    this.appendStatementInput("STATEMENTS")
        .setCheck(null);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(230);
    this.setTooltip('');
    this.setHelpUrl('');
  }
};

Blockly.Blocks['var_declaration'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("var")
        .appendField(new Blockly.FieldDropdown([["int","int"], ["bool","bool"], ["float","float"], ["char","char"], ["string","string"]]), "TYPE")
        .appendField(new Blockly.FieldTextInput("default"), "ID")
        .appendField("=");
    this.appendValueInput("VALUE")
        .setCheck(null);
    this.setInputsInline(true);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(230);
    this.setTooltip('');
    this.setHelpUrl('');
  }
};

Blockly.Blocks['var_arr_declaration'] = {
  init: function() {
    this.appendValueInput("INDEX")
        .setCheck(null)
        .appendField("var")
        .appendField(new Blockly.FieldDropdown([["int","int"], ["bool","bool"], ["float","float"], ["char","char"], ["string","string"]]), "TYPE")
        .appendField(new Blockly.FieldTextInput("default"), "ID");
    this.setInputsInline(true);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(230);
    this.setTooltip('');
    this.setHelpUrl('');
  }
};

Blockly.Blocks['var_free_assign'] = {
  init: function() {
    this.appendValueInput("VALUE")
        .setCheck(null)
        .appendField(new Blockly.FieldTextInput("default"), "ID")
        .appendField("=");
    this.setInputsInline(true);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(230);
    this.setTooltip('');
    this.setHelpUrl('');
  }
};

Blockly.Blocks['var_arr_free_assign'] = {
  init: function() {
    this.appendValueInput("INDEX")
        .setCheck(null)
        .appendField(new Blockly.FieldTextInput("default"), "ID")
            .appendField("[");
    this.appendValueInput("VALUE")
        .setCheck(null)
        .appendField("] =");
    this.setInputsInline(true);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(230);
    this.setTooltip('');
    this.setHelpUrl('');
  }
};

Blockly.Blocks['index_selector_array'] = {
  init: function() {
    this.appendValueInput("INDEX_1")
        .setCheck(null)
        .appendField("[");
    this.appendDummyInput()
        .appendField("]");
    this.setInputsInline(true);
    this.setOutput(true, null);
    this.setColour(230);
    this.setTooltip('');
    this.setHelpUrl('');
  }
};

Blockly.Blocks['index_selector_matrix'] = {
  init: function() {
    this.appendValueInput("INDEX_1")
        .setCheck(null)
        .appendField("[");
    this.appendValueInput("INDEX_2")
        .setCheck(null)
        .appendField("] [");
    this.appendDummyInput()
        .appendField("]");
    this.setInputsInline(true);
    this.setOutput(true, null);
    this.setColour(230);
    this.setTooltip('');
    this.setHelpUrl('');
  }
};

Blockly.Blocks['function'] = {
  init: function() {
    this.appendValueInput("PARAMS")
        .setCheck(null)
        .appendField("function")
        .appendField(new Blockly.FieldDropdown([["void","void"], ["int","int"], ["float","float"], ["string","string"], ["char","char"]]), "TYPE")
        .appendField(new Blockly.FieldTextInput("default"), "ID");
    this.appendStatementInput("function")
        .setCheck(null);
    this.setColour(330);
    this.setTooltip('');
    this.setHelpUrl('');
  }
};

Blockly.Blocks['param_comma'] = {
  init: function() {
    this.appendValueInput("LEFT_PARAM")
        .setCheck(null);
    this.appendValueInput("NAME")
        .setCheck(null)
        .appendField(",");
    this.setInputsInline(true);
    this.setOutput(true, null);
    this.setColour(230);
    this.setTooltip('');
    this.setHelpUrl('');
  }
};

Blockly.Blocks['return'] = {
  init: function() {
    this.appendValueInput("return")
        .setCheck(null)
        .appendField("return");
    this.setPreviousStatement(true, null);
    this.setColour(66);
    this.setTooltip('');
    this.setHelpUrl('');
  }
};

Blockly.Blocks['break'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("break");
    this.setPreviousStatement(true, null);
    this.setColour(230);
    this.setTooltip('');
    this.setHelpUrl('');
  }
};

Blockly.Blocks['continue'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("continue");
    this.setPreviousStatement(true, null);
    this.setColour(230);
    this.setTooltip('');
    this.setHelpUrl('');
  }
};

Blockly.Blocks['output'] = {
  init: function() {
    this.appendValueInput("OUTPUT")
        .setCheck(null)
        .appendField("output");
    this.setInputsInline(true);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(120);
    this.setTooltip('');
    this.setHelpUrl('');
  }
};

Blockly.Blocks['text'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("\"")
        .appendField(new Blockly.FieldTextInput(""), "string")
        .appendField("\"");
    this.setOutput(true, null);
    this.setColour(230);
    this.setTooltip('');
    this.setHelpUrl('');
  }
};

Blockly.Blocks['comment'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("#")
        .appendField(new Blockly.FieldTextInput("coment"), "COMMENT");
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(230);
    this.setTooltip('');
    this.setHelpUrl('');
  }
};

Blockly.Blocks['function_call'] = {
  init: function() {
    this.appendValueInput("PARAMS")
        .setCheck(null)
        .appendField(new Blockly.FieldTextInput("sample"), "ID")
        .appendField("(");
    this.appendDummyInput()
        .appendField(")");
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(330);
    this.setTooltip('');
    this.setHelpUrl('');
  }
};

Blockly.Blocks['function_call_value'] = {
  init: function() {
    this.appendValueInput("PARAMS")
        .setCheck(null)
        .appendField(new Blockly.FieldTextInput("sample"), "ID")
        .appendField("(");
    this.appendDummyInput()
        .appendField(")");
    this.setOutput(true, null);
    this.setColour(330);
    this.setTooltip('');
    this.setHelpUrl('');
  }
};

Blockly.Blocks['param'] = {
  init: function() {
    this.appendValueInput("NEXT")
        .setCheck(null)
        .appendField(new Blockly.FieldDropdown([["int","int"], ["float","float"], ["bool","bool"], ["string","string"], ["char","char"]]), "TYPE")
        .appendField(new Blockly.FieldTextInput("name"), "ID");
    this.setInputsInline(false);
    this.setOutput(true, null);
    this.setColour(230);
    this.setTooltip('');
    this.setHelpUrl('');
  }
};

Blockly.Blocks['outputln'] = {
  init: function() {
    this.appendValueInput("VALUE")
        .setCheck(null)
        .appendField("outputln");
    this.appendDummyInput();
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(230);
    this.setTooltip('');
    this.setHelpUrl('');
  }
};

Blockly.Blocks['var'] = {
  init: function() {
    this.appendDummyInput()
        .appendField(new Blockly.FieldTextInput("default"), "NAME");
    this.setOutput(true, null);
    this.setColour(330);
    this.setTooltip('');
    this.setHelpUrl('');
  }
};


// \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
// =============================================================================
// CODE GENERATION
// =============================================================================
// /////////////////////////////////////////////////////////////////////////////

Blockly.JavaScript['while'] = function(block) {
  var value_condition = Blockly.JavaScript.valueToCode(block, 'CONDITION', Blockly.JavaScript.ORDER_ATOMIC);
  var statements_statements = Blockly.JavaScript.statementToCode(block, 'STATEMENTS');
  // TODO: Assemble JavaScript into code variable.
  var code = "while ¿" + value_condition + "? {\n" + statements_statements + "}\n";
  return code;
};

Blockly.JavaScript['var_declaration'] = function(block) {
  var dropdown_type = block.getFieldValue('TYPE');
  var text_id = block.getFieldValue('ID');
  var value_value = Blockly.JavaScript.valueToCode(block, 'VALUE', Blockly.JavaScript.ORDER_ATOMIC);
  // TODO: Assemble JavaScript into code variable.
  var code = 'var ' + dropdown_type + ' ' + text_id + ' = ' + value_value + '\n';

  return code;
};

Blockly.JavaScript['var_arr_declaration'] = function(block) {
  var dropdown_type = block.getFieldValue('TYPE');
  var text_id = block.getFieldValue('ID');
  var value_index = Blockly.JavaScript.valueToCode(block, 'INDEX', Blockly.JavaScript.ORDER_ATOMIC);
  var code = 'var ' + dropdown_type + ' ' + text_id + value_index + '\n';

  return code;
};

Blockly.JavaScript['var_free_assign'] = function(block) {
  var text_id = block.getFieldValue('ID');
  var value_value = Blockly.JavaScript.valueToCode(block, 'VALUE', Blockly.JavaScript.ORDER_ATOMIC);
  // TODO: Assemble JavaScript into code variable.
  var code = text_id + ' = ' + value_value + '\n';
  return code;
};

Blockly.JavaScript['var_arr_free_assign'] = function(block) {
  var text_id = block.getFieldValue('ID');
  var value_index = Blockly.JavaScript.valueToCode(block, 'INDEX', Blockly.JavaScript.ORDER_ATOMIC);
  var value_value = Blockly.JavaScript.valueToCode(block, 'VALUE', Blockly.JavaScript.ORDER_ATOMIC);
  // TODO: Assemble JavaScript into code variable.
  var code = 'text_id' + '[' + value_index + ']' + ' = ' + value_value + '\n';
  return code;
};

Blockly.JavaScript['index_selector_array'] = function(block) {
  var value_index_1 = Blockly.JavaScript.valueToCode(block, 'INDEX_1', Blockly.JavaScript.ORDER_ATOMIC);
  // TODO: Assemble JavaScript into code variable.
  var code = '[' + value_index_1 + ']';
  // TODO: Change ORDER_NONE to the correct strength.
  return [code, Blockly.JavaScript.ORDER_NONE];
};

Blockly.JavaScript['index_selector_matrix'] = function(block) {
  var value_index_1 = Blockly.JavaScript.valueToCode(block, 'INDEX_1', Blockly.JavaScript.ORDER_ATOMIC);
  var value_index_2 = Blockly.JavaScript.valueToCode(block, 'INDEX_2', Blockly.JavaScript.ORDER_ATOMIC);
  var code = '[' + value_index_1 + '][' + value_index_2 + ']';
  // TODO: Change ORDER_NONE to the correct strength.
  return [code, Blockly.JavaScript.ORDER_NONE];
};

Blockly.JavaScript['function'] = function(block) {
  var dropdown_type = block.getFieldValue('TYPE');
  var text_id = block.getFieldValue('ID');
  var value_params = Blockly.JavaScript.valueToCode(block, 'PARAMS', Blockly.JavaScript.ORDER_ATOMIC);
  var statements_function = Blockly.JavaScript.statementToCode(block, 'function');
  var code = 'function ' + dropdown_type + ' ' + text_id + '¿' + value_params + '? {\n' + statements_function + '}\n';
  return code;
};

Blockly.JavaScript['param_comma'] = function(block) {
  var value_left_param = Blockly.JavaScript.valueToCode(block, 'LEFT_PARAM', Blockly.JavaScript.ORDER_ATOMIC);
  var value_name = Blockly.JavaScript.valueToCode(block, 'NAME', Blockly.JavaScript.ORDER_ATOMIC);
  // TODO: Assemble JavaScript into code variable.
  var code = value_left_param + ',' + fvalue_name;
  // TODO: Change ORDER_NONE to the correct strength.
  return [code, Blockly.JavaScript.ORDER_NONE];
};

Blockly.JavaScript['return'] = function(block) {
  var value_return = Blockly.JavaScript.valueToCode(block, 'return', Blockly.JavaScript.ORDER_ATOMIC);
  var code = 'return ' + value_return + '\n';
  return code;
};

Blockly.JavaScript['break'] = function(block) {
  var code = 'break\n';
  return code;
};

Blockly.JavaScript['continue'] = function(block) {
  var code = 'continue\n';
  return code;
};

Blockly.JavaScript['output'] = function(block) {
  var value_output = Blockly.JavaScript.valueToCode(block, 'OUTPUT', Blockly.JavaScript.ORDER_ATOMIC);
  var code = 'output(' + value_output + ')\n';
  return code;
};

Blockly.JavaScript['text'] = function(block) {
  var text_string = block.getFieldValue('string');
  var code = '\"' + text_string + '\"';
  // TODO: Change ORDER_NONE to the correct strength.
  return [code, Blockly.JavaScript.ORDER_NONE];
};

Blockly.JavaScript['comment'] = function(block) {
  var text_comment = block.getFieldValue('COMMENT');
  var code = '#' + text_comment + '\n';
  return code;
};

Blockly.JavaScript['function_call'] = function(block) {
  var text_id = block.getFieldValue('ID');
  var value_params = Blockly.JavaScript.valueToCode(block, 'PARAMS', Blockly.JavaScript.ORDER_ATOMIC);
  // TODO: Assemble JavaScript into code variable.
  console.log(value_params);
  var code = text_id + '¿' + value_params + '?\n';
  return code;
};

Blockly.JavaScript['function_call_value'] = function(block) {
  var text_id = block.getFieldValue('ID');
  var value_params = Blockly.JavaScript.valueToCode(block, 'PARAMS', Blockly.JavaScript.ORDER_ATOMIC);
  var code = text_id + '¿' + value_params + '?';
  // TODO: Change ORDER_NONE to the correct strength.
  return [code, Blockly.JavaScript.ORDER_NONE];
};

Blockly.JavaScript['param'] = function(block) {
  var dropdown_type = block.getFieldValue('TYPE');
  var text_id = block.getFieldValue('ID');
  var value_next = Blockly.JavaScript.valueToCode(block, 'NEXT', Blockly.JavaScript.ORDER_ATOMIC);
  var code = dropdown_type + ' ' + text_id;
  if (value_next != "") {
    code += ', ' + value_next;
  }
  // TODO: Change ORDER_NONE to the correct strength.
  return [code, Blockly.JavaScript.ORDER_NONE];
};

Blockly.JavaScript['outputln'] = function(block) {
  var value_value = Blockly.JavaScript.valueToCode(block, 'VALUE', Blockly.JavaScript.ORDER_ATOMIC);
  var code = 'outputln¿' + value_value + '?\n';
  return code;
};

Blockly.JavaScript['var'] = function(block) {
  var text_name = block.getFieldValue('NAME');
  var code = text_name;
  // TODO: Change ORDER_NONE to the correct strength.
  return [code, Blockly.JavaScript.ORDER_NONE];
};