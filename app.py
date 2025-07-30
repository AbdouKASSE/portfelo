from flask import Flask, render_template, request, redirect, url_for, flash, send_file
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


app = Flask(__name__)
app.secret_key = os.urandom(24)  # Changez cette clé en production

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/contact', methods=['POST'])
def contact():
    if request.method == 'POST':
        nom = request.form.get('nom')
        email = request.form.get('email')
        message = request.form.get('message')
        
        # Validation basique
        if not nom or not email or not message:
            flash('Tous les champs sont requis.', 'error')
            return redirect(url_for('index') + '#contact')
        
        # Ici vous pourriez ajouter l'envoi d'email, sauvegarde en base, etc.
        send_email(nom=nom,email=email,message=message)
        print(f"Nouveau message de {nom} ({email}): {message}")
        
        flash(f'Merci {nom} ! Votre message a été envoyé avec succès. Je vous répondrai rapidement.', 'success')
        return redirect(url_for('index') + '#contact')

@app.route('/cv')
def download_cv():
    """Route pour télécharger le CV"""
    cv_path = os.path.join(app.static_folder, 'files', 'cv.pdf')
    
    # Vérifier si le fichier existe
    if os.path.exists(cv_path):
        return send_file(cv_path, 
                        as_attachment=True, 
                        download_name='CV_Abdou_KASSE.pdf',
                        mimetype='application/pdf')
    else:
        flash('CV non disponible pour le moment. Veuillez me contacter directement.', 'info')
        return redirect(url_for('index'))

def send_email(nom, email, message):
    # Configuration SMTP
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    sender_email = "kasseabdou21@gmail.com"
    sender_password = "votre-mot-de-passe-app"
    
    # Créer le message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = sender_email
    msg['Subject'] = f"Nouveau message de {nom}"
    
    body = f"""
    Nouveau message reçu via le portfolio :
    
    Nom: {nom}
    Email: {email}
    Message: {message}
    """
    
    msg.attach(MIMEText(body, 'plain'))
    
    # Envoyer l'email
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()
        return True
    except:
        return False

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # récupère le port défini par Heroku
    app.run(host='0.0.0.0', port=port)        # écoute sur toutes les IP (nécessaire)