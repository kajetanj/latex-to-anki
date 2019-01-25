# LaTeX to Anki

Front template:

`[latex]{{Front}}[/latex]`

Styling:

```css
.card {
    font-family: arial;
    font-size: 10px;
    text-align: center;
    color: black;
    background-color: white;
}

img {
    width: auto;
    height: auto;
    max-height:1000px;
}
```

Back template:

```
{{FrontSide}}
  
<hr id=answer>
  
[latex]{{Back}}[/latex]
```

LaTeX header:

```
\documentclass[10pt]{article}

% your language
\usepackage{polski}

\usepackage{amsmath}
\usepackage{amssymb}
\usepackage{amsfonts}
\usepackage{dsfont}
\usepackage{mathabx}

% your packages
% your definitions

\usepackage[paperwidth=5in, paperheight=100in]{geometry}
\pagestyle{empty}
\setlength{\parindent}{0in}
\begin{document} 
```