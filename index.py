from flask import Flask, render_template, request, redirect, url_for, flash, send_file
import os
import tempfile
from werkzeug.utils import secure_filename
from main import corrompre_fichier, restaurer_fichier

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

UPLOAD_FOLDER = 'uploads'
PROCESSED_FOLDER = 'processed'

# Créer les dossiers nécessaires
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('Aucun fichier sélectionné')
        return redirect(request.url)
    
    file = request.files['file']
    action = request.form.get('action')
    
    if file.filename == '':
        flash('Aucun fichier sélectionné')
        return redirect(url_for('index'))
    
    if file and action in ['corrupt', 'restore']:
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        
        try:
            if action == 'corrupt':
                corrompre_fichier_web(filepath)
                processed_filename = filename + '.corrompu'
            else:  # restore
                restaurer_fichier_web(filepath)
                processed_filename = filename.replace('.corrompu', '.restaure')
            
            flash(f'Fichier {action}é avec succès!')
            return redirect(url_for('download', filename=processed_filename))
            
        except Exception as e:
            flash(f'Erreur lors du traitement: {str(e)}')
            return redirect(url_for('index'))
    
    flash('Action non valide')
    return redirect(url_for('index'))

@app.route('/download/<filename>')
def download(filename):
    processed_path = os.path.join(PROCESSED_FOLDER, filename)
    if os.path.exists(processed_path):
        return send_file(processed_path, as_attachment=True)
    else:
        flash('Fichier non trouvé')
        return redirect(url_for('index'))

def corrompre_fichier_web(chemin_fichier):
    with open(chemin_fichier, 'rb') as f:
        contenu = f.read()
    
    contenu_corrompu = bytes([b ^ 0xFF for b in contenu])
    
    filename = os.path.basename(chemin_fichier)
    output_path = os.path.join(PROCESSED_FOLDER, filename + '.corrompu')
    
    with open(output_path, 'wb') as f:
        f.write(contenu_corrompu)

def restaurer_fichier_web(chemin_corrompu):
    with open(chemin_corrompu, 'rb') as f:
        contenu = f.read()
    
    contenu_restaure = bytes([b ^ 0xFF for b in contenu])
    
    filename = os.path.basename(chemin_corrompu)
    output_filename = filename.replace('.corrompu', '.restaure')
    output_path = os.path.join(PROCESSED_FOLDER, output_filename)
    
    with open(output_path, 'wb') as f:
        f.write(contenu_restaure)

if __name__ == '__main__':
    app.run(debug=True, port=10000)