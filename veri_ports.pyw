#!/usr/bin/env python


#########################################################
# This script can convert Verilog module instantiation code
# to port declaration code and vice versa
# Some Verilog editing automation added too.
#########################################################

# detect your Python interpreter version (2 or 3)
from sys import version
if version.split()[0][0] == '2':
    import Tkinter as tk
else:
    import tkinter as tk


import re


root = tk.Tk(
    className="Declare ports for instantiated Verilog modules and vice versa")

# vars
v = tk.StringVar()
v.set("1")

# widgets
fr = tk.Frame()
btnClear = tk.Button(fr, text="Clear")
btnCopy = tk.Button(fr, text="Copy")

fr_sep_3 = tk.Frame(fr, width=20)

btnInstToMod = tk.Button(fr, text="inst. -> ports")
btnModToInst = tk.Button(fr, text="ports -> inst.")
btnRevertDir = tk.Button(fr, text="revert")
btnMakeLocal = tk.Button(fr, text="make local")

fr_sep = tk.Frame(fr, width=20)

fr1 = tk.Frame(fr)
btnWire = tk.Button(fr1, text="wire")
btnReg = tk.Button(fr1, text="reg")

fr_sep_2 = tk.Frame(fr, width=20)

fr3 = tk.Frame(fr)
btnBus = tk.Button(fr3, text="bus")
entry = tk.Entry(fr3, textvariable=v, width=4)
lbl = tk.Label(fr3, text="bit")
btnSingle = tk.Button(fr3, text="single")

fr2 = tk.Frame()
txt = tk.Text(fr2, wrap=tk.NONE)
scroll_x = tk.Scrollbar(fr2, orient=tk.HORIZONTAL)
scroll_y = tk.Scrollbar(fr2)


# pack
fr.pack()
btnClear.pack(side=tk.LEFT)
btnCopy.pack(side=tk.LEFT)

fr_sep_3.pack(side=tk.LEFT)

btnInstToMod.pack(side=tk.LEFT)
btnModToInst.pack(side=tk.LEFT)
btnRevertDir.pack(side=tk.LEFT)
btnMakeLocal.pack(side=tk.LEFT)

fr_sep.pack(side=tk.LEFT)

fr1.pack(side=tk.LEFT)
btnWire.pack(side=tk.LEFT)
btnReg.pack(side=tk.LEFT)

fr_sep_2.pack(side=tk.LEFT)

fr3.pack(side=tk.LEFT)
btnBus.pack(side=tk.LEFT)
entry.pack(side=tk.LEFT)
lbl.pack(side=tk.LEFT)
btnSingle.pack(side=tk.LEFT)


fr2.pack(fill=tk.BOTH, expand=1)
fr2.rowconfigure(0, weight=1)
fr2.columnconfigure(0, weight=1)
txt.grid(row=0, column=0, sticky=tk.N + tk.S + tk.E + tk.W)
scroll_x.grid(row=1, column=0, sticky=tk.E + tk.W)
scroll_y.grid(row=0, column=1, sticky=tk.N + tk.S)

# functions


def InstToMod(event):
    lines = txt.get('0.0', tk.END).split("\n")

    templ = re.compile(r"""^ \s*
                       \. (?P<slot>\w+) \s* \( \s* (?P<port>\w+) \s* \)""", re.X)
    #.*? (?P<dir>(\binput\b)|(\boutput\b)|(\binout\b))?
    #.*? (?P<typ>(\bwire\b)|(\breg\b))? .*?
    #(?P<bus>\[\d+:\d+\])? .*?
    #$""",re.X)
    lines2 = []
    for l in lines:
        m = templ.match(l)
        if m and l:
            s = ""
            m1 = re.search(r"(?P<dir>(\binput\b)|(\boutput\b)|(\binout\b))", l)
            if m1:
                s = s + m1.group("dir") + " "
            else:
                s = s + "input "
            m1 = re.search(r"(?P<typ>(\bwire\b)|(\breg\b))", l)
            if m1:
                s = s + m1.group("typ") + " "
            else:
                s = s + "wire "
            m1 = re.search(r"(?P<bus>\[\s*\d+\s*:\s*\d+\s*\])", l)
            if m1:
                s = s + m1.group("bus") + " "
            if m.group("port"):
                s = s + m.group("port")
            lines2.append(s)

    if lines2:
        txt.delete(1.0, tk.END)
        for l in lines2[:-1]:
            txt.insert(tk.END, l + ",\n")
        txt.insert(tk.END, lines2[-1] + "\n")


