import BasicMath as BM
import math
import sys

class Matrix:
    def __init__(self, map) -> None:
        #map: list[[a, b, c], [d, e, f], [g, h, i]]
        #var security
        if type(map) != list:
            sys.exit("Matrix: incorrect structure")
        row_id = 0
        is_zero = True
        for row in map:
            if type(row) != list:
                sys.exit("Matrix: incorrect structure")
            if row_id > 0 and len(map[row_id]) != len(map[row_id - 1]):
                sys.exit("Matrix: no consistent dimension")
            for number in row:
                if type(number) not in [int, float]:
                    sys.exit("Matrix: only numbers permitted")
                elif number != 0:
                    is_zero = False
            row_id += 1
        
        #attributes
        self.map = map
        self.width = len(map[0])
        self.height = len(map)
        self.size = (self.width, self.height)
        self.zero = is_zero

        #bonus facts
        if self.width == self.height:
            self.square = self.width
        else:
            self.square = False
        if self.square == 1:
            self.number = self.map[0][0]
        else:
            self.number = False
        self.vector = self.width == 1 #Spaltenvektor
        self.point = self.height == 1 #Zeilenvektor

    def add_line(self, matrix, vertical):
        #var security
        if type(matrix) != Matrix or type(vertical) != bool:
            sys.exit("Matrix.add_line: incorrect data type")
        if vertical:
            if matrix.width != self.width:
                sys.exit("Matrix.add_line: vertical - sizes do not match")
        else:
            if matrix.height != self.height:
                sys.exit("Matrix.add_line: not vertical - sizes do not match")
        
        if vertical:
            output = self.map
            for line in matrix.map:
                output.append(line)
        else:
            output = []
            for i, line in enumerate(self.map):
                output.append(line + matrix.map[i])

        return Matrix(output)

    def del_line(self, index, vertical):
        #var security
        if type(index) != int or type(vertical) != bool:
            sys.exit("Matrix.del_line: incorrect data type")
        if vertical:
            if not 0 < index <= self.width:
                sys.exit("Matrix.del_line: index out of range")
        else:
            if not 0 < index <= self.height:
                sys.exit("Matrix.del_line: index out of range")
        
        if vertical:
            output = []
            width_i, height_i = 0, 0
            while height_i < self.height:
                new_row = []
                while width_i < self.width:
                    if width_i != index - 1:
                        new_row.append(self.map[height_i][width_i])
                    width_i += 1
                output.append(new_row)
                width_i = 0
                height_i += 1
        else:
            output = []
            width_i, height_i = 0, 0
            while height_i < self.height:
                if height_i != index - 1:
                    new_row = []
                    while width_i < self.width:
                        new_row.append(self.map[height_i][width_i])
                        width_i += 1
                    output.append(new_row)
                    width_i = 0
                height_i += 1
        return Matrix(output)
    
    def __str__(self):
        output = ""
        for row in self.map:
            for num in row:
                output = output + str(num) + ", "
            output = output + "\n"
        
        return output
    
    def __round__(self, rounder=2, rounder_method="normal"):
        output = []
        for row in self.map:
            new_row = []
            for number in row:
                new_row.append(BM.c_round(number, rounder, rounder_method))
            
            output.append(new_row)
        
        return Matrix(output)
    
    def __add__(self, matrix):
        #var security
        if type(matrix) != Matrix:
            sys.exit("Matrix.add: incorrect data type")
        elif (self.width, self.height) != (matrix.width, matrix.height):
            sys.exit("Matrix.add: sizes do not match")
        
        output = []
        width_i, height_i = 0, 0
        while height_i < self.height:
            new_row = []
            while width_i < self.width:
                new_row.append(self.map[height_i][width_i] + matrix.map[height_i][width_i])
                width_i += 1
            output.append(new_row)
            width_i = 0
            height_i += 1
        return Matrix(output)

    def __sub__(self, matrix):
        #var security
        if type(matrix) != Matrix:
            sys.exit("Matrix.subtract: incorrect data type")

        return self + matrix * (-1)

    def __pow__(self, exponent):
        #var security
        if type(exponent) != int or exponent < 0:
            sys.exit("Matrix.power: incorrect data type")
        
        #cases
        if exponent == 0:
            sys.exit("Matrix.power: identity matrix not defined")
        elif exponent == 1:
            return self
        
        copy = self
        for i in range(exponent - 1):
            copy = copy * copy
        
        return copy
        
    def __eq__(self, matrix):
        #var security
        if type(matrix) != Matrix or self.size != matrix.size:
            return False
        
        for i, row in enumerate(matrix.map):
            for j, element in enumerate(row):
                if self.map[i][j] != element:
                    return False

        return True

    def __ne__(self, matrix):
        return not self == matrix

    def __invert__(self): #transponieren
        output = []
        width_i, height_i = 0, 0
        while height_i < self.width:
            new_row = []
            while width_i < self.height:
                new_row.append(self.map[width_i][height_i])
                width_i += 1
            output.append(new_row)
            width_i = 0
            height_i += 1
        return Matrix(output)
    
    def symmetric(self):
        return self == ~self

    def line_swap(self, index_1, index_2, horizontal=True):
        #var security
        if type(index_1) != int or type(index_2) != int or type(horizontal) != bool:
            sys.exit("Matrix.line_swap: incorrect data type")
        
        #base case
        if index_1 == index_2:
            return self
        if horizontal:
            #var security
            if max([index_1, index_2]) > self.height or min([index_1, index_2]) < 1:
                sys.exit("Matrix.line_swap: horizontal - indices out of range")
            
            output = self.map
            output[index_1 - 1], output[index_2 - 1] = output[index_2 - 1], output[index_1 - 1]

        else:
            #var security
            if max([index_1, index_2]) > self.width or min([index_1, index_2]) < 1:
                sys.exit("Matrix.line_swap: not horizontal - indices out of range")
            
            output = self.map
            for line in output:
                line[index_1 - 1], line[index_2 - 1] = line[index_2 - 1], line[index_1 - 1]
        
        return Matrix(output)

    def det(self):
        #var security
        if not self.square:
            sys.exit("Matrix.det: incorrect matrix size")
        
        #base cases
        if self.number:
            return self.number
        elif self.height == 2:
            return self.map[0][0]*self.map[1][1] - self.map[0][1]*self.map[1][0]
        
        #Laplace Entwicklungssatz
        output = 0
        for i in range(self.width):
            help_map = []
            width_i, height_i = 0, 0
            while height_i < self.height:
                new_row = []
                while width_i < self.width:
                    if width_i != i and height_i != 0:
                        new_row.append(self.map[height_i][width_i])
                    width_i += 1
                if new_row != []:
                    help_map.append(new_row)
                width_i = 0
                height_i += 1

            factor = self.map[0][i]
            if i % 2 != 0:
                factor = -1*factor

            output += factor*Matrix(help_map).det()
        
        return output

    def line_scale(self, index, constant):
        #var security
        if type(constant) not in [int, float]:
            sys.exit("Matrix.line_scale: scalar not a number")
        elif type(index) != int:
            sys.exit("Matrix.line_scale: index not an integer")
        elif not 0 < index <= self.height:
            sys.exit("Matrix.line_scale: index out of range")

        if constant == 1: #base case
            return self
        else:
            output = self.map
            for i, entry in enumerate(output[index - 1]):
                output[index - 1][i] = constant*entry
                
        
        return Matrix(output)

    def __mul__(self, other):
        #var security
        if type(other) not in [Matrix, int, float]:
            sys.exit("Matrix.multiply: incorrect data type")
        
        def scaling(matrix, a):
            #var security
            if type(a) not in [int, float]:
                sys.exit("Matrix.scaling: scalar not a number")

            output = []
            for row in matrix.map:
                new_row = []
                for number in row:
                    new_row.append(number*a)
                
                output.append(new_row)
            
            return Matrix(output)
        
        def multiply(matrix_a, matrix_b):
            #var security
            if type(matrix_b) != Matrix:
                sys.exit("Matrix.multiply: incorrect data type")
            elif matrix_a.width != matrix_b.height:
                sys.exit("Matrix.multiply: incorrect matrix size")
            
            def easy_scalar_product(list_a, list_b):
                if len(list_a) != len(list_b):
                    sys.exit("Matrix.multiply.easy_scalar_product: unequal lengths")
                
                sub_output = 0
                for i in range(len(list_a)):
                    sub_output += list_a[i]*list_b[i]
                
                return sub_output
            
            output = []
            width_i, height_i = 0, 0
            while height_i < matrix_a.height:
                new_row = []
                while width_i < matrix_b.width:
                    list_b_input = []
                    for i in matrix_b.map:
                        list_b_input.append(i[width_i])
                    new_row.append(easy_scalar_product(matrix_a.map[height_i], list_b_input))
                    width_i += 1
                output.append(new_row)
                width_i = 0
                height_i += 1
            return Matrix(output)

        #outsourcing
        if type(other) == Matrix:
            return multiply(self, other)
        else:
            return scaling(self, other)

    def __pos__(self):
        return self
    
    def __neg__(self):
        return self * (-1)

