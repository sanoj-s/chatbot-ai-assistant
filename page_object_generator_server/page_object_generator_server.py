from flask import Flask, jsonify
import subprocess

app = Flask(__name__)


@app.route('/pageobjectgenerator', methods=['POST', 'GET'])
def run_exe():
    try:
        result = subprocess.run(['../PageObjectGenerator/AutoPomGeneratorUI.exe'], capture_output=True, text=True)
        return jsonify({"output": "Page Object Generator Exited"})
    except Exception as e:
        return jsonify({"error": str(e)})


if __name__ == '__main__':
    app.run(port=5000)
