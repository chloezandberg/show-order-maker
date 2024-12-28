from flask import Flask, render_template, request, redirect, url_for, flash
import os
import pandas as pd

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'  # Directory to save uploaded files
app.config['ALLOWED_EXTENSIONS'] = {'csv'}  # Restrict file types to CSV
app.secret_key = 'supersecretkey'  # For flash messages

# Ensure the uploads directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def allowed_file(filename):
    """Check if the file is a CSV."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    """Render the main upload page."""
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle file uploads."""
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    
    file = request.files['file']
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    
    if file and allowed_file(file.filename):
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        
        # Process the file with pandas
        data = pd.read_csv(filepath)
        print(f"Uploaded CSV file contains {len(data)} rows and {len(data.columns)} columns.")
        
        flash('File uploaded and processed successfully!')
        return redirect(url_for('index'))
    else:
        flash('Invalid file type. Only CSV files are allowed.')
        return redirect(request.url)

if __name__ == '__main__':
    app.run(debug=True)
