#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import *
from modeles import modeleResanet
from technique import datesResanet

app = Flask(__name__)
app.secret_key = 'resanet'


@app.route('/', methods=['GET'])
def index():
    return render_template('vueAccueil.html')


@app.route('/usager/session/choisir', methods=['GET'])
def choisirSessionUsager():
    return render_template('vueConnexionUsager.html', carteBloquee=False, echecConnexion=False, saisieIncomplete=False)


@app.route('/usager/seConnecter', methods=['POST'])
def seConnecterUsager():
    numeroCarte = request.form['numeroCarte']
    mdp = request.form['mdp']

    if numeroCarte != '' and mdp != '':
        usager = modeleResanet.seConnecterUsager(numeroCarte, mdp)
        verif = modeleResanet.verificationInitMDP(numeroCarte, mdp)
        if verif == False:
            if len(usager) != 0:
                if usager['activee'] == True:
                    session['numeroCarte'] = usager['numeroCarte']
                    session['nom'] = usager['nom']
                    session['prenom'] = usager['prenom']
                    session['mdp'] = mdp

                    return redirect('/usager/reservations/lister')

                else:
                    return render_template('vueConnexionUsager.html', carteBloquee=True, echecConnexion=False,saisieIncomplete=False)
            else:
                return render_template('vueConnexionUsager.html', carteBloquee=False, echecConnexion=True,saisieIncomplete=False)
        else:
            return render_template('vueConnexionUsager.html',carteBloquee=False, echecConnexion=False,saisieIncomplete=False, verificationAncienMdp=True)
    else:
        return render_template('vueConnexionUsager.html', carteBloquee=False, echecConnexion=False,saisieIncomplete=True)


@app.route('/usager/seDeconnecter', methods=['GET'])
def seDeconnecterUsager():
    print '[START] appResanet::seDeconnecterUsager()'
    session.pop('numeroCarte', None)
    session.pop('nom', None)
    session.pop('prenom', None)
    print '[STOP] appResanet::seDeconnecterUsager()'
    return redirect('/')


@app.route('/usager/reservations/lister', methods=['GET'])
def listerReservations():
    print '[START] appResanet::listerReservations()'
    tarifRepas = modeleResanet.getTarifRepas(session['numeroCarte'])

    soldeCarte = modeleResanet.getSolde(session['numeroCarte'])

    solde = '%.2f' % (soldeCarte,)

    aujourdhui = datesResanet.getDateAujourdhuiISO()

    datesPeriodeISO = datesResanet.getDatesPeriodeCouranteISO()

    datesResas = modeleResanet.getReservationsCarte(session['numeroCarte'], datesPeriodeISO[0], datesPeriodeISO[-1])

    dates = []
    for uneDateISO in datesPeriodeISO:
        uneDate = {}
        uneDate['iso'] = uneDateISO
        uneDate['fr'] = datesResanet.convertirDateISOversFR(uneDateISO)
        uneDate['jour'] = datesResanet.convertirDateVersJourSemaine(uneDateISO)

        if uneDateISO <= aujourdhui:
            uneDate['verrouillee'] = True
        else:
            uneDate['verrouillee'] = False

        if uneDateISO in datesResas:
            uneDate['reservee'] = True
        else:
            uneDate['reservee'] = False

        if soldeCarte < tarifRepas and uneDate['reservee'] == False:
            uneDate['verrouillee'] = True

        dates.append(uneDate)

    if soldeCarte < tarifRepas:
        soldeInsuffisant = True
    else:
        soldeInsuffisant = False

    print '[STOP] appResanet::listerReservations()'
    return render_template('vueListeReservations.html', laSession=session, leSolde=solde, lesDates=dates,
                           soldeInsuffisant=soldeInsuffisant)


@app.route('/usager/reservations/annuler/<dateISO>', methods=['GET'])
def annulerReservation(dateISO):
    modeleResanet.annulerReservation(session['numeroCarte'], dateISO)
    modeleResanet.crediterSolde(session['numeroCarte'])
    return redirect('/usager/reservations/lister')


@app.route('/usager/reservations/enregistrer/<dateISO>', methods=['GET'])
def enregistrerReservation(dateISO):
    modeleResanet.enregistrerReservation(session['numeroCarte'], dateISO)
    modeleResanet.debiterSolde(session['numeroCarte'])
    return redirect('/usager/reservations/lister')


@app.route('/usager/mdp/modification/choisir', methods=['GET'])
def choisirModifierMdpUsager():
    soldeCarte = modeleResanet.getSolde(session['numeroCarte'])
    solde = '%.2f' % (soldeCarte,)

    return render_template('vueModificationMdp.html', laSession=session, leSolde=solde, modifMdp='')


