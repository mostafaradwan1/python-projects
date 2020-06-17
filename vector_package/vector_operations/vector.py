from typing import List
from math import sqrt


vector=List[float]
Matrix=List[List[float]]

class Vector:
    """[summary]
    this class does operations on vectors 
    addition , subtraction,multipication
    """    
    def __init__(self):
        pass

    def add(self,v:vector,w:vector)->vector:
        assert len(v)==len(w),"different lengths"

        return [v_i+w_i for v_i , w_i in zip(v,w)]


    def subtract(self,v:vector,w:vector)->vector:
        assert len(v)==len(w),"different lengths"

        return [v_i-w_i for v_i , w_i in zip(v,w)]


    def multiply(self,v:vector,w:vector)->vector:
        assert len(v)==len(w),"different lengths"

        return [v_i*w_i for v_i , w_i in zip(v,w)]

    def vector_sum(self,vectors:List[vector]):
        """[summary]
            sums all corresponding elements
        Args:
            vectors (List[vector]): [description]
        returns:
            vector contain summations of other vectors
        """        
        assert vectors,"no vectors passed "

        num_elements=len(vectors[0])

        assert all(len(v)==num_elements for v in vectors),"different sizes"

        return [sum(vector[i] for vector in vectors) for i in range(num_elements)]


    def scalar_multiply(self,c:float , v:vector)->vector:
        "multiplies every element by c"

        return [c* v_i for v_i in v]

    def vector_mean(self,vectors:List[vector])->vector:
        "multiplies the mean vector "

        n=len(vectors)
        return self.scalar_multiply( 1/n ,self.vector_sum(vectors))
    

    def dot(self,v:vector,w:vector):
        "returns the dot product of two vectors"

        return sum(self.multiply(v,w))

    def sum_of_squares(self,v:vector)->float:
        
        return self.dot(v,v)

    def magnitude(self,v:vector):

        return sqrt(self.sum_of_squares(v))

    def squared_distance(self,v:vector,w:vector)->float:
        "returns the squared distance"

        return sum(self.subtract(v,w))


    def distance(self,v:vector,w:vector)->float:
        """[distance between two vectors]

        Args:
            v (vector): [first vector]
            w (vector): [secound vector]

        Returns:
            float: [the distance between the vectors]
        """       
        return sqrt(self.squared_distance(v,w))

    

vec =Vector()
assert vec.sum_of_squares([1,1,1])==3
assert  vec.vector_sum([[1,2],[5,6],[7,8],[3,4]])==[16,20]
assert  vec.vector_mean([[1,2],[5,6],[3,4]])==[3,4]
assert vec.dot([1,2,3],[4,5,6])==32