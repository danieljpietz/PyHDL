"use strict";
let isTesting = false;
const ILEscape = "@@";
const ILCommentPrefix = ILEscape + "comments";
const ILIndentedReturnPrefix = ILEscape;
const ILQuote = "⨵";
const ILSingleQuote = "⦼";
const ILBackslash = "⨸";
const ILSemicolon = "⨴";
var FormatMode;
(function (FormatMode) {
    FormatMode[FormatMode["Default"] = 0] = "Default";
    FormatMode[FormatMode["EndsWithSemicolon"] = 1] = "EndsWithSemicolon";
    FormatMode[FormatMode["CaseWhen"] = 2] = "CaseWhen";
    FormatMode[FormatMode["IfElse"] = 3] = "IfElse";
    FormatMode[FormatMode["PortGeneric"] = 4] = "PortGeneric";
})(FormatMode || (FormatMode = {}));
let Mode = FormatMode.Default;
class NewLineSettings {
    constructor() {
        this.newLineAfter = [];
        this.noNewLineAfter = [];
    }
    newLineAfterPush(keyword) {
        this.newLineAfter.push(keyword);
    }
    noNewLineAfterPush(keyword) {
        this.noNewLineAfter.push(keyword);
    }
    push(keyword, addNewLine) {
        let str = addNewLine.toLowerCase();
        if (str == "none") {
            return;
        }
        else if (!str.startsWith("no")) {
            this.newLineAfterPush(keyword);
        }
        else {
            this.noNewLineAfterPush(keyword);
        }
    }
}

function ConstructNewLineSettings(dict) {
    let settings = new NewLineSettings();
    for (let key in dict) {
        settings.push(key, dict[key]);
    }
    return settings;
}

String.prototype.regexCount = function (pattern) {
    if (pattern.flags.indexOf("g") < 0) {
        pattern = new RegExp(pattern.source, pattern.flags + "g");
    }
    return (this.match(pattern) || []).length;
};
String.prototype.count = function (text) {
    return this.split(text).length - 1;
};
String.prototype.regexStartsWith = function (pattern) {
    var searchResult = this.search(pattern);
    return searchResult == 0;
};
String.prototype.regexIndexOf = function (pattern, startIndex) {
    startIndex = startIndex || 0;
    var searchResult = this.substr(startIndex).search(pattern);
    return (-1 === searchResult) ? -1 : searchResult + startIndex;
};
String.prototype.regexLastIndexOf = function (pattern, startIndex) {
    pattern = (pattern.global) ? pattern :
        new RegExp(pattern.source, 'g' + (pattern.ignoreCase ? 'i' : '') + (pattern.multiline ? 'm' : ''));
    if (typeof (startIndex) === 'undefined') {
        startIndex = this.length;
    }
    else if (startIndex < 0) {
        startIndex = 0;
    }
    const stringToWorkWith = this.substring(0, startIndex + 1);
    let lastIndexOf = -1;
    let nextStop = 0;
    let result;
    while ((result = pattern.exec(stringToWorkWith)) != null) {
        lastIndexOf = result.index;
        pattern.lastIndex = ++nextStop;
    }
    return lastIndexOf;
};
String.prototype.reverse = function () {
    return this.split('').reverse().join('');
};
String.prototype.convertToRegexBlockWords = function () {
    let result = new RegExp("(" + this + ")([^\\w]|$)");
    return result;
};
Array.prototype.convertToRegexBlockWords = function () {
    let wordsStr = this.join("|");
    let result = new RegExp("(" + wordsStr + ")([^\\w]|$)");
    return result;
};
function EscapeComments(arr) {
    var comments = [];
    var count = 0;
    for (var i = 0; i < arr.length; i++) {
        var line = arr[i];
        var commentStartIndex = line.indexOf("--");
        if (commentStartIndex >= 0) {
            comments.push(line.substr(commentStartIndex));
            arr[i] = line.substr(0, commentStartIndex) + ILCommentPrefix + count;
            count++;
        }
    }
    var isInComment = false;
    var commentRegex = new RegExp("(?<=" + ILCommentPrefix + "[\\d]+).");
    for (var i = 0; i < arr.length; i++) {
        var commentStartIndex = 0;
        var hasComment = true;
        var commentEndInlineIndex = 0;
        while (hasComment) {
            var line = arr[i];
            if (!isInComment) {
                commentStartIndex = line.indexOf("/*");
                var commentEndIndex = line.indexOf("*/", commentStartIndex);
                if (commentStartIndex >= 0) {
                    if (commentEndIndex >= 0) {
                        commentEndInlineIndex = commentEndIndex + 2;
                        isInComment = false;
                        comments.push(line.substring(commentStartIndex, commentEndInlineIndex));
                        arr[i] = line.substr(0, commentStartIndex) + ILCommentPrefix + count + line.substr(commentEndInlineIndex);
                        count++;
                        hasComment = true;
                        if (commentStartIndex + 2 == line.length) {
                            hasComment = false;
                        }
                    }
                    else {
                        isInComment = true;
                        comments.push(line.substr(commentStartIndex));
                        arr[i] = line.substr(0, commentStartIndex) + ILCommentPrefix + count;
                        count++;
                        hasComment = false;
                    }
                }
                else {
                    hasComment = false;
                }
                continue;
            }
            if (isInComment) {
                var lastCommentEndIndex = line.regexLastIndexOf(commentRegex, line.length);
                if (commentStartIndex == 0) {
                    var commentEndIndex = line.indexOf("*/", lastCommentEndIndex);
                }
                else {
                    var commentEndIndex = line.indexOf("*/", commentStartIndex);
                }
                if (commentEndIndex >= 0) {
                    isInComment = false;
                    comments.push(line.substr(0, commentEndIndex + 2));
                    arr[i] = ILCommentPrefix + count + line.substr(commentEndIndex + 2);
                    count++;
                    hasComment = true;
                }
                else {
                    comments.push(line);
                    arr[i] = ILCommentPrefix + count;
                    count++;
                    hasComment = false;
                }
            }
        }
    }
    return comments;
}
function ToLowerCases(arr) {
    for (var i = 0; i < arr.length; i++) {
        arr[i] = arr[i].toLowerCase();
    }
}
function ToUpperCases(arr) {
    for (var i = 0; i < arr.length; i++) {
        arr[i] = arr[i].toUpperCase();
    }
}
function ToCamelCases(arr) {
    for (var i = 0; i < arr.length; i++) {
        arr[i] = arr[i].charAt(0) + arr[i].slice(1).toLowerCase();
    }
}
function ReplaceKeyWords(text, keywords) {
    for (var k = 0; k < keywords.length; k++) {
        text = text.replace(new RegExp("([^a-zA-Z0-9_@]|^)" + keywords[k] + "([^a-zA-Z0-9_]|$)", 'gi'), "$1" + keywords[k] + "$2");
    }
    return text;
}
function SetKeywordCase(input, keywordcase, keywords) {
    let inputcase = keywordcase.toLowerCase();
    switch (inputcase) {
        case "lowercase":
            ToLowerCases(keywords);
            break;
        case "defaultcase":
            ToCamelCases(keywords);
            break;
        case "uppercase":
            ToUpperCases(keywords);
    }
    input = ReplaceKeyWords(input, keywords);
    return input;
}
function SetNewLinesAfterSymbols(text, newLineSettings) {
    if (newLineSettings == null) {
        return text;
    }
    if (newLineSettings.newLineAfter != null) {
        newLineSettings.newLineAfter.forEach(symbol => {
            let upper = symbol.toUpperCase();
            var rexString = "(" + upper + ")[ ]?([^ \r\n@])";
            let regex = null;
            if (upper.regexStartsWith(/\w/)) {
                regex = new RegExp("\\b" + rexString, "g");
            }
            else {
                regex = new RegExp(rexString, "g");
            }
            text = text.replace(regex, '$1\r\n$2');
            if (upper == "PORT") {
                text = text.replace(/\bPORT\b\s+MAP/, "PORT MAP");
            }
        });
    }
    if (newLineSettings.noNewLineAfter != null) {
        newLineSettings.noNewLineAfter.forEach(symbol => {
            let rexString = "(" + symbol.toUpperCase() + ")[ \r\n]+([^@])";
            let regex = null;
            if (symbol.regexStartsWith(/\w/)) {
                regex = new RegExp("\\b" + rexString, "g");
                text = text.replace(regex, '$1 $2');
            }
            else {
                regex = new RegExp(rexString, "g");
            }
            text = text.replace(regex, '$1 $2');
        });
    }
    return text;
}

