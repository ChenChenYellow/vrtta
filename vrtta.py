from flask import Flask, request, jsonify, make_response
app = Flask(__name__)
global history 
history = []

@app.route('/')
def hello_world():
   return 'Hello World'

@app.route('/score', methods= ['POST'])
def score():
   product_name = request.json.get('product_name')
   materials = request.json.get('materials')
   weight_grams = request.json.get('weight_grams')
   transport = request.json.get('transport')
   packaging = request.json.get('packaging')
   if not isinstance(weight_grams, int) and not isinstance(weight_grams, float):
      return make_response("weight_grams not int nor float", 401)
   score = 0
   suggestions = []
   for m in materials:
      if m == "plastic":
         score -= 10
         suggestions.append("Avoid use of plastic")
      elif m == "aluminium":
         score += 10

   if transport == "air":
      score -= 15
      suggestions.append("Avoid air transport")
   elif transport == "rail" or transport == "sea":
      score += 5
   
   if packaging == "recyclable" or packaging == "biodegradable":
      score += 10
   else:
      suggestions.append("Use biodegradable or recyclable packaging")
   
   score /= weight_grams

   rating = "D"
   if score > 10:
      rating = "A"
   elif score > 1:
      rating = "B"
   elif score > 0:
      rating = "C"

   answer = {
      "product_name" : product_name,
      "sustainability_score" : score,
      "rating" : rating,
      "suggestions" : suggestions
   }

   history.append({
      "submission": request.json,
      "answer": answer
   })

   return make_response(jsonify(answer), 200)
   

@app.route('/history', methods= ['GET'])
def get_history():
   return make_response(jsonify(history), 200)


@app.route('/score-summary', methods= ['GET'])
def score_summary():
   total_products = len(history)
   total_score = 0
   ratings = {
      "A": 0,
      "B": 0,
      "C": 0,
      "D": 0
   }
   top_issues = {
      "Plastic used": 0,
      "Air transport": 0,
      "Non-recyclable packaging": 0
   }
   for h in history:
      total_score += h["answer"]["sustainability_score"]

      if h["answer"]["rating"] == "A":
         ratings["A"] += 1
      elif h["answer"]["rating"] == "B":
         ratings["B"] += 1
      elif h["answer"]["rating"] == "C":
         ratings["C"] += 1
      elif h["answer"]["rating"] == "D":
         ratings["D"] += 1
      
      for s in h["answer"]["suggestions"]:
         if s == "Avoid use of plastic":
            top_issues["Plastic used"] += 1
         elif s == "Avoid air transport":
            top_issues["Air transport"] += 1
         elif s == "Use biodegradable or recyclable packaging":
            top_issues["Non-recyclable packaging"] += 1
   average_score = 0
   if total_products != 0:
      average_score = total_score/total_products
   
   return make_response(jsonify(
      total_products = total_products,
      average_score = average_score,
      ratings = ratings,
      top_issues = top_issues
   ), 200)

if __name__ == '__main__':
   app.run(host='0.0.0.0', port=80)