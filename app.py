from flask import Flask, render_template, request, jsonify
from my_model import recommend_book
app=Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

# @app.route('/recommend', methods=['POST'])
# def get_recommendations():
#     data = request.json
#     book_name = data['bookName']
    
#     recommended_books = recommend_book(book_name)
    
#     return jsonify(recommended_books)

@app.route('/recommend', methods=['POST'])
def get_recommendations():
    try:
        data = request.json
        book_name = data['bookName']
        
        print("Received book name:", book_name)  # Debug statement
        
        recommended_books = recommend_book(book_name)
        
        print("Recommended books:", recommended_books)  # Debug statement
        
        return jsonify(recommended_books)
    except Exception as e:
        print("Error:", e)  # Print the error for debugging
        return jsonify([]), 500  # Return an empty list and a 500 error status


if __name__=="__main__":
    app.run(debug=True)