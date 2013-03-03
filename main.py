import pysces
from igraph import *

class MyGraph:
    """ Class implements visualisation pysces model """
    def __init__(self, file_name):
        self.sbml_file_name = file_name
        self.cols = []
        self.rows = []
        self.values = []
        self.__load_sbml__()
        self.__parse__()
        self.__add_edges__()
        self.set_visual_style(0)
        
    def __load_sbml__(self):
        psc_file_name = self.sbml_file_name + ".psc"
        pysces.interface.convertSBML2PSC(self.sbml_file_name)
        self.pyscesModel = pysces.model(psc_file_name)
        self.pyscesModel.doLoad()
        
    def __get_labels_name__(self):
        return self.cols + self.rows
        
    def __add_edges__(self):
        cols_len = len(self.cols)
        rows_len = len(self.rows)
        vertex_count = cols_len + rows_len
        self.igraph = Graph(vertex_count)

        for row in range(rows_len):
          for col in range(cols_len):
              if (int(float(self.values[row][col])) <> 0):
                 self.igraph.add_edges((col , row + cols_len));
        
    def __parse__(self):
        result_file_name = self.sbml_file_name + '_results.txt'
        rFile = file(result_file_name,'w')
        self.pyscesModel.showN(rFile)
        rFile.close()
        rFile = open(result_file_name, 'r')
        for n in xrange(3):
            rFile.readline() #empty lines and title
        self.cols = rFile.readline().split() # cols
        finish = 0
        for line in rFile.readlines():
            res = line.split()
            if (len(res) > 0 and not finish):
                self.rows.append(res[0])
                self.values.append(res[1:])
            else:
                finish = 1
        rFile.close()
        
    def plot_graph(self, filename = None):
        """ filename: png or pdf extension """
        plot(self.igraph, filename, **self.visual_style)
        
    def set_layout(self, layout_name):
        """ layouts:
        kamada_kawai, circle, drl, fruchterman_reingold,
        grid_fruchterman_reingold, lgl, random, reingold_tilford,
        reingold_tilford_circular
        """
        self.layout = self.visual_style["layout"] = layout_name
        
    def set_visual_style(self, state):
        self.visual_style = {}
        self.visual_style["layout"] = "kamada_kawai"
        if state:
            self.visual_style["autocurve"] = 1
            self.visual_style["vertex_size"] = 46
            self.visual_style["vertex_color"] = '#00aaff'
            self.visual_style["vertex_label_size"] = 10
            self.visual_style["vertex_label"] = self.__get_labels_name__()
            self.visual_style["edge_width"] = 2
            self.visual_style["bbox"] = (1024, 1024)
            self.visual_style["margin"] = 30
    
    def print_degree_distribution(self, histogram = None):
        degrees = self.igraph.degree()
        if histogram:
            h = Histogram(1)
            h << degrees
            print h
        else:
            print "Vertex count: %s" % self.igraph.vcount()
            print "-----------------"
            degrees_count = []
            [degrees_count.append((i,degrees.count(i))) for i in set(degrees)]
            for d in degrees_count:
                print "degree %s: %s" % (d[0], d[1])
                
    def print_stats(self):
        """ Print all statistics about graph"""
        print "Statistics graph %s" % self.sbml_file_name
        print "-----------------"
        print "Density: %s" % self.igraph.density()
        print "-----------------"
        print "Edges count: %s" % self.igraph.ecount()
        self.print_degree_distribution()
        print "-----------------"
        print "Diameter: %s" % self.igraph.diameter()
        print "-----------------"
        print "Average path lenght: %s" % self.igraph.average_path_length()
        print "-----------------"
        print "Path lenght histogram"
        print self.igraph.path_length_hist()


myG = MyGraph("BIOMD0000000042.xml");
myG.set_visual_style(1)

#print stats
print myG.print_stats()

#plot graph and save it in pysces working directory
myG.plot_graph("result.png")
