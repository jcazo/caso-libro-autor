from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)

# mysql database
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'casodb'
mysql = MySQL(app)

app.secret_key='mysecrectkey'


@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute('select * from libro')
    data = cur.fetchall()
    cur.execute('select * from autor')
    data2 = cur.fetchall()
    return render_template('index.html',libro=data,autor=data2)
    # return 'Index - Diseño Software-UTEC'
    # return 'Index - Diseño Software-UTEC'

@app.route('/add_libro',methods=['POST'])
def add_libro():
    if request.method == 'POST':
        nom = request.form['nombre']
        disp = request.form['disponible']
        isbn = request.form['isbn']
        print('INSERT', id, nom, disp, isbn)
        cur = mysql.connection.cursor()
        cur.execute('insert into libro(nombre,disponible,isbn) values(%s,%s,%s)', (nom, disp, isbn))
        mysql.connection.commit()
        flash('libro Insertado correctamente')
        return redirect(url_for('index'))


@app.route('/add_autor',methods=['POST'])
def add_autor():
    
    if request.method == 'POST':
        nom = request.form['nombre']
        edic = request.form['edicion']
        fecha = request.form['fecha']
        print('INSERT', nom, edic, fecha)
        cur = mysql.connection.cursor()
        cur.execute('insert into autor(nombre,edicion,fecha_publicacion) values(%s,%s,%s)', (nom, edic, fecha))
        mysql.connection.commit()
        flash('Autor Insertado correctamente')
        return redirect(url_for('index'))



@app.route('/edit/<id>')
def edit_libro(id):
    cur = mysql.connection.cursor()
    cur.execute('select * from libro where idLibro = %s',{id})
    data = cur.fetchall()
    print(data[0])
    return render_template('edit.html', libro=data[0])


@app.route('/update/<id>',methods=['POST'])
def update_libro(id):
    if request.method == 'POST':
        nom = request.form['nombre']
        dips = request.form['disponible']
        isbn = request.form['isbn']
        print('UPDATE', id, nom, dips, isbn)
        cur = mysql.connection.cursor()
        cur.execute("""
            update libro
            set nombre = %s,
                disponible = %s,
                isbn = %s
            where idLibro = %s
        """,(nom, dips, isbn, id) )
        mysql.connection.commit()
        flash('libro actualizado correctamente')
        return redirect(url_for('index'))
# ---------------- EDITAR Y ACTUALIZAR AUTOR
@app.route('/edit2/<id>')
def edit_autor(id):
    cur = mysql.connection.cursor()
    cur.execute('select * from autor where idAutor = %s',{id})
    data = cur.fetchall()
    print(data[0])
    return render_template('edit2.html', autor=data[0])


@app.route('/update2/<id>',methods=['POST'])
def update_autor(id):
    if request.method == 'POST':
        nom = request.form['nombre']
        edic = request.form['edicion']
        fecha = request.form['fecha']
        print('UPDATE', id, nom, edic, fecha)
        cur = mysql.connection.cursor()
        cur.execute("""
            update autor
            set nombre = %s,
                edicion = %s,
                fecha_publicacion = %s
            where idAutor = %s
        """,(nom, edic, fecha, id) )
        mysql.connection.commit()
        flash('libro actualizado correctamente')
        return redirect(url_for('index'))

@app.route('/delete/<string:id>')
def delete_libro(id):
    cur = mysql.connection.cursor()
    cur.execute('delete from libro where idLibro = {0}'.format(id))
    mysql.connection.commit()
    flash('Libro Eliminado correctamente')
    return redirect(url_for('index'))


@app.route('/delete2/<string:id>')
def delete_autor(id):
    cur = mysql.connection.cursor()
    cur.execute('delete from autor where idAutor = {0}'.format(id))
    mysql.connection.commit()
    flash('Autor Eliminado correctamente')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(port=3010, debug=True)  # 3000 para mariadb cuando se instalo