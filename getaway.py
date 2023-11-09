__author__ = "June Jin"
__version__ = "10.18.3 [Done]"

import math

def allocate(preferences, licenses):
    '''
    Function description:

    This function returns a list of cars in which, for 0 <= j <= ceil (N/5) - 1.
    This list at index j contains the indices of the drivers and passengers allocated to car j.

    This function will allocate the people to the car with the given preferences and licenses list.
    And, it will return at which car the people are allocated.

    If there is no allocation, it will return None.

    Approach description:   

    After we use FlowNetwork class, we will use this allocate function.

    Step 1: Edge type1, make edges from source to person who have license.
    Step 2: run BFS to find the path from source to sink. (who have license and the number of destination is 1)
    Step 3: if there is a path, backtrack and find the minimum flow.
    Step 4: add the minimum flow to the edge.
     - update the capacity max(2, edge.f) before running BFS again.
    Step 5: repeat step 2 to step 4 with the person who have license and the number of desination is 2 or more, until there is no path.
    Step 6: Edge type2, make edges from source to person who doesnt have license.
    Step 7: run BFS to find the path from source to sink (who doesnt have license.)
    Step 8: if there is a path, backtrack and find the minimum flow.
    Step 9: add the minimum flow to the edge.

    The first loop "while path" will run until there is no path from source to sink. (ONLY DRIVER who have only 1 Destination)
    The second loop "while path" will run until there is no path from source to sink. (ONLY DRIVER who have more than 1 Destination)
    The third loop "while path" will run until there is no path from source to sink. (ONLY PASSENGER who doesnt have license)

    During allocation, we will keep add 1 to the maximum_flow.
    After all the allocation, if the maximum_flow is not equal to the number of people, return None.

    :Input:
        argv1: preferences : a list of lists of integers, where preferences[i] is a list of integers representing the preferences of person i.
        argv2: licenses : a list of integers, where licenses[i] is the index of the person who has the license of person i.

    :Output, return: the list of cars, with the index of the drivers who allocated and the index the people who doesnt have license.
    :Time complexity: O (N^3), which N is the number of people.
    :Aux space complexity: O (N^2), which N is the number of people.
    '''

    # make the flow network
    getaway = FlowNetwork(preferences)

    maximum_flow = 0

    # make the car list with the size of the number of car, it will be the output
    car_list = [[] for _ in range(getaway.car_max)]

    # add edges from source to person who have license
    for i in range(len(licenses)):

        driver = licenses[i]

        # initialize license to True for driver
        getaway.vertices_list[driver].license = True

        # add edge from source to driver if driver has only 1 preference
        person_preference = preferences[driver]
        
        if len(person_preference) == 1 and getaway.vertices_list[driver].license:
            getaway.vertices_list[getaway.source_index].add_edge(Edge(getaway.source_index, driver, 1))

    # do bfs to find the path
    path = getaway.bfs(getaway.source_index, getaway.sink_index)

    # while there is a path from source to sink
    # we can know this through the bfs function
    while path:
        
        # initialize the minimum flow to infinity
        minimum_flow = math.inf

        # backtrack and find the minimum flow
        v = getaway.sink_index

        # while we are not at the source
        while v != getaway.source_index:

            # keep track of the previous vertex
            u = getaway.vertices_list[v].previous

            # find the edge from u to v
            for edge in getaway.vertices_list[u].edges:
                
                if edge.v == v:

                    # if the capacity - flow is smaller than the minimum flow,
                    # need to update the minimum flow
                    if edge.c - edge.f < minimum_flow:
                        minimum_flow = edge.c - edge.f
                    break
            v = u

        # add the minimum flow to the edge
        v = getaway.sink_index

        # while we are not at the source
        while v!= getaway.source_index:
            u = getaway.vertices_list[v].previous
            
            # find the edge from u to v
            for edge in getaway.vertices_list[u].edges:
                if edge.v == v:
                    # add the minimum flow to the edge
                    edge.f += minimum_flow

                    # if the edge is from car to sink, add the driver to the car_list
                    if edge.v >= getaway.og_vertices and edge.v <= getaway.og_vertices + getaway.car_max:
                        car_list[edge.v - getaway.og_vertices].append(edge.u)
                        getaway.vertices_list[edge.u].allocated = True
     
                    break
            v = u

        # do bfs to find the path
        path = getaway.bfs(getaway.source_index, getaway.sink_index)

        # add the minimum flow to the maximum_flow
        maximum_flow += minimum_flow    

    # allocate the rest of the people who have more than 1 preference
    for i in range(len(licenses)):
        driver = licenses[i]
   
        # only add edge from source to driver if driver has more than 1 preference
        person_preference = preferences[driver]

        # if the driver has more than 1 preference and has license, add edge from source to driver
        if len(person_preference) > 1 and getaway.vertices_list[driver].license:
            
            # add edge from source to driver
            getaway.vertices_list[getaway.source_index].add_edge(Edge(getaway.source_index, driver, 1))

    # checking if the car is full of driver
    for i in range(getaway.car_max):

        # update the capacity with comparing the flow
        for edge in getaway.vertices_list[getaway.og_vertices + i].edges:
            edge.c = max(2, edge.f) 

    # do bfs to find the path with updated capacity
    path = getaway.bfs(getaway.source_index, getaway.sink_index)

    # while there is a path from source to sink
    while path:
        
        # initialize the minimum flow to infinity
        minimum_flow = math.inf

        # backtrack and find the minimum flow
        v = getaway.sink_index

        # while we are not at the source
        while v != getaway.source_index:
            u = getaway.vertices_list[v].previous

            # find the edge from u to v
            for edge in getaway.vertices_list[u].edges:
                if edge.v == v:
                    # if the capacity - flow is smaller than the minimum flow,
                    # need to update the minimum flow
                    if edge.c - edge.f < minimum_flow:
                        minimum_flow = edge.c - edge.f
                    break
            v = u

        # add the minimum flow to the edge
        v = getaway.sink_index

        # while we are not at the source
        while v!= getaway.source_index:
            u = getaway.vertices_list[v].previous

            # find the edge from u to v
            for edge in getaway.vertices_list[u].edges:
                if edge.v == v:

                    # add the minimum flow to the edge
                    edge.f += minimum_flow

                    # if the edge is from car to sink, allocate the driver to the car_list
                    if edge.v >= getaway.og_vertices and edge.v <= getaway.og_vertices + getaway.car_max:
                        car_list[edge.v - getaway.og_vertices].append(edge.u)

                        #allocated is True
                        getaway.vertices_list[edge.u].allocated = True
                    break
            v = u

        # do bfs to find the path
        path = getaway.bfs(getaway.source_index, getaway.sink_index)

        # add the minimum flow to the maximum_flow
        maximum_flow += minimum_flow    

    # check every driver is allocated with enough number of people in the car
    for i in range(getaway.car_max):
        if len(car_list[i]) < 2:
            return None

    # before allocating the rest of the people who doesnt have license, update the capacity
    for i in range(getaway.car_max):
        for edge in getaway.vertices_list[getaway.og_vertices + i].edges:
            edge.c = 5

    # now, we have to allocate the rest of people who doesnt have license
    for i in range(len(preferences)):

        # make edges from source to person who doesnt have license
        if getaway.vertices_list[i].license == False:
            getaway.vertices_list[getaway.source_index].add_edge(Edge(getaway.source_index, i, 1))

    # do bfs to find the path
    path = getaway.bfs(getaway.source_index, getaway.sink_index)

    # while there is a path from source to sink 
    # edmonds karp algorithm (shortest path)
    while path:
        
        # initialize the minimum flow to infinity
        minimum_flow = math.inf

        # backtrack and find the minimum flow
        v = getaway.sink_index

        # while we are not at the source
        while v != getaway.source_index:

            # keep track of the previous vertex
            u = getaway.vertices_list[v].previous

            # find the edge from u to v
            for edge in getaway.vertices_list[u].edges:
                if edge.v == v:
                    
                    # if the capacity - flow is smaller than the minimum flow,
                    if edge.c - edge.f < minimum_flow:
                        minimum_flow = edge.c - edge.f
                    break
            v = u

        # add the minimum flow to the edge
        v = getaway.sink_index

        # while we are not at the source
        while v!= getaway.source_index:
            u = getaway.vertices_list[v].previous

            # find the edge from u to v
            for edge in getaway.vertices_list[u].edges:
                if edge.v == v:
                    edge.f += minimum_flow

                    # if the edge is from car to sink, allocate the driver to the car_list
                    if edge.v >= getaway.og_vertices and edge.v <= getaway.og_vertices + getaway.car_max:
                        car_list[edge.v - getaway.og_vertices].append(edge.u)

                        #allocated is True
                        getaway.vertices_list[edge.u].allocated = True
                    break
            v = u
        
        # do bfs to find the path
        path = getaway.bfs(getaway.source_index, getaway.sink_index)

        # add the minimum flow to the maximum_flow
        maximum_flow += minimum_flow

    # check every driver is allocated with enough number of people in the car
    if maximum_flow != getaway.og_vertices:
        return None
    else:
        return car_list