class LGS:
    def __init__(self, arg_list, type_matrix=True) -> None:
        #var security
        if type(type_matrix) != bool or type(arg_list) != list:
            sys.exit("LGS: incorrect data type")
        if type_matrix:
            if len(arg_list) != 2:
                sys.exit("LGS: type_matrix - incorrect list structure")
        else:
            if len(arg_list) == 0:
                sys.exit("LGS: type_matrix - incorrect list structure")
            for i in range(len(arg_list)):
                if type(arg_list[i]) != list:
                    sys.exit("LGS: not type_matrix - incorrect data type")
                elif i > 0 and len(arg_list[i]) != len(arg_list[i - 1]):
                    sys.exit("LGS: not type_matrix - incorrect list structure")

        #var declaration
        if type_matrix:
            #LGS([matrix, vector], True)
            #arg_list = [matrix, vector]
            matrix = arg_list[0]
            vector = arg_list[1]
        else:
            #LGS(matrix.map, False)
            #arg_list = [equation1, equation2, equation3]
            #equation = [1, 2, 3] "1x +2y = 3"
            matrix = Matrix(arg_list)
            matrix = matrix.del_line(matrix.width, True)
            vector = Matrix(arg_list)
            for i in range(vector.width - 1):
                vector = vector.del_line(1, True)

        #extended var security
        if type(matrix) != Matrix or type(vector) != Matrix or not vector.vector:
            sys.exit("LGS: incorrect data types")
        elif matrix.height != vector.height:
            sys.exit("LGS: no consistent dimension")
        
        self.matrix = matrix
        self.vector = vector
        self.coefficient_matrix = matrix.add_line(vector, False)
        self.dimension = self.matrix.width
        #homogen
        self.homogenous = True
        for line in self.vector.map:
            if line[0] != 0:
                self.homogenous = False
    
    def __str__(self):
            output = ""
            for i, row in enumerate(self.matrix.map):
                for num in row:
                    output = output + str(num) + ", "
                output = output + "= " + str(self.vector.map[i][0]) + "\n"
            
            return output

    def solve(self):
        #var security
        if not self.matrix.square:
            sys.exit("LGS.solve: wrong size")
        elif self.matrix.det() == 0:
            sys.exit("LGS.solve: no exact solution exists")

        #Cramer
        def cramer_insert(self, position):
            if type(position) != int or position >= self.dimension:
                sys.exit("LGS.solve.cramer_insert: no insert possible")
        
            sub_output = []
            width_i, height_i = 0, 0
            while height_i < self.matrix.height:
                new_row = []
                while width_i < self.matrix.width:
                    if width_i == position:
                        new_row.append(self.vector.map[height_i][0])
                    else:
                        new_row.append(self.matrix.map[height_i][width_i])
                    width_i += 1
                sub_output.append(new_row)
                width_i = 0
                height_i += 1
            return Matrix(sub_output)
        
        output = []
        for i in range(self.dimension):
            output.append([cramer_insert(self, i).det() / self.matrix.det()])
        
        return Matrix(output)

    def line_swap(self, index_1, index_2, horizontal=True):
        #var security
        if type(index_1) != int or type(index_2) != int or type(horizontal) != bool:
            sys.exit("LGS.line_swap: incorrect data type")
        
        if horizontal:
            if max([index_1, index_2]) > self.matrix.height or min([index_1, index_2]) < 1:
                sys.exit("LGS.line_swap: horizontal - indices out of range")
        else:
            if max([index_1, index_2]) > self.matrix.width or min([index_1, index_2]) < 1:
                sys.exit("LGS.line_swap: not horizontal - indices out of range")
        
        return(LGS(self.coefficient_matrix.line_swap(index_1, index_2, horizontal).map, False))
    
    def line_scale(self, index, constant):
        if constant == 0:
            sys.exit("LGS.line_scale: non-zero scalar required")
        
        return(LGS(self.coefficient_matrix.line_scale(index, constant).map, False))

    def line_add(self, index_1, index_2, constant):
        #var security
        if type(index_1) != int or type(index_2) != int or type(constant) not in [int, float]:
            sys.exit("LGS.line_add: incorrect data type")
        elif index_1 == index_2:
            sys.exit("LGS.line_add: indices must differ")
        elif max([index_1, index_2]) > self.matrix.height or min([index_1, index_2]) < 1:
                sys.exit("LGS.line_add: indices out of range")
        
        output = self.coefficient_matrix.map
        for i, line in enumerate(self.coefficient_matrix.map):
            if i == index_2 - 1:
                for j in range(len(line)):
                    output[i][j] += output[index_1 - 1][j]*constant
                

        return(LGS(output, False))

