from flask import Flask, request, render_template, redirect, url_for, abort, flash

app = Flask(__name__)


# Sujet 3

produits = [
    {'id': 1, 'nomproduit': 'Pain Blanc', 'indiceglycémiqueproduit': '75', 'image': 'Painblanc.jpeg'},
    {'id': 2, 'nomproduit': 'Pomme de terre cuite', 'indiceglycémiqueproduit': '85', 'image': 'PommeTerre.jpeg'},
    {'id': 3, 'nomproduit': 'Frites', 'indiceglycémiqueproduit': '75', 'image': 'Frites.jpeg'},
    {'id': 4, 'nomproduit': 'Brocoli', 'indiceglycémiqueproduit': '30', 'image': 'Brocoli.jpeg'},
    {'id': 5, 'nomproduit': 'Salade', 'indiceglycémiqueproduit': '15', 'image': 'Salade.jpeg'},
    {'id': 6, 'nomproduit': 'Tofu', 'indiceglycémiqueproduit': '15', 'image': 'Tofu.jpeg'},
    {'id': 7, 'nomproduit': 'couscous', 'indiceglycémiqueproduit': '60', 'image': 'Couscous.jpeg'},
]


@app.route('/')
def show_accueil():
    return render_template('layout.html')

@app.route('/produit/show')
def show_produit():
    # print(articles)
    return render_template('/produit/show_produit.html', produits=produits)

@app.route('/produit/add', methods=['GET'])
def add_produit():
    return render_template('produit/add_produit.html', produits=produits)

@app.route('/produit/add', methods=['POST'])
def valid_add_produit():
    id = request.form.get('id', '')
    nomproduit = request.form.get('nomproduit', '')
    produit_id = request.form.get('produit_id')
    indiceglycémiqueproduit = request.form.get('indiceglycémiqueproduit', '')
    image = request.form.get('image', '')
    message = u'produit modifié , id:'+id + '---- produit_id :' + produit_id + ' ----nomproduit :' + nomproduit + ' - indiceglycémiqueproduit:'+  indiceglycémiqueproduit + ' - image:' + image + + u' ------ pour le produit d identifiant :' + id
    print(message)
    flash(message, 'alert-success')
    return redirect('/produit/show')

@app.route('/produit/delete', methods=['GET'])
def delete_produit():
    id = request.args.get('id', '')
    message=u'un produit supprimé, id : ' + id
    flash(message, 'alert-warning')
    return redirect('/produit/show')

@app.route('/produit/edit', methods=['GET'])
def edit_produit():
    id = request.args.get('id', '')
    id=int(id)
    produits= produits[id-1]
    return render_template('/produit/edit_produit.html', produits=produits)

@app.route('/produit/edit', methods=['POST'])
def valid_edit_produit():
    id = request.form.get('id', '')
    nomproduit = request.form.get('nomproduit', '')
    produit_id = request.form.get('produit_id')
    indiceglycémiqueproduit = request.form.get('indiceglycémiqueproduit', '')
    image = request.form.get('image', '')
    message = u'produit modifié , id:'+id + '---- produit_id :' + produit_id + ' ----nomproduit :' + nomproduit + ' - indiceglycémiqueproduit:'+  indiceglycémiqueproduit + ' - image:' + image + + u' ------ pour le produit d identifiant :' + id
    print(message)  
    flash(message, 'alert-success')
    return redirect('/produit/show')

@app.route('/production/show')
def show_production():
    mycursor = get_db().cursor()
    sql='''SELECT Id_production AS id, surface_cultivee AS surface_cultivee
    FROM production;'''
    mycursor.execute(sql)
    liste_production = mycursor.fetchall()
    return render_template('production/show_production.html', production=liste_production)

@app.route('/production/delete')
def delete_etudiant():
    print('''suppression d'une production''')
    id = request.args.get('id', 0)
    print(id)
    mycursor = get_db().cursor()
    tuple_param = (id,)
    sql = "DELETE FROM production WHERE Id_production=%s;"
    mycursor.execute(sql, tuple_param)
    get_db().commit()
    print(request.args)
    print(request.args.get('id'))
    id = request.args.get('id', 0)
    return redirect('/production/show')

@app.route('/production/show')
def show_etudiant():
    mycursor = get_db().cursor()
    sql='''SELECT Id_production AS id, surface_cultivee AS surface_cultivee
    FROM production;'''
    mycursor.execute(sql)
    liste_production = mycursor.fetchall()
    return render_template('production/show_production.html', production=liste_production)

@app.route('/production/edit', methods=['GET'])
def edit_production():
    # Récupérer la liste de tous les maraîchers
    mycursor = get_db().cursor()
    maraicher_sql = "SELECT Id_maraicher, Nom_maraicher FROM maraichers;"
    mycursor.execute(maraicher_sql)
    maraichers = mycursor.fetchall()

    # Rendre le modèle en passant les données à utiliser dans le formulaire
    return render_template('production/edit_production.html', maraichers=maraichers)

@app.route('/production/delete')
def delete_production():
    print('''suppression d'une production''')
    id = request.args.get('id', 0)
    print(id)
    mycursor = get_db().cursor()
    tuple_param = (id,)
    sql = "DELETE FROM production WHERE Id_production=%s;"
    mycursor.execute(sql, tuple_param)
    get_db().commit()
    print(request.args)
    print(request.args.get('id'))
    id = request.args.get('id', 0)
    return redirect('/production/show')

@app.route('/production/add', methods=['GET'])
def add_production():
    print('''affichage du formulaire pour saisir une production''')
    mycursor = get_db().cursor()
    maraicher_sql = "SELECT Id_Maraicher, Nom_maraicher FROM maraichers;"
    mycursor.execute(maraicher_sql)
    maraichers = mycursor.fetchall()

    produit_sql = "SELECT Id_produit, Libellé_produit FROM produits;"
    mycursor.execute(produit_sql)
    produits = mycursor.fetchall()
    return render_template('production/add_production.html', maraichers=maraichers, produits=produits)

