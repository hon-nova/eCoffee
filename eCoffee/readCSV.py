import csv
import sys
from util import Node, QueueFrontier
names = {}
people = {}
movies = {}
# directory = 'large'

def read_data(directory):
   # Load people
   with open(f"{directory}/people.csv", encoding="utf-8") as f:
      reader = csv.DictReader(f)
      for row in reader:
         people[row['id']] = {
            'name': row['name'],
            'birth': row['birth'],
            'movies': set()
         }
         row_key_name = row['name'].strip().lower()
         if row_key_name not in names:         
            names[row_key_name] = {row['id']}
         else:
            names[row_key_name].add(row['id'])
            
      # print(f'PEOPLE: {people}')
      # print(f'NAMES: {names}')
   # Load movies
   with open(f"{directory}/movies.csv", encoding="utf-8") as f:
      reader = csv.DictReader(f)
      for row in reader:
         movies[row['id']] = {
            'title': row['title'],
            'year': row['year'],
            'stars': set()            
         }
      print(f'MOVIES: {movies}')
         
   # Load stars
   with open(f"{directory}/stars.csv", encoding="utf-8") as f:
      reader = csv.DictReader(f)
      for row in reader:
         try:
            people[row['person_id']]['movies'].add(row['movie_id'])
            movies[row['movie_id']]['stars'].add(row['person_id'])
         except KeyError:
            pass
   # print(f'PEOPLE: {people}')
   print(f'NAMES: {names}')
   # print(f'MOVIES: {movies}')

def neighbors_for_person(person_id):
   """
   Returns (movie_id, person_id) pairs for people
   who starred with a given person.
   """
   # step 1: get all movies of this person_id
   # step 2: get all people of those movies
   movie_ids = people[person_id].get('movies',set())   
   # print(f'TEST movies_ids: {movie_ids}')
   neighbors = set()
   for movie_id in movie_ids:
      for co_star_id in movies[movie_id]['stars']:
         if co_star_id != person_id:
            neighbors.add((movie_id,co_star_id))  
         
   # print(f'neighbors: {neighbors}')
   return neighbors 

def person_id_for_name(name):
   # person_ids = names[name.lower()]
   person_ids = list(names.get(name.lower(),set()))
   print(f"person_id_for_name(name): {person_ids}")
   if len(person_ids) == 0:
      return None
   elif len(person_ids) >1:
      print(f'Which ID? ')
      for person_id in person_ids:
         details = people[person_id]
         name=details['name']
         birth=details['birth']
         print(f'ID: {person_id}, name: {name}, birth: {birth}')
         
      try:
         intended_id = input("Intended ID: ")
         print(f'Confirmed ID: {intended_id}')
         if intended_id in person_ids:
            return intended_id
      except ValueError:
         pass
         
      return None
   else:
      return person_ids[0]



def shortest_path(source,target):
   """
   Returns the shortest list of (movie_id, person_id) pairs
   that connect the source to the target.

   If no possible path, returns None.
   """   
   # 1 create a start Node
   path= []
   explored = set()
   
   start_node = Node(state=source,parent=None,action=None)
   frontier = QueueFrontier()
   frontier.add(start_node)
   
   while not frontier.empty():
      queue_node = frontier.remove()
      
      if queue_node.state == target:         
         while queue_node.parent is not None:
               path.append((queue_node.action, queue_node.state))
               queue_node = queue_node.parent
         path.reverse()
         return path
      
      explored.add(queue_node.state)
      
      for movie_id,person_id in neighbors_for_person(queue_node.state):
         if person_id not in explored and not frontier.contains_state(person_id):
            child = Node(state=person_id,parent=queue_node,action=movie_id)
            frontier.add(child)
            
   return None      
      
# neighbors_for_person("102")

# neighbors_for_person("102")
# print(f'person_id: {person_id_for_name("Kevin Bacon")}')
def main():
   directory ='large'
   print('Loading data. Please wait ...')         
   read_data(directory)
   print('Data loaded successfully!')
   
   source = person_id_for_name(input("Source Name: "))
   if source is None:
      sys.exit("Person not found.")
   target = person_id_for_name(input("Target Name: "))
   if target is None:
      sys.exit("Person not found.")

   path = shortest_path(source, target)
   
   if path is None:
      print("Not connected.")
   else:
      degrees = len(path)
      print(f"{degrees} degrees of separation.")
      path = [(None, source)] + path
      for i in range(degrees):
         # people[person_id]
         # path[i][1] = person_id
         person1 = people[path[i][1]]["name"]
         person2 = people[path[i + 1][1]]["name"]
         movie = movies[path[i + 1][0]]["title"]
         print(f"{i + 1}: {person1} and {person2} starred in {movie}")   
   
   
if __name__ == "__main__":
   main()