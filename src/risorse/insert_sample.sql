BEGIN TRANSACTION;

-- Dopo la creazione del db, inserimento in Postgres psql: 
-- psql -U <user> -d <db> -f risorse/insert_sample.sql 
insert into documento (id, nome, descrizione, href) values (1, 'macbook offerte', 'offerte macbook 2022', '"macbook" => <path>/pdf/macbook.pdf');
insert into documento (id, nome, descrizione, href) values (2, 'birre artigianali', 'impara a bere bene', '"birre" => <path>/pdf/birre.pdf');
insert into documento (id, nome, descrizione, href) values (3, 'mappa gardaland', 'orientati nel parco', '"mappa_gardaland" => <path>/pdf/mappa_gardaland.pdf');

-- postgis 3.0.0 fa il parsing delle geometrie in SRID=4326 se non è specificato altro
insert into posizione values (1, 'Italia', 'Lombardia', 'Milano', 'Apple Store', ST_GeomFromGeoJSON('{ "type": "Polygon",
        "coordinates": [
          [
            [
              9.193822592496872,
              45.465466737989274
            ],
            [
              9.193916469812393,
              45.46530025704288
            ],
            [
              9.194349646568298,
              45.46542535294116
            ],
            [
              9.194247722625732,
              45.4655955957854
            ],
            [
              9.193822592496872,
              45.465466737989274
            ]
          ]]}'),ST_GeomFromGeoJSON('{ "type": "Polygon",
        "coordinates": [
          [
            [
              9.193822592496872,
              45.465466737989274
            ],
            [
              9.193916469812393,
              45.46530025704288
            ],
            [
              9.194349646568298,
              45.46542535294116
            ],
            [
              9.194247722625732,
              45.4655955957854
            ],
            [
              9.193822592496872,
              45.465466737989274
            ]
]]}'));
insert into posizione values (2, 'Italia', 'Veneto', 'Castelnuovo del Garda', 'Gardaland', ST_GeomFromGeoJSON('{ "type": "Polygon", "coordinates": [
          [
            [
              10.705039501190186,
              45.457496734119594
            ],
            [
              10.706884860992432,
              45.4561571587029
            ],
            [
              10.71463108062744,
              45.4534929647023
            ],
            [
              10.716261863708496,
              45.45793321811177
            ],
            [
              10.70667028427124,
              45.45904698953964
            ],
            [
              10.705039501190186,
              45.457496734119594
            ]
          ]
        ]}'), ST_GeomFromGeoJSON('{ "type": "Polygon", "coordinates": [
          [
            [
              10.705039501190186,
              45.457496734119594
            ],
            [
              10.706884860992432,
              45.4561571587029
            ],
            [
              10.71463108062744,
              45.4534929647023
            ],
            [
              10.716261863708496,
              45.45793321811177
            ],
            [
              10.70667028427124,
              45.45904698953964
            ],
            [
              10.705039501190186,
              45.457496734119594
            ]
          ]
]}'));


-- macbook.pdf in apple store
insert into accesso values (1, 1, 1);
-- birre.pdf in Gardaland
insert into accesso values (2, 2, 2);
-- mappa_gardaland.pdf in Gardaland
insert into accesso values (3, 3, 2);

COMMIT;