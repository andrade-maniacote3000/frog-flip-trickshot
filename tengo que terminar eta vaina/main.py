from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

    db.init_app(app)
    with app.app_context():
        db.create_all()  
    
    return app

app = create_app()

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'<Product {self.title}>'
    
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    login = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(30), nullable=False)

    
@app.route('/login', methods=['GET','POST'])
def login():
        error = ''
        if request.method == 'POST':
            form_login = request.form['email']
            form_password = request.form['password']
            

            users_db = User.query.all()
            for user in users_db:
                if form_login == user.login and form_password == user.password:
                    return redirect('/products')
            else:
                error = 'Nombre de usuario o contraseña incorrectos'
                return render_template('end.html', error=error)
                        
        else:
            return render_template('end.html')

        

@app.route('/reg', methods=['GET','POST'])
def reg():
    if request.method == 'POST':
        login= request.form['email']
        password = request.form['password']
        

        user = User(login=login, password=password)
        db.session.add(user)
        db.session.commit()
        
        return redirect('/')
    
    else:    
        return render_template('registration.html')
@app.route('/')
def index():
    products = Product.query.all()
    return render_template('index.html', products=products)

@app.route('/shop')
def shop():
    return render_template('shop.html')

@app.route('/products', methods=['POST'])
def create_product():
    title = request.form.get('title')
    description = request.form.get('description')
    price = request.form.get('price')

    try:
        price = float(price)
    except ValueError:
        return "El precio debe ser un número válido", 400

    product = Product(title=title, description=description, price=price)
    db.session.add(product)
    db.session.commit()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)