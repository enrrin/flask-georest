BEGIN TRANSACTION;

-- psql -U <user> -d <db> -f risorse/insert_sample.sql 
insert into documento (id, nome, descrizione, href) values (1, 'voucher', 'voucher gadget fiera UNIBAS', '"voucher" => <path>/flask-georest/pdf_sample/voucher.pdf');
insert into documento (id, nome, descrizione, href) values (2, 'no voucher', 'voucher gia scaricato', '"no-voucher" => <path>/flask-georest/pdf_sample/no-voucher.pdf');

-- postgis 3.0.0 fa il parsing delle geometrie in SRID=4326 se non è specificato altro
insert into posizione values (1, 'Italia', 'Lazio', 'Rome', 'Posizione Fiera1', ST_GeomFromGeoJSON('{ "type": "Polygon",
        "coordinates": [
          [
            [
              12.519607543945312,
              41.93211915938387
            ],
            [
              12.518942356109617,
              41.93155645560538
            ],
            [
              12.519811391830444,
              41.93089397529115
            ],
            [
              12.52068042755127,
              41.93158838219375
            ],
            [
              12.519607543945312,
              41.93211915938387
            ]
          ]
        ]}'),ST_GeomFromGeoJSON('{ "type": "Polygon",
        "coordinates": [
          [
            [
              12.519607543945312,
              41.93211915938387
            ],
            [
              12.518942356109617,
              41.93155645560538
            ],
            [
              12.519811391830444,
              41.93089397529115
            ],
            [
              12.52068042755127,
              41.93158838219375
            ],
            [
              12.519607543945312,
              41.93211915938387
            ]
          ]
        ]}'));

insert into posizione values (2, 'Italia', 'Lazio', 'Rome', 'Posizione Fiera2', ST_GeomFromGeoJSON('{ "type": "Polygon",
        "coordinates": [
          [
            [
              12.520530223846436,
              41.93280158070984
            ],
            [
              12.520036697387695,
              41.932330670868026
            ],
            [
              12.520852088928223,
              41.93179989543795
            ],
            [
              12.52142608165741,
              41.932278790757586
            ],
            [
              12.520530223846436,
              41.93280158070984
            ]
          ]]}'),ST_GeomFromGeoJSON('{ "type": "Polygon",
        "coordinates": [
          [
            [
              12.520530223846436,
              41.93280158070984
            ],
            [
              12.520036697387695,
              41.932330670868026
            ],
            [
              12.520852088928223,
              41.93179989543795
            ],
            [
              12.52142608165741,
              41.932278790757586
            ],
            [
              12.520530223846436,
              41.93280158070984
            ]
        ]]}'));

-- voucher in posizione fiera 1
insert into accesso values (1, 1, 1);

-- voucher in posizione fiera 2
insert into accesso values (2, 1, 2);

COMMIT;
