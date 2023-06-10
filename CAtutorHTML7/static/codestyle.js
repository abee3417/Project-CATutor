var editor = CodeMirror.fromTextArea(document.getElementById("codearea"), {
    mode: "text/x-csrc",
    indentWithTabs: true,
    smartIndent: function(state, textBefore) {
    var prevLine = textBefore.trim().split("\n").pop();
    var tabSize = this.getOption("tabSize");
    var baseIndent = prevLine.match(/^\s*/)[0]; // '/'는 정규식(regular expression)을 시작함을 표현, \s는 공백 문자(스페이스, 탭, 줄바꿈 등)에 대응. 따라서 prevLine.match(/^\s*/)[0]은 prevLine 문자열의 시작부터 연속된 공백 문자열 중 가장 긴 것을 반환
    if (/^\s*[\{\(\[]/.test(prevLine)) {
        return baseIndent + tabSize;
    }

    else {
        return baseIndent;
    }
    },
    lineNumbers: true,
    autofocus: true,
    extraKeys: {
    "Enter": "newlineAndIndentContinueComment"
    },
    indentUnit: 4,
    tabSize: 4,
    matchBrackets: true,
    autoCloseBrackets: true,
    theme: "neo",
    lineWrapping: true
});

function setColorMode() {
    //var textarea = document.getElementById("codearea");
    var button = document.getElementById("color-mode-btn");
    var currentTheme = editor.getOption("theme");
    var newTheme = currentTheme === "neo" ? "3024-night" : "neo";
    editor.setOption("theme", newTheme);
    if (newTheme === "neo") {
        button.innerText = "Dark Mode"
        button.className = "btn btn-dark"
    }
    else {
        button.innerText = "Light Mode"
        button.className = "btn btn-light"
    }
}

function clearEditor() {
    //var editor = CodeMirror.fromTextArea(document.getElementById("codearea"));
    editor.getDoc().setValue("");
}

function checkGoIndex() {
    var tmp = editor.getDoc().getValue("");
    if (tmp !== "") {
        if(confirm('지금 나가면 저장되지 않습니다!')) {
            location.href="http://127.0.0.1:8000/catutor/";
        }
        else {
            return false;
        }
    }
    else{
        location.href="http://127.0.0.1:8000/catutor/";
    }
}

function checkGoCode() {
    var tmp = editor.getDoc().getValue("");
    if (tmp !== "") {
        if(confirm('지금 나가면 저장되지 않습니다!')) {
            location.href="http://127.0.0.1:8000/catutor/code/";
        }
        else {
            return false;
        }
    }
    else{
        location.href="http://127.0.0.1:8000/catutor/code/";
    }
}

function checkGoLogin() {
    var tmp = editor.getDoc().getValue("");
    if (tmp !== "") {
        if(confirm('지금 나가면 저장되지 않습니다!')) {
            // 일단 임시로 result페이지로 지정, 나중에 로그인페이지로 바꾸기
            location.href="http://127.0.0.1:8000/catutor/result/";
        }
        else {
            return false;
        }
    }
    else{
        location.href="http://127.0.0.1:8000/catutor/result/";
    }
}
function loadFile() {
    var input = document.getElementById("input-file");
    var file = input.files[0];
    var reader = new FileReader();
    reader.onload = function() {
      editor.setValue(reader.result);
      input.value = "";
    };
    reader.readAsText(file);
}