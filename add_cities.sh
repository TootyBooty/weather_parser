#!/bin/bash

# Список городов
cities_list=(
    "Moscow"
    "Saint Petersburg"
    "Novosibirsk"
    "Ekaterinburg"
    "Kazan"
    "Chelyabinsk"
    "Samara"
    "Omsk"
    "Rostov-on-Don"
    "Ufa"
    "Krasnoyarsk"
    "Voronezh"
    "Perm"
    "Volgograd"
    "Chicago"
    "Houston"
    "Phoenix"
    "Philadelphia"
    "Dallas"
    "Austin"
    "Jacksonville"
    "Indianapolis"
    "Columbus"
    "Charlotte"
    "Seattle"
    "Denver"
    "Washington"
    "Boston"
    "Detroit"
    "Oklahoma"
    "Portland"
    "Israel"
    "Memphis"
    "Louisville"
    "Baltimore"
    "Milwaukee"
    "Albuquerque"
    "Tucson"
    "Fresno"
    "Mesa"
    "Sacramento"
)



# Отправка POST-запросов для  городов
for city in "${cities_list[@]}"; do
    curl -X POST "http://127.0.0.1:8000/api/v1/weather/$city/"
done
