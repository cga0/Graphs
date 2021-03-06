from itertools import combinations
from collections import deque
import random

class Stack:
    def __init__(self):
        self.stack = []
    
    def push(self, item):
        self.stack.append(item)
    
    def pop(self):
        return self.stack.pop()

    def size(self):
        return len(self.stack)

class User:
    def __init__(self, name):
        self.name = name

class SocialGraph:
    def __init__(self):
        self.lastID = 0
        self.users = {}
        self.friendships = {}

    def addFriendship(self, userID, friendID):
        """
        Creates a bi-directional friendship
        """
        if userID == friendID:
            print("WARNING: You cannot be friends with yourself")
        elif friendID in self.friendships[userID] or userID in self.friendships[friendID]:
            print("WARNING: Friendship already exists")
        else:
            self.friendships[userID].add(friendID)
            self.friendships[friendID].add(userID)

    def addUser(self, name):
        """
        Create a new user with a sequential integer ID
        """
        self.lastID += 1  # automatically increment the ID to assign the new user
        self.users[self.lastID] = User(name)
        self.friendships[self.lastID] = set()

    def populateGraph(self, numUsers, avgFriendships):
        """
        Takes a number of users and an average number of friendships
        as arguments

        Creates that number of users and a randomly distributed friendships
        between those users.

        The number of users must be greater than the average number of friendships.
        """
        # Reset graph
        self.lastID = 0
        self.users = {}
        self.friendships = {}
        # !!!! IMPLEMENT ME

        # Add users
        for i in range(numUsers):
            self.addUser(f'User {i}')

        # Create friendships
        friendships_list = list(combinations(range(1, len(self.users) + 1), 2))
        random.shuffle(friendships_list)
        average_amount_of_friends = avgFriendships * len(self.users) // 2
        possible_friendships = friendships_list[:average_amount_of_friends]
        for friendship in possible_friendships:
            self.addFriendship(friendship[0], friendship[1])

    def getAllSocialPaths(self, userID):
        """
        Takes a user's userID as an argument

        Returns a dictionary containing every user in that user's
        extended network with the shortest friendship path between them.

        The key is the friend's ID and the value is the path.
        """
        visited = {}  # Note that this is a dictionary, not a set
        in_network = self.bft(userID)
        for possible_friend in in_network:
            visited[possible_friend] = self.bfs(userID, possible_friend)

        return visited

    def bfs(self, starting_vertex, target_vertex):
        if starting_vertex == target_vertex:
            return [starting_vertex]
        visited = []
        queue = deque()
        queue.append([starting_vertex])
        
        while len(queue) > 0:
            current_path_list = queue.popleft()
            current_vertex = current_path_list[-1]

            if current_vertex not in visited:
                visited.append(current_vertex)

            for child in self.friendships[current_vertex]:
                dupe_path = list(current_path_list)
                dupe_path.append(child)
                if dupe_path[-1] == target_vertex:
                    return dupe_path
                else:
                    queue.append(dupe_path)
        return visited

    def bft(self, starting_vertex):
        visited = []

        queue = deque()
        queue.append(starting_vertex)
        
        while len(queue) > 0:
            current = queue.popleft()
            
            if current not in visited:
                visited.append(current)

            for item in self.friendships[current]:
                if item not in visited:
                    queue.append(item)
        return visited

if __name__ == '__main__':
    sg = SocialGraph()
    sg.populateGraph(10, 2)
    print(sg.friendships)
    connections = sg.getAllSocialPaths(4)
    print(connections)
