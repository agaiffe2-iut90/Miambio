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

# routes de Nathan
@app.route('/production/show')
def show_production():

    mycursor = get_db().cursor()
    sql = '''
    SELECT p.Id_production AS id, pr.Libellé_produit AS nom_produit, m.Nom_maraicher AS nom_maraicher, p.surface_cultivee
    FROM production p
    JOIN maraichers m ON p.Id_maraicher = m.Id_maraicher
    JOIN produits pr ON p.Id_produit = pr.Id_produit;
    '''
    mycursor.execute(sql)
    liste_production = mycursor.fetchall()

    return render_template('production/show_production.html', production=liste_production)

@app.route('/production/edit', methods=['GET'])
def show_edit_production_form():
    print("affichage du formulaire de modification d'une production")
    print(request.args)
    print(request.args.get('id'))

    mycursor = get_db().cursor()

    production_id = request.args.get('id', 0)

    produits_sql='''SELECT Id_produit, Libellé_produit FROM produits;'''
    mycursor.execute(produits_sql)
    produits = mycursor.fetchall()
    maraichers_sql='''SELECT Id_maraicher, Nom_maraicher FROM maraichers;'''
    mycursor.execute(maraichers_sql)
    maraichers = mycursor.fetchall()

    production_sql='''
    SELECT Id_production AS id, Id_produit, Id_maraicher, surface_cultivee
    FROM production
    WHERE Id_production = %s;
    '''
    mycursor.execute(production_sql, (production_id,))
    liste_production = mycursor.fetchone()

    return render_template('production/edit_production.html', produits=produits, maraichers=maraichers, production=liste_production)

@app.route('/production/edit', methods=['POST'])
def edit_production():
    print("une modification d'une production a eu lieu:")

    production_id = request.form.get('id')
    produit_id = request.form.get('produit')
    maraicher_id = request.form.get('maraicher')
    surface_cultivee = request.form.get('surface')
    message='id: ' + production_id + ', produit: ' + produit_id + ', maraicher: ' + maraicher_id + ', surface cultivee: ' + surface_cultivee
    print(message)

    mycursor = get_db().cursor()
    sql = '''
    UPDATE production
    SET Id_produit=%s, Id_maraicher=%s, surface_cultivee=%s
    WHERE Id_production=%s;
    '''
    tuple_param = (produit_id, maraicher_id, surface_cultivee, production_id)
    mycursor.execute(sql, tuple_param)
    get_db().commit()

    return redirect('/production/show')

@app.route('/production/delete')
def delete_production():
    print("Suppression d'une production")

    id = request.args.get('id', 0)

    mycursor = get_db().cursor()
    tuple_param = (id,)
    sql = "DELETE FROM production WHERE Id_production=%s;"
    mycursor.execute(sql, tuple_param)
    get_db().commit()

    print(request.args)
    print(request.args.get('id'))

    return redirect('/production/show')

@app.route('/production/add', methods=['GET'])
def add_production_form():
    print("affichage du formulaire d'ajout d'une production")

    mycursor = get_db().cursor()

    produit_sql='''SELECT Id_produit, Libellé_produit FROM produits;'''
    mycursor.execute(produit_sql)
    produits = mycursor.fetchall()
    maraicher_sql='''SELECT Id_maraicher, Nom_maraicher FROM maraichers;'''
    mycursor.execute(maraicher_sql)
    maraichers = mycursor.fetchall()

    return render_template('production/add_production.html', produits=produits, maraichers=maraichers)

@app.route('/production/add', methods=['POST'])
def add_production():
    print("ajout d'une production")

    produit_id = request.form.get('produit')
    maraicher_id = request.form.get('maraicher')
    surface_cultivee = request.form.get('surface')
    message='produit: ' + produit_id + ', maraicher: ' + maraicher_id + ', surface cultivee: ' + surface_cultivee
    print(message)

    mycursor = get_db().cursor()
    sql = "INSERT INTO production (Id_produit, Id_maraicher, surface_cultivee) VALUES (%s, %s, %s);"
    tuple_param = (produit_id, maraicher_id, surface_cultivee)
    mycursor.execute(sql, tuple_param)
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

