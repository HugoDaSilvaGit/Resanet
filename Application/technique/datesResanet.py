#!/usr/bin/python
# -*- coding: utf-8 -*-

import datetime
import locale

def convertirDateISOversFR( dateISO ) :
	print '[START] datesResanet::convertirDateISOversFR'
	annee , mois , jour = dateISO.split( '-' )
	dateFR = '/'.join( ( jour , mois , annee ) )
	print '[STOP] datesResanet::convertirDateISOversFR'
	return dateFR
	
def convertirDateFRversISO( dateFR ) :
	jour , mois , annee = dateFR.split( '/' )
	dateISO = '-'.join( ( annee , mois , jour ) )
	return dateISO

def convertirDateVersNumeroSemaine( dateISO ):
    date = dateISO
    annee, mois, jour = (int(x) for x in dateISO.split('-'))
    numeroSemaine = datetime.date(annee , mois , jour)
    numeroSemaine = int(numeroSemaine.strftime("%w"))
    return numeroSemaine

def convertirDateVersJourSemaine( dateISO ):
    date = dateISO
    annee, mois, jour = (int(x) for x in dateISO.split('-'))
    jourSemaine = datetime.date(annee , mois , jour)
    jourSemaine = int(jourSemaine.strftime("%w"))
    if jourSemaine == 1:
        jourSemaine = 'Lundi'
    elif jourSemaine == 2:
		jourSemaine = 'Mardi'
    elif jourSemaine == 3:
		jourSemaine = 'Mercredi'
    elif jourSemaine == 4:
		jourSemaine = 'Jeudi'
    elif jourSemaine == 5:
		jourSemaine = 'Vendredi'
    elif jourSemaine == 6:
		jourSemaine = 'Samedi'
    else:
		jourSemaine = 'Dimanche'
    return jourSemaine

def getDateAujourdhuiFR() :
	dateCourante = datetime.datetime.today()
	aujourdhui = '%02d/%02d/%04d' % ( dateCourante.day , dateCourante.month , dateCourante.year )
	return aujourdhui

def getDateAujourdhuiISO() :
	print '[START] datesResanet::getDateAujourdhuiISO'
	dateCourante = datetime.datetime.today()
	aujourdhui = '%04d-%02d-%02d' % ( dateCourante.year , dateCourante.month , dateCourante.day )
	print '[STOP] datesResanet::getDateAujourdhuiISO'
	return aujourdhui
	
def getDatesPeriodeCouranteISO() :
	print '[START] datesResanet::getDatesPeriodeCOuranteISO()'
	dates = []
	
	dateAujourdhui= datetime.datetime.today()
	numJourAujourdhui = dateAujourdhui.weekday()
	
	dateCourante = dateAujourdhui - datetime.timedelta( numJourAujourdhui )
	
	for i in range( 12 ) :
		if i != 5 and i != 6 :
			dateISO = '%04d-%02d-%02d' % ( dateCourante.year , dateCourante.month , dateCourante.day )
			dates.append( dateISO )
			
		dateCourante = dateCourante + datetime.timedelta( 1 )

	print '[STOP] datesResanet::getDatesPeriodeCOuranteISO()'
	return dates


def getDatesPeriodeCouranteFR():
	dates = []

	dateAujourdhui = datetime.datetime.today()
	numJourAujourdhui = dateAujourdhui.weekday()

	dateCourante = dateAujourdhui - datetime.timedelta(numJourAujourdhui)

	for i in range(12):
		if i != 5 and i != 6:
			dateFR = '%02d/%02d/%04d' % (dateCourante.day, dateCourante.month, dateCourante.year)
			dates.append(dateFR)

		dateCourante = dateCourante + datetime.timedelta(1)

	return dates

if __name__ == '__main__' :
	print convertirDateUSversFR( '2017-02-01' )
	print convertirDateFRversUS( '01/02/2017' )
	print getDateAujourdhuiFR()
	print getDateAujourdhuiUS()
	
	dates = getDatesPeriodeCouranteUS()
	for uneDate in dates :
		print uneDate