class Queue:

    def __init__(self) -> None:
        '''
        Function description:

        This function returns the queue.

        Approach description:

        It will make the queue with the list.

        :Time complexity: O(1)
        :Aux space complexity: O(1)
        '''
        self.queue = []

    def append(self, item):
        '''
        Function description:

        This function append the item to the queue.

        Approach description:

        It will append the item to the queue.

        :Input:
            argv1: item
            - the item that will be appended to the queue

        :Output, return: None

        :Time complexity: O(1)
        :Aux space complexity: O(1)
        '''
        self.queue.append(item)

    def serve(self):
        '''
        Function description:

        This function serve the item from the queue.

        Approach description:

        It will serve the item from the queue.

        :Time complexity: O(1)
        :Aux space complexity: O(1)
        '''
        return self.queue.pop(0)

    def __len__(self):
        '''
        Function description:

        This function returns the length of the queue.

        Approach description:

        It will return the length of the queue.

        :Output, return: 
            return the length of the queue

        :Time complexity: O(1)
        :Aux space complexity: O(1)
        '''
        return len(self.queue)

class FlowNetwork:
    def __init__(self,preferences):

        '''
        Function description:

        This function returns the flownetwork with the given preferences and licenses list.

        Between source and sink, we need to visit person vertices and car vertices.

        During allocating, we need to know about the capacity of the car and need to know about the license of the person.

        Approach description:

        Step 1: make all the vertices for people. 
        Step 2: find the enough number of car, and make vertices for car.
        Step 3: add source and sink vertices.
        Step 4: add edges from person to car.
        Step 5: add edges from car to sink.

        For finding the path,(from source to sink) we will use the BFS algorithm.
        during finding the path, it will compare the capacity and flow of the edge.
  
        :Input:
            argv1: preferences
            preferences : a list of lists of integers, where preferences[i] is a list of integers representing the preferences of person i.
        
        :Output, return: None

        :Time complexity: O (N^2), where N is the number of people. 
        :Aux space complexity: O (N^2), where N is the number of people. 
        '''
        
        self.og_vertices = len(preferences)
        self.vertices_list = []

        # make all the vertices for each person
        for i in range(self.og_vertices):
            p1_vertex = Vertex(i)
            self.vertices_list.append(p1_vertex)

        # find the enough number of car , which is 2
        self.car_max = math.ceil(len(preferences)/5)

        # make all the vertices for car/destination
        self.total_vertices = len(self.vertices_list)
        for i in range(self.car_max):
            c1_vertex = Vertex(self.total_vertices + i)
            self.vertices_list.append(c1_vertex)

        # add source and sink vertices
        self.vertices_list.append(Vertex(self.total_vertices + self.car_max))
        self.vertices_list.append(Vertex(self.total_vertices + self.car_max + 1))

        # add edges from person to car
        for i in range(self.og_vertices):
            for j in preferences[i]:
                self.vertices_list[i].add_edge(Edge(i, self.total_vertices + j,1))

        # add edges from car to sink
        for i in range(self.car_max):
            self.vertices_list[self.total_vertices + i].add_edge(Edge(self.total_vertices + i, self.total_vertices + self.car_max + 1,5))

        # add source and sink index
        self.source_index = self.total_vertices + self.car_max
        self.sink_index = self.total_vertices + self.car_max + 1

    def add_edges(self,u,v,c):
        '''
        Function description:

        Function for adding edges in the graph.

        Approach description:

        It will make edge between u and v with the capacity of c.

        :Input:
            u : the first vertex
            v : the second vertex
            c : the capacity of the edge

        :Time complexity: O(1)
        :Aux space complexity: O(1)
        '''

        my_edge = Edge(u,v,c)

        # add edge to the first vertex
        self.vertices_list[u].append(my_edge)

    def reset(self):
        '''
        Function description:

        Function for reset the vertices before running BFS.

        Approach description:

        It will make all the vertices undiscovered, visited to False and previous to None.

        :Time complexity: O(N), where N is the number of people.
        :Aux space complexity: O(1)
        '''
        for vertex in self.vertices_list:
            vertex.discovered = False
            vertex.visited = False
            vertex.previous = None

    def bfs(self, source, sink):
        '''
        Function description:

        A method that runs this function is BFS algorithm to find the path from source to sink.
        It uses queue from the source and discover the shortest next vertex with the weight but in here, all the weight is 1..
        After discovering the vertex, it will mark the vertex as visited.

        Approach description:

        There are 2 main steps in this function.
        Step 1: make all the vertices undiscovered, visited to False and previous to None.
        Step 2: discover the vertex and mark it as visited.

        But during finding the path, it will compare the capacity and flow of the edge.
        If the capacity is bigger than flow, it will go down the path.
        If the capacity is smaller than flow, it will not go down the path because we consider the flow is already full.

        :Input:
            argv1: source
            - vertex index of the source
            argv2: sink
            - vertex index of the sink

        :Output, return:
            return True if there is a path from source to sink.

        :Time complexity: O(N^2), where N is the number of people.
        :Aux space complexity: O(N), where N is the number of people.
        '''
        # reset the vertices
        self.reset()

        # make the source vertex discovered and visited
        discovered = Queue()
        discovered.append(source)
        self.vertices_list[source].visited = True


        # it will run while there is a vertex in the queue
        while len(discovered) > 0 :
            u = discovered.serve() 

            # it will go through all the edges of the vertex, N neighbours
            for edge in self.vertices_list[u].edges:

                v = edge.v

                # if the vertex is not discovered and the capacity is bigger than flow, discover the vertex
                if self.vertices_list[v].visited == False and edge.c - edge.f > 0 :

                    self.vertices_list[v].previous = u

                    self.vertices_list[v].visited = True
                
                    discovered.append(v)

        # return True if there is a path from source to sink
        return self.vertices_list[sink].visited