# LES ROUTES DE SIMONE

@app.route('/')
@app.route('/produit/show')
def show_produit():
    mycursor = get_db().cursor()
    sql='''
 SELECT  Id_produit AS id,  libelle_produit AS lbproduit, Id_categorie_produit AS cgid
    FROM Produits
    ORDER BY id;
    '''
    mycursor.execute(sql)
    produits = mycursor.fetchall()
    return render_template('produit/show_produit.html', produits=produits)

@app.route('/produit/add', methods=['GET'])
def add_produit():
    mycursor = get_db().cursor()
    sql = '''Select * from categorie_produit'''
    mycursor.execute(sql)
    categorie = mycursor.fetchall()
    return render_template('produit/add_produit.html',categories=categorie)



@app.route('/produit/add', methods=['POST'])
def valid_add_produit():
    print('''ajout du produit dans le tableau''')
    lbproduit = request.form.get('lbproduit')
    Id_categorie_produit = request.form.get('Id_categorie_produit')
    message = u' produit ajouté , lbproduit:' + lbproduit + ' - Id_categorie_produit:' + Id_categorie_produit
    print(message)
    mycursor = get_db().cursor()
    tuple_param=(lbproduit,Id_categorie_produit)
    sql = "INSERT INTO Produits(libelle_produit,Id_categorie_produit,Id_produit) VALUES (%s,%s,NULL)"
    mycursor.execute(sql, tuple_param)
    get_db().commit()
    return redirect('/produit/show')
@app.route('/produit/delete')
def delete_produit():
    print('''suppression d'un produit''')
    id = request.args.get('id', None)
    verifier = []
    mycursor = get_db().cursor()
    sql="SELECT * FROM recolte WHERE Id_produit=%s"
    mycursor.execute(sql, id)
    verifier+=mycursor.fetchall()
    sql="SELECT * FROM produit WHERE Id_produit=%s"
    mycursor.execute(sql, id)
    verifier+=mycursor.fetchall()
    sql="SELECT * FROM periode_de_vente WHERE Id_produit=%s"
    mycursor.execute(sql, id)
    verifier+=mycursor.fetchall()
    sql="SELECT * FROM Vente WHERE Id_produit=%s"
    mycursor.execute(sql, id)
    verifier+=mycursor.fetchall()
    print(verifier)
    if len(verifier) ==0 :
        sql = "DELETE FROM Produits WHERE Id_produit=%s;"
        mycursor.execute(sql, id)
        get_db().commit()
    else:
        print("ce n'est pas possible")
    print(f'''le produit dans le tableau {id} a été supprimer''' )
    return redirect('/produit/show')

@app.route('/produit/edit', methods=['GET'])
def edit_produit():
    print('''affichage du formulaire pour modifier un étudiant''')
    id=request.args.get('id')
    mycursor = get_db().cursor()

    sql = '''
     SELECT  Id_produit AS id,  libelle_produit AS lbproduit, Id_categorie_produit AS cgid
        FROM Produits
        WHERE Id_produit = %s
        '''
    mycursor.execute(sql,id)
    produit = mycursor.fetchone()
    sql='''SELECT * FROM categorie_produit'''
    mycursor.execute(sql)
    categories = mycursor.fetchall()
    return render_template('produit/edit_produit.html', produit=produit ,  categories=categories)

@app.route('/produit/edit', methods=['POST'])
def valid_edit_produit():
    print('''affichage du formulaire pour modifier un étudiant''')
    id=request.form.get('id')
    categorie = request.form.get('Id_categorie_produit')
    lbproduit = request.form.get('lbproduit')
    print(id)
    print(categorie)

    mycursor = get_db().cursor()
    sql = '''UPDATE Produits SET libelle_produit=%s , Id_categorie_produit=%s WHERE Id_produit = %s'''
    mycursor.execute(sql,(lbproduit,categorie,id))
    get_db().commit()
    return redirect('/produit/show')














if __name__ == '__main__':
    app.run()
