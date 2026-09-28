from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

MEASURE_WEIGHTS = [
    1.1, 1.1, 1.1, 1.1, 1.1, 1.1, 1.1, 1.3,
    1.1, 1.1, 1.1, 1.1, 1.1, 1.1, 1.2, 1.2,
    1.2, 1.2, 1.2, 1.2, 1.2, 1.2, 1.2, 1.2, 1.2, 1.2
]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/evaluate', methods=['POST'])
def evaluate():
    data = request.json
    accuracies = data.get('accuracies', [])
    
    total_score = 0.0
    measure_results = []

    for i, weight in enumerate(MEASURE_WEIGHTS):
        acc = accuracies[i] if i < len(accuracies) else 0.0
        m_score = weight * (acc / 100.0)
        total_score += m_score
        measure_results.append({
            'measure': i + 1,
            'weight': weight,
            'accuracy': acc,
            'score': round(m_score, 2)
        })

    final_score = round(total_score, 1)
    is_pass = final_score >= 24.0

    return jsonify({
        'total_score': final_score,
        'max_score': 30.0,
        'is_pass': is_pass,
        'measures': measure_results
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)