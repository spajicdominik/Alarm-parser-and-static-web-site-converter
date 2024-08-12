% Declare that this style file requires at least LaTeX version 2e.
\NeedsTeXFormat{LaTeX2e}

% Provide the name of your page, the date it was last updated, and a comment about what it's used for

% test whether main document provides options. 
\ProvidesClass{mathos}

% report
\LoadClass[a4paper, twoside,openright]{report}

% ostalo


% dimenzije
\usepackage[a4paper,top=3cm,bottom=3cm,left=3cm,right=3cm]{geometry} 
% velicina fonta
\usepackage[fontsize=12pt]{scrextend}

% vrsta fonta
\usepackage[sc]{mathpazo} % use mathpazo for math fonts
\usepackage{tgpagella} % but use tgpagella as main font

% jezik
\usepackage[croatian]{babel}
% jezik bibliografije
\usepackage[fixlanguage]{babelbib}
% ulazno kodiranje
\usepackage[utf8]{inputenc} 
% kodiranje znakova
\usepackage[T1]{fontenc}
% zamjenski tekst
\usepackage{lipsum}
% rotacije
\usepackage{rotating}
% promjena zaglavnja
\usepackage{fancyhdr}     

% oblik poglavlja
\usepackage{titlesec}

% matematicki paketi
\usepackage{amssymb}
\usepackage{amsmath}
\usepackage{amsthm}         

% slike
\usepackage{graphicx}
% boje
\usepackage[dvipsnames]{xcolor}         
% programski kod
\usepackage{listings}    
\usepackage{algorithm}
\usepackage[noend]{algpseudocode}
% URL poveznice
\usepackage{hyperref}     
% ???
\usepackage[normalem]{ulem}



% -----------------------------------------------------------------
% oblik poglavlja
\newcommand{\hsp}{\hspace{20pt}}
\titleformat{\chapter}[hang]{\Huge\bfseries}{\thechapter\hsp\textcolor{Blue}{|}\hsp}{0pt}{\Huge\bfseries}

% prijevod
\makeatletter
\renewcommand{\ALG@name}{Algoritam}
\makeatother


% definicija zaglavlja
\pagestyle{fancy}
\fancyhf{}
\lhead{\rightmark}
\rhead{\textbf{\thepage}}
\fancyfoot{}
\setlength{\headheight}{12.5pt}

% izbaci numeraciju na naslovnoj stranici
%\fancypagestyle{plain}{
  %\fancyfoot{}
  %\fancyhead{}
  %\renewcommand{\headrulewidth}{0pt}
%}

% stil koda
\lstdefinestyle{codeStyle}{
    % komentari
    commentstyle=\color{Green},
    % kljucne rijeci
    keywordstyle=\color{Blue},
    % stil brojeva
    numberstyle=\tiny\color{Blue},
    % boja stringova
    stringstyle=\color{Blue},
    % Dimensione e stile del testo
    basicstyle=\ttfamily\footnotesize,
    % newline solo ai whitespaces
    breakatwhitespace=false,     
    % newline si/no
    breaklines=true,                 
    % Posizione della caption, top/bottom 
    captionpos=b,                    
    % Mantiene gli spazi nel codice, utile per l'indentazione
    keepspaces=true,                 
    % Dove visualizzare i numeri di linea
    numbers=left,                    
    % Distanza tra i numeri di linea
    numbersep=5pt,                  
    % Mostra gli spazi bianchi o meno
    showspaces=false,                
    % Mostra gli spazi bianchi nelle stringhe
    showstringspaces=false,
    % Mostra i tab
    showtabs=false,
    % Dimensione dei tab
    tabsize=2
} \lstset{style=codeStyle}

% postavke koda
\lstdefinestyle{longBlock}{
    commentstyle=\color{teal},
    keywordstyle=\color{Magenta},
    numberstyle=\tiny\color{gray},
    stringstyle=\color{violet},
    basicstyle=\ttfamily\scriptsize,
    breakatwhitespace=false,         
    breaklines=true,                 
    captionpos=b,                    
    keepspaces=true,                 
    numbers=left,                    
    numbersep=5pt,                  
    showspaces=false,                
    showstringspaces=false,
    showtabs=false,                  
    tabsize=2
} \lstset{style=codeStyle}

% lineskip
\lstset{aboveskip=20pt,belowskip=20pt}

% Modifica dello stile dei riferimenti, con il testo in cyano
\hypersetup{
    colorlinks,
    linkcolor=Blue,
    citecolor=Blue
}

% teoremi, definicije
\newtheorem{definition}{Definicija}[section]
\newtheorem{theorem}{Teorem}[section]
\providecommand*\definitionautorefname{Definicija}
\providecommand*\theoremautorefname{Teorem}
\providecommand*{\listingautorefname}{Listing}
\providecommand*\lstnumberautorefname{Linea}

\raggedbottom

%%%%% ili ovo 
\newtheorem{defin}{Definicija}
\newtheorem{teorem}{Teorem}
\newtheorem{lema}{Lema}
\newtheorem{korolar}{Korolar}
\newtheorem{propozicija}{Propozicija} 
\newtheorem{primjer}{Primjer} 
\newtheorem{nap}{Napomena}
\renewcommand{\tablename}{Tablica}

%\newcommand{\cgs}[1]{{\textcolor{brown}[\textcolor{red}{\bf{GS: }}{ \textcolor{brown}{#1]}}}}             
%\newcommand{\cmc}[1]{{\textcolor{blue}[\textcolor{magenta}{\bf{MC: }}{ \textcolor{blue}{#1]}}}} 

