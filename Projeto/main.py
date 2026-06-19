import sys
import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

BACKEND_DIR = os.path.join(os.path.dirname(__file__), "backend")
sys.path.insert(0, os.path.abspath(BACKEND_DIR))

import roteamento_coloração_redes
import alocacao_canais_wifi

# ──────────────────────────────────────────────
#  ESTILOS
# ──────────────────────────────────────────────

BG        = "#f5f5f5"
CARD_BG   = "#ffffff"
ACCENT    = "#1a56db"
TEXT      = "#1a1a1a"
MUTED     = "#6b7280"
SUCCESS   = "#166534"
SUCCESS_BG = "#f0fdf4"
ERR       = "#991b1b"
ERR_BG    = "#fee2e2"
BORDER    = "#d1d5db"

FONT_MONO = ("Courier New", 10)
FONT_UI   = ("Segoe UI", 10)


class SolverApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Grafos")
        self.configure(bg=BG)
        self.resizable(True, True)
        self.minsize(740, 580)

        self.p1_path    = tk.StringVar(value="Nenhum arquivo carregado")
        self.p2_path    = tk.StringVar(value="Nenhum arquivo carregado")
        self.p1_content = ""
        self.p2_content = ""

        self._build_header()
        self._build_notebook()
        self._build_statusbar()

        self.update_idletasks()
        w, h = 860, 640
        x = (self.winfo_screenwidth()  - w) // 2
        y = (self.winfo_screenheight() - h) // 2
        self.geometry(f"{w}x{h}+{x}+{y}")


    def _build_header(self):
        hdr = tk.Frame(self, bg=ACCENT, pady=12)
        hdr.pack(fill="x")
        tk.Label(
        ).pack()
        tk.Label(
        ).pack()


    def _build_notebook(self):
        style = ttk.Style(self)
        style.theme_use("default")
        style.configure("TNotebook", background=BG, borderwidth=0)
        style.configure("TNotebook.Tab", font=FONT_UI, padding=[18, 6],
                        background="#e5e7eb", foreground=MUTED)
        style.map("TNotebook.Tab",
                  background=[("selected", CARD_BG)],
                  foreground=[("selected", ACCENT)])

        nb = ttk.Notebook(self)
        nb.pack(fill="both", expand=True, padx=16, pady=(12, 0))

        self.tab1 = tk.Frame(nb, bg=CARD_BG)
        self.tab2 = tk.Frame(nb, bg=CARD_BG)
        nb.add(self.tab1, text="  Parte 1 — Roteamento  ")
        nb.add(self.tab2, text="  Parte 2 — Coloração Wi-Fi  ")

        self._build_tab(
            parent=self.tab1, part=1,
            description=(
                "Grafo direcionado com pesos. O algoritmo é escolhido automaticamente:\n"
                "Dijkstra (sem pesos negativos) ou Bellman-Ford (com pesos negativos)."
            ),
            file_var=self.p1_path,
            load_cmd=self._load_p1,
            solve_cmd=self._solve_p1,
            out_attr="p1_out",
            status_attr="p1_status",
        )
        self._build_tab(
            parent=self.tab2, part=2,
            description=(
                "Grafo não-direcionado sem pesos. Coloração mínima via DSatur:\n"
                "prioriza vértices com maior grau de saturação nos vizinhos."
            ),
            file_var=self.p2_path,
            load_cmd=self._load_p2,
            solve_cmd=self._solve_p2,
            out_attr="p2_out",
            status_attr="p2_status",
        )

    def _build_tab(self, parent, part, description, file_var,
                   load_cmd, solve_cmd, out_attr, status_attr):

        tk.Label(
            parent, text=description, font=("Segoe UI", 9),
            bg=CARD_BG, fg=MUTED, justify="left"
        ).pack(anchor="w", padx=20, pady=(16, 4))

        ttk.Separator(parent, orient="horizontal").pack(fill="x", padx=20, pady=2)

        row_file = tk.Frame(parent, bg=CARD_BG)
        row_file.pack(fill="x", padx=20, pady=10)

        tk.Button(
            row_file, text="📂  Carregar arquivo", command=load_cmd,
            font=FONT_UI, bg="#e0e7ff", fg=ACCENT, activebackground="#c7d2fe",
            relief="flat", cursor="hand2", padx=12, pady=6
        ).pack(side="left")

        tk.Label(
            row_file, textvariable=file_var, font=("Segoe UI", 9),
            bg=CARD_BG, fg=MUTED, wraplength=520, justify="left"
        ).pack(side="left", padx=12)

        tk.Label(
            parent, text="Conteúdo do arquivo:",
            font=("Segoe UI", 9, "bold"), bg=CARD_BG, fg=TEXT
        ).pack(anchor="w", padx=20)

        frame_prev = tk.Frame(parent, bg=BORDER, padx=1, pady=1)
        frame_prev.pack(fill="x", padx=20, pady=(3, 10))

        prev = tk.Text(
            frame_prev, height=6, font=FONT_MONO, bg="#f9fafb",
            fg=TEXT, relief="flat", wrap="none", state="disabled"
        )
        sb_v = ttk.Scrollbar(frame_prev, orient="vertical",   command=prev.yview)
        sb_h = ttk.Scrollbar(frame_prev, orient="horizontal", command=prev.xview)
        prev.configure(yscrollcommand=sb_v.set, xscrollcommand=sb_h.set)
        sb_v.pack(side="right",  fill="y")
        sb_h.pack(side="bottom", fill="x")
        prev.pack(fill="both", expand=True)
        setattr(self, f"p{part}_preview", prev)

        row_btn = tk.Frame(parent, bg=CARD_BG)
        row_btn.pack(fill="x", padx=20, pady=4)

        tk.Button(
            row_btn, text="Resolver", command=solve_cmd,
            font=("Segoe UI", 10, "bold"), bg=ACCENT, fg="white",
            activebackground="#1e40af", relief="flat", cursor="hand2",
            padx=16, pady=7
        ).pack(side="left")

        status = tk.Label(row_btn, text="", font=("Segoe UI", 9), bg=CARD_BG, fg=MUTED)
        status.pack(side="left", padx=12)
        setattr(self, status_attr, status)

        ttk.Separator(parent, orient="horizontal").pack(fill="x", padx=20, pady=(8, 2))

        row_out_hdr = tk.Frame(parent, bg=CARD_BG)
        row_out_hdr.pack(fill="x", padx=20, pady=(4, 2))

        tk.Label(
            row_out_hdr, text="Resultado:",
            font=("Segoe UI", 9, "bold"), bg=CARD_BG, fg=TEXT
        ).pack(side="left")

        frame_out = tk.Frame(parent, bg=BORDER, padx=1, pady=1)
        frame_out.pack(fill="both", expand=True, padx=20, pady=(2, 16))

        out = tk.Text(
            frame_out, font=FONT_MONO, bg=SUCCESS_BG, fg=SUCCESS,
            relief="flat", wrap="word", state="disabled"
        )
        out_sb = ttk.Scrollbar(frame_out, orient="vertical", command=out.yview)
        out.configure(yscrollcommand=out_sb.set)
        out_sb.pack(side="right", fill="y")
        out.pack(fill="both", expand=True)
        setattr(self, out_attr, out)


    def _build_statusbar(self):
        bar = tk.Frame(self, bg="#e5e7eb", pady=4)
        bar.pack(fill="x", side="bottom")
        tk.Label(
            bar, text="Python 3  ·  Sem dependências externas",
            font=("Segoe UI", 8), bg="#e5e7eb", fg=MUTED
        ).pack(side="right", padx=12)

    def _set_preview(self, part, content):
        w = getattr(self, f"p{part}_preview")
        w.config(state="normal")
        w.delete("1.0", "end")
        w.insert("1.0", content)
        w.config(state="disabled")

    def _set_output(self, attr, text, error=False):
        w = getattr(self, attr)
        w.config(
            state="normal",
            bg=ERR_BG if error else SUCCESS_BG,
            fg=ERR    if error else SUCCESS,
        )
        w.delete("1.0", "end")
        w.insert("1.0", text)
        w.config(state="disabled")

    def _set_status(self, attr, text, error=False):
        getattr(self, attr).config(text=text, fg=ERR if error else SUCCESS)

    def _copy(self, attr):
        content = getattr(self, attr).get("1.0", "end").strip()
        if content:
            self.clipboard_clear()
            self.clipboard_append(content)
            messagebox.showinfo("Copiado", "Resultado copiado para a área de transferência.")

    def _save(self, attr):
        content = getattr(self, attr).get("1.0", "end").strip()
        if not content:
            messagebox.showwarning("Aviso", "Nenhum resultado para salvar.")
            return
        path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Arquivo de texto", "*.txt"), ("Todos", "*.*")],
            title="Salvar resultado",
        )
        if path:
            with open(path, "w", encoding="utf-8") as f:
                f.write(content + "\n")
            messagebox.showinfo("Salvo", f"Arquivo salvo em:\n{path}")

    def _load_file(self, part, file_var):
        path = filedialog.askopenfilename(
            title=f"Selecione o arquivo da Parte {part}",
            filetypes=[("Arquivos de texto", "*.txt"), ("Todos", "*.*")],
        )
        if not path:
            return None
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        file_var.set(os.path.basename(path))
        self._set_preview(part, content)
        return content

    def _load_p1(self):
        content = self._load_file(1, self.p1_path)
        if content is not None:
            self.p1_content = content
            self._set_output("p1_out", "")
            self._set_status("p1_status", "Arquivo carregado. Clique em Resolver.")

    def _load_p2(self):
        content = self._load_file(2, self.p2_path)
        if content is not None:
            self.p2_content = content
            self._set_output("p2_out", "")
            self._set_status("p2_status", "Arquivo carregado. Clique em Resolver.")


    def _solve_p1(self):
        if not self.p1_content:
            messagebox.showwarning("Aviso", "Carregue um arquivo primeiro.")
            return
        try:
            result = roteamento_coloração_redes.solve_from_text(self.p1_content)
            self._set_output("p1_out", result)
            self._set_status("p1_status", "Resolvido com sucesso.")
        except Exception as e:
            self._set_output("p1_out", f"ERRO: {e}", error=True)
            self._set_status("p1_status", f"Erro: {e}", error=True)

    def _solve_p2(self):
        if not self.p2_content:
            messagebox.showwarning("Aviso", "Carregue um arquivo primeiro.")
            return
        try:
            result = alocacao_canais_wifi.solve_from_text(self.p2_content)
            self._set_output("p2_out", result)
            self._set_status("p2_status", "Resolvido com sucesso.")
        except Exception as e:
            self._set_output("p2_out", f"ERRO: {e}", error=True)
            self._set_status("p2_status", f"Erro: {e}", error=True)



if __name__ == "__main__":
    app = SolverApp()
    app.mainloop()
