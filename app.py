from config import SQLALCHEMY_DATABASE_URI
from flask import Flask, render_template, request, redirect, url_for
from models import db, Document, DocumentVersion, DocumentDeletion
from sqlalchemy.orm import sessionmaker
from diff_match_patch import diff_match_patch
import webbrowser

app = Flask(__name__, template_folder='Templates')

app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI

# создаем объект SQLAlchemy и связываем его с приложением
db.init_app(app)


def diff_filter(text1, text2):
    dmp = diff_match_patch()
    diff = dmp.diff_main(text1, text2)
    dmp.diff_cleanupSemantic(diff)
    return dmp.diff_prettyHtml(diff)


app.jinja_env.filters['diff'] = diff_filter


with app.app_context():
    Session = sessionmaker(bind=db.engine)
    session = Session()


@app.route('/')
def index():
    with app.app_context():
        documents = Document.query.filter_by(is_deleted=False).order_by(Document.created_at.desc()).all()
        return render_template('index.html', documents=documents)


@app.route('/documents/new', methods=['GET', 'POST'])
def new_document():
    with app.app_context():
        if request.method == 'POST':
            name = request.form['name']
            content = request.form['content']
            document = Document(name=name, content=content)
            db.session.add(document)
            db.session.commit()
            return redirect(url_for('document', document_id=document.id))
        else:
            return render_template('new_document.html')


@app.route('/documents/<int:document_id>', methods=['GET', 'POST'])
def document(document_id):
    document = Document.query.get_or_404(document_id)
    if request.method == 'POST':
        name = request.form['name']
        content = request.form['content']
        document_version = DocumentVersion(document_id=document_id, name=document.name, content=document.content)
        document.name = name
        document.content = content
        db.session.add(document_version)
        db.session.commit()
        return redirect(url_for('document', document_id=document.id))
    else:
        return render_template('document.html', document=document)


@app.route('/documents/<int:document_id>/versions')
def document_versions(document_id):
    document = Document.query.get(document_id)
    versions = DocumentVersion.query.filter_by(document_id=document_id).order_by(
        DocumentVersion.created_at.desc()).all()
    return render_template('document_versions.html', document=document, versions=versions)


@app.route('/documents/<int:document_id>/delete', methods=['POST'])
def delete_document(document_id):
    with app.app_context():
        document = Document.query.get_or_404(document_id)
        document_deletion = DocumentDeletion(document_id=document_id)
        document.is_deleted = True
        db.session.add(document_deletion)
        db.session.commit()
    return redirect(url_for('index'))


@app.route('/documents/<int:document_id>/compare/<int:version_id>')
def compare_versions(document_id, version_id):
    document = Document.query.get(document_id)
    version = DocumentVersion.query.get(version_id)
    return render_template('compare_versions.html', document=document, version=version)


if __name__ == '__main__':
    url = 'http://localhost:5000'
    webbrowser.open(url)
    #
    app.run(debug=True, use_reloader=False)