def ModToInst(event):
    lines = txt.get('0.0', tk.END).split("\n")
    templ = re.compile(r"""^ \s*
                       (?P<dir>(\binput\b)|(\boutput\b)|(\binout\b))? \s*
                       (?P<typ>(\breg\b)|(\bwire\b))? \s*
                       (?P<bus>\[\s* \d+ \s* : \s* \d+ \s*\])? \s*
                       (?P<port>\w+)""", re.X)
    lines2 = []
    for l in lines:
        m = templ.match(l)
        s = "."
        if m and l:
            if m.group("port"):
                s = s + m.group("port") + "(" + m.group("port") + "),"
            s = s + " " * 10 + "// "
            if m.group("dir"):
                s = s + m.group("dir")
            s = s + " "
            if m.group("typ"):
                s = s + m.group("typ")
            else:
                s = s + "wire"
            if m.group("bus"):
                s = s + " " + m.group("bus")
            s = s + " " + m.group("port")
            lines2.append(s)

    if lines2:
        txt.delete(1.0, tk.END)
        for l in lines2:
            txt.insert(tk.END, l + "\n")


def clear(event):
    txt.delete(1.0, tk.END)


def copy(event):
    root.clipboard_clear()
    root.clipboard_append(txt.get('0.0', tk.END))


def process_text(fn):
    try:
        i = txt.index("sel.first")
        j = txt.index("sel.last")
        S = txt.get(i + " linestart", j + " lineend")
        S = fn(S)
        txt.delete(i + " linestart", j + " lineend")
        txt.insert(i + " linestart", S)
    finally:
        i = txt.index("insert")
        S = txt.get(i + " linestart", i + " lineend")
        S = fn(S)
        txt.delete(i + " linestart", i + " lineend")
        txt.insert(i, S)


def revert(event):
    def repl(S):
        S = S.replace("input", "INPUT")
        S = S.replace("output", "input")
        S = S.replace("INPUT", "output")
        return S
    process_text(repl)


def make_local(event):
    def repl(S):
        S = S.replace("input ", "")
        S = S.replace("output ", "")
        return S
    process_text(repl)


def make_wire(event):
    def repl(S):
        if "wire" in S:
            pass
        elif "reg" in S:
            S = S.replace("reg", "wire")
        elif "input" in S:
            S = S.replace("input", "input wire")
        elif "output" in S:
            S = S.replace("output", "output wire")
        else:
            S = "wire " + S

        return S
    process_text(repl)


def make_reg(event):
    def repl(S):
        if "reg" in S:
            pass
        elif "wire" in S:
            S = S.replace("wire", "reg")
        elif "input" in S:
            S = S.replace("input", "input reg")
        elif "output" in S:
            S = S.replace("output", "output reg")
        else:
            S = "reg " + S
        return S
    process_text(repl)


def make_bus(event):
    w = int(v.get())
    i = str(w - 1)

    def repl(S):
        if "[" not in S:
            if "wire" in S:
                S = S.replace("wire", "wire " + "[" + i + ":0]")
            elif "reg" in S:
                S = S.replace("reg", "reg " + "[" + i + ":0]")
        else:
            m = re.search(r"(?P<bus>\[\s*(?P<w>\d+)\s*\:\s*\d+\s*\])", S)
            if m:
                if m.group("w") != i:
                    S = S.replace(m.group("bus"), "[" + i + ":0]")
        return S
    process_text(repl)


def make_single(event):
    def repl(S):
        if "[" in S:
            m = re.search(r"(?P<bus>\[\s*\d+\s*\:\s*\d+\s*\]\s)", S)
            if m:
                S = S.replace(m.group("bus"), "")
        return S
    process_text(repl)

# bind
btnInstToMod.bind("<Button-1>", InstToMod)
btnModToInst.bind("<Button-1>", ModToInst)
btnClear.bind("<Button-1>", clear)
btnCopy.bind("<Button-1>", copy)

btnRevertDir.bind("<Button-1>", revert)
btnMakeLocal.bind("<Button-1>", make_local)
btnWire.bind("<Button-1>", make_wire)
btnReg.bind("<Button-1>", make_reg)
btnBus.bind("<Button-1>", make_bus)
btnSingle.bind("<Button-1>", make_single)

# scrollbars binding to Text
txt.config(xscrollcommand=scroll_x.set)
scroll_x.config(command=txt.xview)

txt.config(yscrollcommand=scroll_y.set)
scroll_y.config(command=txt.yview)


root.mainloop()
