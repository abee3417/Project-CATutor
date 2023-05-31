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
    theme: "neat",
    lineWrapping: true
});

function setColorMode() {
    //var textarea = document.getElementById("codearea");
    var button = document.getElementById("color-mode-btn");
    var currentTheme = editor.getOption("theme");
    var newTheme = currentTheme === "neat" ? "3024-night" : "neat";
    editor.setOption("theme", newTheme);
    if (newTheme === "neat") {
        console.log("newTheme is neat")
        button.innerText = "Dark Mode"
        button.className = "btn btn-dark"
    }
    else {
        console.log("newTheme is dark")
        button.innerText = "Light Mode"
        button.className = "btn btn-light"
    }
}

function clearEditor() {
    //var editor = CodeMirror.fromTextArea(document.getElementById("codearea"));
    editor.getDoc().setValue("");
}