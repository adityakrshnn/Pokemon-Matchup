# -*- coding: utf-8 -*-
"""
Created on Mon Aug 14 00:35:06 2017

@author: 76b2
"""

your_attack_pokemon = 'Ho-oh'
their_defense_pokemon = 'Mewtwo'
mode = 'ORIGINAL' # GO or ORIGINAL

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from io import StringIO

pokemon = pd.read_csv('Pokemon.csv')
#pokemon = pokemon[pokemon['#'] < 151 if mode == 'GO' else 799]

types = pd.read_csv(StringIO("""Attacking,Normal,Fire,Water,Electric,Grass,Ice,Fighting,Poison,Ground,Flying,Psychic,Bug,Rock,Ghost,Dragon,Dark,Steel,Fairy
Normal,1,1,1,1,1,1,1,1,1,1,1,1,0.5,0,1,1,0.5,1
Fire,1,0.5,0.5,1,2,2,1,1,1,1,1,2,0.5,1,0.5,1,2,1
Water,1,2,0.5,1,0.5,1,1,1,2,1,1,1,2,1,0.5,1,1,1
Electric,1,1,2,0.5,0.5,1,1,1,0,2,1,1,1,1,0.5,1,1,1
Grass,1,0.5,2,1,0.5,1,1,0.5,2,0.5,1,0.5,2,1,0.5,1,0.5,1
Ice,1,0.5,0.5,1,2,0.5,1,1,2,2,1,1,1,1,2,1,0.5,1
Fighting,2,1,1,1,1,2,1,0.5,1,0.5,0.5,0.5,2,0,1,2,2,0.5
Poison,1,1,1,1,2,1,1,0.5,0.5,1,1,1,0.5,0.5,1,1,0,2
Ground,1,2,1,2,0.5,1,1,2,1,0,1,0.5,2,1,1,1,2,1
Flying,1,1,1,0.5,2,1,2,1,1,1,1,2,0.5,1,1,1,0.5,1
Psychic,1,1,1,1,1,1,2,2,1,1,0.5,1,1,1,1,0,0.5,1
Bug,1,0.5,1,1,2,1,0.5,0.5,1,0.5,2,1,1,0.5,1,2,0.5,0.5
Rock,1,2,1,1,1,2,0.5,1,0.5,2,1,2,1,1,1,1,0.5,1
Ghost,0,1,1,1,1,1,1,1,1,1,2,1,1,2,1,0.5,1,1
Dragon,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,1,0.5,0
Dark,1,1,1,1,1,1,0.5,1,1,1,2,1,1,2,1,0.5,1,0.5
Steel,1,0.5,0.5,0.5,1,2,1,1,1,1,1,1,2,1,1,1,0.5,2
Fairy,1,0.5,1,1,1,1,2,0.5,1,1,1,1,1,1,2,2,0.5,1"""))

pokemon_attack = pokemon.merge(types, left_on='Type 1', right_on='Attacking')

opponent_type = pokemon[pokemon['Name'] == their_defense_pokemon]['Type 1'].iloc[0]
opponent_multiplier = pokemon_attack[opponent_type]
adjusted_attack = pokemon_attack['Total'] * opponent_multiplier

pokemon_attack['Adjusted Attack'] = (adjusted_attack - adjusted_attack.min()) / (adjusted_attack.max() - adjusted_attack.min()) * 100

pokemon_attack.sort_values('Adjusted Attack', inplace=True)
pokemon_attack.tail(n=20).plot(kind='barh', x='Name', y='Adjusted Attack', figsize=(10, 7), title='Best 20 Pokemon to Attack %s' % their_defense_pokemon)

def pokeplot(x, y):
    f = sns.FacetGrid(pokemon, hue='Type 1', size=8) \
       .map(plt.scatter, x, y, alpha=0.5) \
       .add_legend()
    plt.subplots_adjust(top=0.9)
    f.fig.suptitle('%s vs. %s' % (x, y))
    f.ax.set_xlim(0,)
    f.ax.set_ylim(0,)

    attack_pokemon  = pokemon[pokemon['Name']==your_attack_pokemon]
    defense_pokemon = pokemon[pokemon['Name']==their_defense_pokemon]

    plt.scatter(attack_pokemon[x],attack_pokemon[y], s=100, c='#f46d43')
    plt.text(attack_pokemon[x]+6,attack_pokemon[y]-3, your_attack_pokemon, 
             fontsize=16, weight='bold', color='#f46d43')

    plt.scatter(defense_pokemon[y],defense_pokemon[y], s=100, c='#74add1')
    plt.text(defense_pokemon[x]+6,defense_pokemon[y]-3, their_defense_pokemon, 
             fontsize=16, weight='bold', color='#74add1')
    
pokeplot('Attack', 'Defense')
    
pokeplot('Speed', 'HP')