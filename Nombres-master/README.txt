Ce petit programme est capable de trouver un chiffre:
    - de le convertir dans sa valeur (8 >>> 'huit')
mais aussi de trouver une graphie et de la convertir en chiffre.

Ce programme fait partie d'un segmenteur plus large que les unités chiffrées. Le tout est de savoir
que fait partie du "mot". Par exemple en français, nous avons "mille deux cent", cette unité est un bloc et en rien
"mille","deux", puis "cent" mais bien un seul et même bloc 1200 composé de trois numéraux.
Cependant la graphie française est problématique car, l'espace " " sert à séparer des unité au niveau historique,
diachronique, la réalité de la langue en est tout autre. Observons:

    - mille deux cent
    - quatre-vingt-dix-sept mille
    - quatre millions un
    - un million cent

tandis que les deux premiers expriment un numéral, les deux derniers sont différents. mille et millions agissent
différemment. tandis que mille accepte d'être utilisé sans autre numéral à sa gauche, million, lui en a besoin.