@app.route('/production/add', methods=['POST'])
def valid_add_production():
    print('''ajout de la production dans le tableau''')
    Nom_maraicher = request.form.get('Nom_maraicher')
    Libellé_produit = request.form.get('produit')
    surface_cultivee = request.form.get('surface_cultivee')
    if Nom_maraicher is not None and Libellé_produit is not None and surface_cultivee is not None:
        message = f'nom : {Nom_maraicher} - produit : {Libellé_produit} - surface cultivée : {surface_cultivee}'
    else:
        # Gérer le cas où l'une des valeurs est None
        message = 'Erreur : l\'une des valeurs est manquante.'

    mycursor = get_db().cursor()
    tuple_param=(surface_cultivee, Nom_maraicher, Libellé_produit)
    sql="INSERT INTO production(surface_cultivee, Id_maraicher, Id_produit) VALUES (%s, %s, %s);"
    mycursor.execute(sql,tuple_param)
    get_db().commit()
    return redirect('/production/show')





# ROUTES D'ANNA

@app.route('/recolte/show')
def show_recolte():
    mycursor = get_db().cursor()
    sql='''
 SELECT  Id_recolte AS id,  quantite_recoltee AS qtRecolte, Id_Semaine AS semaine, Id_produit AS id_produit, Id_Maraicher AS id_maraicher
 FROM recolte
    ORDER BY id;
    '''
    mycursor.execute(sql)
    recoltes = mycursor.fetchall()
    return render_template('recolte/show_recolte.html', recoltes=recoltes)

@app.route('/recolte/add', methods=['GET'])
def add_recolte():
    print('''affichage du formulaire pour saisir une récolte''')
    mycursor = get_db().cursor()
    sql='''SELECT * FROM Semaine
    '''
    mycursor.execute(sql)
    semaines = mycursor.fetchall()

    sql='''SELECT * FROM Produits '''
    mycursor.execute(sql)
    produits = mycursor.fetchall()

    sql = '''SELECT * FROM Maraichers '''
    mycursor.execute(sql)
    maraichers = mycursor.fetchall()

    return render_template('recolte/add_recolte.html' , semaines=semaines , produits=produits , maraichers=maraichers)


@app.route('/recolte/edit', methods=['GET'])
def edit_recolte():
    print('''Modifier une récolte''')
    id=request.args.get('id')
    mycursor = get_db().cursor()
    sql=''' SELECT  Id_recolte AS id,  quantite_recoltee AS qtRecolte, Id_Semaine AS semaine, Id_produit AS id_produit, Id_Maraicher AS id_maraicher
 FROM recolte
    WHERE Id_Recolte=%s;'''
    mycursor.execute(sql,id)
    recolte = mycursor.fetchone()

    mycursor = get_db().cursor()
    sql='''SELECT * FROM Semaine
    '''
    mycursor.execute(sql)
    semaines = mycursor.fetchall()

    sql='''SELECT * FROM Produits '''
    mycursor.execute(sql)
    produits = mycursor.fetchall()

    sql = '''SELECT * FROM Maraichers '''
    mycursor.execute(sql)
    maraichers = mycursor.fetchall()
    return render_template('recolte/edit_recolte.html', recolte=recolte , semaines=semaines , produits=produits , maraichers=maraichers)


@app.route('/recolte/add', methods=['POST'])
def valid_add_recolte():
    print('''ajout de récolte dans le tableau''')
    qtRecolte = request.form.get('qtRecolte')
    semaine = request.form.get('Id_Semaine')
    id_produit = request.form.get('Id_produit')
    id_maraicher = request.form.get('Id_Maraicher')

    message = ' - Quantité récoltée :' + qtRecolte + ' - semaine n° :' + semaine +' - produit n° :' + id_produit +' - récolté par :' + id_maraicher
    print(message)
    mycursor = get_db().cursor()
    tuple_param=(qtRecolte,semaine,id_produit,id_maraicher)
    sql="INSERT INTO recolte(Id_recolte, quantite_recoltee, Id_Semaine, Id_produit, Id_Maraicher) VALUES (NULL, %s, %s, %s, %s);"
    mycursor.execute(sql,tuple_param)
    get_db().commit()
    return redirect('/recolte/show')

@app.route('/recolte/edit', methods=['POST'])
def valid_edit_recolte():
    print('''modification de la récolte ''')
    id = request.form.get('id')
    qtRecolte = request.form.get('qtRecolte')
    semaine = request.form.get('Id_Semaine')
    id_produit = request.form.get('Id_produit')
    id_maraicher = request.form.get('Id_Maraicher')
    print(qtRecolte,semaine,id_produit,id_maraicher,id)


    mycursor = get_db().cursor()
    sql="UPDATE recolte SET quantite_recoltee = %s, Id_Semaine=%s,  Id_produit=%s, Id_Maraicher= %s WHERE Id_recolte=%s;"
    mycursor.execute(sql,(qtRecolte,semaine,id_produit,id_maraicher,id))
    get_db().commit()
    return redirect('/recolte/show')

@app.route('/recolte/delete' , methods=['GET'])
def delete_recolte():
    print('''suppression d'une récolte''')
    id = request.args.get('id', 'heyyy')
    mycursor = get_db().cursor()
    sql = "DELETE FROM recolte WHERE Id_recolte=%s;"
    mycursor.execute(sql, id)
    get_db().commit()
    print('La recolte avec le numéro '+id + 'a été supprimé')
    return redirect('/recolte/show')
















if __name__ == '__main__':
    app.run()
