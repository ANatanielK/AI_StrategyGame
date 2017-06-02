from enum import Enum

import random

import configuration

attackClass = {'knight' : KnightAttack, 'wizard' : WizardAttack}
defenseClass = {'knight' : KnightDefense, 'wizard' : WizardDefense}



class Unit:
    def __init__(self,player,ID,typeOfUnit):
        '''Constructor: receives the type of The Unit (knight, wizard...) as a String
        And builds the unit accordingly to the corresponding CSV File'''

        import csv, sys
        filename = typeOfUnit + '.csv'
        with open(filename, newline='') as f:
            reader = csv.reader(f)
            try:
                self.__init__((player,ID)+tuple(row[1] for row in reader))
            except csv.Error as e:
                sys.exit('file {}, line {}: {}'.format(filename, reader.line_num, e))


    def __init__(self,player,ID,maxHP,moveRange,isLight,attack,defense):
        self._player = player
        self._ID = ID
        self._maxHP = maxHP
        self._moveRange = moveRange
        self._isLight = isLight
        self._attack = attackClass[attack]()
        self._defense = defenseClass[defense]()

        self._experience = 0


    def startMatch(self,map,initialLocation):
        '''To be called at the start each match'''
        self._map = map
        self._location = initialLocation
        self._HP = self.maxHP


    def euristica(self):
        ''' How "strong" is this unit '''
        raise NotImplementedError

    @property
    def ID(self):
        return self._ID

    @property
    def player(self):
        return self._player

    @property
    def HP(self):
        '''Health Points'''
        return self._HP

    @HP.setter
    def setHP(self, val):
        if val < 0:
            self.dye()
        else:
            self._HP = min(self._maxHP, val)


    @property
    def moveRange(self):
        return self._moveRange

    @property
    def location(self):
        return self._location

    @property
    def cell(self):
        return self._map.map[self._location]

    @property
    def isLight(self):
        return self._isLight

    def receiveAttack(self):
        raise NotImplementedError

    def sendAttack(self,):
        raise NotImplementedError

    def dye(self):
        raise NotImplementedError





    def earnExperience(self,val):
        raise NotImplementedError


    @property
    def experience(self):
        return self._experience


    def penalty(self,percent):
        ''' Decrase all the the properties by indicated percent% '''