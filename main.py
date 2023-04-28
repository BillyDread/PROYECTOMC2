import tkinter as tk
from tkinter import ttk
import networkx as nx
import matplotlib.pyplot as plt

if __name__ == '__main__':

    class GraphEditor(tk.Frame):
        def __init__(self, master):
            super().__init__(master)
            self.master = master
            self.vertices = set()
            self.edges = []
            self.create_widgets()

        def create_widgets(self):
            self.vertex_var = tk.StringVar()
            self.edge_var = tk.StringVar()
            self.weight_var = tk.StringVar()

            tk.Label(self, text="Agregar vértice").grid(row=0, column=0)
            self.vertex_entry = tk.Entry(self, textvariable=self.vertex_var)
            self.vertex_entry.grid(row=0, column=1)

            tk.Label(self, text="Agregar arista (formato A->B)").grid(row=1, column=0)
            self.edge_entry = tk.Entry(self, textvariable=self.edge_var)
            self.edge_entry.grid(row=1, column=1)

            tk.Label(self, text="Peso de la arista").grid(row=2, column=0)
            self.weight_entry = tk.Entry(self, textvariable=self.weight_var)
            self.weight_entry.grid(row=2, column=1)

            self.add_button = ttk.Button(self, text="Agregar", command=self.add_graph_element)
            self.add_button.grid(row=3, column=0, columnspan=2)

            self.generate_button = ttk.Button(self, text="Generar gráfico", command=self.generate_graph)
            self.generate_button.grid(row=4, column=0, columnspan=2)

            self.clear_button = ttk.Button(self, text="Limpiar", command=self.clear_text)
            self.clear_button.grid(row=9, column=0, columnspan=2)

            self.remove_edge_button = ttk.Button(self, text="Eliminar última arista", command=self.remove_last_edge)
            self.remove_edge_button.grid(row=10, column=0, columnspan=2)

            self.remove_vertex_button = ttk.Button(self, text="Eliminar último vértice", command=self.remove_last_vertex)
            self.remove_vertex_button.grid(row=11, column=0, columnspan=2)


            tk.Label(self, text="Vértices ingresados").grid(row=5, column=0)
            self.vertex_listbox = tk.Listbox(self, height=5)
            self.vertex_listbox.grid(row=6, column=0, columnspan=2)

            tk.Label(self, text="Aristas ingresadas").grid(row=7, column=0)
            self.edge_listbox = tk.Listbox(self, height=5)
            self.edge_listbox.grid(row=8, column=0, columnspan=2)

        def add_graph_element(self):
            if self.vertex_var.get():
                self.vertices.add(self.vertex_var.get())
                self.vertex_listbox.insert(tk.END, self.vertex_var.get())
                self.vertex_var.set('')
            if self.edge_var.get() and self.weight_var.get():
                self.edges.append((self.edge_var.get(), int(self.weight_var.get())))
                self.edge_listbox.insert(tk.END, f"{self.edge_var.get()} ({self.weight_var.get()})")
                self.edge_var.set('')
                self.weight_var.set('')

        def generate_graph(self):
            G = nx.Graph()
            G.add_nodes_from(self.vertices)
            G.add_weighted_edges_from([(x[0].split('->')[0], x[0].split('->')[1], x[1]) for x in self.edges])

            pos = nx.spring_layout(G)
            edge_labels = {(edge[0], edge[1]): str(edge[2]['weight']) for edge in G.edges(data=True)}

            nx.draw_networkx_nodes(G, pos, node_color='lightblue', node_size=500)
            nx.draw_networkx_edges(G, pos, edge_color='gray')
            nx.draw_networkx_labels(G, pos, font_weight='bold')
            nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red')

            plt.show()


        def clear_text(self):
            self.vertex_var.set('')
            self.edge_var.set('')
            self.weight_var.set('')
            self.vertex_listbox.delete(0, tk.END)
            self.edge_listbox.delete(0, tk.END)

        def remove_last_edge(self):
            if len(self.edges) > 0:
                self.edge_listbox.delete(tk.END)
                self.edges.pop()

        def remove_last_vertex(self):
            if len(self.vertices) > 0:
                self.vertex_listbox.delete(tk.END)
                vertex = self.vertices.pop()
                self.edges = [edge for edge in self.edges if vertex not in edge[0].split('->')]


    root = tk.Tk()
    editor = GraphEditor(root)
    editor.pack()
    root.mainloop()
