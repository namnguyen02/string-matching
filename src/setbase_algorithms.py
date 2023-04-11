def jaccard_measure(x, y, q_grams):
   if len(x) == 0 or len(y) == 0: return 0
   for i in range(q_grams - 1):
      x = "#" + x
      x = x + "#"
      y = "#" + y
      y = y + "#" 
   setX = []
   setY = []
   for i in range(len(x) - q_grams + 1):
      setX.append(x[i : i + q_grams])
   for i in range(len(y) - q_grams + 1):
      setY.append(y[i : i + q_grams])
   ans = 0
   union_set = set()
   for token in setX:
      if token in setY:
         ans += 1
      union_set.add(token)
   for token in setY:
      union_set.add(token)
   return ans / len(union_set)

def overlap_measure(x, y, q_grams):
   if len(x) == 0 or len(y) == 0: return 0
   for i in range(q_grams - 1):
      x = "#" + x
      x = x + "#"
      y = "#" + y
      y = y + "#" 
   setX = []
   setY = []
   for i in range(len(x) - q_grams + 1):
      setX.append(x[i : i + q_grams])
   for i in range(len(y) - q_grams + 1):
      setY.append(y[i : i + q_grams])
   ans = 0
   for token in setX:
      if token in setY:
         ans += 1
   return ans
