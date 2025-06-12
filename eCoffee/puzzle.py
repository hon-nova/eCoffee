from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
   # TODO
   Not(Biconditional(AKnight, AKnave)),
   Implication(AKnight,And(AKnight,AKnave)),
   Implication(AKnave,Not(And(AKnight,AKnave))),
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    # TODO
   Not(Biconditional(AKnight, AKnave)),
   Implication(AKnight,And(AKnave,BKnave)),
   Implication(AKnave,Not(And(AKnave,BKnave))),
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
S_A = Or(And(AKnight,BKnight),And(AKnave,BKnave))
S_B = Or(And(BKnight,AKnave),And(BKnave,AKnight))
knowledge2 = And(
    # TODO

   Not(Biconditional(AKnight, AKnave)),   
   Not(Biconditional(BKnight, BKnave)),
   
   Implication(AKnight,S_A),
   Implication(AKnave,Not(S_A)),
   
   Implication(BKnight,S_B),
   Implication(BKnave,Not(S_B)),
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    # TODO
   Not(Biconditional(AKnight, AKnave)),   
   Not(Biconditional(BKnight, BKnave)),     
   Not(Biconditional(CKnight, CKnave)),
    
   Implication(BKnight, And(CKnight)),
   Implication(BKnave, Not(And(CKnight))),
   
   Implication(CKnight, And(AKnight)),
   Implication(CKnave, Not(And(AKnight))),
    
)

def main():
   # test_knowledge = And(
   #  AKnight
   # )

   # print("TEST")
   # for symbol in [AKnight, AKnave]:
   #    if model_check(test_knowledge, symbol):
   #       print(f"    {symbol} is true")

   symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
   # print(f'All symbols: ')
   # for sb in symbols:
   #    print(f"{sb}")
      
   puzzles = [
      ("Puzzle 0", knowledge0),
      ("Puzzle 1", knowledge1),
      ("Puzzle 2", knowledge2),
      ("Puzzle 3", knowledge3)
   ]
   for puzzle, knowledge in puzzles:
      print(puzzle)
      if len(knowledge.conjuncts) == 0:
         print("Not yet implemented.")
      else:
         for symbol in symbols:            
            print(f"true/false model_check: {model_check(knowledge, symbol)}")
            if model_check(knowledge, symbol):
               print(f"{symbol}")


if __name__ == "__main__":
    main()