class Vertex:
    def __init__(self, id) -> None:
        '''
        Function description:
        Initialize a new vertex with the given ID.
        My reference is from the lecutre and tutorial FIT2004.
        
        Approach description:
        it will initialize the vertex with the given ID with the following attributes.

        Attributes:
        id : id of vertex.

        edges : A list of the edges.

        discovered : True if the vertex is found (pushed).
        visited : True if the vertex is visited (poped).

        previous : The previous vertex in the bfs's shortest path.
        license  : True if the vertex has license.

        allocated: True if the vertex is allocated.

        :Time complexity: O(1)
        :Aux space complexity: O(1) 
        '''
        self.id = id

        # list
        self.edges = []

        # for traversal
        self.discovered = False
        self.visited = False

        # backtracking
        self.previous = None

        # license
        self.license = False

        self.allocated = False

    def add_edge(self, edge):
        '''
        function description:
        Add edge to the vertex.

        Approach description:
        It will add the edge to the vertex.

        Attributes:
        edge : the edge that will be added to the vertex.

        :Time complexity: O(1)
        :Aux space complexity: O(1)
        '''
        self.edges.append(edge)

class Edge:
    def __init__(self, u, v, c):
        '''
        Edge from start vertex u, to vertex v, with capacity c.
        My reference is from the lecutre and tutorial FIT2004.
        
        Attributes:
        u : The vertex ID that the edge is pointing from.
        v : The vertex ID that the edge is pointing to.
        c : The capacity of this edge.

        f : The flow of this edgee, we default first as a 0.

        :Time complexity: O(1)
        :Aux space complexity: O(1)
        '''
        self.u = u
        self.v = v
        self.c = c
        self.f = 0