class Poly:
    def __init__(self, map) -> None:
        #map: list[a, ..., n]
        #var security
        if type(map) != list:
            sys.exit("Poly: incorrect structure")
        while map[-1] == 0 and len(map) > 1:
            map.pop()
        is_zero = True
        for number in map:
            if type(number) not in [int, float]:
                sys.exit("Matrix: only numbers permitted")
            elif number != 0:
                is_zero = False
        
        #attributes
        self.map = map
        self.zero = is_zero
        self.normed = False
        if map[-1] == 1:
            self.normed = True
        self.degree = len(map) -1
        if map == [0]:
            self.degree = -math.inf

    def __str__(self):
        output = "f(x) = "
        add_on = ""
        if self.map == [0]:
            add_on = "0"
        else:
            for i in range(len(self.map)):
                if i == 0:
                    var = ""
                elif i == 1:
                    var = "x"
                else:
                    var = "x^" + str(i)

                if self.map[i] > 0:
                    if self.map[i] == 1:
                        if add_on == "":
                            if i == 0:
                                add_on = add_on + "1"
                            else:
                                add_on = add_on + var
                        else:
                            add_on = add_on + " +" + var
                    else:
                        if add_on == "":
                            if self.map[i] == BM.c_round(self.map[i],0):
                                add_on = add_on + str(int(self.map[i])) + var
                            else:
                                add_on = add_on + str(self.map[i]) + var
                        else:
                            if self.map[i] == BM.c_round(self.map[i],0):
                                add_on = add_on + " +" + str(int(self.map[i])) + var
                            else:
                                add_on = add_on + " +" + str(self.map[i]) + var
                elif self.map[i] < 0:
                    if self.map[i] == -1 and i != 0:
                        add_on = add_on + " -" + var
                    else:
                        if self.map[i] == BM.c_round(self.map[i],0):
                            add_on = add_on + " -" + str(int(abs(self.map[i]))) + var
                        else:
                            add_on = add_on + " -" + str(abs(self.map[i])) + var
                else:
                    pass
            
        return output + add_on

    def __round__(self, rounder=2, rounder_method="normal"):
        output = []
        for number in self.map:
            output.append(BM.c_round(number, rounder, rounder_method))

        
        return Poly(output)

    def __add__(self, polynom):
        #var security
        if type(polynom) != Poly:
            sys.exit("Poly.add: incorrect data type")
        
        lg_map = self.map
        sm_map = polynom.map
        if polynom.degree > self.degree:
            sm_map = self.map
            lg_map = polynom.map

        output = []
        for i in range(len(lg_map)):
            if i+1 > len(sm_map):
                output.append(lg_map[i])
            else:
                output.append(lg_map[i]+sm_map[i])
        
        return Poly(output)

    def __sub__(self, polynom):
            #var security
            if type(polynom) != Poly:
                sys.exit("Poly.subtract: incorrect data type")

            return self + polynom * (-1)

    def __mul__(self, other):
        #var security
        if type(other) not in [Poly, int, float]:
            sys.exit("Poly.multiply: incorrect data type")
        
        def scaling(polynom, a):
            #var security
            if type(a) not in [int, float]:
                sys.exit("Poly.scaling: scalar not a number")

            output = []
            for number in polynom.map:
                output.append(number*a)
            
            return Poly(output)
        
        def multiply(poly_a, poly_b):
            #var security
            if type(poly_b) != Poly:
                sys.exit("Poly.multiply: incorrect data type")
            
            output = []

            for i in range(len(poly_a.map) + len(poly_b.map)):
                new_number = 0
                k = 0
                while k <= i:
                    try:
                        new_number += poly_a.map[k]*poly_b.map[i-k]
                    except IndexError:
                        new_number += 0
                    k += 1
                
                output.append(new_number)

            return Poly(output)

        #outsourcing
        if type(other) == Poly:
            return multiply(self, other)
        else:
            return scaling(self, other)

    def __truediv__(self, other):
        #var security
        if type(other) not in [Poly, int, float]:
            sys.exit("Poly.divide: incorrect data type")
        
        def polydiv(poly_a, poly_b):
            lg = poly_a
            sm = poly_b
            if poly_a.degree < poly_b.degree:
                lg = poly_b
                sm = poly_a
            
            a = lg.map[-1]/sm.map[-1]
            rest = []
            for i in range(len(sm.map)):
                rest.append(lg.map[-1-i]-a*sm.map[-1-i])
            for j in range(len(lg.map)-len(sm.map)):
                rest.append(lg.map[-1-j-len(sm.map)])
            
            
            return [a,BM.list_rev(rest)]
        
        #outsourcing
        if type(other) == Poly:
            output = []
            rest = self
            safety = 0
            while rest != Poly([0]) and safety < 20:
                mid_sol = polydiv(rest, other)
                output.append(mid_sol[0])
                rest = Poly(mid_sol[1]).__round__(4)
                safety += 1
            return Poly(BM.list_rev(output))
        else:
            return self*(1/other)

    def __pow__(self, exponent):
        #var security
        if type(exponent) != int or exponent < 0:
            sys.exit("Poly.power: incorrect data type")
        
        #cases
        if exponent == 0:
            return Poly([1])
        elif exponent == 1:
            return self
        
        copy = self
        for i in range(exponent - 1):
            copy = copy * copy
        
        return copy

    def __eq__(self, polynom):
        #var security
        if type(polynom) != Poly or self.degree != polynom.degree:
            return False
        
        for i, element in enumerate(polynom.map):
            if self.map[i] != element:
                return False

        return True
    
    def __ne__(self, polynom):
        return not self == polynom

    def __pos__(self):
            return self

    def __neg__(self):
            return self * (-1)

    def norm(self):
        return self*(1/self.map[-1])

    def insert(self, x):
        #var security
        if type(x) not in [int, float]:
            sys.exit("Poly.insert: incorrect data type.")
        
        #basic case
        if self.degree == 0:
            return self
        
        output = 0
        for i, number in enumerate(self.map):
            output += (x**i)*number
        
        return output

    def derive(self, n = 1):
        if type(n) != int or n < 0:
            sys.exit("Poly.derive: incorrect data type")
        
        #basic case
        if n == 0:
            return self

        def derive_one(poly):
            #basic case
            if poly.degree < 1:
                return Poly([0])
            
            output = []
            for i, factor in enumerate(poly.map):
                if i > 0:
                    output.append(i*factor)
            
            return Poly(output)
        
        output = self
        for i in range(n):
            output = derive_one(output)

        return output