@app.route('/usager/mdp/modification/appliquer', methods=['POST'])
def modifierMdpUsager():
    ancienMdp = request.form['ancienMDP']
    nouveauMdp = request.form['nouveauMDP']

    soldeCarte = modeleResanet.getSolde(session['numeroCarte'])
    solde = '%.2f' % (soldeCarte,)

    if ancienMdp != session['mdp'] or nouveauMdp == '':
        return render_template('vueModificationMdp.html', laSession=session, leSolde=solde, modifMdp='Nok')

    else:
        modeleResanet.modifierMdpUsager(session['numeroCarte'], nouveauMdp)
        session['mdp'] = nouveauMdp
        return render_template('vueModificationMdp.html', laSession=session, leSolde=solde, modifMdp='Ok')


@app.route('/gestionnaire/session/choisir', methods=['GET'])
def choisirSessionGestionnaire():
    # return
    return render_template('vueConnexionGestionnaire.html', echecConnexion=False, saisieIncomplete=False)


@app.route('/gestionnaire/seConnecter', methods=['POST'])
def seConnecterGestionnaire():
    # return('Traitement tentative connexion Gestionnaire')
    login = request.form['login']
    mdp = request.form['mdp']

    if login != '' and mdp != '':
        gestionnaire = modeleResanet.seConnecterGestionnaire(login, mdp)
        if len(gestionnaire) != 0:
            session['login'] = gestionnaire['login']
            session['nom'] = gestionnaire['nom']
            session['prenom'] = gestionnaire['prenom']
            session['mdp'] = mdp
            # return ("Connexion gestionnaire Ok")
            return redirect('/gestionnaire/personnel-avec-carte/lister')
        else:
            return render_template('vueConnexionGestionnaire.html', echecConnexion=True, saisieIncomplete=False)
    else:
        return render_template('vueConnexionGestionnaire.html', echecConnexion=False, saisieIncomplete=True)


@app.route('/gestionnaire/seDeconnecter', methods=['GET'])
def seDeconnecterGestionnaire():
    session.pop('login', None)
    session.pop('nom', None)
    session.pop('prenom', None)
    return redirect('/')


@app.route('/gestionnaire/personnel-avec-carte/lister', methods=['GET'])
def listerPersonnelAvecCarte():
    personnelAvecCarte = modeleResanet.getPersonnelsAvecCarte()
    return render_template('vuePersonnelAvecCarte.html', laSession=session, personnel=personnelAvecCarte)

@app.route('/gestionnaire/personnel-sans-carte/lister', methods=['GET'])
def listerPersonnelSansCarte():
    personnelSansCarte = modeleResanet.getPersonnelsSansCarte()
    return render_template('vuePersonnelSansCarte.html', laSession=session, personnel=personnelSansCarte)


@app.route('/gestionnaire/personnel-avec-carte/bloquer-carte/<numeroCarte>', methods=['GET'])
def bloquerCarte(numeroCarte):
    modeleResanet.bloquerCarte(numeroCarte)
    return redirect('/gestionnaire/personnel-avec-carte/lister')


@app.route('/gestionnaire/personnel-avec-carte/activer-carte/<numeroCarte>', methods=['GET'])
def activerCarte(numeroCarte):
    modeleResanet.activerCarte(numeroCarte)
    return redirect('/gestionnaire/personnel-avec-carte/lister')


@app.route('/gestionnaire/personnel-avec-carte/mdp/modification/appliquer/<numeroCarte>', methods=['GET'])
def reinitialiserMdp(numeroCarte):
    year = str(modeleResanet.getYear(numeroCarte))
    mdp = str(modeleResanet.getMdp(numeroCarte))
    if  year == mdp:
        return redirect('/gestionnaire/personnel-avec-carte/lister')
    else:
        modeleResanet.reinitialiserMdp(numeroCarte)
    return redirect('/gestionnaire/personnel-avec-carte/lister')

@app.route('/gestionnaire/personnel-sans-carte/creer-carte/bloquer/<numeroCarte>', methods=['GET'])
def bloquerPersonnelCreerCarte(numeroCarte):
    modeleResanet.creerCarte(numeroCarte)
    return redirect('/gestionnaire/personnel-sans-carte/lister')

@app.route('/gestionnaire/personnel-sans-carte/creer-carte/activer/<numeroCarte>', methods=['GET'])
def activerPersonnelCreerCarte(numeroCarte):
    modeleResanet.creerCarte(numeroCarte)
    modeleResanet.activerCarte(numeroCarte)
    return redirect('/gestionnaire/personnel-sans-carte/lister')

@app.route('/gestionnaire/personnel-avec-carte/crediter-carte/<numeroCarte>', methods=['POST'])
def personnelCrediterCarte(numeroCarte):
    somme = request.form['somme']
    modeleResanet.crediterCarte(numeroCarte, somme)
    return redirect('/gestionnaire/personnel-avec-carte/lister')




if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
