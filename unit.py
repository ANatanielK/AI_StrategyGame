from enum import Enum

import random

from configuration import *

attackClass = {'knight': KnightAttack, 'wizard': WizardAttack}
defenseClass = {'knight': KnightDefense, 'wizard': WizardDefense}



class Unit:
    def __init__(self,player,ID,typeOfUnit):
        '''Constructor: receives the type of The Unit (knight, wizard...) as a String
        And builds the unit accordingly to the corresponding CSV File'''

        import csv, sys
        filename = typeOfUnit + '.csv'
        with open(filename, newline='') as f:
            reader = csv.reader(f)
            try:
                self.constructor((player,ID)+tuple(row[1] for row in reader))
            except csv.Error as e:
                sys.exit('file {}, line {}: {}'.format(filename, reader.line_num, e))

    def constructor(self, player, ID, maxHP, moveRange, isLight, attack, defense):
        self._player = player
        self._ID = ID
        self._maxHP = maxHP
        self._moveRange = moveRange
        self._isLight = isLight
        self._attack = attackClass[attack]()
        self._defense = defenseClass[defense]()

        self._experience = 0


    def startMatch(self,board,initialLocation):
        '''To be called at the start of each match'''
        self._board = board
        self._location = initialLocation
        self._HP = self._maxHP
        self._dead = False

    #AI strategy purposes
    def euristica(self):
        ''' How "strong" is this unit '''
        #raise NotImplementedError
        val = self._HP*weightHP + self._maxHP*weightMaxHP + self._attack.euristica() + self._defense.euristica() + self._experience * weightExperience + self._isLight * weightIsLight + self._moveRange * weightMoveRange
        return val


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
    def HP(self, value):
        if value < 0:
            self.dye()
        else:
            self._HP = min(self._maxHP, value)


    @property
    def moveRange(self):
        return self._moveRange

    @property
    def location(self):
        return self._location

    @location.setter
    def location(self,value):
        self._location = value


    @property
    def cell(self):
        return self._board.board[self._location]

    @property
    def isLight(self):
        return self._isLight

    def receiveAttack(self, attacker, attackType, value):
        '''Attacker is the unit that sends the attack, value is a number indicating the damage in case of success '''
        damage = self._defense.receive( attacker, attackType, value)
        self.HP -= damage
        return damage

    def sendAttack(self, target):
        '''Target is the unit to be attacked'''
        return self._attack(target, self._location, self._board)

    def attackRanges(self):
        return self._attack.ranges

    def dye(self):
        self._dead = True

    def useAbility(self):
        raise NotImplementedError

    def earnExperience(self, val):
        self._experience += val
        while self._experience > maxExperience:
            self.levelUP()
            self._experience -= maxExperience

    def levelUP(self):
        self._moveRange *= levelUPProportion
        self._maxHP *= levelUPProportion
        self._attack.levelUP()
        self._defense.levelUp()

    @property
    def experience(self):
        return self._experience

    def penalty(self,percent = defaultPenaltyPercent):
        '''Decrease all the the properties by indicated percent% '''

        self._attack.penalty(percent)
        self._defense.penalty(percent)
        value = 1 - defaultPenaltyPercent / 100
        self._maxHP.penalty(percent)
        self._moveRange *= value
        self._experience *= value
        self._HP *= value



