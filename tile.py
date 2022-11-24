class Tile:
      def __init__(self, type, position, name):
        self.type = type #Unclicked, Blank, Flag, 1, 2, 3, 4, 5, Edge
        self.position = position
        self.neighbors = []
        self.name = name
        self.blanks = []
        self.flags = []

      def print_neighbors(self):
        try:
          print("{} | {} | {}".format(self.neighbors[0].type, self.neighbors[1].type, self.neighbors[2].type))
          print("{} | {} | {}".format(self.neighbors[3].type, self.name, self.neighbors[4].type))
          print("{} | {} | {}".format(self.neighbors[5].type, self.neighbors[6].type, self.neighbors[7].type))
        except IndexError:
          print("Neighbors not set correctly.")

      def neighbor_blanks(self):
        blanks=[]
        for i in self.neighbors:
          if i.type == "Unclicked":
            blanks.append(i)
        self.blanks = blanks
        return blanks

      def neighbor_flags(self):
        flags=[]
        for i in self.neighbors:
          if i.type == "Flag":
            flags.append(i)
        self.flags = flags
        return flags