class signAlignSettings {
    constructor(isRegional, isAll, mode, keyWords, alignComments = false) {
        this.isRegional = isRegional;
        this.isAll = isAll;
        this.mode = mode;
        this.keyWords = keyWords;
        this.alignComments = alignComments;
    }
}

class BeautifierSettings {
    constructor(removeComments, removeReport, checkAlias, signAlignSettings, keywordCase, typeNameCase, indentation, newLineSettings, endOfLine, addNewLine) {
        this.RemoveComments = removeComments;
        this.RemoveAsserts = removeReport;
        this.CheckAlias = checkAlias;
        this.SignAlignSettings = signAlignSettings;
        this.KeywordCase = keywordCase;
        this.TypeNameCase = typeNameCase;
        this.Indentation = indentation;
        this.NewLineSettings = newLineSettings;
        this.EndOfLine = endOfLine;
        this.AddNewLine = addNewLine;
    }
}

let KeyWords = ["ABS", "ACCESS", "AFTER", "ALIAS", "ALL", "AND", "ARCHITECTURE", "ARRAY", "ASSERT", "ATTRIBUTE", "BEGIN", "BLOCK", "BODY", "BUFFER", "BUS", "CASE", "COMPONENT", "CONFIGURATION", "CONSTANT", "CONTEXT", "COVER", "DISCONNECT", "DOWNTO", "DEFAULT", "ELSE", "ELSIF", "END", "ENTITY", "EXIT", "FAIRNESS", "FILE", "FOR", "FORCE", "FUNCTION", "GENERATE", "GENERIC", "GROUP", "GUARDED", "IF", "IMPURE", "IN", "INERTIAL", "INOUT", "IS", "LABEL", "LIBRARY", "LINKAGE", "LITERAL", "LOOP", "MAP", "MOD", "NAND", "NEW", "NEXT", "NOR", "NOT", "NULL", "OF", "ON", "OPEN", "OR", "OTHERS", "OUT", "PACKAGE", "PORT", "POSTPONED", "PROCEDURE", "PROCESS", "PROPERTY", "PROTECTED", "PURE", "RANGE", "RECORD", "REGISTER", "REJECT", "RELEASE", "REM", "REPORT", "RESTRICT", "RESTRICT_GUARANTEE", "RETURN", "ROL", "ROR", "SELECT", "SEQUENCE", "SEVERITY", "SHARED", "SIGNAL", "SLA", "SLL", "SRA", "SRL", "STRONG", "SUBTYPE", "THEN", "TO", "TRANSPORT", "TYPE", "UNAFFECTED", "UNITS", "UNTIL", "USE", "VARIABLE", "VMODE", "VPROP", "VUNIT", "WAIT", "WHEN", "WHILE", "WITH", "XNOR", "XOR"];
let TypeNames = ["BOOLEAN", "BIT", "CHARACTER", "INTEGER", "TIME", "NATURAL", "POSITIVE", "STD_LOGIC", "STD_LOGIC_VECTOR", "STD_ULOGIC", "STD_ULOGIC_VECTOR", "STRING"];
function beautify(input, settings) {
    input = input.replace(/\r\n/g, "\n");
    input = input.replace(/\n/g, "\r\n");
    var arr = input.split("\r\n");
    var comments = EscapeComments(arr);
    var backslashes = escapeText(arr, "\\\\[^\\\\]+\\\\", ILBackslash);
    let quotes = escapeText(arr, '"([^"]+)"', ILQuote);
    let singleQuotes = escapeText(arr, "'[^']'", ILSingleQuote);
    RemoveLeadingWhitespaces(arr);
    input = arr.join("\r\n");
    input = SetKeywordCase(input, "uppercase", KeyWords);
    input = SetKeywordCase(input, "uppercase", TypeNames);
    input = RemoveExtraNewLines(input);
    input = input.replace(/[\t ]+/g, ' ');
    input = input.replace(/\([\t ]+/g, '\(');
    input = input.replace(/[ ]+;/g, ';');
    input = input.replace(/:[ ]*(PROCESS|ENTITY)/gi, ':$1');
    arr = input.split("\r\n");
    ReserveSemicolonInKeywords(arr);
    input = arr.join("\r\n");
    input = input.replace(/\b(PORT|GENERIC)\b\s+MAP/g, '$1 MAP');
    input = input.replace(/\b(PORT|PROCESS|GENERIC)\b[\s]*\(/g, '$1 (');
    let newLineSettings = settings.NewLineSettings;
    if (newLineSettings != null) {
        input = SetNewLinesAfterSymbols(input, newLineSettings);
        arr = input.split("\r\n");
        ApplyNoNewLineAfter(arr, newLineSettings.noNewLineAfter);
        input = arr.join("\r\n");
    }
    input = input.replace(/([a-zA-Z0-9\); ])\);(@@comments[0-9]+)?@@end/g, '$1\r\n);$2@@end');
    input = input.replace(/[ ]?([&=:\-\+|\*]|[<>]+)[ ]?/g, ' $1 ');
    input = input.replace(/(\d+e) +([+\-]) +(\d+)/g, '$1$2$3'); // fix exponential notation format broken by previous step
    input = input.replace(/[ ]?([,])[ ]?/g, '$1 ');
    input = input.replace(/[ ]?(['"])(THEN)/g, '$1 $2');
    input = input.replace(/[ ]?(\?)?[ ]?(<|:|>|\/)?[ ]+(=)?[ ]?/g, ' $1$2$3 ');
    input = input.replace(/(IF)[ ]?([\(\)])/g, '$1 $2');
    input = input.replace(/([\(\)])[ ]?(THEN)/gi, '$1 $2');
    input = input.replace(/(^|[\(\)])[ ]?(AND|OR|XOR|XNOR)[ ]*([\(])/g, '$1 $2 $3');
    input = input.replace(/ ([\-\*\/=+<>])[ ]*([\-\*\/=+<>]) /g, " $1$2 ");
    //input = input.replace(/\r\n[ \t]+--\r\n/g, "\r\n");
    input = input.replace(/[ ]+/g, ' ');
    input = input.replace(/[ \t]+\r\n/g, "\r\n");
    input = input.replace(/\r\n\r\n\r\n/g, '\r\n');
    input = input.replace(/[\r\n\s]+$/g, '');
    input = input.replace(/[ \t]+\)/g, ')');
    input = input.replace(/\s*\)\s+RETURN\s+([\w]+;)/g, '\r\n) RETURN $1'); //function(..)\r\nreturn type; -> function(..\r\n)return type;
    input = input.replace(/\)\s*(@@\w+)\r\n\s*RETURN\s+([\w]+;)/g, ') $1\r\n' + ILIndentedReturnPrefix + 'RETURN $2'); //function(..)\r\nreturn type; -> function(..\r\n)return type;
    let keywordAndSignRegex = new RegExp("(\\b" + KeyWords.join("\\b|\\b") + "\\b) +([\\-+]) +(\\w)", "g");
    input = input.replace(keywordAndSignRegex, "$1 $2$3"); // `WHEN - 2` -> `WHEN -2`
    input = input.replace(/([,|]) +([+\-]) +(\w)/g, '$1 $2$3'); // `1, - 2)` -> `1, -2)`
    input = input.replace(/(\() +([+\-]) +(\w)/g, '$1$2$3'); // `( - 2)` -> `(-2)`
    arr = input.split("\r\n");
    let result = [];
    let block = new CodeBlock(arr);
    beautify3(block, result, settings, 0);
    var alignSettings = settings.SignAlignSettings;
    if (alignSettings != null && alignSettings.isAll) {
        AlignSigns(result, 0, result.length - 1, alignSettings.mode, alignSettings.alignComments);
    }
    arr = FormattedLineToString(result, settings.Indentation);
    input = arr.join("\r\n");
    input = input.replace(/@@RETURN/g, "RETURN");
    input = SetKeywordCase(input, settings.KeywordCase, KeyWords);
    input = SetKeywordCase(input, settings.TypeNameCase, TypeNames);
    input = replaceEscapedWords(input, quotes, ILQuote);
    input = replaceEscapedWords(input, singleQuotes, ILSingleQuote);
    input = replaceEscapedComments(input, comments, ILCommentPrefix);
    input = replaceEscapedWords(input, backslashes, ILBackslash);
    input = input.replace(new RegExp(ILSemicolon, "g"), ";");
    input = input.replace(/@@[a-z]+/g, "");
    var escapedTexts = new RegExp("[" + ILBackslash + ILQuote + ILSingleQuote + "]", "g");
    input = input.replace(escapedTexts, "");
    input = input.replace(/\r\n/g, settings.EndOfLine);
    if (settings.AddNewLine && !input.endsWith(settings.EndOfLine)) {
        input += settings.EndOfLine;
    }
    return input;
}

function replaceEscapedWords(input, arr, prefix) {
    for (var i = 0; i < arr.length; i++) {
        var text = arr[i];
        var regex = new RegExp("(" + prefix + "){" + text.length + "}");
        input = input.replace(regex, text);
    }
    return input;
}
function replaceEscapedComments(input, arr, prefix) {
    for (var i = 0; i < arr.length; i++) {
        input = input.replace(prefix + i, arr[i]);
    }
    return input;
}
function RemoveLeadingWhitespaces(arr) {
    for (var i = 0; i < arr.length; i++) {
        arr[i] = arr[i].replace(/^\s+/, "");
    }
}
class FormattedLine {
    constructor(line, indent) {
        this.Line = line;
        this.Indent = indent;
    }
}

class CodeBlock {
    constructor(lines, start = 0, end = lines.length - 1) {
        this.lines = lines;
        this.start = start;
        this.end = end;
        this.parent = null;
        this.cursor = start;
    }
    _notifySplit(atLine) {
        if (this.start > atLine)
            this.start++;
        if (this.end >= atLine)
            this.end++;
        if (this.cursor >= atLine)
            this.cursor++;
        if (this.parent)
            this.parent._notifySplit(atLine);
    }
    splitLine(atLine, firstText, secondText) {
        this.lines[atLine] = firstText;
        this.lines.splice(atLine + 1, 0, secondText);
        this._notifySplit(atLine);
    }
    subBlock(start, end) {
        let newBlock = new CodeBlock(this.lines, start, end);
        newBlock.parent = this;
        return newBlock;
    }
}

function FormattedLineToString(arr, indentation) {
    let result = [];
    if (arr == null) {
        return result;
    }
    if (indentation == null) {
        indentation = "";
    }
    arr.forEach(i => {
        if (i instanceof FormattedLine) {
            if (i.Line.length > 0) {
                result.push((Array(i.Indent + 1).join(indentation)) + i.Line);
            }
            else {
                result.push("");
            }
        }
        else {
            result = result.concat(FormattedLineToString(i, indentation));
        }
    });
    return result;
}

function GetCloseparentheseEndIndex(block) {
    let openParentheseCount = 0;
    let closeParentheseCount = 0;
    let startIndex = block.cursor;
    for (; block.cursor <= block.end; block.cursor++) {
        let input = block.lines[block.cursor];
        openParentheseCount += input.count("(");
        closeParentheseCount += input.count(")");
        if (openParentheseCount > 0
            && openParentheseCount <= closeParentheseCount) {
            return;
        }
    }
    block.cursor = startIndex;
}
function beautifyPortGenericBlock(block, result, settings, indent, mode) {
    let startIndex = block.cursor;
    let firstLine = block.lines[startIndex];
    let regex = new RegExp("[\\w\\s:]*(" + mode + ")([\\s]|$)");
    if (!firstLine.regexStartsWith(regex)) {
        return;
    }
    let firstLineHasParenthese = firstLine.indexOf("(") >= 0;
    let secondLineHasParenthese = startIndex + 1 <= block.end && block.lines[startIndex + 1].startsWith("(");
    let hasParenthese = firstLineHasParenthese || secondLineHasParenthese;
    let blockBodyStartIndex = startIndex + (secondLineHasParenthese ? 1 : 0);
    if (hasParenthese) {
        GetCloseparentheseEndIndex(block);
    }
    let endIndex = block.cursor;
    let bodyBlock = block.subBlock(blockBodyStartIndex, endIndex);
    if (endIndex != startIndex && firstLineHasParenthese) {
        block.lines[startIndex] = block.lines[startIndex].replace(/\b(PORT|GENERIC|PROCEDURE)\b([\w ]+)\(([\w\(\) ]+)/, '$1$2(\r\n$3');
        let newInputs = block.lines[startIndex].split("\r\n");
        if (newInputs.length == 2) {
            bodyBlock.splitLine(startIndex, newInputs[0], newInputs[1]);
        }
    }
    else if (endIndex > startIndex + 1 && secondLineHasParenthese) {
        block.lines[startIndex + 1] = block.lines[startIndex + 1].replace(/\(([\w\(\) ]+)/, '(\r\n$1');
        let newInputs = block.lines[startIndex + 1].split("\r\n");
        if (newInputs.length == 2) {
            bodyBlock.splitLine(startIndex + 1, newInputs[0], newInputs[1]);
        }
    }
    if (firstLineHasParenthese && block.lines[startIndex].indexOf("MAP") > 0) {
        block.lines[startIndex] = block.lines[startIndex].replace(/([^\w])(MAP)\s+\(/g, '$1$2(');
    }
    result.push(new FormattedLine(block.lines[startIndex], indent));
    if (secondLineHasParenthese) {
        let secondLineIndent = indent;
        if (endIndex == startIndex + 1) {
            secondLineIndent++;
        }
        result.push(new FormattedLine(block.lines[startIndex + 1], secondLineIndent));
    }
    beautify3(bodyBlock.subBlock(bodyBlock.start + 1, bodyBlock.end), result, settings, indent + 1);
    if (block.lines[block.cursor].startsWith(")")) {
        result[block.cursor].Indent--;
        bodyBlock.end--;
    }
    var alignSettings = settings.SignAlignSettings;
    if (alignSettings != null) {
        if (alignSettings.isRegional && !alignSettings.isAll
            && alignSettings.keyWords != null
            && alignSettings.keyWords.indexOf(mode) >= 0) {
            AlignSigns(result, bodyBlock.start + 1, bodyBlock.end, alignSettings.mode, alignSettings.alignComments);
        }
    }
}

function AlignSigns(result, startIndex, endIndex, mode, alignComments = false) {
    AlignSign_(result, startIndex, endIndex, ":", mode);
    AlignSign_(result, startIndex, endIndex, ":=", mode);
    AlignSign_(result, startIndex, endIndex, "<=", mode);
    AlignSign_(result, startIndex, endIndex, "=>", mode);
    AlignSign_(result, startIndex, endIndex, "direction", mode);
    if (alignComments) {
        AlignSign_(result, startIndex, endIndex, "@@comments", mode);
    }
}

function indexOfGroup(regex, input, group) {
    var match = regex.exec(input);
    if (match == null) {
        return -1;
    }
    var index = match.index;
    for (let i = 1; i < group; i++) {
        index += match[i].length;
    }
    return index;
}
function AlignSign_(result, startIndex, endIndex, symbol, mode) {
    let maxSymbolIndex = -1;
    let symbolIndices = {};
    let startLine = startIndex;
    let labelAndKeywords = [
        "([\\w\\s]*:(\\s)*PROCESS)",
        "([\\w\\s]*:(\\s)*POSTPONED PROCESS)",
        "([\\w\\s]*:\\s*$)",
        "([\\w\\s]*:.*\\s+GENERATE)"
    ];
    let labelAndKeywordsStr = labelAndKeywords.join("|");
    let labelAndKeywordsRegex = new RegExp("(" + labelAndKeywordsStr + ")([^\\w]|$)");
    for (let i = startIndex; i <= endIndex; i++) {
        let line = result[i].Line;
        if (symbol == ":" && line.regexStartsWith(labelAndKeywordsRegex)) {
            continue;
        }
        let regex;
        if (symbol == "direction") {
            regex = new RegExp("(:\\s*)(IN|OUT|INOUT|BUFFER)(\\s+)(\\w)");
        }
        else {
            regex = new RegExp("([\\s\\w\\\\]|^)" + symbol + "([\\s\\w\\\\]|$)");
        }
        if (line.regexCount(regex) > 1) {
            continue;
        }
        let colonIndex;
        if (symbol == "direction") {
            colonIndex = indexOfGroup(regex, line, 4);
        }
        else {
            colonIndex = line.regexIndexOf(regex);
        }
        if (colonIndex > 0) {
            maxSymbolIndex = Math.max(maxSymbolIndex, colonIndex);
            symbolIndices[i] = colonIndex;
        }
        else if ((mode != "local" && !line.startsWith(ILCommentPrefix) && line.length != 0)
            || (mode == "local")) {
            if (startLine < i - 1) // if cannot find the symbol, a block of symbols ends
             {
                AlignSign(result, startLine, i - 1, symbol, maxSymbolIndex, symbolIndices);
            }
            maxSymbolIndex = -1;
            symbolIndices = {};
            startLine = i;
        }
    }
    if (startLine < endIndex) // if cannot find the symbol, a block of symbols ends
     {
        AlignSign(result, startLine, endIndex, symbol, maxSymbolIndex, symbolIndices);
    }
}
function AlignSign(result, startIndex, endIndex, symbol, maxSymbolIndex = -1, symbolIndices = {}) {
    if (maxSymbolIndex < 0) {
        return;
    }
    for (let lineIndex in symbolIndices) {
        let symbolIndex = symbolIndices[lineIndex];
        if (symbolIndex == maxSymbolIndex) {
            continue;
        }
        let line = result[lineIndex].Line;
        result[lineIndex].Line = line.substring(0, symbolIndex)
            + (Array(maxSymbolIndex - symbolIndex + 1).join(" "))
            + line.substring(symbolIndex);
    }
}

function beautifyCaseBlock(block, result, settings, indent) {
    if (!block.lines[block.cursor].regexStartsWith(/(.+:\s*)?(CASE)([\s]|$)/)) {
        return;
    }
    result.push(new FormattedLine(block.lines[block.cursor], indent));
    block.cursor++;
    beautify3(block, result, settings, indent + 2);
    result[block.cursor].Indent = indent;
}

function getSemicolonBlockEndIndex(block, settings) {
    let endIndex = block.cursor;
    let openBracketsCount = 0;
    let closeBracketsCount = 0;
    for (; block.cursor <= block.end; block.cursor++) {
        let input = block.lines[block.cursor];
        let indexOfSemicolon = input.indexOf(";");
        let splitIndex = indexOfSemicolon < 0 ? input.length : indexOfSemicolon + 1;
        let stringBeforeSemicolon = input.substring(0, splitIndex);
        let stringAfterSemicolon = input.substring(splitIndex);
        stringAfterSemicolon = stringAfterSemicolon.replace(new RegExp(ILCommentPrefix + "[0-9]+"), "");
        openBracketsCount += stringBeforeSemicolon.count("(");
        closeBracketsCount += stringBeforeSemicolon.count(")");
        if (indexOfSemicolon < 0) {
            continue;
        }
        if (openBracketsCount == closeBracketsCount) {
            endIndex = block.cursor;
            if (stringAfterSemicolon.trim().length > 0 && settings.NewLineSettings.newLineAfter.indexOf(";") >= 0) {
                block.splitLine(block.cursor, stringBeforeSemicolon, stringAfterSemicolon);
            }
            break;
        }
    }
    block.cursor = endIndex;
}
function beautifyComponentBlock(block, result, settings, indent) {
    let startIndex = block.cursor;
    for (; block.cursor <= block.end; block.cursor++) {
        if (block.lines[block.cursor].regexStartsWith(/END(\s|$)/)) {
            break;
        }
    }
    result.push(new FormattedLine(block.lines[startIndex], indent));
    if (block.cursor != startIndex) {
        beautify3(block.subBlock(startIndex + 1, block.cursor), result, settings, indent + 1);
    }
}

function beautifyPackageIsNewBlock(block, result, settings, indent) {
    let startIndex = block.cursor;
    for (; block.cursor <= block.end; block.cursor++) {
        if (block.lines[block.cursor].regexIndexOf(/;(\s|$)/) >= 0) {
            break;
        }
    }
    result.push(new FormattedLine(block.lines[startIndex], indent));
    if (block.cursor != startIndex) {
        beautify3(block.subBlock(startIndex + 1, block.cursor), result, settings, indent + 1);
    }
}

function beautifyVariableInitialiseBlock(block, result, settings, indent) {
    let startIndex = block.cursor;
    for (; block.cursor <= block.end; block.cursor++) {
        if (block.lines[block.cursor].regexIndexOf(/;(\s|$)/) >= 0) {
            break;
        }
    }
    result.push(new FormattedLine(block.lines[startIndex], indent));
    if (block.cursor != startIndex) {
        beautify3(block.subBlock(startIndex + 1, block.cursor), result, settings, indent + 1);
    }
}

function beautifySemicolonBlock(block, result, settings, indent) {
    let startIndex = block.cursor;
    getSemicolonBlockEndIndex(block, settings);
    result.push(new FormattedLine(block.lines[startIndex], indent));
    if (block.cursor != startIndex) {
        beautify3(block.subBlock(startIndex + 1, block.cursor), result, settings, indent + 1);
        alignSignalAssignmentBlock(settings, block.lines, startIndex, block.cursor, result);
    }
}

function alignSignalAssignmentBlock(settings, inputs, startIndex, endIndex, result) {
    if (settings.Indentation.replace(/ +/g, "").length == 0) {
        let reg = new RegExp("^([\\w\\\\]+[\\s]*<=\\s*)");
        let match = reg.exec(inputs[startIndex]);
        if (match != null) {
            let length = match[0].length;
            let prefixLength = length - settings.Indentation.length;
            let prefix = new Array(prefixLength + 1).join(" ");
            for (let i = startIndex + 1; i <= endIndex; i++) {
                let fl = result[i];
                fl.Line = prefix + fl.Line;
            }
        }
    }
}
function beautify3(block, result, settings, indent) {
    let regexOneLineBlockKeyWords = new RegExp(/(PROCEDURE)[^\w](?!.+[^\w]IS([^\w]|$))/); //match PROCEDURE..; but not PROCEDURE .. IS;
    let regexFunctionMultiLineBlockKeyWords = new RegExp(/(FUNCTION|IMPURE FUNCTION)[^\w](?=.+[^\w]IS([^\w]|$))/); //match FUNCTION .. IS; but not FUNCTION
    let blockMidKeyWords = ["BEGIN"];
    let blockStartsKeyWords = [
        "IF",
        "CASE",
        "ARCHITECTURE",
        "PROCEDURE",
        "PACKAGE",
        "(([\\w\\s]*:)?(\\s)*PROCESS)",
        "(([\\w\\s]*:)?(\\s)*POSTPONED PROCESS)",
        "(.*\\s*PROTECTED)",
        "(COMPONENT)",
        "(ENTITY(?!.+;))",
        "FOR",
        "WHILE",
        "LOOP",
        "(.*\\s*GENERATE)",
        "(CONTEXT[\\w\\s\\\\]+IS)",
        "(CONFIGURATION(?!.+;))",
        "BLOCK",
        "UNITS",
        "\\w+\\s+\\w+\\s+IS\\s+RECORD"
    ];
    let blockEndsKeyWords = ["END", ".*\\)\\s*RETURN\\s+[\\w]+;"];
    let indentedEndsKeyWords = [ILIndentedReturnPrefix + "RETURN\\s+\\w+;"];
    let blockEndsWithSemicolon = [
        "(WITH\\s+[\\w\\s\\\\]+SELECT)",
        "([\\w\\\\]+[\\s]*<=)",
        "([\\w\\\\]+[\\s]*:=)",
        "FOR\\s+[\\w\\s,]+:\\s*\\w+\\s+USE",
        "REPORT"
    ];
    let newLineAfterKeyWordsStr = blockStartsKeyWords.join("|");
    let regexBlockMidKeyWords = blockMidKeyWords.convertToRegexBlockWords();
    let regexBlockStartsKeywords = new RegExp("([\\w]+\\s*:\\s*)?(" + newLineAfterKeyWordsStr + ")([^\\w]|$)");
    let regexBlockEndsKeyWords = blockEndsKeyWords.convertToRegexBlockWords();
    let regexBlockIndentedEndsKeyWords = indentedEndsKeyWords.convertToRegexBlockWords();
    let regexblockEndsWithSemicolon = blockEndsWithSemicolon.convertToRegexBlockWords();
    let regexMidKeyWhen = "WHEN".convertToRegexBlockWords();
    let regexMidKeyElse = "ELSE|ELSIF".convertToRegexBlockWords();
    for (; block.cursor <= block.end; block.cursor++) {
        if (indent < 0) {
            indent = 0;
        }
        let input = block.lines[block.cursor].trim();
        if (input.regexStartsWith(regexBlockIndentedEndsKeyWords)) {
            result.push(new FormattedLine(input, indent));
            return;
        }
        if (input.regexStartsWith(/COMPONENT\s/)) {
            let modeCache = Mode;
            Mode = FormatMode.EndsWithSemicolon;
            beautifyComponentBlock(block, result, settings, indent);
            Mode = modeCache;
            continue;
        }
        if (input.regexStartsWith(/PACKAGE[\s\w]+IS\s+NEW/)) {
            let modeCache = Mode;
            Mode = FormatMode.EndsWithSemicolon;
            beautifyPackageIsNewBlock(block, result, settings, indent);
            Mode = modeCache;
            continue;
        }
        if (input.regexStartsWith(/\w+\s+\w+\s*:.+:\s*=\s*\(([^;]|$)/)) { // 'variable symbol: type [:= initial_value];'
            let modeCache = Mode;
            Mode = FormatMode.EndsWithSemicolon;
            let endsWithBracket = input.regexIndexOf(/:\s*=\s*\(/) > 0;
            let startIndex = block.cursor;
            beautifySemicolonBlock(block, result, settings, indent);
            if (endsWithBracket && startIndex != block.cursor) {
                let fl = result[block.end];
                if (fl.Line.regexStartsWith(/\);$/)) {
                    fl.Indent--;
                }
            }
            Mode = modeCache;
            continue;
        }
        if (input.regexIndexOf(/:=(\s*@@comments\d+\s*)?$/) > 0) {
            let modeCache = Mode;
            Mode = FormatMode.EndsWithSemicolon;
            beautifySemicolonBlock(block, result, settings, indent);
            Mode = modeCache;
            continue;
        }
        if (input.regexStartsWith(/\w+\s*:\s*ENTITY/)) {
            let modeCache = Mode;
            Mode = FormatMode.EndsWithSemicolon;
            beautifySemicolonBlock(block, result, settings, indent);
            Mode = modeCache;
            continue;
        }
        if (Mode != FormatMode.EndsWithSemicolon && input.regexStartsWith(regexblockEndsWithSemicolon)) {
            let modeCache = Mode;
            Mode = FormatMode.EndsWithSemicolon;
            beautifySemicolonBlock(block, result, settings, indent);
            Mode = modeCache;
            continue;
        }
        if (input.regexStartsWith(/(.+:\s*)?(CASE)([\s]|$)/)) {
            let modeCache = Mode;
            Mode = FormatMode.CaseWhen;
            beautifyCaseBlock(block, result, settings, indent);
            Mode = modeCache;
            continue;
        }
        if (input.regexStartsWith(/[\w\s:]*(:=)([\s]|$)/)) {
            beautifyPortGenericBlock(block, result, settings, indent, ":=");
            continue;
        }
        if (input.regexStartsWith(/[\w\s:]*\bPORT\b([\s]|$)/)) {
            var preCursor = block.cursor;
            beautifyPortGenericBlock(block, result, settings, indent, "PORT");
            var preLine = preCursor - 1;
            if (preLine >= 0) {
                var preL = block.lines[preLine];
                if (preL.regexIndexOf(/:\s+(COMPONENT|ENTITY)/) >= 0) {
                    indent--;
                }
            }
            continue;
        }
        if (input.regexStartsWith(/TYPE\s+\w+\s+IS\s+\(/)) {
            beautifyPortGenericBlock(block, result, settings, indent, "IS");
            continue;
        }
        if (input.regexStartsWith(/[\w\s:]*GENERIC([\s]|$)/)) {
            beautifyPortGenericBlock(block, result, settings, indent, "GENERIC");
            continue;
        }
        if (input.regexStartsWith(/[\w\s:]*PROCEDURE[\s\w]+\($/)) {
            beautifyPortGenericBlock(block, result, settings, indent, "PROCEDURE");
            if (block.lines[block.cursor].regexStartsWith(/.*\)[\s]*IS/)) {
                block.cursor++;
                beautify3(block, result, settings, indent + 1);
            }
            continue;
        }
        if (input.regexStartsWith(/FUNCTION[^\w]/)
            && input.regexIndexOf(/[^\w]RETURN[^\w]/) < 0) {
            beautifyPortGenericBlock(block, result, settings, indent, "FUNCTION");
            if (!block.lines[block.cursor].regexStartsWith(regexBlockEndsKeyWords)) {
                block.cursor++;
                beautify3(block, result, settings, indent + 1);
            }
            else {
                result[block.cursor].Indent++;
            }
            continue;
        }
        if (input.regexStartsWith(/IMPURE FUNCTION[^\w]/)
            && input.regexIndexOf(/[^\w]RETURN[^\w]/) < 0) {
            beautifyPortGenericBlock(block, result, settings, indent, "IMPURE FUNCTION");
            if (!block.lines[block.cursor].regexStartsWith(regexBlockEndsKeyWords)) {
                if (block.lines[block.cursor].regexStartsWith(regexBlockIndentedEndsKeyWords)) {
                    result[block.cursor].Indent++;
                }
                else {
                    block.cursor++;
                    beautify3(block, result, settings, indent + 1);
                }
            }
            else {
                result[block.cursor].Indent++;
            }
            continue;
        }
        result.push(new FormattedLine(input, indent));
        if (indent > 0
            && (input.regexStartsWith(regexBlockMidKeyWords)
                || (Mode != FormatMode.EndsWithSemicolon && input.regexStartsWith(regexMidKeyElse))
                || (Mode == FormatMode.CaseWhen && input.regexStartsWith(regexMidKeyWhen)))) {
            result[block.cursor].Indent--;
        }
        else if (indent > 0
            && (input.regexStartsWith(regexBlockEndsKeyWords))) {
            result[block.cursor].Indent--;
            return;
        }
        if (input.regexStartsWith(regexOneLineBlockKeyWords)) {
            continue;
        }
        if (input.regexStartsWith(regexFunctionMultiLineBlockKeyWords)
            || input.regexStartsWith(regexBlockStartsKeywords)) {
            block.cursor++;
            beautify3(block, result, settings, indent + 1);
        }
    }
    block.cursor--;
}

function ReserveSemicolonInKeywords(arr) {
    for (let i = 0; i < arr.length; i++) {
        if (arr[i].match(/FUNCTION|PROCEDURE/) != null) {
            arr[i] = arr[i].replace(/;/g, ILSemicolon);
        }
    }
}
function ApplyNoNewLineAfter(arr, noNewLineAfter) {
    if (noNewLineAfter == null) {
        return;
    }
    for (let i = 0; i < arr.length; i++) {
        noNewLineAfter.forEach(n => {
            let regex = new RegExp("(" + n.toUpperCase + ")[ a-z0-9]+[a-z0-9]+");
            if (arr[i].regexIndexOf(regex) >= 0) {
                arr[i] += "@@singleline";
            }
        });
    }
}

function RemoveAsserts(arr) {
    let need_semi = false;
    let inAssert = false;
    let n = 0;
    for (let i = 0; i < arr.length; i++) {
        let has_semi = arr[i].indexOf(";") >= 0;
        if (need_semi) {
            arr[i] = '';
        }
        n = arr[i].indexOf("ASSERT ");
        if (n >= 0) {
            inAssert = true;
            arr[i] = '';
        }
        if (!has_semi) {
            if (inAssert) {
                need_semi = true;
            }
        }
        else {
            need_semi = false;
        }
    }
}

function escapeText(arr, regex, escapedChar) {
    let quotes = [];
    let regexEpr = new RegExp(regex, "g");
    for (let i = 0; i < arr.length; i++) {
        let matches = arr[i].match(regexEpr);
        if (matches != null) {
            for (var j = 0; j < matches.length; j++) {
                var match = matches[j];
                arr[i] = arr[i].replace(match, escapedChar.repeat(match.length));
                quotes.push(match);
            }
        }
    }
    return quotes;
}
function RemoveExtraNewLines(input) {
    input = input.replace(/(?:\r\n|\r|\n)/g, '\r\n');
    input = input.replace(/ \r\n/g, '\r\n');
    input = input.replace(/\r\n\r\n\r\n/g, '\r\n');
    return input;
}
//# sourceMappingURL=VHDLFormatter.js.map

function noFormat() {
    let elements = [
        "remove_comments",
        "remove_lines",
        "remove_report",
        "check_alias",
        "sign_align_in",
        "sign_align_port",
        "sign_align_generic",
        "sign_align_function",
        "sign_align_procedure",
        "sign_align_all",
        "new_line_after",
        "use_space",
        "customise_indentation",
        "compress",
        "mix_letter",
        "cust_eol",
        "sign_align_mode",
        "keyword",
        "typename",
        "align_comments",
        "add_extraEOL"
    ];
    var isDisabled = getHTMLInputElement("no_format").checked;
}

function Compress(input) {
    input = input.replace(/\r\n/g, '');
    input = input.replace(/[\t ]+/g, ' ');
    input = input.replace(/[ ]?([&=:\-<>\+|])[ ]?/g, '$1');
    return input;
}

function alignAllSigns(alignAll) {
    if (alignAll) {
        getHTMLInputElement("sign_align_port").checked = false;
        getHTMLInputElement("sign_align_generic").checked = false;
        getHTMLInputElement("sign_align_procedure").checked = false;
        getHTMLInputElement("sign_align_function").checked = false;
        getHTMLInputElement("sign_align_mode_div").disabled = false;
    }
    else {
        getHTMLInputElement("sign_align_all").checked = false;
    }
    let isDisabled = !alignAll;
    changeStateOfElements(["sign_align_mode"], isDisabled);
    
}
//# sourceMappingURL=main.js.map

"use strict";

function counterDecode(inputId, outputId) {

}
function descriptiveCounter(input) {
    input = input.replace(/\\t/g, "	");
    input = input.replace(/\\r/g, "\r");
    input = input.replace(/\\n/g, "\n");
    var tokens = input.split("");
    var result = "";
    var repeatedCharCount = 0;
    for (var i = 0; i < tokens.length; i++) {
        var char = input.substr(i, 1);
        if (char == input.substr(i + 1, 1)) {
            repeatedCharCount++;
        }
        else {
            switch (char) {
                case " ":
                    char = "blankspace";
                    break;
                case "\t":
                    char = "tab";
                    break;
                case "\n":
                    char = "\\n";
                    break;
                case "\r":
                    char = "\\r";
                    break;
                default:
                    char = "'" + char + "'";
            }
            repeatedCharCount = repeatedCharCount > 8 ? 8 : repeatedCharCount;
            if (repeatedCharCount > 0) {
                char += "s";
            }
            result += getCountText(repeatedCharCount, char);
            repeatedCharCount = 0;
        }
    }
    if (result.length < 0) {
        switch (char) {
            case " ":
                char = "blankspace";
                break;
            case "\t":
                char = "tab";
        }
        repeatedCharCount = repeatedCharCount > 8 ? 8 : repeatedCharCount;
        result = getCountText(repeatedCharCount, char);
    }
    result = result.replace(/^ & /, "");
    return result;
}

function getCountText(count, char) {
    const dict = ["one", "two", "three", "four", "five", "six", "seven", "eight", "many"];
    const ampersand = " & ";
    return ampersand + dict[count] + " " + char;
}
//# sourceMappingURL=descriptiveCounter.js.map

const localStorageSettingKey = "settings";
        const localStorageNoFormatKey = "noFormat";

        function showHideSettings() {
            var settingsDiv = document.getElementById("settings_div");
            var control = document.getElementById("settings_control");
            if (settingsDiv.className.indexOf("hide") >= 0) {
                settingsDiv.className = settingsDiv.className.replace(/\s*hide/, "");
                control.innerHTML = "Show Less ▲";
            }
            else {
                settingsDiv.className += "hide";
                control.innerHTML = "Show More Settings ▼";
            }
        }

        function onLoad() {
            let global_endOfLine = navigator.platform === 'Win32' ? '\\r\\n' : '\\n';
            document.getElementById("cust_eol").value = global_endOfLine;
            var setting = loadSetting();
            if (setting == null) {
                return;
            }

            var beautifierSettings = setting.setting;
            document.getElementById("remove_comments").checked = beautifierSettings.RemoveComments;
            document.getElementById("remove_lines").checked = setting.removeLines;
            document.getElementById("remove_report").checked = beautifierSettings.RemoveAsserts;
            document.getElementById("check_alias").checked = beautifierSettings.CheckAlias;
            var alignSettings = beautifierSettings.SignAlignSettings;
            if (alignSettings != null) {
                var signAlignKeywords = alignSettings.keyWords;
                if (signAlignKeywords != null && signAlignKeywords.length > 0) {
                    document.getElementById("sign_align_port").checked = signAlignKeywords.indexOf("PORT") >= 0;
                    document.getElementById("sign_align_function").checked = signAlignKeywords.indexOf("FUNCTION") >= 0;
                    document.getElementById("sign_align_procedure").checked = signAlignKeywords.indexOf("PROCEDURE") >= 0;
                    document.getElementById("sign_align_generic").checked = signAlignKeywords.indexOf("GENERIC") >= 0;
                }
                document.getElementById("sign_align_all").checked = alignSettings.isAll;
                document.getElementById("sign_align_mode_div").elements.namedItem("sign_align_modecase").value = alignSettings.mode;
                document.getElementById("align_comments").checked = alignSettings.alignComments;
            }
            var newLineSettings = beautifierSettings.NewLineSettings;
            var newLineAfter = newLineSettings.newLineAfter;
            var noNewLineAfter = newLineSettings.noNewLineAfter;
            document.getElementById("new_line_after_port").elements.namedItem("new_line_after_portcase").value = decodeNewLineSetting(newLineAfter, noNewLineAfter, "port");
            document.getElementById("new_line_after_then").elements.namedItem("new_line_after_thencase").value = decodeNewLineSetting(newLineAfter, noNewLineAfter, "then");
            document.getElementById("new_line_after_semicolon").elements.namedItem("new_line_after_semicoloncase").value = decodeNewLineSetting(newLineAfter, noNewLineAfter, ";");
            document.getElementById("new_line_after_else").elements.namedItem("new_line_after_elsecase").value = decodeNewLineSetting(newLineAfter, noNewLineAfter, "else");
            document.getElementById("new_line_after_generic").elements.namedItem("new_line_after_genericcase").value = decodeNewLineSetting(newLineAfter, noNewLineAfter, "generic");
            document.getElementById("compress").checked = setting.compress;
            var indentation = beautifierSettings.Indentation;
            document.getElementById("use_space").checked = indentation != "\t";
            document.getElementById("add_extraEOL").checked = beautifierSettings.AddNewLine;
            document.getElementById("customise_indentation").value = indentation;
            document.getElementById("keyword_div").elements.namedItem("keywordcase").value = beautifierSettings.KeywordCase;
            document.getElementById("typename_div").elements.namedItem("typenamecase").value = beautifierSettings.TypeNameCase;
            document.getElementById("mix_letter").checked = setting.mixLetter;
            var eof = beautifierSettings.EndOfLine
            eof = eof.replace(/\r/g, "\\r");
            eof = eof.replace(/\n/g, "\\n");
            eof = eof.replace(/\t/g, "\\t");
            document.getElementById("cust_eol").value = eof;
            var noFormatBool = loadNoFormatSetting();
            if (noFormatBool) {
                document.getElementById("no_format").checked = true;
                noFormat();
            }
            counterDecode('customise_indentation', 'indent_s');
            counterDecode('cust_eol', 'eol_s');
        }

        function decodeNewLineSetting(hasNewLine, noNewLine, str) {
            if (hasNewLine.indexOf(str) >= 0) {
                return "NewLine";
            }
            if (noNewLine.indexOf(str) >= 0) {
                return "NoNewLine";
            }
            return "None";
        }

        //onLoad();
        var beautifierSettings;
        var compress;
        var no_format = false;
            var remove_lines = false;
            var mix_letter = false;
        function f(input) {


            

            var beautifierSettings = {
                "RemoveComments": false,
                "RemoveAsserts": false,
                "CheckAlias": false,
                "SignAlignSettings": {
                    "isRegional": false,
                    "isAll": false,
                    "mode": "",
                    "keyWords": [],
                    "alignComments": true
                },
                "KeywordCase": "LowerCase",
                "TypeNameCase": "LowerCase",
                "Indentation": "\t",
                "NewLineSettings": {
                    "newLineAfter": [
                        ";",
                        "then"
                    ],
                    "noNewLineAfter": []
                },
                "EndOfLine": "\n",
                "AddNewLine": true
            }
            var vhdlSettings = {
                "setting": {
                    "RemoveComments": false,
                    "RemoveAsserts": false,
                    "CheckAlias": false,
                    "SignAlignSettings": {
                        "isRegional": false,
                        "isAll": false,
                        "mode": "",
                        "keyWords": [],
                        "alignComments": true
                    },
                    "KeywordCase": "LowerCase",
                    "TypeNameCase": "LowerCase",
                    "Indentation": "\t",
                    "NewLineSettings": {
                        "newLineAfter": [
                            ";",
                            "then"
                        ],
                        "noNewLineAfter": []
                    },
                    "EndOfLine": "\n",
                    "AddNewLine": true
                },
                "removeLines": true,
                "compress": false,
                "mixLetter": false
            };
            return beautify(input, beautifierSettings).replace(/(\r\n)*[ \t]*\r\n/g, '\r\n');
        }

        var indentation = "\t";

        function CreateSettings() {
            var remove_comments = false;            
            var remove_report = false;
            var check_alias = false;
            var sign_align_port = false;
            var sign_align_function = false;
            var sign_align_procedure = false;
            var sign_align_generic = false;
            var sign_align_all = false;
            var align_comments = true;
            var sign_align_mode = false;
            var new_line_after_port = true;
            var new_line_after_then = true;
            var new_line_after_semicolon = true;
            var new_line_after_else = true;
            var new_line_after_generic = true;
            var use_space = false;
            var compress = false;
            var cust_indent = '\t';
            var addNewLine = true;
            var keywordcase = 'UpperCase';
            var typenamecase = 'UpperCase';
            var endOfLine = '\\n';
            endOfLine = endOfLine.replace(/\\r/g, "\r");
            endOfLine = endOfLine.replace(/\\n/g, "\n");
            if (compress) {
                remove_comments = true;
            }

            
            if (use_space) {
                cust_indent = cust_indent.replace(/\\t/, "	");
                indentation = cust_indent;
            }

            var newLineSettingsDict = {};
            newLineSettingsDict["generic"] = new_line_after_generic;
            newLineSettingsDict["generic map"] = new_line_after_generic;
            newLineSettingsDict["port"] = new_line_after_port;
            newLineSettingsDict["port map"] = new_line_after_port;
            newLineSettingsDict[";"] = new_line_after_semicolon;
            newLineSettingsDict["then"] = new_line_after_then;
            newLineSettingsDict["else"] = new_line_after_else;
            newLineSettings = ConstructNewLineSettings(newLineSettingsDict);
            var signAlignKeywords = [];
            if (sign_align_function) {
                signAlignKeywords.push("FUNCTION");
                signAlignKeywords.push("IMPURE FUNCTION");
            }
            if (sign_align_generic) {
                signAlignKeywords.push("GENERIC");
            }
            if (sign_align_port) {
                signAlignKeywords.push("PORT");
            }
            if (sign_align_procedure) {
                signAlignKeywords.push("PROCEDURE");
            }
            sign_align = signAlignKeywords.length > 0;
            let alignSettings = new signAlignSettings(sign_align, sign_align_all, sign_align_mode, signAlignKeywords, align_comments)

            beautifierSettings = new BeautifierSettings(remove_comments, remove_report, check_alias,
                alignSettings,
                keywordcase,
                typenamecase,
                indentation,
                newLineSettings,
                endOfLine,
                addNewLine);

            return [beautifierSettings, compress];
        }

        function outputSetting() {
            [beautifierSettings, compress] = CreateSettings();
            var json = JSON.stringify(beautifierSettings, null, 4);
            document.getElementById("vhdl").innerHTML = json;
        }

        var localStorage = {
            "settings": "{\"setting\":{\"RemoveComments\":false,\"RemoveAsserts\":false,\"CheckAlias\":false,\"SignAlignSettings\":{\"isRegional\":false,\"isAll\":false,\"mode\":\"\",\"keyWords\":[],\"alignComments\":false},\"KeywordCase\":\"UpperCase\",\"TypeNameCase\":\"UpperCase\",\"Indentation\":\"\\t\",\"NewLineSettings\":{\"newLineAfter\":[\";\",\"then\"],\"noNewLineAfter\":[]},\"EndOfLine\":\"\\n\",\"AddNewLine\":true},\"removeLines\":false,\"compress\":false,\"mixLetter\":false}",
            "noFormat": "false"
        }

        function saveSetting(setting) {
            var json = JSON.stringify(setting);
            json = json.replace(/\r/g, "\\r");
            json = json.replace(/\n/g, "\\n");
            json = json.replace(/\t/g, "\\t");
            localStorage.setItem(localStorageSettingKey, json);
        }
        
        function loadSetting() {
            var json = localStorage.getItem(localStorageSettingKey);
            if (json == null) {
                return null;
            }
            return JSON.parse(json);
        }

        function saveNoFormatSetting(no_format) {
            localStorage.setItem(localStorageNoFormatKey, no_format);
        }
        
        function loadNoFormatSetting() {
            return JSON.parse(localStorage.getItem(localStorageNoFormatKey));
        }

        class VhdlSettings {
            constructor(setting, removeLines, compress, mixLetter) {
                this.setting = setting;
                this.removeLines = removeLines;
                this.compress = compress;
                this.mixLetter = mixLetter;
            }
        }