#v = 1

def cn_rest(a_list, r_list):
    #var security
    pass
    
    #u_list
    u_list = []
    new_u = 1
    for r1 in r_list:
        for r2 in r_list:
            if r2 != r1:
                new_u *= r2
        u_list.append(new_u)
        new_u = 1

    def rel_modulo(lg,sm):
        lg_copy = lg
        counter = 0
        while lg_copy >= sm:
            lg_copy = lg_copy - sm
            counter += 1
        return [counter, lg - counter*sm]

    def relation(a,b): #a,b müssen positiv & teilerfremd sein
        lg = a
        sm = b
        if a < b:
            lg = b
            sm = a
        
        rel_list = [None, None]
        lg_copy = lg
        while rel_list[1] != 1:
            rel_list = rel_modulo(lg_copy,sm)
            lg_copy += lg
        
        sm_factor = -rel_list[0]
        lg_factor = (lg_copy-lg)/lg

        return [1, lg_factor, lg, sm_factor, sm]
    
    output = 0

    for i in range(len(a_list)):
        output += a_list[i]*u_list[i]*relation(r_list[i],u_list[i])[1]

    #product r
    prod_r = 1
    for k in r_list:
        prod_r *= k

    #Darstellung
    while output > 0:
        output -= prod_r
    output = int(output + prod_r)


    print("\nx = " + str(output))
    print("Y = {" + str(output) + " + " + str(prod_r) + "*r | r in Z}")
    for i in range(len(r_list)):
        print(str(output) + " = " + str(int((output-a_list[i])/r_list[i])) + "*" + str(r_list[i]) + " + " + str(a_list[i]))

    print("Output:")
    return output

aa = Poly([4,0.5,2])
bb = Poly([0,0,0.5,0.5,-1])
cc = Poly([5/24,-9/8,11/12,1])
dd = Poly([-0.5,1])

print(cc)
print(dd)
print(cc/dd)
